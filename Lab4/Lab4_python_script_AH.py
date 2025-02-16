# GEOG 676 - GIS Programming
# Lab 4: Fun with ArcPy

# Imports arcpy module, setups environment workspace, and creates file gdb
import arcpy
arcpy.env.workspace = 'C:\Hinojosa-online-GEOG676-spring2025\Lab4'
folder_path = r'C:\Hinojosa-online-GEOG676-spring2025\Lab4'
arcpy.CreateFileGDB_management(folder_path, 'Lab4.gdb')

# folder path for created file gdb
Lab4_gdb = r'C:\Hinojosa-online-GEOG676-spring2025\Lab4\Lab4.gdb'

# Add csv layer into geodatabase
# cvs location path
csv = r'C:\Hinojosa-online-GEOG676-spring2025\Lab4\garages.csv'
# turns csv into a feature class called garages
garages = arcpy.management.MakeXYEventLayer(csv, 'X', 'Y', 'Garage_Points')
# this method copies the feature class into the gdb
arcpy.FeatureClassToGeodatabase_conversion(garages, Lab4_gdb)

# Add campus.gdb into created geodatabase
campus = r'C:\Hinojosa-online-GEOG676-spring2025\Lab4\Campus.gdb'
campus_buildings_path = campus + '\Structures'  # path for structures layer in campus.gdb
lab4_buildings_path = Lab4_gdb + '\Buildings'   # path where I want to copy over the buldings layer into
# Copies the campus buildings layer into the lab4 buildings layer
arcpy.management.Copy(campus_buildings_path, lab4_buildings_path)

# Reproject Garage Points to have the same projection as buildings layer in Lab4 gdb
spatial_ref = arcpy.Describe(lab4_buildings_path).spatialReference
arcpy.management.Project(Lab4_gdb + '\Garage_points', Lab4_gdb + '\Garage_points_Reprojected', spatial_ref)

# Buffers the garage points
# Asks for user input for the buffer distance
input_buffer = input('Enter the buffer distance in meters: ')
garage_buffered = arcpy.analysis.Buffer(Lab4_gdb + '\Garage_points', Lab4_gdb + '\Garage_points_buffered', input_buffer + ' Meters') # Need to specify units

# Intersect buildings with buffered garage points
arcpy.analysis.Intersect([garage_buffered, lab4_buildings_path], Lab4_gdb + '\Garage_Building_Intersect', 'ALL') # joins all attributes from input into output

# Outputs to a .csv table
arcpy.conversion.TableToTable(Lab4_gdb + '\Garage_Building_Intersect', folder_path, 'Buildings_Near_Garages.csv')