# ---------------------------------------------------------------------------
# final_merge.py
#
# Description: Completes TES processing by merging all the feature classes from each
#              geodatabase into one feature class and a final staging geodatabase.
#              This gdb will contain non-distributable data.
#              A dissolve runs on the merged feature class to eliminate all fields
#              except UnitID and GRANK_FIRE and then exported to
#              final staging database where the WO deliverables and individual
#              forest geodatabases will be pulled from.
#
# Runtime Estimates: 37 min 31 sec
#
# Created by: Josh Klaus 08/17/2017 jklaus@fs.fed.us
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
import sys
import datetime

in_workspace = sys.argv[1]

# in_workspace = "C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\"

# using the now variable to assign year every time there is a hardcoded 2017
now = datetime.datetime.today()
curMonth = str(now.month)
curYear = str(now.year)
arcpy.AddMessage("Year is " + curYear)

sr = arcpy.SpatialReference(3310)

arcpy.env.workspace = in_workspace

arcpy.env.overwriteOutput = True

tesvariablelist = ["Endangered", "Threatened", "Sensitive"]

final_r05_nodist_gdb = curYear + "_S_R05_FireRetardantEIS_CAALB83_NoDistribution_FWS.gdb"
final_r05_dist_gdb   = curYear + "_S_R05_FireRetardantEIS_CAALB83_DistributableDatasets.gdb"

wo_folder = in_workspace + "\\" + "WO"
tes_folder = wo_folder + "\\" + "TES_Submitted" + "\\"
fws_folder = wo_folder + "\\" + "FWS" + "\\"

final_no_wksp = fws_folder + "\\" + final_r05_nodist_gdb
final_wksp    = fws_folder + "\\" + final_r05_dist_gdb

try:
    if not os.path.exists(wo_folder):
        arcpy.AddMessage("Creating directory for WO Data Deliverables ....")
        os.makedirs(wo_folder)

    if not os.path.exists(fws_folder):
        arcpy.AddMessage("Creating directory for FWS Data Deliverables ....")
        os.makedirs(fws_folder)

    if arcpy.Exists(final_r05_nodist_gdb):
        arcpy.AddMessage("Final FWS GDB not for distribution exists")
    else:
        arcpy.AddMessage("Creating Final Geodatabase with non-distributable Data Deliverables containing merged data")
        arcpy.CreateFileGDB_management(fws_folder, final_r05_nodist_gdb)

    if arcpy.Exists(final_r05_dist_gdb):
        arcpy.AddMessage("Final GDB with distributable datasets exists")
    else:
        arcpy.AddMessage("Creating Final Geodatabase with distrubatable Data Deliverables containing merged data")
        arcpy.CreateFileGDB_management(fws_folder, final_r05_dist_gdb)

    for tes in tesvariablelist:

        newPath = in_workspace + "\\" + curYear + "_" + tes

        # Geodatabases for final merge
        merge_gdb = curYear + "_" + tes + "_Merged_CAALB83.gdb"
        merge_gdb_wkspace = newPath + "\\" + merge_gdb + "\\"

        if arcpy.Exists(merge_gdb_wkspace):
            arcpy.AddMessage(tes + " GDB exists")
        else:
            arcpy.AddMessage("Creating Geodatabase for " + tes + " Data Deliverables containing merged data")
            arcpy.CreateFileGDB_management(newPath, merge_gdb)

    arcpy.AddMessage("Creating Geodatabase for Forest Data Deliverables ....")

    for tes in tesvariablelist:
        merge_gdb = curYear + "_" + tes + "_Merged_CAALB83.gdb"
        newpath = in_workspace + "\\" + curYear + "_" + tes
        tes_workspace = newpath + "\\" + curYear + "_" + tes + "_IdentInter_CAALB83.gdb"
        arcpy.env.workspace = tes_workspace

        if arcpy.Exists(tes_workspace):
            arcpy.AddMessage(tes + " GDB exists")
        else:
            arcpy.AddMessage("Creating Geodatabase for " + tes + " Data Deliverables containing merged data")
            arcpy.CreateFileGDB_management(newpath, merge_gdb)

        fcList = arcpy.ListFeatureClasses()

        inputs = ""

        arcpy.AddMessage("__________________________________________________________________")
        arcpy.AddMessage("List of features being merged:")
        for fc in fcList:
            inputs += os.path.join(arcpy.env.workspace, fc)
            inputs += ";"
            arcpy.AddMessage("   " + fc)

        merge_fc = newpath + "\\" + merge_gdb + "\\" + "FireRetardantEIS_" + tes + "_Merged"

        arcpy.AddMessage("-----------------------------------------------------------------")
        arcpy.AddMessage("Merging " + tes + " feature classes")

        arcpy.Merge_management(inputs, merge_fc)

        arcpy.AddMessage("Finished merging " + tes + " feature classes")

        arcpy.AddMessage("Exporting feature class to final non-distributable Geodatabase")

        final_no_fc_old = final_no_wksp + "\\" + "FireRetardantEIS_" + tes + "_Merged"
        final_no_fc = final_no_wksp + "\\" + "FireRetardantEIS_" + tes + "_NoDistribution"

        arcpy.FeatureClassToGeodatabase_conversion(merge_fc, final_no_wksp)

        arcpy.Rename_management(final_no_fc_old, final_no_fc)

        arcpy.AddMessage("Export to non-distributable GDB complete")

        arcpy.AddMessage("Dissolving " + tes + " Features")

        dissolveFeatureClass = final_no_fc + "_dissolved"

        if sys.version_info[0] < 3:
            arcpy.Dissolve_management(final_no_fc, dissolveFeatureClass, ["UnitID", "GRANK_FIRE"], "", "SINGLE_PART")
        else:
            arcpy.PairwiseDissolve_analysis(final_no_fc, dissolveFeatureClass,["UnitID", "GRANK_FIRE"])

        arcpy.AddMessage("Repairing Dissolved Geometry ......")
        arcpy.RepairGeometry_management(dissolveFeatureClass)
        arcpy.AddMessage("Dissolve and Repair complete")

        arcpy.AddMessage('Exporting dissolved feature class with only UnitID and GRANK_FIRE '
                         'fields to final distributable Geodatabase')

        final_fc_old = final_wksp + "\\" + "FireRetardantEIS_" + tes + "_NoDistribution_dissolved"
        final_fc = final_wksp + "\\" + "FireRetardantEIS_" + tes

        arcpy.FeatureClassToGeodatabase_conversion(dissolveFeatureClass, final_wksp)

        arcpy.Rename_management(final_fc_old, final_fc)

        # Delete old file to eliminate any filename confusion
        arcpy.Delete_management(dissolveFeatureClass)

        arcpy.AddMessage("Export to final distributable GDB complete")

    arcpy.AddMessage("Merge and Export Complete ready to run wo_deliverable!!")

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(e)
