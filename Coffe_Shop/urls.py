"""Coffe_Shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from sale import views
from report import views as views_report
urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('sale', views.index, name='index'),
    path('index1', views.index1, name='index1'),
    path('index2', views.index2, name='index2'),
    path('homepage2', views.homepage2, name='homepage2'),
    path('indexformanagement',views.indexformanagement,name='indexformanagement'),
    path('users/',include('app_users.urls')),
    

    path('product/list', views.ProductList.as_view(), name='product_list'),
    path('customer/list', views.CustomerList.as_view(), name='customer_list'),
    path('customer/detail/<customer_code>', views.CustomerDetail.as_view(), name='customer_detail'),

    path('sale/list', views.SaleList.as_view(), name='sale_list'),
    path('sale/detail/<str:pk>/<str:pk2>', views.SaleDetail.as_view(), name='sale_detail'),
    path('sale/create', views.SaleCreate.as_view(), name='sale_create'),
    path('sale/update', views.SaleUpdate.as_view(), name='sale_update'),
    path('sale/delete', views.SaleDelete.as_view(), name='sale_delete'),
    path('sale/report/<str:pk>/<str:pk2>', views.SaleReport.as_view(), name='sale_report'),

    path('payment_method/list', views.ListPaymentMethod.as_view(), name='payment_method_list'),
    path('payment_method/detail/<payment_method>', views.PaymentDetail.as_view(), name='paymemt_detail'),

    path('admin/', admin.site.urls),
    path('', views_report.index, name='Index'),
    path('report', views_report.index, name='Index'),
    path('all_forms.html',views_report.all_forms,name='all_forms.html'),
    path('central_forms',views_report.central_forms,name='central_forms'),
    path('forms_customer',views_report.forms_customer,name='forms_customer'),
    path('forms_product',views_report.forms_product,name='forms_product'),
    path('forms_payment_method',views_report.forms_payment_method,name='forms_payment_method'),

    path('ReportListAllSales', views_report.ReportListAllSales),
    path('ReportListAllSalesLineItem', views_report.ReportListAllSalesLineItem),
    path('ReportListAllProducts', views_report.ReportListAllProducts),

    path('customer/list', views_report.CustomerList.as_view(), name='customer_list'), 
    path('customer/get', views_report.customer), 
    path('customer/get/<customer_code>', views_report.CustomerGet.as_view(), name='customer_get'), 
    path('customer/save', views_report.CustomerSave.as_view(), name='customer_save'),   
    path('customer/save2', views_report.CustomerSave2.as_view(), name='customer_save2'), 
    path('customer/delete', views_report.CustomerDelete.as_view(), name='customer_delete'), 

    path('product/list', views_report.ProductList.as_view(), name='product_list'),
    path('product/get', views_report.product), 
    path('product/get/<product_code>', views_report.ProductGet.as_view(), name='product_get'), 
    path('product/save', views_report.ProductSave.as_view(), name='product_save'),   
    path('product/save2', views_report.ProductSave2.as_view(), name='product_save2'), 
    path('product/delete', views_report.ProductDelete.as_view(), name='product_delete'), 

    path('payment_method/list', views_report.PaymentMethodList.as_view(), name='payment_method_list'), 
    path('payment_method/get', views_report.payment_method), 
    path('payment_method/get/<payment_method>', views_report.PaymentMethodGet.as_view(), name='payment_method_get'), 
    path('payment_method/save', views_report.PaymentMethodSave.as_view(), name='payment_method_save'),   
    path('payment_method/save2', views_report.PaymentMethodSave2.as_view(), name='payment_method_save2'), 
    path('payment_method/delete', views_report.PaymentMethodDelete.as_view(), name='payment_method_delete'), 

]
