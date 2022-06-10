from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ReviewData
from .models import BuildingData

admin.site.register(BuildingData)
admin.site.register(ReviewData)