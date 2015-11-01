from django.contrib import admin

from .models import Font, Noticia, Cataleg

class CatalegInline(admin.StackedInline):
	model = Cataleg.fonts.through
	extra = 1

class FontAdmin(admin.ModelAdmin):
	list_display = ('nom', 'url', 'horari')
	#FUTURE WORK: textpath i urlpath
	fieldsets = [
        (None, {'fields': ['nom', 'url', 'path', 'horari']}),
    ]
	inlines = [CatalegInline]
	
class NoticiaAdmin(admin.ModelAdmin):
	#FUTURE WORK: text i URL
	fieldsets = [
        (None, {'fields': ['titol', 'data', 'font']}),
    ]
	
class CatalegAdmin(admin.ModelAdmin):
    list_display = ('nom')
    fieldsets = [
        (None, {'fields': ['nom', 'frases', 'fonts']}),
    ]

admin.site.register(Font, FontAdmin)
admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Cataleg, CatalegAdmin)
