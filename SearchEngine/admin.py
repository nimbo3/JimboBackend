from django.contrib import admin

from SearchEngine.models import Search


@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    search_fields = ['query']
    list_filter = ['language', 'category', 'search_time']
    list_display_links = ['query']
    list_display = ['query', 'language', 'category', 'user', 'search_time']
    readonly_fields = ['query', 'language', 'category', 'user', 'result', 'search_time']
