管道管理服务

pipService: 项目的容器。
manage.py: 一个实用的命令行工具，可让你以各种方式与该 Django 项目进行交互。
HelloWorld/__init__.py: 一个空文件，告诉 Python 该目录是一个 Python 包。
HelloWorld/asgi.py: 一个 ASGI 兼容的 Web 服务器的入口，以便运行你的项目。
HelloWorld/settings.py: 该 Django 项目的设置/配置。
HelloWorld/urls.py: 该 Django 项目的 URL 声明; 一份由 Django 驱动的网站"目录"。
HelloWorld/wsgi.py: 一个 WSGI 兼容的 Web 服务器的入口，以便运行你的项目。




<!-- 项目相关 -->

<!-- django安装 -->
pip3 install Django

<!-- 查看django版本 -->
python3 -m django --version

<!-- 启动django项目 -->
python3 manage.py runserver 0.0.0.0:8000

<!-- 模型变更通知 -->
python3 manage.py makemigrations TestModel  # 通知Django指定模型变更
python3 manage.py makemigrations 通知Django模型变更

<!-- 创建表结构 -->
python3 manage.py migrate   # 创建所有表结构
python3 manage.py migrate TestModel   # 创建指定表结构






<!-- 数据库相关 -->

cd /Users/wangjiaxing/work/myqrcode/pipService/db

<!-- 打开 sqlite -->
sqlite3

<!-- 打开数据库 -->
.open pipService.db

<!-- 查看表 -->
.tables

<!-- 查看表结构 -->
.schema pipelines

<!-- 删除表 -->
DROP TABLE pipelines;




<!-- 部署相关 -->

pip3 install uwsgi
pip3 install django
pip3 install pandas
pip3 install qrcode
sudo yum install zlib-devel 
pip3 install Pillow
pip3 install openpyxl


<!-- 项目相关 -->

<!-- excel生成sqllite 数据 -->
http://101.201.173.95:8000/pipline/import/data/
<!-- 生成二维码 -->
http://localhost:8001/pipline/create/qrcode/0096+1/
http://localhost:8001/pipline/infos/0096+1/

http://localhost:8001/pipline/infos/download/code/0096+1/

http://localhost:8001/pipline/create/all/qrcodes/

<!-- 导入数据 -->
http://localhost:8001/pipline/import/data/




<!-- ------------------API  接口------------------------- -->
http://101.201.173.95:8000/pipline/infos/download/all/?code=0096+1&pipe_group=汉安线

单个/组下载：
   /pipline/infos/download/all/?code=0096+1&pipe_group=汉安线
全部下载：
   /pipline/infos/download/all/
单个信息查询json：:   
   /pipline/infos/str/0096+1/

二维码视图：
   /pipline/infos/<str:code>/   

<!-- 文件上传 -->
pipline/upload/



<!-- 视频名称 -->
large_scale_construction.mp4  pipline_protect.mp4  security_allance.mp4
