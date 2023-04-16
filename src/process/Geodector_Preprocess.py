# Copyright (c) 2023.
# -*- coding: UTF-8 -*-
# @Project: UHI-Factors-CC-2015
# @FileName: Geodector_Preprocess
# @Author：Uyoin (Yilong Wu) (https://github.com/uyoin)
# @DateTime: 4/16/2023

import os
import arcpy
import pandas as pd
import numpy as np
# Process: 栅格转点 (栅格转点) (conversion)
def Geodector_Preprocess(path=r"assert\ISD"):
    中部地区_热岛 = os.path.join(path, "中部地区_热岛.tif")
    输出点要素 = os.path.join(path, "中部地区_热岛_点")
    _2015_GDP_WGS84 = arcpy.Raster(os.path.join(path, "gdp2015_WGS84"))
    _2015_POP_WGS84, = arcpy.Raster(os.path.join(path, "tpop2015_WGS84"))
    _2015_VNL_1km =  arcpy.Raster(os.path.join(path, "tpop2015"))
    VNL_v21_npp_2015_global_average = arcpy.Raster(os.path.join(path, "VNL_v21_npp_2015_global_vcmslcfg_c202205302300.average_masked.dat.tif"))
    _2015_ISD_ele = arcpy.Raster(os.path.join(path, "tpop2015"))
    多值提取至点 = os.path.join(path, "多值提取至点")
    _2015_热岛_各因子 = os.path.join(path, "HSI_IF_Origin.csv")

    with arcpy.EnvManager(outputMFlag="Disabled", outputZFlag="Disabled"):
        arcpy.conversion.RasterToPoint(in_raster=中部地区_热岛, out_point_features=输出点要素,
                                       raster_field="Value")

    _2015_点_热岛_各因子 = arcpy.sa.ExtractMultiValuesToPoints(in_point_features=输出点要素, in_rasters=[[_2015_GDP_WGS84, "GDP_1"], [_2015_POP_WGS84, "POP_1"], [_2015_VNL_1km, "VNL_1"], [_2015_ISD_ele, ""]], bilinear_interpolate_values="NONE")
    .save(多值提取至点)

    arcpy.conversion.ExportTable(in_table=_2015_点_热岛_各因子, out_table=_2015_热岛_各因子, where_clause="", use_field_alias_as_name="NOT_USE_ALIAS", field_mapping="pointid \"pointid\" true true false 4 Long 0 0,First,#,C:\\Users\\LENOVO\\Desktop\\大三下\\【1下】空间信息计算机编程\\期中\\Projects\\MyProject6\\MyProject6.gdb\\RasterT_中部地区_热岛1,pointid,-1,-1;grid_code \"grid_code\" true true false 8 Double 0 0,First,#,C:\\Users\\LENOVO\\Desktop\\大三下\\【1下】空间信息计算机编程\\期中\\Projects\\MyProject6\\MyProject6.gdb\\RasterT_中部地区_热岛1,grid_code,-1,-1;GDP \"GDP\" true true false 4 Long 0 0,First,#,C:\\Users\\LENOVO\\Desktop\\大三下\\【1下】空间信息计算机编程\\期中\\Projects\\MyProject6\\MyProject6.gdb\\RasterT_中部地区_热岛1,GDP,-1,-1;POP \"POP\" true true false 4 Float 0 0,First,#,C:\\Users\\LENOVO\\Desktop\\大三下\\【1下】空间信息计算机编程\\期中\\Projects\\MyProject6\\MyProject6.gdb\\RasterT_中部地区_热岛1,POP,-1,-1;VNL \"VNL\" true true false 4 Float 0 0,First,#,C:\\Users\\LENOVO\\Desktop\\大三下\\【1下】空间信息计算机编程\\期中\\Projects\\MyProject6\\MyProject6.gdb\\RasterT_中部地区_热岛1,VNL,-1,-1;Air_Temp \"Air_Temp\" true true false 4 Float 0 0,First,#,C:\\Users\\LENOVO\\Desktop\\大三下\\【1下】空间信息计算机编程\\期中\\Projects\\MyProject6\\MyProject6.gdb\\RasterT_中部地区_热岛1,Air_Temp,-1,-1;Dew_Point_Temp \"Dew_Point_Temp\" true true false 4 Float 0 0,First,#,C:\\Users\\LENOVO\\Desktop\\大三下\\【1下】空间信息计算机编程\\期中\\Projects\\MyProject6\\MyProject6.gdb\\RasterT_中部地区_热岛1,Dew_Point_Temp,-1,-1;Sea_Level_Pressure \"Sea_Level_Pressure\" true true false 4 Float 0 0,First,#,C:\\Users\\LENOVO\\Desktop\\大三下\\【1下】空间信息计算机编程\\期中\\Projects\\MyProject6\\MyProject6.gdb\\RasterT_中部地区_热岛1,Sea_Level_Pressure,-1,-1;Wind_Direction \"Wind_Direction\" true true false 4 Float 0 0,First,#,C:\\Users\\LENOVO\\Desktop\\大三下\\【1下】空间信息计算机编程\\期中\\Projects\\MyProject6\\MyProject6.gdb\\RasterT_中部地区_热岛1,Wind_Direction,-1,-1;Wind_Speed_Rate \"Wind_Speed_Rate\" true true false 4 Float 0 0,First,#,C:\\Users\\LENOVO\\Desktop\\大三下\\【1下】空间信息计算机编程\\期中\\Projects\\MyProject6\\MyProject6.gdb\\RasterT_中部地区_热岛1,Wind_Speed_Rate,-1,-1;Precipitation \"Precipitation\" true true false 4 Float 0 0,First,#,C:\\Users\\LENOVO\\Desktop\\大三下\\【1下】空间信息计算机编程\\期中\\Projects\\MyProject6\\MyProject6.gdb\\RasterT_中部地区_热岛1,Precipitation,-1,-1", sort_field=[])

    gdf = pd.read_csv(
        r"C:\Users\LENOVO\Desktop\大三下\【1下】空间信息计算机编程\期中\UHI-Factors-CC-2015\output\HSI_IF.csv")

    # 将指定要素中的缺失值设为np.nan
    missing_vals = [""]
    cols_to_interpolate = ['HSI', 'GDP', 'POP', 'VNL', 'Air_Temp', 'Dew_Point_Temp', 'Sea_Level_Pressure', 'Wind_Direction',
                           'Wind_Speed_Rate', 'Precipitation']

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

    # 等间隔分类
    gdf['GDP_group'] = pd.qcut(gdf['POP'], q=5, labels=False, duplicates='drop')
    gdf['POP_group'] = pd.qcut(gdf['POP'], q=5, labels=False, duplicates='drop')
    gdf['VNL_group'] = pd.qcut(gdf['VNL'], q=5, labels=False, duplicates='drop')
    gdf['Air_Temp_group'] = pd.qcut(gdf['Air_Temp'], q=5, labels=False, duplicates='drop')
    gdf['Dew_Point_Temp_group'] = pd.qcut(gdf['Dew_Point_Temp'], q=5, labels=False, duplicates='drop')
    gdf['Sea_Level_Pressure_group'] = pd.qcut(gdf['Sea_Level_Pressure'], q=5, labels=False, duplicates='drop')
    gdf['Wind_Direction_group'] = pd.qcut(gdf['Wind_Direction'], q=5, labels=False, duplicates='drop')
    gdf['Wind_Speed_Rate_group'] = pd.qcut(gdf['Wind_Speed_Rate'], q=5, labels=False, duplicates='drop')
    gdf['Precipitation_group'] = pd.qcut(gdf['Precipitation'], q=5, labels=False, duplicates='drop')
    gdf = gdf.drop(columns=['GDP', 'POP', 'VNL', 'Air_Temp', 'Dew_Point_Temp', 'Sea_Level_Pressure', 'Wind_Direction',
                           'Wind_Speed_Rate', 'Precipitation'])

    # 保存为新的 shapefile 文件
    gdf.to_csv(os.path.join(path,r"HSI_IF_Classification.csv"))