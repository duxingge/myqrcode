from django.shortcuts import render
from pipline import views
from pipService.qrutil import qrcodehelp
from django.http import HttpResponse
import zipfile
import os
import io
from django.http import HttpResponse, Http404
from django.conf import settings
from django.http import FileResponse
import json
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.db import models

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from pipline.models import Pipelines
# from pipline.serializers import PipelineInfoSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator




def getPipdetails(request):
    return render(request, 'allpipdetails.html',{"pipDetails": views.getAllpiplines(request)})

@login_required
def getPipdetailsByCode(request, code):
    return render(request, 'pipdetails.html',{"pipDetails": views.get_pipeline_data_by_code(request, code)})

@login_required
def getPipdetailStrByCode(request, code):
    pipeline_data = views.get_pipeline_data_by_code(request, code)

    # 如果 pipeline_data 是 QuerySet 或 Django 模型实例，需将其转换为可序列化的格式
    if isinstance(pipeline_data, models.Model):  # 如果是单个模型实例
        # 将对象转换为字典
        pipeline_data = model_to_dict(pipeline_data)
    elif hasattr(pipeline_data, '__iter__'):  # 检查是否为可迭代对象（如 QuerySet）
        pipeline_data = list(pipeline_data.values())  # 转换为字典列表

    # 将数据转换为 JSON 字符串
    pipDetails = json.dumps(pipeline_data, ensure_ascii=False)

    # 返回 HttpResponse 并指定 Content-Type 为 application/json
    return HttpResponse(pipDetails, content_type='application/json')


@login_required
def createQrcode(request, code):
    qrcodehelp.createQrcode(request, code)
    return HttpResponse("<p>生成成功</p>")

@login_required
def createAllQrcode(request):
    allpips = views.getAllpiplines(request)
    for pip in allpips:
        qrcodehelp.createQrcode(request, pip.code)
    return HttpResponse("<p>所有二维码生成成功</p>")

@login_required
def downloadQrcode(request, code):
    # 构造二维码图片的文件路径
    qr_file_path = os.path.join(settings.BASE_DIR, 'data', 'qrcoderes', f'QRCODE_PIC_{code}.jpg')

    # 检查文件是否存在
    if not os.path.exists(qr_file_path):
        qrcodehelp.createQrcode(request, code)
    

    # 使用 FileResponse 返回图片，并设置 Content-Disposition 头为 attachment 强制下载
    response = FileResponse(open(qr_file_path, 'rb'), content_type='image/jpeg')
    response['Content-Disposition'] = f'attachment; filename="QRCODE_PIC_{code}.jpg"'
    return response   


    
@login_required
def downloadAllQrcode(request):
    # 定义二维码图片存储目录
    qr_folder_path = os.path.join(settings.BASE_DIR, 'data', 'qrcoderes')

    # 检查目录是否存在
    if not os.path.exists(qr_folder_path):
        raise Http404("QR code directory not found")

    # 创建一个内存中的 BytesIO 对象，作为 ZIP 文件
    zip_buffer = io.BytesIO()

    # 使用 zipfile.ZipFile 创建一个 zip 文件
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # 遍历目录中的所有文件
        for root, dirs, files in os.walk(qr_folder_path):
            for file in files:
                # 将文件添加到 zip 包中
                file_path = os.path.join(root, file)
                zip_file.write(file_path, arcname=file)  # arcname 确保只保留文件名，而不是完整路径

    # 将缓冲区指针移到开始位置，以便可以读取数据
    zip_buffer.seek(0)

    # 构建 HttpResponse 返回 zip 文件
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="all_qrcodes.zip"'

    return response


@method_decorator(login_required, name='dispatch')
class PipelineListView(APIView):
    def get(self, request):
        page_size = request.GET.get('page_size', 10)
        page_number = request.GET.get('page', 1)
        paginator = PageNumberPagination()
        paginator.page_size = int(page_size)

        # 按 code 查询的部分
        code = request.GET.get('code')
        if code:
            queryset = Pipelines.objects.filter(code=code)
        else:
            queryset = Pipelines.objects.all()

        results = paginator.paginate_queryset(queryset, request)

        return render(request, 'pipemanager.html', {
            'pipelines': results,
            'previous_page_url': paginator.get_previous_link(),
            'next_page_url': paginator.get_next_link(),
            'current_page': paginator.page.number,
            'total_pages': paginator.page.paginator.num_pages,
            'searched_code': code,
        })
