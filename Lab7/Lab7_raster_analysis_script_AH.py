import arcpy
#import arcpy.ddd

path = r'C:\Hinojosa-online-GEOG676-spring2025\Lab7'

# Assigns bands
band1 = arcpy.sa.Raster(path + r'\band1.tif')
band2 = arcpy.sa.Raster(path + r'\band2.tif')
band3 = arcpy.sa.Raster(path + r'\band3.tif')
band4 = arcpy.sa.Raster(path + r'\band4.tif')

# Composite raster image
composite_raster = arcpy.CompositeBands_management([band1, band2, band3, band4], path + r'\composite_raster.tif')

# Hillshade analysis raster
azimuth = 315 # Azimuth angle of the light source
altitude = 45 # Altitude angle of the light source above the horizon
model_shadows = 'NO_SHADOWS' # The effects of shadows are not considered
z_factor = 1
arcpy.ddd.HillShade(path + r'\DEM.tif', path + r'\hillshade_raster.tif', azimuth, altitude, model_shadows, z_factor)

# Slope analysis raster
output_measurement = 'DEGREE'
z_factor = 1
arcpy.ddd.Slope(path + r'\DEM.tif', path + r'\slope_raster.tif', output_measurement, z_factor)

print('Success!')