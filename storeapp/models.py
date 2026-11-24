from django.db import models


class Products(models.Model):
    ecommerce_name=models.CharField(max_length=100)
    brand_name=models.CharField(max_length=100)
    details=models.CharField(max_length=200)
    image=models.URLField()
    price=models.PositiveIntegerField()

class Contact(models.Model):
    name=models.CharField()
    email=models.EmailField()
    subject=models.CharField()
    message=models.CharField()

class Cart_item(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    session_key=models.CharField(max_length=40,blank=True,default="",db_index=True)
