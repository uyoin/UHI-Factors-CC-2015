# Copyright (c) 2023.
# -*- coding: UTF-8 -*-
# @Project: UHI-Factors-CC-2015
# @FileName: ISD_extract
# @Author：Uyoin (Yilong Wu) (https://github.com/uyoin)
# @DateTime: 4/14/2023

import pandas as pd
import geopandas as gpd
from tqdm import tqdm


def pdf_dict(input_path):
    import pdfplumber
    """
    提取pdf文件的所有页面的表格数据为list。

        Parameters
    ----------
    input_path : str
        pdf文件的路径，例如："./data/test.pdf"。
    
    Returns
    -------
    list of list
        包含每个页面表格数据的列表的列表，例如：[['省份', '区站号', '站名', '纬度（度分）', '经度（度分）', '气压传感器拔海高度（米）', '观测场拔海高度（米）'], ['安徽', '58015', '砀山', '3427', '11620', '45.4', '44.2'],...]
    """

    # 定义一个函数来提取表格数据，返回一个列表
    def extract_table(page):
        # 使用pdfplumber的extract_table方法，返回一个列表
        table = page.extract_table()
        # 如果表格为空，返回空列表
        if table is None:
            return []
        # 否则，返回表格数据
        else:
            return table

    # 定义空列表存储数据
    data_list = []

    # 打开pdf文件
    with pdfplumber.open(input_path) as pdf:
        # 遍历所有页面
        pbar = tqdm(total=len(pdf.pages))
        for page in pdf.pages:
            pbar.update(1)
            # 提取表格数据，返回一个列表
            table = extract_table(page)
            if page.page_number == 1:
                for i in range(1, len(table)):
                    table[i][3] = float(table[i][3]) / 100
                    table[i][4] = float(table[i][4]) / 100
            else:
                for i in range(len(table)):
                    table[i][3] = float(''.join(list(filter(str.isdigit, table[i][3])))) / 100
                    table[i][4] = float(table[i][4]) / 100
            # 将列表添加到列表中
            data_list.extend(table)

    # 返回数据列表
    return data_list[1:]


def extract_data(start_date, end_date, elements, file_path, st_id):
    """
    从ISD-Lite数据集中提取特定时间段和气象要素的数据。

    Parameters
    ----------
    start_date : str
        起始日期，格式为'YYYY-MM-DD'。
    end_date : str
        结束日期，格式为'YYYY-MM-DD'。
    elements : list of int
        要提取的气象要素代码，参见数据说明文档。例如：[5, 6, 7]。
    file_path : str
        数据文件路径。

    Returns
    -------
    pandas.DataFrame
        满足要求的数据，每行包含所有指定的气象要素数据。
    """

    # 将起始日期和结束日期转换为Pandas中的Timestamp对象
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)

    # 读取数据文件
    column_names = ['year', 'month', 'day', 'hour'] + ['element{}'.format(i) for i in elements]
    df = pd.read_fwf(file_path + "\\" + str(st_id) + "0-" + "99999" + "-" + "2015", colspecs=get_colspecs(elements),
                     header=None, names=column_names)

    # 将日期和时间合并为单个Pandas时间戳对象
    timestamps = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

    # 根据起始日期和结束日期过滤数据
    mask = (timestamps >= start_date) & (timestamps <= end_date)
    df = df[mask].reset_index(drop=True)

    return df


def get_colspecs(elements):
    """
    获取指定元素的列规格列表。

    Parameters
    ----------
    elements : list of int
        要提取的气象要素代码，参见数据说明文档。例如：[5, 6, 7]。

    Returns
    -------
    list of tuple
        列规格列表，用于读取数据文件。
    """
    cols = [(0, 4), (4, 8), (8, 10), (11, 13)]
    for element in elements:
        if element == 5:
            cols.append((13, 18))
        elif element == 6:
            cols.append((19, 24))
        elif element == 7:
            cols.append((25, 30))
        elif element == 8:
            cols.append((31, 36))
        elif element == 9:
            cols.append((37, 42))
        elif element == 10:
            cols.append((43, 48))
        elif element == 11:
            cols.append((49, 54))
        elif element == 12:
            cols.append((55, 61))
    return cols


