#-------------------------------------------------------------------------------
# Name:    NRS568 Midterm Script
# Purpose: NMSDD density extraction, based on a stakeholder provided AOI (area of interest)
#          that will provide a single, merged shape file to be used as acoustic effects
#          modeling input.
#
# Author:      Ben Bartley
#
# Created:     03/10/2019
# Copyright:   <null>
# Licence:     <null>
#-------------------------------------------------------------------------------


import arcpy, os, sys

# Amazing little gem that overwrites shape file output
arcpy.env.overwriteOutput = True
#
### Setting workspace - ANDY, PLEASE CHANGE THIS BELOW WORKSPACE
#
arcpy_env_workspace = r"C:\pythonMidterm"
print "NOTE!..." + str(arcpy_env_workspace) + " is the current workspace."
# version control for density extraction
extract_vers = "1.0" ### Currently not active in code - will revisit and add the extract_vers
# as an attribute to the final extraction
# Set the spatial reference
spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984

# Define the input directory, aka folder where shape files exist and output will go
if not os.path.exists(os.path.join(arcpy_env_workspace, "clipOutput")):
    os.mkdir(os.path.join(arcpy_env_workspace, "clipOutput"))
    print "Clipping output folder created"
else:
    print "Clipping output folder exists"

if not os.path.exists(os.path.join(arcpy_env_workspace, "mergeOutput")):
    os.mkdir(os.path.join(arcpy_env_workspace, "mergeOutput"))
    print "Merged output folder created"
else:
    print "Merged output folder exists"

# setting up directory variables
input_directory = os.path.join(arcpy_env_workspace, "species")
merge_output_dir = os.path.join(arcpy_env_workspace, "mergeOutput")
clip_output_dir = os.path.join(arcpy_env_workspace, "clipOutput")

# working in input_directory
arcpy.env.workspace = input_directory
print input_directory + " is the current workspace."
shp_files_all = arcpy.arcpy.ListFeatureClasses("*")

# setting up to detect AOI polygon shape file within the shape files directory
aoi_file = ""
aoi_found = 0
# looking for the AOI in the shape files. Alert if not present. Continue if present
# and valid type (polygon, Geographic coordinate system)
for i in shp_files_all:
    if "AOI" in i:
        aoi_found = 1
        aoi_file = i

if aoi_found == 0:
    print "NO AOI FILE FOUND...ADD AOI TO WORKSPACE!!!"
    sys.exit()
else:
    print "AOI found, inspecting file..."
    aoi_file_charac = arcpy.Describe(aoi_file)
    if (aoi_file_charac.shapeType == "Polygon") and (aoi_file_charac.spatialReference.type == "Geographic"):
        print "Valid polygon found! Proceeding to clip species to AOI..."
    else:
        aoi_file_charac = arcpy.Describe(aoi_file)
        print "ERROR: Need to provide a POLYGON for clipping, or existing polygon is in the wrong coordinate system. See below:"
        print "--- Selected AOI file type is " + aoi_file_charac.shapeType
        print "--- Current projection of selected AOI file is " + aoi_file_charac.spatialReference.type
        sys.exit()

# Clipping the AOI (extraction area) from each individual species file

for shp in shp_files_all:
    if ("spring" in shp) or ("fall" in shp):
        # Do something with spring files (i.e. field with spring in the filename)
        print "processing file: " + shp
        arcpy.Clip_analysis(shp, aoi_file, os.path.join(clip_output_dir, shp + "_clip"), "")
    # if arcpy.Exists(arcpy.Clip_analysis(i)): ### Want to do a check to make sure everything has processed
    #     print "AOI clip was successful!"
print "All species successfully clipped"

# Performing the merge of all clipped species into an "density extraction"

arcpy.Merge_management(arcpy.arcpy.ListFeatureClasses("*"), merge_output_dir + "/All_species_merge.shp")
print "Merge successfully completed"

print "Extraction is ready."
sys.exit()
# arcpy.AddField_management(clip_output_dir + "/output.shp", "Extr_Vers", "TEXT", "", "", "10")

# arcpy.Da.UpdateCursor
#
# script_version