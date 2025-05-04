import qrcode
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from pipline import views

def createQrcode(request,pipeGroup,pipCode):
    # 创建QRCode对象
    ewm = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=4,
    )
    
    pipinfos = views.get_pipeline_data_by_code(request, pipCode)
    title = pipinfos.pipe_group+ '管道信息'
    # 设置二维码数据
    data = settings.QRCODE_SHOW_HOST + pipCode + '/'
    ewm.add_data(data=data)
    ewm.make(fit=True)
    ewm_img = ewm.make_image(fill_color="#000000", back_color="white").convert("RGB")
    
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
    text_space_height = 280  # 留出180像素高度的空白
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
    text_position = ((ewm_size_w - text_w) // 2, ewm_size_h-20)  # 文本位置，在二维码下方

    # 绘制文字
    draw.text(text_position, text, fill="black", font=font)

    
    # 加载背景图片
    background = Image.open(f"{settings.BASE_DIR}/data/icons/pipe_back5.jpg")
    bg_w, bg_h = background.size

    # 将背景图片放大2倍
    background = background.resize((bg_w * 2 - 360, bg_h * 2-200), Image.LANCZOS)
    bg_w, bg_h = background.size 
    
    # 将二维码粘贴到背景图的中心
    qr_x = (bg_w - ewm_size_w) // 2
    qr_y = ((bg_h - ewm_size_h) // 2 ) + 200  # 让二维码靠上，留出下面加文字的空间
    background.paste(extended_img, (qr_x, qr_y))
    
    draw = ImageDraw.Draw(background)



    # 绘制标题
    
    titlefont_path = f"{settings.BASE_DIR}/data/font/simhei2.ttf"  # 替换为支持中文的字体路径
    title_font_size = 100  # 设置字体大小
    title_font = ImageFont.truetype(titlefont_path, title_font_size)  # 加载字体
    
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_text_w = title_bbox[2] - title_bbox[0]
    title_text_h = title_bbox[3] - title_bbox[1]
    title_position = ((bg_w-title_text_w) // 2 , 150)  # 文本位置，在二维码下方

    draw.text(title_position, title, fill="black", font=title_font)

    # 将图像转换为RGB模式再保存为JPEG
    background = background.convert("RGB")

    # 显示并保存生成的图片
    # background.show()
    background.save(f"{settings.QRCODE_PIC_RESULT_PATH}/{settings.QRCODE_PIC_PREFIX}{pipeGroup}{pipCode}.jpg")