from django.contrib import admin
from wiki_page.models import WikiPage

class WikiPageAdmin(admin.ModelAdmin):
    list_display = ('slug','last_edit', 'author', 'ttl', 'version')
	
admin.site.register(WikiPage, WikiPageAdmin)
