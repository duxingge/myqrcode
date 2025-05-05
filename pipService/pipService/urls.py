

"""
URL configuration for pipService project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import loginHome
from .views import pipdetails
from pipline import views
from django.conf.urls.static import static
from django.conf import settings
from .views.pipdetails import PipelineListView, PipelineHomeView
from pipline.views import inspection_create, InspectionListView,  inspector_search_api, stake_number_search_api


urlpatterns = ([
    # 文件导入数据库
    path('pipline/import/data/', views.import_pipelines_data),
    path('accounts/login/', loginHome.login_view, name='login'),
    path('pipline/logout/', loginHome.logout_view, name='logout'),
    path('accounts/init/', loginHome.create_user, name='create_user'),
    # path('pipline/infos/', pipdetails.getPipdetails),
    # 查看pip视图
    path('pipline/infos/<str:code>/', pipdetails.getPipdetailsByCode),
    # 查看pip视图
    path('pipline/infos/navigate/<str:code>/', pipdetails.getPipNavigateByCode, name='pipeline_navigate'),
    # 查询pip信息json
    path('pipline/info/str/<str:code>/', pipdetails.getPipdetailStrByCode),
    # 列表查询管理
    path('pipline/manager/qrcode/', PipelineListView.as_view(), name='pipeline_manager_qrocode'),
    path('pipline/manager/', PipelineHomeView.as_view(), name='pipeline_manager'),
    path('pipline/create/qrcode/<str:code>/', pipdetails.createQrcode),
    path('pipline/create/all/qrcodes/', pipdetails.createAllQrcode),
    path('pipline/infos/download/code/<str:code>/', pipdetails.downloadQrcode),
    path('pipline/infos/download/all/', pipdetails.downloadAllQrcode),
    path('pipline/uploadmedia/', pipdetails.uploadMediafile, name='upload_media_file'),
    path('pipline/upload/', pipdetails.uploadfile, name='upload_file'),
    path('pipline/properties/', pipdetails.getPipProperties, name='getPipProperties'),
    path('pipline/properties/update/', pipdetails.setproerties, name='setproerties'),
    path('pipline/inspection/create/', inspection_create, name='inspection_create'),
    path('pipline/manager/list/', InspectionListView.as_view(), name='inspection_list'),
    path('pipline/register/', views.register_view, name='register'),
    path('pipline/inspection/inspector/search/', inspector_search_api, name='inspector-search'),
    path('pipline/inspection/stake-numbers/search/', stake_number_search_api, name='stake-number-search'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

