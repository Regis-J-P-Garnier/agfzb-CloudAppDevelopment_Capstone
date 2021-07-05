from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5
    show_change_link = True

class CarMakeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'description')
    inlines = [CarModelInline]

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('make', 'name', 'dealerId', 'type', 'year')
    list_filter = ['make']
    search_fields = ['make', 'name']

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
