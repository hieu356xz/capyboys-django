## Giới thiệu
Dự án Django này là website cửa hàng cho môn Phát triển Ứng dụng Python.

## Cài đặt & chạy dự án
1. Tạo môi trường ảo và kích hoạt:

```
python -m venv .\env
.\env\Scripts\Activate.ps1
```

2. Cài dependencies và áp migrations:

```
pip install -r requirements.txt
python manage.py migrate
```

3. Chạy server phát triển:

```
python manage.py runserver
```
