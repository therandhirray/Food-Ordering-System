from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Order
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.

def index_page(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', {'recipes': recipes})

@login_required(login_url='/login/')
def order_page(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == "POST":
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        quantity = int(request.POST.get('quantity'))
        total_price = quantity * recipe.price
        
        order = Order.objects.create(
            user=request.user,
            recipe=recipe,
            address=address,
            phone_number=phone_number,
            quantity=quantity,
            total_price=total_price
        )
        
        # # Here you can integrate SMS sending functionality for order confirmation
        messages.info(request, 'Order Placed Successfully!')
        return redirect('/home/')
    
    return render(request, 'order.html', {'recipe': recipe})

def confirm_order(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        
        username = request.POST.get('username')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))
        total = float(request.POST.get('total'))

        # Process the order and save to the database
        Order.objects.create(
            user=request.user,
            recipe=recipe,
            address=address,
            phone_number=phone,
            quantity=quantity,
            total_price=total
        )
    return render(request, 'confirmation.html')

def profile_page(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-id')
    return render(request, 'profile.html', {'user': user, 'orders': orders})

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username = username).exists():
            messages.info(request, 'Invalid Username')
            return redirect('/login/')
        
        user = authenticate(username = username, password = password)
        
        if user is None:
            messages.info(request, 'Invalid Password')
            return redirect('/login/')
        else:
            login(request, user)
            next_url = request.GET.get('next', '/home/')
            return redirect(next_url)
        
    return render(request, 'login.html' )

def logout_page(request):
    logout(request)
    return redirect('/home/')

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, 'Username Already Taken')
            return redirect('/register/')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
        )
        user.set_password(password)
        user.save() 
        
        messages.info(request, 'Account Created Successfully !')
        
        return redirect('/register/')
    
    return render(request, 'register.html' )