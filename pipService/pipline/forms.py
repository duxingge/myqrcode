from django import forms
from .models import InspectionRecord
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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
    
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
    