from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user_model, password_validation
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

def logout_view(request):
    logout(request)
    return redirect("home")

def register_view(request):
    email = ""
    first_name = ""
    last_name = ""
    errors = {}
    
    if request.method == "POST":
        # Lấy dữ liệu từ form
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        
        User = get_user_model()

        # Kiểm tra trường first_name có trống không
        if not first_name:
            errors.setdefault("first_name", []).append("Tên không được để trống.")
        
        # Kiểm tra trường email có trống không
        if email:
            # Kiểm tra email đã tồn tại hay chưa
            if User.objects.filter(email=email).exists():
                errors.setdefault("email", []).append("Email này đã được sử dụng.")
            # Kiểm tra email có đúng định dạng không
            try:
                validate_email(email)
            except Exception:
                errors.setdefault("email", []).append("Vui lòng nhập địa chỉ email hợp lệ.")
        else:
            errors.setdefault("email", []).append("Email không được để trống.")
        
        # Kiểm tra trường password có trống không
        if password:
            try:
                # Tạo user tạm thời để validate trường password
                temp_user = User(
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )

                password_validation.validate_password(password, user=temp_user)
            except ValidationError as e:
                # Tìm từng tin nhắn lỗi và thêm vào error dict bản dịch
                for error in e.messages:
                    if "short" in error.lower():
                        message = "Mật khẩu quá ngắn, cần ít nhất 8 ký tự."
                    elif "common" in error.lower():
                        message = "Mật khẩu quá phổ biến."
                    elif "numeric" in error.lower():
                        message = "Mật khẩu không thể chỉ chứa số."
                    elif "similar" in error.lower():
                        message = "Mật khẩu quá giống với thông tin cá nhân."

                    errors.setdefault("password", []).append(message)
        else:
            errors.setdefault("password", []).append("Mật khẩu không được để trống.")

        # Kiểm tra trường password2 có trống không
        if password2:
            # Kiểm tra 2 trường password có giống nhau không
            if password != password2:
                errors.setdefault("password2", []).append("Hai mật khẩu không khớp.")
        else:
            errors.setdefault("password2", []).append("Mật khẩu xác nhận không được để trống.")

        # Tạo user nếu như không có lỗi
        if not errors:
            try:
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                login(request, user)
                return redirect("home")
            except Exception as e:
                errors['general'] = [f"Lỗi khi tạo tài khoản: {str(e)}"]
    
    context = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "errors": errors
    }
    return render(request, "user/register.html", context)

@login_required
def profile_detail_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        # Kiểm tra trường first_name có trống không
        if not first_name:
            messages.error(request, "Tên không được để trống.")
        
        # Cập nhật thông tin người dùng nếu không có lỗi
        if not messages.get_messages(request):
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()
            messages.success(request, "Cập nhật thông tin thành công.")

    context = {
        "email": request.user.email,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
    }
    return render(request, "user/profile.html", context)