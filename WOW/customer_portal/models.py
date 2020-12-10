from django.db import models
from datetime import date
from django.db.models import Subquery, OuterRef
from django.contrib.auth.models import User

#
class Corporation(models.Model):
    copr_name = models.CharField(max_length=30)
    registration_number = models.CharField(max_length=30)
    corp_discount = models.FloatField()

class Coupon(models.Model):
    coupon_rate = models.FloatField() 
    start_date = models.DateField()
    end_date = models.DateField()

# vehicle_class model
class Vehicle_class(models.Model):
    vehicle_type = models.CharField(max_length=30)
    rent_charge = models.FloatField()
    extra_charge = models.FloatField()

    def __str__(self):
        return 'Vehicle_class %s' % (self.vehicle_type)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # user
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    street = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    customer_type = models.CharField(max_length=1, choices=(
        ('C', 'Corporate'),
        ('I', 'Individual')
    ))

# location model
class Location(models.Model):
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=5)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return 'Office located in %s' % (self.self.street_address)

# vehicle model
class Vehicle(models.Model):
    vin = models.CharField(max_length=17, primary_key=True)
    make = models.CharField(max_length=5)
    model = models.CharField(max_length=5)
    year = models.CharField(max_length=4)
    lpn = models.CharField(max_length=6)

    location = models.ForeignKey(Location,on_delete=models.SET_NULL, null=True)
    vehicle_class = models.ForeignKey(Vehicle_class,on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s, model year %s' % (self.vin, self.model)

class Rental_service(models.Model):
    p_date = models.DateField()
    d_date = models.DateField()
    s_odometer = models.FloatField()
    e_odometer = models.FloatField()
    d_odometer_limit = models.FloatField()

    p_location = models.ForeignKey(Location,on_delete=models.SET_NULL, null=True,related_name='p_loaction')
    d_location = models.ForeignKey(Location,on_delete=models.SET_NULL, null=True,related_name='d_loaction')
    vin = models.ForeignKey(Vehicle,on_delete=models.SET_NULL, null=True)
    customer_id = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True)


# invoice model
class Invoice(models.Model):
    invoice_date = models.DateField()
    invoice_amount = models.FloatField()

    rental_service = models.ForeignKey(Rental_service,on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return 'Invoice issued at %s with amount %s' % (self.invoice_date, self.invoice_amount)

# payment model
class Payment(models.Model):
    payment_date = models.DateField()
    payment_amount = models.FloatField()
    payment_method = models.CharField(max_length=30)
    payment_number = models.CharField(max_length=16)
    inovice = models.ForeignKey(Invoice,on_delete=models.SET_NULL, null=True)

    def __str__(self):
            return '%s paid on %s for the invoice %s' % (self.payment_amount, self.payment_date, str(self.invoice))







class Corporate(Customer):
    employee_ID = models.CharField(max_length=30)

    corporation = models.ForeignKey(Corporation,on_delete=models.SET_NULL, null=True)

class Individual(Customer):
    dln = models.CharField(max_length=10)
    ins_name = models.CharField(max_length=30)
    ins_no = models.CharField(max_length=30)

    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL, null=True)

