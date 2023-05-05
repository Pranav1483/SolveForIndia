from django.urls import path
from . import views

urlpatterns = [
    path('api/admin/product/', views.create_product, name='create_product'),
    path('api/admin/reports/', views.reports, name='all_reports'),
    path('api/admin/reports/<id>', views.indv_reports, name='indv_reports'),
    path('', views.login, name='login'),
    path('dashboard/', views.logincheck, name='dashboard'),
    path('dashboard/reports/', views.show_reports, name='show_reports'),
    path('dashboard/reports/delete/<id>', views.delete_reports, name='delete_reports'),
    path('dashboard/createpdt/', views.createpdt, name='createpdt'),
    path('dashboard/createpdt/1/', views.createpdtfn, name='createproductfn'),
    path('dashboard/showpdt/', views.showpdt, name="showpdt"),
    path('dashboard/showpdt/delete/<id>', views.deletepdt, name='deletepdt'),
    path('dashboard/logout/', views.logout, name='logout'),
    path('dashboard/reports/back/', views.back, name='back_from_reports'),
    path('dashboard/createpdt/back/', views.back, name='back_from_createpdt'),
    path('dashboard/showpdt/back/', views.back, name='back_from_showpdt'),
]
