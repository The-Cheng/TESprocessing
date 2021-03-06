# ---------------------------------------------------------------------------
# wo_hydro.py
#
# Description: Creates the final deliverable product for the WO.
#              This includes generating geodatabases for each forest
#
# Runtime Estimates: 2 min 33 sec
#
# Created by: Josh Klaus 08/24/2017 jklaus@fs.fed.us
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

arcpy.env.workspace = in_workspace

arcpy.env.overwriteOutput = True

outputWorkSpace = in_workspace + "\\" + "Output" + "\\"

test_hydro_gdb = "Hydro_" + curYear + "_CAALB83.gdb"
# test_hydro_gdb = "Hydro_Test_2017_CAALB83_newproj.gdb"

final_hydro_gdb = curYear + "_NHDfinal_CAALB83.gdb"
staging_hydro_gdb = curYear + "_S_R05_FireRetardantEIS_CAALB83_AllHydroDatasets.gdb"

outputHydro = outputWorkSpace + "Hydro" + curYear + "\\" + test_hydro_gdb + "\\"

wo_folder = in_workspace + "\\" + "WO"

hydro_folder = wo_folder + "\\" + "Hydro_Submitted" + "\\"

final_wksp = hydro_folder + "\\" + final_hydro_gdb + "\\"

forestGDBList = ["S_R05_ANF_FireRetardantEIS_Hydro.gdb",
                 "S_R05_BDF_FireRetardantEIS_Hydro.gdb",
                 "S_R05_CNF_FireRetardantEIS_Hydro.gdb",
                 "S_R05_ENF_FireRetardantEIS_Hydro.gdb",
                 "S_R05_INF_FireRetardantEIS_Hydro.gdb",
                 "S_R05_KNF_FireRetardantEIS_Hydro.gdb",
                 "S_R05_LNF_FireRetardantEIS_Hydro.gdb",
                 "S_R05_LPF_FireRetardantEIS_Hydro.gdb",
                 "S_R05_MDF_FireRetardantEIS_Hydro.gdb",
                 "S_R05_MNF_FireRetardantEIS_Hydro.gdb",
                 "S_R05_PNF_FireRetardantEIS_Hydro.gdb",
                 "S_R05_SHU_FireRetardantEIS_Hydro.gdb",
                 "S_R05_SNF_FireRetardantEIS_Hydro.gdb",
                 "S_R05_SQF_FireRetardantEIS_Hydro.gdb",
                 "S_R05_SRF_FireRetardantEIS_Hydro.gdb",
                 "S_R05_STF_FireRetardantEIS_Hydro.gdb",
                 "S_R05_TMU_FireRetardantEIS_Hydro.gdb",
                 "S_R05_TNF_FireRetardantEIS_Hydro.gdb" ]

forestGDBDict = {"S_R05_ANF_FireRetardantEIS_Hydro.gdb": "0501",
                 "S_R05_BDF_FireRetardantEIS_Hydro.gdb": "0512",
                 "S_R05_CNF_FireRetardantEIS_Hydro.gdb": "0502",
                 "S_R05_ENF_FireRetardantEIS_Hydro.gdb": "0503",
                 "S_R05_INF_FireRetardantEIS_Hydro.gdb": "0504",
                 "S_R05_KNF_FireRetardantEIS_Hydro.gdb": "0505",
                 "S_R05_LNF_FireRetardantEIS_Hydro.gdb": "0506",
                 "S_R05_LPF_FireRetardantEIS_Hydro.gdb": "0507",
                 "S_R05_MDF_FireRetardantEIS_Hydro.gdb": "0509",
                 "S_R05_MNF_FireRetardantEIS_Hydro.gdb": "0508",
                 "S_R05_PNF_FireRetardantEIS_Hydro.gdb": "0511",
                 "S_R05_SHU_FireRetardantEIS_Hydro.gdb": "0514",
                 "S_R05_SNF_FireRetardantEIS_Hydro.gdb": "0515",
                 "S_R05_SQF_FireRetardantEIS_Hydro.gdb": "0513",
                 "S_R05_SRF_FireRetardantEIS_Hydro.gdb": "0510",
                 "S_R05_STF_FireRetardantEIS_Hydro.gdb": "0516",
                 "S_R05_TMU_FireRetardantEIS_Hydro.gdb": "0519",
                 "S_R05_TNF_FireRetardantEIS_Hydro.gdb": "0517"}

try:
    if not os.path.exists(wo_folder):
        arcpy.AddMessage("Creating directory for WO Data Deliverables ....")
        os.makedirs(wo_folder)

    if not os.path.exists(hydro_folder):
        arcpy.AddMessage("Creating directory for WO Hydrology Data Deliverables ....")
        os.makedirs(hydro_folder)

        arcpy.AddMessage("Creating Geodatabase for Forest Data Deliverables ....")
        for forest in forestGDBList:
            arcpy.CreateFileGDB_management(hydro_folder, forest)

        arcpy.CreateFileGDB_management(hydro_folder, final_hydro_gdb)

    # May take out after testing is complete
    arcpy.AddMessage("exporting from test gdb to final gdb")
    # arcpy.FeatureClassToGeodatabase_conversion(outputHydro +
    #                                            "NHDFlowline_Merge_Buff_intersect", final_wksp)
    # arcpy.FeatureClassToGeodatabase_conversion(outputHydro +
    #                                            "NHDWaterbody_Area_Merge_Buff_intersect", final_wksp)
    arcpy.FeatureClassToGeodatabase_conversion(outputHydro +
                                               "NHDFlowline_Merge_geocomplete", final_wksp)
    arcpy.FeatureClassToGeodatabase_conversion(outputHydro +
                                               "NHDWaterbody_Area_Merge_geocomplete", final_wksp)
    arcpy.AddMessage("renaming files to final staging name")

    arcpy.Rename_management(final_wksp + "NHDFlowline_Merge_geocomplete",
                            final_wksp + "NHD_Flowline")
    arcpy.Rename_management(final_wksp + "NHDWaterbody_Area_Merge_geocomplete",
                            final_wksp + "NHD_Waterbody")

    hydroList = ["NHD_Flowline", "NHD_Waterbody"]

    for forest in forestGDBList:
        for hydro in hydroList:
            final_fc = final_wksp + "\\" + hydro
            arcpy.MakeFeatureLayer_management(final_fc, "lyr")
            arcpy.AddMessage("Selecting records based on " + hydro + " ...")
            unitIDnum = forestGDBDict.get(forest)
            arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "UnitID = '" + unitIDnum + "'")

            final_wo_space = hydro_folder + forest + "\\" + hydro

            result = arcpy.GetCount_management("lyr")
            count = int(result.getOutput(0))
            arcpy.AddMessage("Total Number of Records: " + str(count))

            if count > 0:
                arcpy.AddMessage("Copying selected records to " + forest + "  Geodatabase ......")
                arcpy.CopyFeatures_management("lyr", final_wo_space)

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(e)