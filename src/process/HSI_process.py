# Copyright (c) 2023.
# -*- coding: UTF-8 -*-
# @Project: UHI-Factors-CC-2015
# @FileName: HSI_process
# @Author：Uyoin (Yilong Wu) (https://github.com/uyoin)
# @DateTime: 4/15/2023

import os
import arcpy


def HSI(path=r"assert\ISD"):
    关中_island_2015_tif = arcpy.Raster(os.path.join(path, "关中_island_2015.tif"))
    中原_island_2015_tif = arcpy.Raster(os.path.join(path, "中原_island_2015.tif"))
    京津冀_island_2015_tif = arcpy.Raster(os.path.join(path, "京津冀_island_2015.tif"))

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Process: 镶嵌至新栅格 (镶嵌至新栅格) (management)
    中部地区_热岛 = arcpy.management.MosaicToNewRaster(
        input_rasters=[关中_island_2015_tif, 中原_island_2015_tif, 京津冀_island_2015_tif], output_location=path,
        raster_dataset_name_with_extension="中部地区_热岛.tif", coordinate_system_for_the_raster="",
        pixel_type="64_BIT", cellsize=None, number_of_bands=1, mosaic_method="MEAN", mosaic_colormap_mode="MATCH")[0]
    中部地区_热岛 = arcpy.Raster(中部地区_热岛)

    # Process: 栅格范围 (栅格范围) (3d)
    中部地区_热岛_有洞洞的面_ = os.path.join(path, "中部地区_热岛_洞洞")
    arcpy.ddd.RasterDomain(in_raster=中部地区_热岛, out_feature_class=中部地区_热岛_有洞洞的面_,
                           out_geometry_type="POLYGON")

    # Process: 消除面部件 (消除面部件) (management)
    中部地区_研究区 = os.path.join(path, "中部地区_研究区")
    arcpy.management.EliminatePolygonPart(in_features=中部地区_热岛_有洞洞的面_, out_feature_class=中部地区_研究区,
                                          condition="PERCENT", part_area="0 Unknown", part_area_percent=50,
                                          part_option="CONTAINED_ONLY")
