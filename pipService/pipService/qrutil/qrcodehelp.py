

# # 生成一个根据内容生成二维码的程序

# import qrcode

# from PIL import Image

# from qrcode.image.styledpil import StyledPilImage

# from django.conf import settings


# # # 定义要生成二维码的内容
# # content = "https://www.baidu.com"

# # # 生成二维码
# # img = qrcode.make(content)


# # # 保存二维码
# # img.save("qrcode.png")  

# # # 显示二维码
# # img.show()
# # # 打印二维码内容
# # # print(content)


# # -*- coding:utf-8 -*-
# import os , qrcode
# from PIL import  Image
 
# import qrcode,os




# def createQrcode(pipCode):
#     # 创建QRCode对象
#     ewm = qrcode.QRCode(
#         version=5,
#         error_correction=qrcode.constants.ERROR_CORRECT_H,
#         box_size=10,
#         border=4,
#     )
#     # 设置二维码数据, 并添加到二维码中
#     data = settings.QRCODE_SHOW_HOST + pipCode+'/'
#     ewm.add_data(data=data)
#     # 更改二维码的颜色，默认是黑色。得到的结果是 PIL 图像对象
#     ewm.make(fit=True) # 让二维码得到一个适合的大小值。
#     ewm_img = ewm.make_image(fill_color="#000000", back_color="white")
#     # 获取二维码大小:宽，高
#     ewm_size = ewm_img.size
#     ewm_size_w ,ewm_size_h = ewm_size
    
#     # 打开图标文件，并获取图标的大小，重新设定图标大小
#     # 这里设置icon宽高为二维码的 6分之一。

#     s = 4
#     icon = Image.open(f"{settings.BASE_DIR}/data/icons/android-chrome-512x512.png")
#     # 设置小图标的大小，缩放的时候尺寸必须是整数，否则报错
#     icon_w,icon_h = int(ewm_size_w/s) ,int(ewm_size_h/s)
#     icon_small = icon.resize( (icon_w ,icon_h) ,Image.LANCZOS)  # Image.ANTIALIAS 画面平滑缩放
#     # 获取粘贴小图标的坐标，必须整数，否则粘贴的时候，报错
#     icon_x, icon_y = int( (ewm_size_w-icon_w)/2 ), int( (ewm_size_h-icon_h)/2)
#     # 把图标“粘贴”到二维码上正中间。
#     ewm_img.paste( icon_small,(icon_x,icon_y)  )
    
#     # 显示二维码
#     ewm_img.show()    # 如果数据被clear了，会有个二维码，扫它什么都不会发生
#     ewm_img.save(f"{settings.QRCODE_PIC_RESULT_PATH}/{settings.QRCODE_PIC_PREFIX}{pipCode}.jpg")



import qrcode
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

def createQrcode(pipCode):
    # 创建QRCode对象
    ewm = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=4,
    )
    
    # 设置二维码数据
    data = settings.QRCODE_SHOW_HOST + pipCode + '/'
    ewm.add_data(data=data)
    ewm.make(fit=True)
    ewm_img = ewm.make_image(fill_color="#000000", back_color="white")
    
    # 获取二维码大小
    ewm_size_w, ewm_size_h = ewm_img.size

    # 打开图标文件，调整图标大小并粘贴到二维码中
    s = 4
    icon = Image.open(f"{settings.BASE_DIR}/data/icons/android-chrome-512x512.png")
    icon_w, icon_h = int(ewm_size_w / s), int(ewm_size_h / s)
    icon_small = icon.resize((icon_w, icon_h), Image.LANCZOS)
    icon_x, icon_y = (ewm_size_w - icon_w) // 2, (ewm_size_h - icon_h) // 2
    ewm_img.paste(icon_small, (icon_x, icon_y))

    # 加载背景图片
    background = Image.open(f"{settings.BASE_DIR}/data/icons/qrcode_backgroud.jpg")
    bg_w, bg_h = background.size
    
    # 将二维码粘贴到背景图的中心
    qr_x = (bg_w - ewm_size_w) // 2
    qr_y = (bg_h - ewm_size_h - 180)  # 让二维码靠上，留出下面加文字的空间
    background.paste(ewm_img, (qr_x, qr_y))
    
    draw = ImageDraw.Draw(background)
    

    # 显示并保存生成的图片
    background.show()
    background.save(f"{settings.QRCODE_PIC_RESULT_PATH}/{settings.QRCODE_PIC_PREFIX}{pipCode}.jpg")





# 



import qrcode
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

def createQrcode(pipCode):
    # 创建QRCode对象
    ewm = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=4,
    )
    
    # 设置二维码数据
    data = settings.QRCODE_SHOW_HOST + pipCode + '/'
    ewm.add_data(data=data)
    ewm.make(fit=True)
    ewm_img = ewm.make_image(fill_color="#000000", back_color="white")
    
    # 获取二维码大小
    ewm_size_w, ewm_size_h = ewm_img.size

    # 打开图标文件，调整图标大小并粘贴到二维码中
    s = 4
    icon = Image.open(f"{settings.BASE_DIR}/data/icons/android-chrome-512x512.png")
    icon_w, icon_h = int(ewm_size_w / s), int(ewm_size_h / s)
    icon_small = icon.resize((icon_w, icon_h), Image.LANCZOS)
    icon_x, icon_y = (ewm_size_w - icon_w) // 2, (ewm_size_h - icon_h) // 2
    ewm_img.paste(icon_small, (icon_x, icon_y))

    # 增加空白区域，为文本留出空间
    text_space_height = 180  # 留出180像素高度的空白
    new_img_height = ewm_size_h + text_space_height
    extended_img = Image.new("RGB", (ewm_size_w, new_img_height), "white")
    extended_img.paste(ewm_img, (0, 0))

    # 在二维码下方添加文字
    # 使用支持中文的字体
    font_path = f"{settings.BASE_DIR}/data/font/NotoSansSC-VariableFont_wght.ttf"  # 替换为支持中文的字体路径
    font_size = 60  # 设置字体大小
    font = ImageFont.truetype(font_path, font_size)  # 加载字体
    
    text = f"打开微信[扫一扫] \n 查看{pipCode}信息"
    
    draw = ImageDraw.Draw(extended_img)
    
    # 使用 textbbox 来获取文本大小
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_position = ((ewm_size_w - text_w) // 2, ewm_size_h + 20)  # 文本位置，在二维码下方

    # 绘制文字
    draw.text(text_position, text, fill="black", font=font)


    # 加载背景图片
    background = Image.open(f"{settings.BASE_DIR}/data/icons/qrcode_backgroud.jpg")
    bg_w, bg_h = background.size
    
    # 将二维码粘贴到背景图的中心
    qr_x = (bg_w - ewm_size_w) // 2
    qr_y = (bg_h - ewm_size_h - 180)  # 让二维码靠上，留出下面加文字的空间
    background.paste(extended_img, (qr_x, qr_y))
    
    draw = ImageDraw.Draw(background)
    

    # 显示并保存生成的图片
    background.show()
    background.save(f"{settings.QRCODE_PIC_RESULT_PATH}/{settings.QRCODE_PIC_PREFIX}{pipCode}.jpg")