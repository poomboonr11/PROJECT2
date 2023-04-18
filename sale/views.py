from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.db.models import Max
from django.db import transaction
from .models import *
import json
import re

# Create your views here.
def index(request):
    data = {}
    return render(request, 'sale/index.html', data)
def index1(request):
    data = {}
    return render(request, 'sale/index1.html', data)
def index2(request):
    data = {}
    return render(request, 'sale/index2.html', data)
def homepage2(request):
    data = {}
    return render(request, 'sale/homepage2.html', data)

def indexformanagement(request):
    data = {}
    return render(request, 'sale/indexformanagement.html', data) 


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

class CustomerDetail(View):
    def get(self, request, customer_code):
        customer = list(Customer.objects.filter(customer_code=customer_code).values())
        data = dict()
        data['customers'] = customer

        return JsonResponse(data)

class SaleList(View):
    def get(self, request):
        sales = list(Sale.objects.order_by('sale_no').all().values())
        data = dict()
        data['sales'] = sales

        return JsonResponse(data)

class SaleDetail(View):
    def get(self, request, pk, pk2):

        sale_no = pk + '/' + pk2

        sale = list(Sale.objects.select_related('customer_code')
            .filter(sale_no=sale_no)
            .values('sale_no', 'date', 'customer_code', 'customer_code__name','total'))
        
        salelineitem = list(SaleLineItem.objects.select_related('product_code')
            .filter(sale_no=sale_no)
            .values('sale_no', 'item_no', 'product_code', 'product_code__name', 'unit_price', 'quantity', 'product_total'))

        data = dict()
        data['sale'] = sale
        data['salelineitem'] = salelineitem

        return JsonResponse(data)

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'

class LineItemForm(forms.ModelForm):
    class Meta:
        model = SaleLineItem
        fields = '__all__'

