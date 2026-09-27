from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """注册表单：Django自带密码强度校验"""
    
    class Meta:
        model = User
        fields = ["username"]
        labels = {"username": "用户名"}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 一次性给所有字段套上Bootstrap样式
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            

class LoginForm(AuthenticationForm):
    """登录表单"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"