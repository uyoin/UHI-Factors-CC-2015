# Copyright (c) 2023.
# -*- coding: UTF-8 -*-
# @Project: UHI-Factors-CC-2015
# @FileName: Visualize_Geodector
# @Author：Uyoin (Yilong Wu) (https://github.com/uyoin)
# @DateTime: 4/16/2023
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def Visualize_Factor_Detector(output_path="output", pic_path="pic"):
    # 读取 CSV 文件
    df = pd.read_excel(os.path.join(output_path, 'Geodector_result.xlsx'))
    save_path = os.path.join(pic_path, 'Factor_Detector.png')

    # 按照 p 值从大到小排序
    df = df.sort_values(by='q-statistic', ascending=False)

    # 设置图表样式，并绘制柱状图
    sns.set_style('whitegrid')
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x='Factor', y='q-statistic', data=df, color='grey')

    # 设置前四个柱体为深红色
    for i in range(4):
        ax.get_children()[i].set_color('#b40426')

    # 调整布局并展示图表
    plt.title('Q-Statistic by Factor')
    plt.xlabel('Factor')
    plt.ylabel('Q-Statistic')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def Visualize_Interaction_Detector(output_path="output", pic_path="pic"):
    df = pd.read_csv(os.path.join(output_path, 'Geodector_result.xlsx'))
    save_path = os.path.join(pic_path, 'Interaction_Detector.png')
    # 绘制热力图
    plt.figure(figsize=(10, 8))
    # 保存图表到本地文件
    sns.heatmap(df.pivot_table(index='V1', columns='V2', values='V3', aggfunc='mean'), cmap='coolwarm', annot=True,
                fmt=".2f", linewidths=.5)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