def get_station_data(folder_path, province, year, station_dict):
    """获取指定省份和年份的测站数据，并根据对照表筛选。

    Parameters
    ----------
    province : str
        要获取数据的省份名称，例如："北京"。
    year : int
        要获取数据的年份，例如：2021。
    station_dict : list of dict
        包含测站信息的对照表，每个字典为一个测站，例如：[{'省份': '安徽', '区站号': '58015', '站名': '砀山', '纬度（度分）': '3427', '经度（度分）': '11620', '气压传感器拔海高度（米）': '45.4', '观测场拔海高度（米）': '44.2'},...]

    Returns
    -------
    pd.DataFrame
        包含筛选后的测站数据的数据框，每个测站为一行，每个气象要素为一列。
    """

    # 定义空列表存储数据
    data_list = []
    file_name_list = []

    # 遍历文件夹中的文件
    st_id = []
    for d in station_dict:
        if d[0] == province:
            try:
                st_id.append([int(d[1]), float(d[3]), float(d[4])])
            except:
                st_id.append([int(d[1][:-1]), float(d[3]), float(d[4])])
        # for d in station_dict:
        #     if isinstance(d, dict) and d.get("省份") == province:
        #         st_id.append([int(d["区站号"]),folat(d["区站号"]),folat(d["区站号"])])  # 把字符串转换成整数

    # 返回st_id
    return st_id


def get_data_by_province(start_date, end_date, elements, file_path, province, data_list):
    """ 从ISD-Lite数据集中提取特定省份、时间段和气象要素的数据，并转换为shp要素点。
    Parameters
    ----------
    start_date : str
        起始日期，格式为'YYYY-MM-DD'。
    end_date : str
        结束日期，格式为'YYYY-MM-DD'。
    elements : list of int
        要提取的气象要素代码，参见数据说明文档。例如：[5, 6, 7]。
    file_path : str
        数据文件路径。
    province : str
        要提取的省份名称，例如："广东"。
    station_dict : list of dict
        包含测站信息的对照表，每个字典为一个测站，例如：[{'省份': '安徽', '区站号': '58015', '站名': '砀山', '纬度（度分）': '3427', '经度（度分）': '11620', '气压传感器拔海高度（米）': '45.4', '观测场拔海高度（米）': '44.2'},...]

    Returns
    -------
    None
        生成一个shp文件，包含特定省份所有站点的自定义气象元素数据。
    """
    import geopandas as gpd
    from shapely.geometry import Point

    # 获取特定省份的所有st_id编号列表
    st_ids = get_station_data(file_path, province, year, data_list)

    # 创建一个空的Pandas.DataFrame对象，用于存储所有站点的数据
    df_all = pd.DataFrame()

    st_id2 = []
    # 遍历st_id编号列表，调用extract_data函数提取每个站点的数据，并将其合并到df_all中
    for st_id in st_ids:
        try:
            df = extract_data(start_date, end_date, elements, file_path, st_id[0])
            df['st_id'] = st_id[0]  # 添加一列st_id，用于区分不同站点
            df['st_lon'] = st_id[1]
            df['st_lat'] = st_id[2]
            st_id2.append(st_id)
            df_all = pd.concat([df_all, df], ignore_index=True)  # 合并数据
        except:
            # print(str(st_id) + "is nodata")
            pass

    # 将df_all转换为geopandas.GeoDataFrame对象，添加一列geometry，用于存储每个站点的经纬度坐标
    gdf = gpd.GeoDataFrame(df_all)

    gdf['geometry'] = gpd.points_from_xy(gdf['st_lat'], gdf['st_lon'])

    # 设置gdf的坐标参考系为WGS84（EPSG:4326）
    gdf.crs = "EPSG:4326"
    shp_name = f"{start_date}_{end_date}_{province}_{elements}.shp"
    # 生成一个shp文件，命名为"province_elements.shp"，其中province和elements分别用实际参数替换
    gdf.to_file("output/" + shp_name)
    return shp_name


def shp_merge(shp_list):
    gdf_list = []
    # 读取shp
    for shp in shp_list:
        gdf = gpd.read_file(shp)
        gdf_list.append(gdf)
    # 合并所有shp
    merged_gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True), crs=gdf.crs)
    # 导出
    merged_gdf.to_file(r"output/temp/merged_ISD.shp")