@method_decorator(csrf_exempt, name='dispatch')
class SaleCreate(View):

    @transaction.atomic
    def post(self, request):
        if Sale.objects.count() != 0:        # Check Number of Record of Invoice Table == SELECT COUNT(*) FROM invoice
            sale_no_max = Sale.objects.aggregate(Max('sale_no'))['sale_no__max']    # SELECT MAX(invoice_no) FROM invoice
            sale_no_temp = [re.findall(r'(\w+?)(\d+)', sale_no_max)[0]][0]                # Split 'IN100/22' to 'IN' , '100'
            next_sale_no = sale_no_temp[0] + str(int(sale_no_temp[1])+1) + "/22"       # next_invoice_no = 'IN' + '101' + '/22' = 'IN101/22'
        else:
            next_sale_no = "IN100/22"        # If Number of Record of Invoice = 0 , next_invoice_no = IN100/22
        print(next_sale_no)
        # Copy POST data and correct data type Ex 1,000.00 -> 1000.00
        request.POST = request.POST.copy()
        request.POST['sale_no'] = next_sale_no
        request.POST['date'] = reFormatDateMMDDYYYY(request.POST['date'])
        request.POST['total'] = reFormatNumber(request.POST['total'])


        data = dict()
        # Insert correct data to invoice
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save()
            
            # Delete all invoice_line_item of invoice_no before loop insert new data
            SaleLineItem.objects.filter(sale_no=next_sale_no).delete()

            # Read lineitem from ajax and convert to json dictionary
            dict_lineitem = json.loads(request.POST['lineitem'])

            # Loop replace json data with correct data type Ex 1,000.00 -> 1000.00
            for lineitem in dict_lineitem['lineitem']:
                lineitem['sale_no'] = next_sale_no
                lineitem['product_code'] = lineitem['product_code']
                lineitem['quantity'] = reFormatNumber(lineitem['quantity'])
                lineitem['unit_price'] = reFormatNumber(lineitem['unit_price'])
                lineitem['product_total'] = reFormatNumber(lineitem['extended_price'])
                
                # Insert correct data to invoice_line_item
                formlineitem = LineItemForm(lineitem)
                try:
                    formlineitem.save()
                except :
                    # Check something error to show and rollback transaction both invoice and invoice_line_item table
                    data['error'] = formlineitem.errors
                    print (formlineitem.errors)
                    transaction.set_rollback(True)

            # if insert invoice and invoice_line_item success, return invoice data to caller
            data['sale'] = model_to_dict(sale)
        else:
            # if invoice from is not valid return error message
            data['error'] = form.errors
            print (form.errors)

        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class SaleUpdate(View):

    @transaction.atomic
    def post(self, request):
        # Get inovice_no from POST data
        sale_no = request.POST['sale_no']

        sale = Sale.objects.get(sale_no=sale_no)
        request.POST = request.POST.copy()
        request.POST['sale_no'] = sale_no
        request.POST['date'] = reFormatDateMMDDYYYY(request.POST['date'])
        request.POST['total'] = reFormatNumber(request.POST['total'])

        data = dict()
        # instance is object that will be udpated
        form = SaleForm(instance=sale, data=request.POST)
        if form.is_valid():
            sale = form.save()

            SaleLineItem.objects.filter(sale_no=sale_no).delete()

            dict_lineitem = json.loads(request.POST['lineitem'])
            for lineitem in dict_lineitem['lineitem']:
                lineitem['sale_no'] = sale_no
                lineitem['product_code'] = lineitem['product_code']
                lineitem['unit_price'] = reFormatNumber(lineitem['unit_price'])
                lineitem['quantity'] = reFormatNumber(lineitem['quantity'])
                lineitem['product_total'] = reFormatNumber(lineitem['extended_price'])
                formlineitem = LineItemForm(lineitem)
                if formlineitem.is_valid():
                    formlineitem.save()
                else:
                    data['error'] = form.errors
                    transaction.set_rollback(True)

            data['sale'] = model_to_dict(sale)
        else:
            data['error'] = form.errors
            print (form.errors)

        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class SaleDelete(View):
    def post(self, request):
        sale_no = request.POST["sale_no"]

        data = dict()
        sale = Sale.objects.get(sale_no=sale_no)
        if sale:
            sale.delete()
            SaleLineItem.objects.filter(sale_no=sale_no).delete()
            data['message'] = "Sale Deleted!"
        else:
            data['error'] = "Error!"

        return JsonResponse(data)

class SaleReport(View):
    def get(self, request, pk, pk2):
        sale_no = pk + "/" + pk2
        sale = list(Sale.objects.select_related('customer_code')
            .filter(sale_no=sale_no)
            .values('sale_no', 'date', 'customer_code', 'customer_code__name','total'))
        print(sale)
        salelineitem = list(SaleLineItem.objects.select_related('product_code')
            .filter(sale_no=sale_no)
            .values('sale_no', 'item_no', 'product_code', 'product_code__name', 'unit_price', 'quantity', 'product_total'))
        print(salelineitem)
        data = dict()
        data['sale'] =sale[0]
        data['salelineitem'] = salelineitem
        
        return render(request, 'sale/report.html', data)
class ListPaymentMethod(View):
    def get(self,request):
        payment_methods = list(PaymentMethod.objects.all().values())
        data = dict()
        data['payment_methods'] = payment_methods
        return JsonResponse(data)

class PaymentDetail(View):
    def get(self, request, payment_method):
        payment = list(PaymentMethod.objects.filter(payment_method=payment_method).values())
        data = dict()
        data['payment_methods'] = payment

        return JsonResponse(data)

def CursorToDict(data,columns):
    result = []
    fieldnames = [name.replace(" ", "_").lower() for name in columns]
    for row in data:
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result        

def reFormatDateMMDDYYYY(ddmmyyyy):
        if (ddmmyyyy == ''):
            return ''
        return ddmmyyyy[3:5] + "/" + ddmmyyyy[:2] + "/" + ddmmyyyy[6:]

def reFormatNumber(str):
        if (str == ''):
            return ''
        return str.replace(",", "")