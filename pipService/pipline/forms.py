from django import forms
from .models import InspectionRecord
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.core.exceptions import PermissionDenied


class UploadFileForm(forms.Form):
    file = forms.FileField(label='选择文件')




class InspectionRecordForm(forms.ModelForm):
    class Meta:
        model = InspectionRecord
        fields = ['stake_number', 'inspection_result', 'abnormal_record', 'photo', 'location_info']
        widgets = {
            'inspection_result': forms.RadioSelect,
        }

class RegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=True, help_text='请输入手机号')
    
    class Meta:
        model = CustomUser
        fields = ("username", "phone", "password1", "password2")
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # 获取request对象
        super().__init__(*args, **kwargs)
        
        # 如果不是超级管理员访问，直接拒绝
        if self.request and not self.request.user.is_superuser:
            raise PermissionDenied("只有超级管理员可以注册新用户")
        
        # 添加Bootstrap类到所有字段
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    