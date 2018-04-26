from django.contrib import admin

# Register your models here.
from eaves.models import *

# admin.site.register(Author, AuthorAdmin)

admin.site.register(Community)
admin.site.register(FloorPlan)
admin.site.register(Apartment)
admin.site.register(AptPrice)
