import os
import arcpy
from src.ISD import ISD
from src.process.HSI_process import HSI
from src.process.Other_process import Other_process
from src.process.Geodector_Preprocess import Geodector_Preprocess
from src.Visualize.Visualize_Geodector import Visualize_Factor_Detector,Visualize_Interaction_Detector

year = 2015
start_date = "2015-01-01"
end_date = "2015-12-31 23:00"
elements = [5, 6, 7, 8, 9, 10, 11, 12]
provinces = ["安徽", "北京", "重庆", "福建", "甘肃", "广东", "广西", "贵州", "海南", "河北", "黑龙江", "河南",
             "湖北", "湖南", "江苏", "江西", "吉林", "辽宁", "内蒙古", "宁夏", "青海", "山东", "山西", "陕西",
             "上海", "四川", "天津", "西藏", "新疆", "云南", "浙江"]

path = r"output\temp"
gdb_path = os.path.join(path, "study.gdb")
with arcpy.EnvManager(scratchWorkspace=gdb_path,workspace=gdb_path):
    ISD(year, start_date, end_date, elements, provinces, path=r"assert\ISD")
    HSI(path)
    Other_process(path)
    Geodector_Preprocess(path)

# 转到R语言进行处理后可以进行可视化
# Visualize_Factor_Detector(output_path="output",pic_path="pic")
# Visualize_Interaction_Detector(output_path="output", pic_path="pic")