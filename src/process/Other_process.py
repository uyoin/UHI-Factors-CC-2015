# Copyright (c) 2023.
# -*- coding: UTF-8 -*-
# @Project: UHI-Factors-CC-2015
# @FileName: Other_process
# @Author：Uyoin (Yilong Wu) (https://github.com/uyoin),Xinyi Liu
# @DateTime: 4/16/2023
import os
import arcpy

def Other_process(path=r"assert\ISD"):
    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False
    中部地区_研究区 = os.path.join(path, '中部地区_研究区')
    ISD_Annual = os.path.join(path, 'ISD_interpolated.shp')
    _2015_GDP = os.path.join(path, "gdp2015")
    VNL_v21_npp_2015_global_average =os.path.join(path, "gdp2015")
    # Process: 投影栅格 (投影栅格) (management)

    _2015_GDP_WGS84 = os.path.join(path, "gdp2015_WGS84")
    arcpy.management.ProjectRaster(in_raster=_2015_GDP, out_raster=_2015_GDP_WGS84,
                                   out_coor_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]",
                                   resampling_type="CUBIC", cell_size="1.20952129083985E-02 1.20952129083985E-02",
                                   geographic_transform=[], Registration_Point="",
                                   in_coor_system="PROJCS[\"Krasovsky_1940_Albers\",GEOGCS[\"GCS_Krasovsky_1940\",DATUM[\"D_Krasovsky_1940\",SPHEROID[\"Krasovsky_1940\",6378245.0,298.3]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Albers\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",105.0],PARAMETER[\"Standard_Parallel_1\",25.0],PARAMETER[\"Standard_Parallel_2\",47.0],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]",
                                   vertical="NO_VERTICAL")
    _2015_GDP_WGS84 = arcpy.Raster(_2015_GDP_WGS84)

    # Process: 投影栅格 (2) (投影栅格) (management)
    _2015_POP_WGS84 = os.path.join(path, "pop2015_WGS84")
    arcpy.management.ProjectRaster(in_raster=_2015_POP, out_raster=_2015_POP_WGS84,
                                   out_coor_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]",
                                   resampling_type="CUBIC", cell_size="1.20952129083985E-02 1.20952129083985E-02",
                                   geographic_transform=[], Registration_Point="",
                                   in_coor_system="PROJCS[\"Krasovsky_1940_Albers\",GEOGCS[\"GCS_Krasovsky_1940\",DATUM[\"D_Krasovsky_1940\",SPHEROID[\"Krasovsky_1940\",6378245.0,298.3]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Albers\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",105.0],PARAMETER[\"Standard_Parallel_1\",25.0],PARAMETER[\"Standard_Parallel_2\",47.0],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]",
                                   vertical="NO_VERTICAL")
    _2015_POP_WGS84 = arcpy.Raster(_2015_POP_WGS84)

    # Process: 按掩膜提取 (按掩膜提取) (sa)
    _2015_VNL_研究区 = os.path.join(path, "研究区")
    按掩膜提取 = _2015_VNL_研究区
    with arcpy.EnvManager(
            outputCoordinateSystem="PROJCS["WGS_1984_World_Mercator",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],UNIT["Meter",1.0]]"):
        _2015_VNL_研究区 = arcpy.sa.ExtractByMask(in_raster=VNL_v21_npp_2015_global_average,
                                                  in_mask_data=中部地区_研究区, extraction_area="INSIDE",
                                                  analysis_extent=r"11834523.3885013 3661713.81592204 13340976.683238 5223603.80146651 PROJCS[\"WGS_1984_World_Mercator\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Mercator\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",0.0],PARAMETER[\"Standard_Parallel_1\",0.0],UNIT[\"Meter\",1.0]]")
        _2015_VNL_研究区.save(按掩膜提取)

    # Process: 滤波器 (滤波器) (sa)
    _2015_VNL_降噪 = os.path.join(path, "2015_VNL_降噪")
    滤波器 = _2015_VNL_降噪
    _2015_VNL_降噪 = arcpy.sa.Filter(in_raster=_2015_VNL_研究区, filter_type="LOW", ignore_nodata="DATA")
    _2015_VNL_降噪.save(滤波器)

    # Process: 重采样 (重采样) (management)
    _2015_VNL_1km = os.path.join(path, "2015_VNL_1km")
    with arcpy.EnvManager(tileSize="1000 1000"):
        arcpy.management.Resample(in_raster=_2015_VNL_降噪, out_raster=_2015_VNL_1km, cell_size="1000 1000",
                                  resampling_type="CUBIC")
        _2015_VNL_1km = arcpy.Raster(_2015_VNL_1km)


