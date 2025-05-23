from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("profile/detail/", views.profile_detail_view , name="profile_detail"),
    path("profile/orders/", views.order_tracking_view , name="order_tracking"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name="password_reset_complete"),
    path("password_change/", auth_views.PasswordChangeView.as_view(template_name='user/password_change.html'), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'), name="password_change_done"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
]
