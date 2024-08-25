# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

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
