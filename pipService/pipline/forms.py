from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label='选择文件')
