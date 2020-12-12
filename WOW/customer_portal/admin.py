from django.contrib import admin
from .models import *
admin.site.register(Customer)
admin.site.register(Vehicle)

admin.site.register(Individual)

admin.site.register(Corporate)
admin.site.register(Corporation)

admin.site.register(Vehicle_class)
admin.site.register(Coupon)
admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(Rental_service)
admin.site.register(Location)


# Register your models here.


