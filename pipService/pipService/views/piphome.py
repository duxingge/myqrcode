from django.shortcuts import render

def showinfo(request): 
  views_dict = {"name":"菜鸟教程"}
  return  render(request,"runoob.html",  {"views_dict": views_dict})