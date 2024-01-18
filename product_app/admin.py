from django.contrib import admin

from . import models
# Register your models here.

admin.site.register(models.Clothes)
admin.site.register(models.Category)
admin.site.register(models.Review)
admin.site.register(models.Rating)
admin.site.register(models.WishList)
admin.site.register(models.Order)
