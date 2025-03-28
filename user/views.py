from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages

def login_view(request):
    email = ""

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            email = form.data["username"]
            messages.error(request, "Email hoặc mật khẩu không đúng")
    
    context = {
        "email": email,
    }
    return render(request, "user/login.html", context)
