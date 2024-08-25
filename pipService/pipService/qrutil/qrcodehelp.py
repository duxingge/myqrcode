

# 生成一个根据内容生成二维码的程序

import qrcode

from PIL import Image

from qrcode.image.styledpil import StyledPilImage

from django.conf import settings


# # 定义要生成二维码的内容
# content = "https://www.baidu.com"

# # 生成二维码
# img = qrcode.make(content)


# # 保存二维码
# img.save("qrcode.png")  

# # 显示二维码
# img.show()
# # 打印二维码内容
# # print(content)


# -*- coding:utf-8 -*-
import os , qrcode
from PIL import  Image
 
import qrcode,os




def createQrcode(pipCode):
    # 创建QRCode对象
    ewm = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    # 设置二维码数据, 并添加到二维码中
    data = settings.QRCODE_SHOW_HOST + pipCode+'/'
    ewm.add_data(data=data)
    # 更改二维码的颜色，默认是黑色。得到的结果是 PIL 图像对象
    ewm.make(fit=True) # 让二维码得到一个适合的大小值。
    ewm_img = ewm.make_image(fill_color="#000000", back_color="white")
    # 获取二维码大小:宽，高
    ewm_size = ewm_img.size
    ewm_size_w ,ewm_size_h = ewm_size
    
    # 打开图标文件，并获取图标的大小，重新设定图标大小
    # 这里设置icon宽高为二维码的 6分之一。

    s = 4
    icon = Image.open("./pipService/data/icons/android-chrome-512x512.png")
    # 设置小图标的大小，缩放的时候尺寸必须是整数，否则报错
    icon_w,icon_h = int(ewm_size_w/s) ,int(ewm_size_h/s)
    icon_small = icon.resize( (icon_w ,icon_h) ,Image.LANCZOS)  # Image.ANTIALIAS 画面平滑缩放
    # 获取粘贴小图标的坐标，必须整数，否则粘贴的时候，报错
    icon_x, icon_y = int( (ewm_size_w-icon_w)/2 ), int( (ewm_size_h-icon_h)/2)
    # 把图标“粘贴”到二维码上正中间。
    ewm_img.paste( icon_small,(icon_x,icon_y)  )
    
    # 显示二维码
    # ewm_img.show()    # 如果数据被clear了，会有个二维码，扫它什么都不会发生
    ewm_img.save(f"{settings.QRCODE_PIC_RESULT_PATH}/{settings.QRCODE_PIC_PREFIX}{pipCode}.jpg")