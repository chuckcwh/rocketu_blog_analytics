from django.contrib import admin

# Register your models here.
from analytics.models import Location, View, Page

admin.site.register(Page)
admin.site.register(View)
admin.site.register(Location)