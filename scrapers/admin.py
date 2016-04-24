from django.contrib import admin

from .models import URL, State, Provider


class UrlAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'state', 'provider')
    list_filter = ('state', 'provider')
    ordering = ('url', 'state', 'provider')
    search_fields = ('url',)

admin.site.register(URL, UrlAdmin)
admin.site.register(State)
admin.site.register(Provider)
