# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [BuildingProximity]


class BuildingProximity(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Building Proximity"
        self.description = "Determines which buildings intersect with nearby garages at TAMU's main campus."
        self.canRunInBackground = False
        self.category = "Building Tools" # group different tools within toolbox

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
        displayName="GDB Folder",
        name="GDBFolder",
        datatype="DEFolder",
        parameterType="Required",
        direction="Input")

        param1 = arcpy.Parameter(
        displayName="GDB Name",
        name="GDBName",
        datatype="GPString",
        parameterType="Required",
        direction="Input")

        param2 = arcpy.Parameter(
        displayName="Garage CSV File",
        name="GarageCSVFile",
        datatype="DEFile",
        parameterType="Required",
        direction="Input")

        param3 = arcpy.Parameter(
        displayName="Garage Layer Name",
        name="GarageLayerName",
        datatype="GPString",
        parameterType="Required",
        direction="Input")

        param4 = arcpy.Parameter(
        displayName="Campus GDB",
        name="CampusGDB",
        datatype="DEType",
        parameterType="Required",
        direction="Input")

        param5 = arcpy.Parameter(
        displayName="Buffer Distance",
        name="BufferDistance",
        datatype="GPDouble",
        parameterType="Required",
        direction="Input")

        params = [param0, param1, param2, param3, param4, param5]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        folder_path = parameters[0].valueAsText
        file_gdb_name = parameters[1].valueAsText
        gdb_file_path = folder_path + '\\' + file_gdb_name
        # creates file gdb
        arcpy.CreateFileGDB_management(folder_path, file_gdb_name)

        csv_file_path = parameters[2].valueAsText
        garage_layer_name = parameters[3].valueAsText
        # turns csv into a feature class called garages
        garages = arcpy.MakeXYEventLayer_management(csv_file_path, 'X', 'Y', garage_layer_name)
        
        # this method copies the feature class into the gdb
        input_layer = garages
        arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_file_path)
        garage_points = gdb_file_path +'\\' + garage_layer_name

        # Add campus.gdb into created geodatabase
        campus = parameters[4].valueAsText
        campus_buildings_path = campus + '\Structures'  # path for structures layer in campus.gdb
        buildings_path = gdb_file_path +  '\\' + 'Buildings'   # path where I want to copy over the buldings layer into
        
        # Copies the campus buildings layer into the lab5 buildings layer
        arcpy.Copy_management(campus_buildings_path, buildings_path)

        # Reproject Garage Points to have the same projection as buildings layer in Lab4 gdb
        spatial_ref = arcpy.Describe(buildings_path).spatialReference
        arcpy.Project_management(garage_points, gdb_file_path + '\Garage_points_Reprojected', spatial_ref)

        # Buffers the garage points
        buffer_distance = int(parameters[5].value)
        garage_buffered = arcpy.Buffer_analysis(gdb_file_path + '\Garage_points_Reprojected', gdb_file_path + '\Garage_points_buffered', buffer_distance)

        # Intersect buildings with buffered garage points
        arcpy.Intersect_analysis([garage_buffered, buildings_path], gdb_file_path + '\Garage_Building_Intersect', 'ALL') # joins all attributes from input into output

        # Outputs to a .csv table
        arcpy.TableToTable_conversion(gdb_file_path + '\Garage_Building_Intersect', folder_path, 'Buildings_Near_Garages.csv')
        
        return None