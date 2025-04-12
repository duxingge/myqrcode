# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.conf import settings
from django.contrib.auth.models import User

import os



# Create your models here.


class Pipelines(models.Model):
    # id 字段会自动创建并作为主键 (Primary Key)
    name = models.CharField(max_length=255, verbose_name='管线名称')
    code = models.CharField(max_length=255, unique=True, verbose_name='桩号')  # 唯一
    orientation = models.CharField(max_length=255, null=True, blank=True, verbose_name='平面转角')
    length_km = models.CharField(max_length=255, null=True, blank=True, verbose_name='里程 (单位: Km)')
    depth_m = models.CharField(max_length=255, null=True, blank=True, verbose_name='管道埋深 (单位: m)')
    distance_position_des = models.TextField(null=True, blank=True, verbose_name='离管道位置描述')
    wall_thickness_mm = models.CharField(max_length=255, null=True, blank=True, verbose_name='壁厚 (单位: mm)')
    material = models.CharField(max_length=255, null=True, blank=True, verbose_name='材质')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    qr_code_url = models.URLField(max_length=200, null=True, blank=True, verbose_name='二维码地址')
    pipe_group  = models.CharField(max_length=255, verbose_name='汉安线')



class PipelinesConifg(models.Model):
    # id 字段会自动创建并作为主键 (Primary Key)
    name = models.CharField(max_length=255, verbose_name='属性名')
    value = models.CharField(max_length=255, unique=True, verbose_name='值')  #
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

class UploadedFile(models.Model):
    
    file = models.FileField(upload_to='uploads/')  # 文件将上传到 'uploads/' 目录
     
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 上传时间

class InspectionRecord(models.Model):
    INSPECTION_RESULT_CHOICES = [
        ('normal', '正常'),
        ('abnormal', '异常'),
    ]
    
    inspector = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="巡检人")
    stake_number = models.CharField(max_length=100, verbose_name="桩号")
    inspection_result = models.CharField(
        max_length=10, 
        choices=INSPECTION_RESULT_CHOICES, 
        verbose_name="巡检结果"
    )
    abnormal_record = models.TextField(blank=True, null=True, verbose_name="异常记录")
    inspection_time = models.DateTimeField(auto_now_add=True, verbose_name="巡检时间")
    location_info = models.CharField(max_length=255, verbose_name="位置信息")
    photo = models.ImageField(upload_to='inspection_photos/', blank=True, null=True, verbose_name="现场照片")
    
    def __str__(self):
        return f"{self.inspector.username} - {self.stake_number} - {self.inspection_result}"
    
    class Meta:
        verbose_name = "巡检记录"
        verbose_name_plural = "巡检记录"