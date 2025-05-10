# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from .models import Pipelines
import pandas as pd
from datetime import datetime
from django.conf import settings
import os
from django.views.generic import ListView
from .models import InspectionRecord
from .forms import InspectionRecordForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404




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

def inspection_create(request):
    if request.method == 'POST':
        form = InspectionRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.save()
            return HttpResponse("提交成功")
        else:
            print(form.errors)  # 打印错误信息
    else:
        form = InspectionRecordForm()
    return render(request, 'inspection_create.html', {'form': form})

@method_decorator(xframe_options_exempt, name='dispatch')
class InspectionListView(ListView):
    model = InspectionRecord
    template_name = 'inspection_list.html'
    context_object_name = 'records'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 获取查询参数
        name = self.request.GET.get('name')
        stake_number = self.request.GET.get('stake_number')
        start_time = self.request.GET.get('start_time')
        end_time = self.request.GET.get('end_time')
        
        # 构建查询条件
        filters = Q()
        
        # 按姓名过滤
        if name:
            filters &= Q(inspector__icontains=name)
            
        # 按桩号过滤
        if stake_number:
            filters &= Q(stake_number__icontains=stake_number)
            
        # 按时间范围过滤
        if start_time:
            try:
                start_date = timezone.make_aware(datetime.strptime(start_time, '%Y-%m-%dT%H:%M'))
                filters &= Q(inspection_time__gte=start_date)
            except ValueError:
                pass
                
        if end_time:
            try:
                end_date = timezone.make_aware(datetime.strptime(end_time, '%Y-%m-%dT%H:%M'))
                end_date = end_date.replace(hour=23, minute=59, second=59)
                filters &= Q(inspection_time__lte=end_date)
            except ValueError:
                pass
                
        return queryset.filter(filters).order_by('-inspection_time')


# 新增的API接口
@require_GET
def inspector_search_api(request):
    """巡检人模糊查询接口"""
    keyword = request.GET.get('keyword', '').strip()
    
    # if not keyword:
    #     return JsonResponse([], safe=False)
    
    # 获取所有匹配的巡检人（去重）
    inspectors = User.objects.filter(
        Q(username__icontains=keyword),
        Q(inspectionrecord__isnull=False)  # 确保有巡检记录
    ).distinct().values_list('username', flat=True)
    
    return JsonResponse(list(inspectors), safe=False)

@require_GET
def stake_number_search_api(request):
    """桩号模糊查询接口"""
    keyword = request.GET.get('keyword', '').strip()
    
    if not keyword:
        return JsonResponse([], safe=False)
    
    # 获取所有匹配的桩号（去重）
    stake_numbers = InspectionRecord.objects.filter(
        stake_number__icontains=keyword
    ).order_by('stake_number').values_list('stake_number', flat=True).distinct()
    
    return JsonResponse(list(stake_numbers), safe=False)

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_superuser, login_url='/accounts/login')
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 注册后自动登录
            return redirect('../manager/')  # 重定向到首页
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})

def delete_inspection_record(request, record_id):
    if request.method == 'DELETE':
        record = get_object_or_404(InspectionRecord, id=record_id)
        record.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)