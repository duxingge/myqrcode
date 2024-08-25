from django.shortcuts import render
from pipline import views

def getPipdetails(request):
    return render(request, 'pipdetails.html',{"pipDetails": views.get_pipelines_data(request)})