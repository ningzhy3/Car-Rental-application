from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from customer_portal.models import *
from django.contrib.auth.decorators import login_required
# from car_dealer_portal.models import *
from django.http import HttpResponseRedirect
import datetime
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'customer/login.html')
    else:
        return render(request, 'customer/home_page.html')

def login(request):
    return render(request, 'customer/login.html')

def auth_view(request):
    if request.user.is_authenticated:
        return render(request, 'customer/home_page.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            customer = Customer.objects.get(user = user)
        except:
            customer = None
        if customer is not None:
            auth.login(request, user)
            return render(request, 'customer/home_page.html')
        else:
            return render(request, 'customer/login_failed.html')

def logout_view(request):
    auth.logout(request)
    return render(request, 'customer/login.html')

def register(request):
    return render(request, 'customer/register.html')

def registration(request):
    username = request.POST['username']
    password = request.POST['password']
    
    firstname = request.POST['first_name']
    lastname = request.POST['last_name']
    email = request.POST['email']
    city = request.POST['city']
    city = city.lower()
    state = request.POST['state']
    zipcode = request.POST['zipcode']
    street = request.POST['street']
    customertype = request.POST['customer_type']

    dln = request.POST['dln']
    ins_name = request.POST['ins_name']
    ins_no = request.POST['ins_no']
    try:
        user = User.objects.create_user(username = username, password = password, email = email)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
    except:
        return render(request, 'customer/registration_error.html')
    # try:
    #     area = Area.objects.get(city = city, pincode = pincode)
    # except:
    #     area = None
    # if area is not None:
    #     customer = Customer(user = user, mobile = mobile, area = area)
    # else:
    #     area = Area(city = city, pincode = pincode)
    #     area.save()
    #     area = Area.objects.get(city = city, pincode = pincode)

    customer = Customer(user = user, first_name = firstname, last_name = lastname, email = email, 
    city = city, state = state, zipcode = zipcode, street = street, customer_type = customertype)
    coupon = Coupon.objects.get(id=1)
    customer.save()

    individual = Individual(user = user, customer_ptr = customer, dln = dln, ins_name = ins_name, ins_no = ins_no,coupon = coupon)

    individual.save()
    return render(request, 'customer/registered.html')

# @login_required
# def search(request):
#     return render(request, 'customer/search.html')

# @login_required
# def search_results(request):
#     city = request.POST['city']
#     city = city.lower()
#     vehicles_list = []
#     area = Area.objects.filter(city = city)
#     for a in area:
#         vehicles = Vehicles.objects.filter(area = a)
#         for car in vehicles:
#             if car.is_available == True:
#                 vehicle_dictionary = {'name':car.car_name, 'color':car.color, 'id':car.id, 'pincode':car.area.pincode, 'capacity':car.capacity, 'description':car.description}
#                 vehicles_list.append(vehicle_dictionary)
#     request.session['vehicles_list'] = vehicles_list
#     return render(request, 'customer/search_results.html')


@login_required
def rent_vehicle(request):
    # # return render(request, 'customer/confirmation.html', )
    # return render(request, 'customer/rent_failed.html', )
    customer = Customer.objects.get(user = request.user)
    try: 
        rental_service = Rental_service.objects.get(customer_id = customer) 
        return render(request, 'customer/rent_failed.html', )
    except:
        return render(request, 'customer/confirmation.html', )


@login_required
def return_vehicle(request):
    
    customer = Customer.objects.get(user = request.user)
    try:
        rental_service = Rental_service.objects.get(customer_id = customer)
        try:
            invoice = Invoice.objects.get(rental_service = rental_service)
            return render(request, 'customer/return_failed.html')
        except:
            return render(request, 'customer/return.html', {'rental_service':rental_service})
    except:
        return render(request, 'customer/return_failed.html')

@login_required
def return_detail(request):
    customer = Customer.objects.get(user = request.user)

    rental_service = Rental_service.objects.get(customer_id = customer) 
    e_odometer = request.POST['e_odometer']
    #update rental_service table
    rental_service.objects.filter(id=rental_service.id).update(e_odometer=e_odometer)

    
    invoice = Invoice.objects.get(rental_service = rental_service)
    

    vehicle = rental_service.vin
    vehicle_class = Vehicle_class.objects.get(id = vehicle.vehicle_class)

    rent_charge = vehicle_class.rent_charge
    extra_charge = vehicle_class.extra_charge

    s_odometer = rental_service.s_odometer
    e_odometer = rental_service.e_odometer
    d_odometer_limit = rental_service.d_odometer_limit

    if customer.customer_type == 'I':
        individual = individual.objects.get(user = request.user)
        coupon = Coupon.objects.get(id = individual.coupon)
        discount = coupon.coupon_rate
    else:
        corporate = Corporate.objects.get(user = request.user)
        corporation = Corporation.objects.get(id = corporate.corporation)
        discount = corporation.corp_discount

    interval = rental_service.d_date - rental_service.p_date
    days = interval.days

    if (e_odometer-s_odometer) > d_odometer_limit:
        sum = days*rent_charge+extra_charge*(e_odometer-s_odometer)
    else:
        sum = days*rent_charge

    amount=discount*sum
    
    
    # Rental_service.objects.filter(customer_id=customer).delete()
    date=datetime.date.today()

    invoice = Invoice(invoice_amount = amount, invoice_date = date, rental_service = rental_service)
    invoice.save()

    return render(request, 'customer/return_detail.html',)

    

@login_required
def invoice(request):
    


    customer = Customer.objects.get(user = request.user)
    rental_service = Rental_service.objects.get(customer_id = customer) 

    invoice = Invoice.objects.get(rental_service = rental_service)

    return render(request, 'customer/invoice.html',{'invoice':invoice})

@login_required
def pay(request):
    
    return render(request, 'customer/pay.html')
    

@login_required
def confirm(request):
    username = request.user
    customer = Customer.objects.get(user = request.user)
    customer_id = customer.id 

    days = request.POST['days']
    p_location = Location.objects.get(city = request.POST['p_location'])
    d_location = Location.objects.get(city = request.POST['d_location'])

    p_date = request.POST['p_date']
    d_date = request.POST['d_date']

    s_odometer = 0
    e_odometer = 0
    d_odometer_limit = 0
    
    vehicle = Vehicle.objects.get(model = request.POST['model'])

    rental_service = Rental_service(customer_id = customer, p_location = p_location,
    d_location = d_location, p_date = p_date, d_date = d_date, s_odometer = s_odometer,
    e_odometer = e_odometer, vin = vehicle, d_odometer_limit = d_odometer_limit)
    rental_service.save()

    return render(request, 'customer/confirmed.html')

    # if vehicle.is_available:
    #     car_dealer = vehicle.dealer
    #     rent = (int(vehicle.capacity))*300*(int(days))
    #     car_dealer.wallet += rent
    #     car_dealer.save()
    #     try:
    #         order = Orders(vehicle = vehicle, car_dealer = car_dealer, user = user, rent=rent, days=days)
    #         order.save()
    #     except:
    #         order = Orders.objects.get(vehicle = vehicle, car_dealer = car_dealer, user = user, rent=rent, days=days)
    #     vehicle.is_available = False
    #     vehicle.save()
    #     return render(request, 'customer/confirmed.html', {'order':order})
    # else:
    #     return render(request, 'customer/order_failed.html')

# @login_required
# def manage(request):
#     order_list = []
#     user = User.objects.get(username = request.user)
#     try:
#         orders = Orders.objects.filter(user = user)
#     except:
#         orders = None
#     if orders is not None:
#         for o in orders:
#             if o.is_complete == False:
#                 order_dictionary = {'id':o.id,'rent':o.rent, 'vehicle':o.vehicle, 'days':o.days, 'car_dealer':o.car_dealer}
#                 order_list.append(order_dictionary)
#     return render(request, 'customer/manage.html', {'od':order_list})

# @login_required
# def update_order(request):
#     order_id = request.POST['id']
#     order = Orders.objects.get(id = order_id)
#     vehicle = order.vehicle
#     vehicle.is_available = True
#     vehicle.save()
#     car_dealer = order.car_dealer
#     car_dealer.wallet -= int(order.rent)
#     car_dealer.save()
#     order.delete()
#     cost_per_day = int(vehicle.capacity)*300
#     return render(request, 'customer/confirmation.html', {'vehicle':vehicle}, {'cost_per_day':cost_per_day})

# @login_required
# def delete_order(request):
#     order_id = request.POST['id']
#     order = Orders.objects.get(id = order_id)
#     car_dealer = order.car_dealer
#     car_dealer.wallet -= int(order.rent)
#     car_dealer.save()
#     vehicle = order.vehicle
#     vehicle.is_available = True
#     vehicle.save()
#     order.delete()
#     return HttpResponseRedirect('/customer_portal/manage/')


@login_required
def pay_confirmed(request):
    payment_number = request.POST.get('payment_number')
    payment_method = request.POST.get('payment_method')
    payment_name = request.POST.get('payment_name')
    customer = Customer.objects.get(user = request.user)
    rental_service = Rental_service.objects.get(customer_id = customer) 
    invoice = Invoice.objects.get(rental_service = rental_service)
    
    payment_amount = invoice.invoice_amount

    payment_date = datetime.date.today()
    payment = Payment(payment_amount = payment_amount, payment_number = payment_number, 
    payment_method = payment_method, inovice = invoice, payment_date = payment_date)
    payment.save()

    return render(request, 'customer/confirmed.html')