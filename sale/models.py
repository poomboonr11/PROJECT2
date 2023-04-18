from django.db import models

# Create your models here.
class ProductType(models.Model):
    product_type = models.CharField(max_length=10,primary_key=True)
    description = models.CharField(max_length=100)
    class Meta:
        db_table = "product_type"
        managed = False
    def __str__(self):
        return self.product_type

class Product(models.Model):
    code = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=100)
    units = models.CharField(max_length=10)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, db_column='product_type')
    class Meta:
        db_table = "product"
        managed = False
    def __str__(self):
        return self.code

class Customer(models.Model):
    customer_code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, null=True)
    customer_tel = models.CharField(max_length=10)
    class Meta:
        db_table = "customer"
        managed = False
    def __str__(self):
        return self.customer_code

class PaymentMethod(models.Model):
    payment_method = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=100)
    class Meta:
        db_table = "payment_method" # ตั้งตาม table ใน Pgadmin4
        managed = False
    def __str__(self):
        return self.payment_method


class Sale(models.Model):
    sale_no = models.CharField(max_length=10, primary_key=True)
    date = models.DateField(null=True)
    customer_code = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='customer_code')
    total = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = "sale"
        managed = False
    def __str__(self):
        return self.sale_no

class SaleLineItem(models.Model): #มีบัคของ จังเกิ้ล เพื่อไปหลอกให้เป็น PK 
    sale_no = models.ForeignKey(Sale, on_delete=models.CASCADE, db_column='sale_no')
    item_no = models.IntegerField()
    product_code = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_code')
    quantity = models.IntegerField(null=True)
    unit_price = models.FloatField(null=True)
    product_total = models.FloatField(null=True)
    class Meta:
        db_table = "sale_line_item"
        unique_together = ("sale_no", "item_no")
        managed = False
    def __str__(self):
        return '{"sale_no":"%s","item_no":"%s","product_code":"%s","product_name":"%s","quantity":%s,"unit_price":"%s","product_total":"%s"}' % (self.sale_no, self.item_no, self.product_code, self.product_code.name, self.quantity, self.unit_price, self.product_total)
