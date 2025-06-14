from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('store:home')
        else:
            messages.error(request, '使用者名稱或密碼錯誤')
            # 如果是 modal 請求，返回 modal 模板
            if 'modal' in request.POST:
                return render(request, 'accounts/login_modal.html', {'form': form})
    else:
        form = AuthenticationForm()
    # 預設返回獨立頁面
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('store:home')
        else:
            messages.error(request, '請修正表單錯誤')
            # 如果是 modal 請求，返回 modal 模板
            if 'modal' in request.POST:
                return render(request, 'accounts/register_modal.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'accounts/logged_out.html')