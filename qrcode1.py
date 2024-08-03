

# 生成一个根据内容生成二维码的程序

import qrcode

from PIL import Image

from qrcode.image.styledpil import StyledPilImage



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


import qrcode
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q)
qr.add_data('Some data')

# 文本显示
img = qr.make_image(fill_color="black", back_color="white")
img.show()

# 带logo的二维码
# img_3 = qr.make_image(image_factory=StyledPilImage, embeded_image_path="/Users/wangjiaxing/work/qrcodetest/icon.jpg")

# img_3.show()