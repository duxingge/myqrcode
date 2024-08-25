from django.shortcuts import render
from pipline import views
from pipService.qrutil import qrcodehelp
from django.http import HttpResponse


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

