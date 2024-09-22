# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Pipelines
import pandas as pd
from datetime import datetime
from django.conf import settings
from .forms import UploadFileForm
from .models import UploadedFile
import os

# 导入Pipeline数据到数据库
def import_pipelines_data(request):
    # Excel文件路径
    FILE_PATH = f'{settings.MEDIA_ROOT}/uploads/piplinedatas.xlsx'

    # 1. 读取Excel文件
    df = pd.read_excel(FILE_PATH,engine='openpyxl')

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
                'pipe_group': row.get('pipe_group', None),
                'updated_at': datetime.now(),  # 每次更新或创建时更新updated_at
            }
        )

    return HttpResponse("数据已成功插入并更新到pipelines表中。")


def getAllpiplines(request):
    # 获取所有Pipeline对象
    allpips = Pipelines.objects.all()

    return allpips

def get_pipeline_data_by_code(request, qCode):
    # 根据code获取Pipeline对象
    pip = Pipelines.objects.filter(code=qCode)[0]
    return pip


# 处理文件上传
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            FILE_PATH = f'{settings.MEDIA_ROOT}/uploads/piplinedatas.xlsx'

            # 删除文件
            if os.path.exists(FILE_PATH):
                os.remove(FILE_PATH)

            # 获取上传的文件
            uploaded_file = request.FILES['file']
            original_name = uploaded_file.name
            uploaded_file.name = 'piplinedatas.xlsx';
            # 将文件保存到数据库中
            instance = UploadedFile(file=uploaded_file)
            instance.save()
            import_pipelines_data(request)

            return HttpResponse(f'文件 "{original_name}" 上传成功')
    else:
        form = UploadFileForm()
    return render(request, 'pipemanager.html', {'form': form})