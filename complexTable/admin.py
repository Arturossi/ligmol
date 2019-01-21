from django.contrib import admin

from .models import Complex

class ChoiceInline(admin.TabularInline):
    model = Complex
    extra = 1

class complexAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['id']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('id')
    list_filter = ['id']
    search_fields = ['id']

admin.site.register(Complex)