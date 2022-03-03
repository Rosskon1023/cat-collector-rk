from django.contrib import admin

# Register your models here.

from .models import Cat, Toy, Feeding, Photo

admin.site.register(Cat)
admin.site.register(Toy)
admin.site.register(Feeding)
admin.site.register(Photo)