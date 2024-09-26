from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pipeline_manager')  # 登录成功后重定向
        else:
            error_message = "Invalid credentials"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # 注销后重定向到登录页面


def create_user(request):    
    # 创建新用户
    user = User.objects.create_user(username='liutao', password='xxx')
    return HttpResponse("初始化管理员成功。")