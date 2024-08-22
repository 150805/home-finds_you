from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from .models import House,CustomUser
from .decorators import login_required
from django.db import IntegrityError
@login_required
def house_list(request):
    houses = House.objects.filter(booked=False)

    # Filtering logic
    location = request.GET.get('location')
    if location:
        houses = houses.filter(location__icontains=location)

    price = request.GET.get('price')
    if price:
        houses = houses.filter(price__lte=price)

    bedrooms = request.GET.get('bedrooms')
    if bedrooms:
        houses = houses.filter(bedrooms__gte=bedrooms)

    context = {
        'houses': houses,
    }
    return render(request, 'house_list.html', context)

@login_required
def house_detail(request, house_id):
    if request.method == 'POST':
        house.booked = True
        house.save()
    house = get_object_or_404(House, id=house_id)
    return render(request, 'house_detail.html', {'house': house})

# Booking view
def book_house(request, house_id):
    house = get_object_or_404(House, id=house_id)
    house.booked_by = CustomUser.objects.get(id=request.session['user_id']).email
    house.booked = True
    house.save()
    return redirect('dash')

def signup(request):
    error_message = None
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password != password2:
            error_message = 'Passwords do not match'
        else:
            try:
                # Attempt to create new user
                new_user = CustomUser(name=name, email=email, password=password)
                new_user.save()
                return redirect('login')  # Redirect to login page after successful signup
            
            except IntegrityError:
                error_message = 'Email already exists. Please use a different email.'
    
    return render(request, 'signup.html', {'error_message': error_message})
def login(request):
        error_message=None
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                # Handle invalid login credentials
                return render(request, 'login.html', {'error_message': 'Invalid email or password'})
            
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return redirect('dash')  # Redirect to dashboard or home page after successful login
            error_message = 'Invalid email or password'
            # Handle invalid login credentials
         #   return render(request, 'login.html', {'error': 'Invalid email or password'})
        return render(request, 'login.html', {'error_message': error_message})
        #return render(request, 'login.html')
def logout_view(request):
    user=CustomUser.objects.get(id=request.session['user_id'])
    if request.method=='POST': 

        if 'user_id' in request.session:
            del request.session['user_id']
            return redirect('/')
    return render(request, 'logout.html', {'user':user})
        