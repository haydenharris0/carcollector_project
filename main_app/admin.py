from django.contrib import admin
from .models import Car, Washing, Accessory, Photo

# Register your models here.
admin.site.register(Car)
admin.site.register(Washing)
admin.site.register(Accessory)
admin.site.register(Photo)
