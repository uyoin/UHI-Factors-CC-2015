# Copyright (c) 2023.
# -*- coding: UTF-8 -*-
# @Project: UHI-Factors-CC-2015
# @FileName: ISD_process
# @Author：Xiaoqi Huang
# @DateTime: 4/14/2023

import arcpy
import os
import numpy as np
import geopandas as gpd

inpath = r'D:\merged_ISD'
outpath = r'D:\merged_ISD\ISD'
ISDpath = r'D:\merged_ISD\element5'


def Nodata_Linear_interpolation( missing_vals, cols_to_interpolate,path=r"output/temp"):
    # 加载 shapefile 文件
    gdf = gpd.read_file(os.path.join(path, 'merged_ISD.shp'))

    # 将指定要素中的缺失值设为np.nan
    for col in cols_to_interpolate:
        gdf[col] = gdf[col].replace(missing_vals, np.nan)
    # 插值
    for col in cols_to_interpolate:
        # 获取缺失值的索引
        missing = gdf[col].isna()
        # 如果缺失值的数量等于要素总数，则不进行插值操作
        if missing.sum() == len(missing):
            continue
        # 对缺失值进行线性插值
        gdf[col] = gdf[col].interpolate()
    # 保存为新的 shapefile 文件
    gdf.to_file(os.path.join(path, 'ISD_interpolated.shp'))


def ISD_process(path=r"output/temp"):
    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False
    # 加载 shapefile 文件
    gdf_ISD_interpolated = gpd.read_file(os.path.join(path, 'merged_ISD.shp'))
    ISD_interpolated = os.path.join(path, 'ISD_interpolated.shp')

    # Process: 投影 (投影) (management)
    merged_ISD_WGS84 = os.path.join(path, 'ISD_WGS84')
    arcpy.management.Project(in_dataset=ISD_interpolated , out_dataset=merged_ISD_WGS84,
                             out_coor_system="PROJCS[\"WGS_1984_World_Mercator\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Mercator\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",0.0],PARAMETER[\"Standard_Parallel_1\",0.0],UNIT[\"Meter\",1.0]]",
                             transform_method=[],
                             in_coor_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]",
                             preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")

    # 按照 st_id 分组并对每个组中的元素进行加总和计数
    group_cols = ['st_id']
    sum_cols = ['element5', 'element6', 'element7', 'element8', 'element9', 'element10', 'element11', 'element12']
    count_cols = [f'{col}_count' for col in sum_cols]
    gdf_sum = gdf_ISD_interpolated.groupby(group_cols)[sum_cols].sum().reset_index()
    gdf_count = gdf_ISD_interpolated.groupby(group_cols)[sum_cols].count().reset_index()
    gdf_count.columns = group_cols + count_cols

    # 合并加总和计数结果
    gdf_merged = gdf_sum.merge(gdf_count, on='st_id')
    gdf_merged = gdf_merged.merge(gdf_ISD_interpolated[['st_id', 'st_lat', 'st_lon']], on='st_id')
    gdf_merged = gdf_merged[['st_id', 'st_lat', 'st_lon'] + sum_cols + count_cols]

    # 计算每个测站的年均气象要素并保存为新的 shapefile 文件
    for col in sum_cols:
        col_count = f'{col}_count'
        gdf_merged[f'{col}_annual'] = gdf_merged[col] / gdf_merged[col_count]

    # 将每个测站每年的数据进行时间升尺度处理
    gdf_annual = gdf_merged.groupby(['st_id', 'st_lon', 'st_lat']).agg({
        'element5_annual': 'mean',
        'element6_annual': 'mean',
        'element7_annual': 'mean',
        'element8_annual': 'mean',
        'element9_annual': 'mean',
        'element10_annual': 'mean',
        'element11_annual': 'mean',
        'element12_annual': 'mean'
    }).reset_index()

    # 将结果保存为新的 shapefile 文件
    gdf_annual = gpd.GeoDataFrame(gdf_annual, geometry=gdf_ISD_interpolated.geometry)
    gdf_annual.to_file(os.path.join(path, 'ISD_Annual.shp'), driver='ESRI Shapefile')
    arcpy.ImportToolbox(r"d:\arcgis pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
    ISD_Annual = os.path.join(path, 'ISD_Annual')
    Study_Area = os.path.join(path, '研究区.shp')

    # Process: XY 表转点 (XY 表转点) (management)
    ISD_Annual_XYTableToPoint_shp = os.path.join(path, 'ISD_Annual_XYTableToPoint.shp')
    arcpy.management.XYTableToPoint(in_table=ISD_Annual, out_feature_class=ISD_Annual_XYTableToPoint_shp,
                                    x_field="lontitude", y_field="latitude", z_field="",
                                    coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")

    # Process: 投影 (投影) (management)
    ISD_Annual_XYTableTo_Project = os.path.join(path, 'ISD_Annual_XYTableTo_Project')
    arcpy.management.Project(in_dataset=ISD_Annual_XYTableToPoint_shp, out_dataset=ISD_Annual_XYTableTo_Project,
                             out_coor_system="PROJCS[\"WGS_1984_World_Mercator\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Mercator\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",0.0],PARAMETER[\"Standard_Parallel_1\",0.0],UNIT[\"Meter\",1.0]]",
                             transform_method=[],
                             in_coor_system="PROJCS[\"WGS_1984_World_Mercator\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Mercator\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",0.0],PARAMETER[\"Standard_Parallel_1\",0.0],UNIT[\"Meter\",1.0]]",
                             preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")

    # Process: 探索性插值 (探索性插值) (ga)
    ISD5_2_ = os.path.join(path, 'ISD5')
    ISD5 = os.path.join(path, 'ISD5')
    arcpy.ga.ExploratoryInterpolation(in_features=ISD_Annual_XYTableTo_Project, value_field="element5_a",
                                      out_cv_table=ISD5_2_, out_geostat_layer=ISD5,
                                      interp_methods=["SIMPLE_KRIGING", "ORDINARY_KRIGING", "UNIVERSAL_KRIGING", "EBK",
                                                      "KERNEL_INTERPOLATION", "IDW", "RBF", "GPI"],
                                      comparison_method="SINGLE", criterion="ACCURACY",
                                      criteria_hierarchy=[["ACCURACY", "PERCENT", ""]],
                                      weighted_criteria=[["ACCURACY", "1"]], exclusion_criteria=[])

    # Process: GA 图层转栅格 (GA 图层转栅格) (ga)
    GA5_tif = os.path.join(path, 'GA5.tif')
    其他栅格 = arcpy.ga.GALayerToRasters(in_geostat_layer=ISD5, out_raster=GA5_tif, output_type="PREDICTION",
                                         quantile_probability_value=None, cell_size="1000", points_per_block_horz=1,
                                         points_per_block_vert=1, additional_rasters=[], out_elevation="")[0]
    GA5_tif = arcpy.Raster(GA5_tif)

    # Process: 按掩膜提取 (按掩膜提取) (sa)
    ISD5_Output_tif = os.path.join(path, 'ISD5_Output.tif')
    Mask = ISD5_Output_tif
    ISD5_Output_tif = arcpy.sa.ExtractByMask(in_raster=GA5_tif, in_mask_data=Study_Area, extraction_area="INSIDE",
                                             analysis_extent="106.311332401607 31.3935794916558 119.844032596349 42.6082940707857 GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]")
    ISD5_Output_tif.save(Mask)



