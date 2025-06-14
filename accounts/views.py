from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': '/'
                })
            return redirect('store:home')
        else:
            messages.error(request, '使用者名稱或密碼錯誤')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                html = render_to_string('accounts/login_modal.html', {'form': form}, request=request)
                return JsonResponse({
                    'success': False,
                    'html': html
                })
    else:
        form = AuthenticationForm()
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
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': '/'
                })
            return redirect('store:home')
        else:
            messages.error(request, '請修正表單錯誤')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                html = render_to_string('accounts/register_modal.html', {'form': form}, request=request)
                return JsonResponse({
                    'success': False,
                    'html': html
                })
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'accounts/logged_out.html')