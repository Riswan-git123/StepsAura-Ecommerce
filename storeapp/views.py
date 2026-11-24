from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from .collections import shoes
from .models import Products,Contact,Cart_item
from .form import ContactForm
import json

def home(request):
    print("dfvbjhdfbvjhdfbvjdfbvjdfhbfdhjbvhdfbhvdfbhdfvb")
    # brand_name="STEPSAURA"
    if not Products.objects.exists():
        for shoe in shoes:
            Products.objects.create(ecommerce_name=shoe['ecommerce_name'],
                                    brand_name=shoe['brand_name'],
                                    details=shoe['details'],
                                    image=shoe['image'],
                                    price=shoe['price'])
        print("datas inserted")
    product_datas=Products.objects.all()
    count=Cart_item.objects.count()
    if request.method=="POST":
        data=json.loads(request.body)
        action=data['action']
        print(action)
        if action == 'add':
            result=cart_item(request)
            count=result
            return JsonResponse({"message":"success","count":result})
        # elif action == 'remove':
        #     cart_remove(request)
        else:
            print("not found")
        
        # details(re)
    
    
    return render(request,'home.html',{"shoes":product_datas,"count":count})

def cart(request):
    cart=Cart_item.objects.all()
    total=0
    for item in cart:
        total+=item.product.price
    
   
    if request.method=="POST":
        data=json.loads(request.body)
        id=data.get('id')
        items=Cart_item.objects.get(id=id)
        items.delete()
        datas=Cart_item.objects.all()
        total=0
        for item in datas:
                total+=item.product.price
        count=Cart_item.objects.count()
        empty=False
        if not datas:
            empty=True
            return JsonResponse({'message':'Deleted','empty':empty,'total':total,"count":count})
        else:
            empty=False
            return JsonResponse({'message':'Deleted','empty':empty,'total':total,"count":count})
        
    # print("your total amount is",total)

    count=Cart_item.objects.count()
    return render(request,'cart.html',{"carts":cart,"total":total,"count":count})

# def cart_remove(id):

#     items=Cart_item.objects.get(id=id)
#     items.delete()
#     print(id)
#     return JsonResponse({'message':'Deleted'})

def details(request,id):
    product=Products.objects.get(id=id)
    return render(request,'details.html',{"product":product})

def cart_item(request):
    data=json.loads(request.body)
    id=data.get('id')
    product_details=Products.objects.get(id=id)
    items=Cart_item.objects.filter(product=product_details).first()
    if items:
        items.quantity += 1
        items.save()
    else:
        Cart_item.objects.create(product=product_details,quantity=1)
    count=Cart_item.objects.count()
    return count



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
    count=Cart_item.objects.count()
            # print(form.errors)
    return render(request,'contact.html',{"form":form,"count":count})


def order_placed(request):
    return render(request,'order_placed.html'
                  
                  )
def signup(request):
    count=Cart_item.objects.count()
    return render(request,'signup.html',{"count":count})

def login(request):
    count=Cart_item.objects.count()
    return render(request,'login.html',{"count":count})