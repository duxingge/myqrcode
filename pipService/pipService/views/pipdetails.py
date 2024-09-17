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


def getPipdetails(request):
    return render(request, 'allpipdetails.html',{"pipDetails": views.getAllpiplines(request)})

def getPipdetailsByCode(request, code):
    return render(request, 'pipdetails.html',{"pipDetails": views.get_pipeline_data_by_code(request, code)})

def createQrcode(request, code):
    qrcodehelp.createQrcode(code)

    return HttpResponse("<p>生成成功</p>")


def createAllQrcode(request):
    allpips = views.getAllpiplines(request)
    for pip in allpips:
        qrcodehelp.createQrcode(pip.code)
    return HttpResponse("<p>所有二维码生成成功</p>")


def downloadQrcode(request, code):
    # 构造二维码图片的文件路径
    qr_file_path = os.path.join(settings.BASE_DIR, 'data', 'qrcoderes', f'QRCODE_PIC_{code}.jpg')

    # 检查文件是否存在
    if not os.path.exists(qr_file_path):
        qrcodehelp.createQrcode(code)
    

    # 使用 FileResponse 返回图片，并设置 Content-Disposition 头为 attachment 强制下载
    response = FileResponse(open(qr_file_path, 'rb'), content_type='image/jpeg')
    response['Content-Disposition'] = f'attachment; filename="QRCODE_PIC_{code}.jpg"'
    return response   


    

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