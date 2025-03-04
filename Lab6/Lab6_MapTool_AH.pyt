# -*- coding: utf-8 -*-

import arcpy
import time
import os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]


class GraduatedColorsRenderer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Graduated Colors Renderer"
        self.description = "Creates a graduated colored map."
        self.canRunInBackground = False
        self.category = "Map Creation Tools"

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
        displayName="Enter ArcGIS Pro Project Name",
        name="aprxProjectName",
        datatype="DEFile",
        parameterType="Required",
        direction="Input")

        param1 = arcpy.Parameter(
        displayName="Layer to Classify",
        name="LayertoClassify",
        datatype="GPLayer",
        parameterType="Required",
        direction="Input")

        param2 = arcpy.Parameter(
        displayName="Output Folder Location",
        name="OutputFolderLocation",
        datatype="DEFolder",
        parameterType="Required",
        direction="Input")

        param3 = arcpy.Parameter(
        displayName="Output Project Name",
        name="OutputProjectName",
        datatype="GPString",
        parameterType="Required",
        direction="Input")


        params = [param0, param1, param2, param3]
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
        output_path = os.path.join(parameters[2].valueAsText, parameters[3].valueAsText + ".aprx")

        # Processor Variables
        readTime = 3 # seconds
        start = 0
        maximum = 100
        step = 33

        # Progressor will provide user feedback on code execution status
        arcpy.SetProgressor("step", "Validating Project File...", start, maximum, step)
        time.sleep(readTime) # pauses based on readtime variable
        arcpy.AddMessage("Validating Project File...")

        # Loads input project file from the first parameter
        project_file = arcpy.mp.ArcGISProject(parameters[0].valueAsText)

        # Returns the default map named 'Map' from project
        campus = project_file.listMaps('Map')[0]

        # Updates Progressor
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Locating map layer...")
        time.sleep(readTime)
        arcpy.AddMessage("Locating map layer...")

        # Loops through every layer in the map
        for lyr in campus.listLayers():
            if lyr.isFeatureLayer: # checks that the current layer is a feature layer
                symbology = lyr.symbology # copies symbology

                if hasattr(symbology, 'renderer'): # returns if specified attribute name exists
                    if lyr.name == parameters[1].valueAsText: # checks that layer name matches the layer selected by the user
                        
                        # Updates Progressor
                        arcpy.SetProgressorPosition(start + step*2)
                        arcpy.SetProgressorLabel("Layer is being classified...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Layer is being classified...")

                        # Updates symbology to Graduated Colors
                        symbology.updateRenderer('GraduatedColorsRenderer')
                        # Sets the classification field to Shape_Area
                        symbology.renderer.classificationField = "Shape_Area"
                        # Sets the number of classification classes
                        symbology.renderer.breakCount = 5
                        # Selects the color ramp
                        symbology.renderer.colorRamp = project_file.listColorRamps('Oranges (5 Classes)')[0]

                        # Makes the layers symbology match the copies symbology
                        lyr.symbology = symbology # Very important step
                        arcpy.AddMessage("Finishing generating layer...")
                        
                    else:
                        print("Layer not located")
        
        # Updates Progressor
        arcpy.SetProgressorPosition(start + step*3)
        arcpy.SetProgressorLabel("Saving project...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving project...")

        # saves a new .aprx project using the Output Folder Location and Output Project Name inputted by user
        project_file.saveACopy(output_path)

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
