from django.urls import path
from . import views

urlpatterns = [
    path('api/product/<id>', views.get_product, name='get_product'),
    path('api/user/<id>', views.get_user, name='get_user'),
    path('api/user/register/', views.register_user, name='register'),
    path('api/user/addpdt/', views.add_product, name='add_product'),
    path('api/user/login/', views.login, name='login'),
    path('api/user/report/', views.report_product, name='report_product'),
    path('api/user/sendotp/', views.send_otp, name='send_otp'),
    path('api/user/verifyotp/', views.check_otp, name='verify_otp'),
    path('api/user/changepwd/', views.edit_password, name='change_password'),
    path('dashboard/', views.dashboard, name='user_dashboard'),
    path('', views.user_login, name="user_login"),
    path('register/', views.register, name="user_register"),
    path('register/1/', views.registration, name='registration'),
    path('dashboard/report/', views.report_page, name='report_page'),
    path('dashboard/report/1/', views.report_page_submit, name='submit_report'),
    path('dashboard/logout/', views.logout, name="user_logout"),
    path('forgotpwd/', views.forgotpwd, name="forgotpwd"),
    path('forgotpwd/1/', views.forgotpwd_mail, name="forgotpwd_mail"),
    path('forgotpwd/1/2/', views.verify_otp, name="verify_otp_page"),
    path('forgotpwd/1/2/3/', views.change_password, name="change_password_page"),
    path('forgotpwd/1/resend/', views.resend_otp, name='resend_otp_page'),
    path('dashboard/addproduct/', views.addproduct, name='addproductpage'),
    path('dashboard/addproduct/1/', views.addproduct_fn, name='addproductfn'),

]