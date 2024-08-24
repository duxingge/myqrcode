# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Pipelines
import pandas as pd
from datetime import datetime

def import_pipelines_data(request):
    # Excel文件路径
    FILE_PATH = '/Users/wangjiaxing/work/myqrcode/pipService/insertData/piplinedatas.xlsx'

    # 1. 读取Excel文件
    df = pd.read_excel(FILE_PATH)

    # 2. 将数据插入到数据库表中
    for index, row in df.iterrows():
        # 创建或更新Pipeline对象
        pipeline, created = Pipelines.objects.update_or_create(
            code=row['code'],  # 使用code作为唯一标识符进行查找或创建
            defaults={
                'name': row['name'],
                'orientation': row.get('orientation', ''),
                'length_km': row.get('length_km', None),
                'depth_m': row.get('depth_m', None),
                'distance_position_des': row.get('distance_position_des', ''),
                'wall_thickness_mm': row.get('wall_thickness_mm', None),
                'material': row.get('material', ''),
                'qr_code_url': row.get('qr_code_url', None),
                'updated_at': datetime.now(),  # 每次更新或创建时更新updated_at
            }
        )

    return HttpResponse("数据已成功插入并更新到pipelines表中。")
