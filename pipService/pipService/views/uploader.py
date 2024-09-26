from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import UploadedFile
from django.contrib.auth.decorators import login_required

# 处理文件上传
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # 获取上传的文件
            uploaded_file = request.FILES['file']
            
            # 将文件保存到数据库中
            instance = UploadedFile(file=uploaded_file)
            instance.save()

            return HttpResponse(f'文件 "{uploaded_file.name}" 上传成功')
    else:
        form = UploadFileForm()
    return render(request, 'pipemanager.html', {'form': form})
