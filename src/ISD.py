import os
import arcpy
from src.extract.ISD_extract import pdf_dict,get_station_data,get_data_by_province,shp_merge
from src.process.ISD_process import Nodata_Linear_interpolation,ISD_process

def ISD(year,start_date,end_date,elements,provinces,path=r"assert\ISD"):
    folder_path = os.path.join(path, 'china_isd_lite_2015')
    station_table = os.path.join(path, '中国地面气象站基本气象要素观测资料台站表.pdf')

    print("------[1/6]开始读取台站表------")
    station_list = pdf_dict(station_table)

    print("-------[2/6]ISD开始提取-------")
    i = 1
    shp_list = []
    for province in provinces:
        st_ids = get_station_data(folder_path, province, year, station_list)
        shp_list.append(get_data_by_province(start_date, end_date, elements, folder_path, province, station_list))
        print(f"[{i}/{len(provinces)}] {province} over")
        i += 1

    print("------[3/6]ISD提取结束，开始合并...------")
    # 把各省的shp合并
    shp_merge(shp_list)

    print("--------[4/6]合并结束,开始线性插值缺失值--------")
    missing_vals=[-999,-9999]
    cols_to_interpolate = ['element5', 'element6', 'element7', 'element8', 'element9', 'element10', 'element11', 'element12']
    Nodata_Linear_interpolation(missing_vals,cols_to_interpolate)

    print("--------[5/6]线性插值缺失值结束,开始处理ISD数据--------")
    with arcpy.EnvManager(scratchWorkspace=r"assert/ISD.gdb", workspace=r"assert/ISD.gdb"):
        ISD_process(path=r"output/temp")

    print("--------[6/6]ISD over--------")