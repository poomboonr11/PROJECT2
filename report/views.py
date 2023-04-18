from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import connection

from report.models import *
import json

# Create your views here.
def index(request):
    return render(request, 'index.html')

def central_forms(request):
    return render(request, 'central_forms.html')  

def all_forms(request):
    return render(request, 'all_forms.html')  

def forms_customer(request):
    return render(request, 'forms_customer.html')  

def forms_product(request):
    return render(request, 'forms_product.html')  

def forms_payment_method(request):
    return render(request, 'forms_payment_method.html')  

def customer(request):
    customer_code = request.GET.get('customer_code', '')
    customers = list(Customer.objects.filter(customer_code=customer_code).values())
    data = dict()
    data['customers'] = customers
    
    return render(request, 'forms_customer.html', data)
    
def product(request):
    code = request.GET.get('code', '')
    products = list(Product.objects.filter(code=code).values())
    data = dict()
    data['products'] = products
    
    return render(request, 'forms_product.html', data)

def payment_method(request):
    payment_method = request.GET.get('payment_method','')
    payment_methods = list(PaymentMethod.objects.filter(payment_method=payment_method).values())
    data = dict()
    data['payment_methods'] = payment_methods
    
    return render(request, 'forms_payment_method.html', data)


class ProductList(View):
    def get(self, request):
        products = list(Product.objects.all().values())
        data = dict()
        data['products'] = products

        return JsonResponse(data)

class CustomerList(View):
    def get(self, request):
        customers = list(Customer.objects.all().values())
        data = dict()
        data['customers'] = customers

        return JsonResponse(data)

class CustomerGet(View):
    def get(self, request, customer_code):
        customers = list(Customer.objects.filter(customer_code=customer_code).values())
        data = dict()
        data['customers'] = customers

        return JsonResponse(data)        

class ProductGet(View):
    def get(self, request, code):
        products = list(Product.objects.filter(code=code).values())
        data = dict()
        data['products'] = products

        return JsonResponse(data)        

class PaymentMethodList(View):
    def get(self, request):
        payment_methods = list(PaymentMethod.objects.all().values())
        data = dict()
        data['payment_methods'] = payment_methods

        return JsonResponse(data) 

class PaymentMethodGet(View):
    def get(self, request, payment_method):
        payment_methods = list(PaymentMethod.objects.filter(payment_method=payment_method).values())
        data = dict()
        data['payment_methods'] = payment_methods
        
        return JsonResponse(data)       

@method_decorator(csrf_exempt, name='dispatch')
class CustomerSave(View):
    def post(self, request):

        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            return JsonResponse(ret)

        customers = list(Customer.objects.all().values())
        data = dict()
        data['customers'] = customers
        
        return render(request, 'forms_customer.html', data)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

@method_decorator(csrf_exempt, name='dispatch')
class CustomerSave2(View):
    def post(self, request):

        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            ret['customers'] = list()
            return JsonResponse(ret)

        customers = list(Customer.objects.all().values())
        data = dict()
        data['customers'] = customers

        return JsonResponse(data)
        #return render(request, 'forms_customer.html', data)

@method_decorator(csrf_exempt, name='dispatch')
class CustomerDelete(View):
    def post(self, request):

        customer_code = request.POST['customer_code']
        customer = Customer.objects.get(customer_code=customer_code)
        data = dict()
        if customer:
            customer.delete()
            data['message'] = "Customer Deleted!"
        else:
            data['message'] = "Error!"
            return JsonResponse(data)

        customers = list(Customer.objects.all().values())
        data['customers'] = customers

        return JsonResponse(data)
        #return render(request, 'forms_customer.html', data)


def ReportListAllProducts(request):
    
    dataReport = dict()
    data = list(Product.objects.all().values())
    columns = ("Code", "Name", "Units", "Product Type")
    dataReport['column_name'] = columns
    dataReport['data'] = data
    

    return render(request, 'report_list_all_products.html', dataReport)

