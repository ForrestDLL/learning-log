from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from .forms import RegisterForm, LoginForm

# Create your views here.
def register(request):
    """注册新用户"""
    if request.method != "POST":
        form = RegisterForm()
    else:
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # 注册完毕，直接登录
            return redirect("learning_logs:index")
        
    context = {"form": form}
    return render(request, "users/register.html", context)


def login_view(request):
    """登录"""
    if request.method != "POST":
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user()) # 取出校验通过的用户    
            return redirect("learning_logs:index")
        
    context = {"form": form}
    return render(request, "users/login.html", context)


def logout_view(request):
    """注销"""
    logout(request)
    return redirect("learning_logs:index")