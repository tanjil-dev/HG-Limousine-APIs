from django.contrib import admin

from .models import CarModel


admin.site.register(CarModel)

admin.site.site_header = "H&G Limousine"
admin.site.site_title = "H&G Limousine Admin"
admin.site.index_title = "H&G Limousine Dashboard"