def ReportListAllSales(request):
    cursor = connection.cursor()
    cursor.execute ('SELECT i.sale_no as "Sale No", i.date as "Date" '
                             ' , c.customer_code as "Customer Code" '
                             ' , i.total as "Total"'
                             ' FROM sale i JOIN customer c ON c.customer_code = i.customer_code '
                             ' ')
    dataReport = dict()
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    dataReport['column_name'] = columns
    dataReport['data'] = CursorToDict(data,columns)

    return render(request, 'report_list_all_sales.html', dataReport)

def ReportListAllSalesLineItem(request):

    cursor = connection.cursor()
    cursor.execute ('SELECT ili.sale_no as "Sale No", p.code as "Product Code",p.name as "Product Name"'
                            ', ili.quantity as "Quantity", ili.unit_price as "Unit Price"'
                            ', ili.product_total as "Product Total" '
                            'FROM sale_line_item ili JOIN sale i ON i.sale_no = ili.sale_no '
                            'JOIN product p ON p.code = ili.product_code'
                             ' ')
    dataReport = dict()
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    dataReport['column_name'] = columns
    dataReport['data'] = CursorToDict(data,columns)
    print(dataReport)
    return render(request, 'report_list_all_sales_line_item.html', dataReport)

def CursorToDict(data,columns):
    result = []
    fieldnames = [name.replace(" ", "_").lower() for name in columns]
    for row in data:
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result

#Product
@method_decorator(csrf_exempt, name='dispatch')
class ProductSave(View):
    def post(self, request):

        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            return JsonResponse(ret)

        products = list(Product.objects.all().values())
        data = dict()
        data['products'] = products
        
        return render(request, 'forms_product.html', data)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

@method_decorator(csrf_exempt, name='dispatch')
class ProductSave2(View):
    def post(self, request):

        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            ret['products'] = list()
            return JsonResponse(ret)

        products = list(Product.objects.all().values())
        data = dict()
        data['products'] = products

        return JsonResponse(data)
        #return render(request, 'forms_product.html', data)

@method_decorator(csrf_exempt, name='dispatch')
class ProductDelete(View):
    def post(self, request):

        code = request.POST['code']
        product = Product.objects.get(code=code)
        data = dict()
        if product:
            product.delete()
            data['message'] = "Product Deleted!"
        else:
            data['message'] = "Error!"
            return JsonResponse(data)

        products = list(Product.objects.all().values())
        data['products'] = products

        return JsonResponse(data)
        #return render(request, 'forms_product.html', data)

#paymentmetthod


@method_decorator(csrf_exempt, name='dispatch')
class PaymentMethodSave(View):
    def post(self, request):

        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            return JsonResponse(ret)

        payment_methods = list(PaymentMethod.objects.all().values())
        data = dict()
        data['payment_methods'] = payment_methods
        
        return render(request, 'forms_payment_method.html', data)

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

@method_decorator(csrf_exempt, name='dispatch')
class PaymentMethodSave2(View):
    def post(self, request):

        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            ret['payment_methods'] = list()
            return JsonResponse(ret)

        payment_methods = list(PaymentMethod.objects.all().values())
        data = dict()
        data['payment_methods'] = payment_methods

        return JsonResponse(data)
        #return render(request, 'forms_payment_method.html', data)

@method_decorator(csrf_exempt, name='dispatch')
class PaymentMethodDelete(View):
    def post(self, request):

        payment_method = request.POST['payment_method']
        payment_method = PaymentMethod.objects.get(payment_method=payment_method)
        data = dict()
        if payment_method:
            payment_method.delete()
            data['message'] = "PaymentMethod Deleted!"
        else:
            data['message'] = "Error!"
            return JsonResponse(data)

        payment_methods = list(PaymentMethod.objects.all().values())
        data['payment_methods'] = payment_methods

        return JsonResponse(data)
        #return render(request, 'forms_payment_method.html', data)
