

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

from .views import piphome
from .views import pipdetails
from pipline import views
from django.conf.urls.static import static
from django.conf import settings
  


urlpatterns = ([
    path('pipline/import/data/', views.import_pipelines_data),
    path('pipline/infos/', pipdetails.getPipdetails),
    path('pipline/infos/<str:code>/', pipdetails.getPipdetailsByCode),
    path('pipline/create/qrcode/<str:code>/', pipdetails.createQrcode),
    path('pipline/create/all/qrcodes/', pipdetails.createAllQrcode),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

