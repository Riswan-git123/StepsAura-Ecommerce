from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from .collections import shoes
from .models import Products,Contact,Cart_item
from .form import ContactForm
import json

def cart_session_key(request):
    if request.session.session_key is None:
        request.session.create()
    return request.session.session_key


def cart_count(request):
    return sum(Cart_item.objects.filter(session_key=cart_session_key(request)).values_list("quantity", flat=True))


def cart_total(items):
    return sum(item.product.price * item.quantity for item in items)


def home(request):
    if not Products.objects.exists():
        for shoe in shoes:
            Products.objects.create(ecommerce_name=shoe['ecommerce_name'],
                                    brand_name=shoe['brand_name'],
                                    details=shoe['details'],
                                    image=shoe['image'],
                                    price=shoe['price'])
    product_datas=Products.objects.all()
    count=cart_count(request)
    if request.method=="POST":
        try:
            data=json.loads(request.body or b"{}")
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"message":"Invalid request"},status=400)
        if data.get('action') == 'add':
            try:
                result=add_product_to_cart(request, data.get('id'))
            except (ValueError, Products.DoesNotExist):
                return JsonResponse({"message":"Product not found"},status=404)
            return JsonResponse({"message":"success","count":result})
        return JsonResponse({"message":"Unsupported action"},status=400)

    return render(request,'home.html',{"shoes":product_datas,"count":count})

def cart(request):
    session_key=cart_session_key(request)
    items=Cart_item.objects.filter(session_key=session_key).select_related("product")
    if request.method=="POST":
        try:
            data=json.loads(request.body or b"{}")
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"message":"Invalid request"},status=400)
        item=items.filter(id=data.get('id')).first()
        if item is None:
            return JsonResponse({"message":"Cart item not found"},status=404)
        item.delete()
        remaining=list(Cart_item.objects.filter(session_key=session_key).select_related("product"))
        return JsonResponse({
            'message':'Deleted',
            'empty':not remaining,
            'total':cart_total(remaining),
            'count':sum(item.quantity for item in remaining),
        })

    items=list(items)
    return render(request,'cart.html',{"carts":items,"total":cart_total(items),"count":sum(item.quantity for item in items)})

def details(request,id):
    product=Products.objects.get(id=id)
    return render(request,'details.html',{"product":product,"count":cart_count(request)})

def add_product_to_cart(request, product_id):
    if product_id is None:
        raise ValueError("A product id is required")
    product_details=Products.objects.get(id=product_id)
    session_key=cart_session_key(request)
    items=Cart_item.objects.filter(product=product_details,session_key=session_key).first()
    if items:
        items.quantity += 1
        items.save()
    else:
        Cart_item.objects.create(product=product_details,quantity=1,session_key=session_key)
    count=cart_count(request)
    return count


def cart_item(request, product_id):
    if request.method != "POST":
        return JsonResponse({"message":"Use POST to add a product"},status=405)
    try:
        count=add_product_to_cart(request,product_id)
    except (ValueError, Products.DoesNotExist):
        return JsonResponse({"message":"Product not found"},status=404)
    return JsonResponse({"message":"success","count":count})



def contact(request):
    print("your metthod is",request.method)

    form=ContactForm()
    if request.method=="POST":
        form=ContactForm(request.POST)

        if form.is_valid():
            print("form valid")
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            subject=form.cleaned_data['subject']
            message=form.cleaned_data['message']
            print(name,email,subject,message)

            Contact.objects.create(name=name,email=email,subject=subject,message=message)
            print("datas are inserted")

        else:
            print("invalid")
    count=cart_count(request)
            # print(form.errors)
    return render(request,'contact.html',{"form":form,"count":count})


def order_placed(request):
    return render(request,'order_placed.html'
                  
                  )
def signup(request):
    count=cart_count(request)
    return render(request,'signup.html',{"count":count})

def login(request):
    count=cart_count(request)
    return render(request,'login.html',{"count":count})
