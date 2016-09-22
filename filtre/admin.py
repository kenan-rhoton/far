## En aquest fitxer es defineixen totes les classes que permeten administrar els models des del panel d'administració


from django.contrib import admin

from .models import Font, Avis, Cataleg

## Aquesta classe permet gestionar el Model Font des de la aplicació d'administració
class FontAdmin(admin.ModelAdmin):
	list_display = ('nom', 'url')
	fieldsets = [
        (None, {'fields': ['nom', 'url', 'catalegs']}),
    ]
            
## Aquesta classe permet gestionar el Model Avis des de l'aplicació d'administració (tot i que no hauria de ser necessaria i apareix sobretot a nivell informatiu)
class AvisAdmin(admin.ModelAdmin):
	#FUTURE WORK: text i URL
	fieldsets = [
        (None, {'fields': ['coincidencia', 'url', 'tipus', 'pagina', 'data', 'font']}),
    ]

## Aquesta classe permet gestionar el Model Catàleg des de l'aplicació d'administració
class CatalegAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    fieldsets = [
        (None, {'fields': ['nom', 'frases', 'fonts']}),
    ]

admin.site.register(Font, FontAdmin)
admin.site.register(Avis, AvisAdmin)
admin.site.register(Cataleg, CatalegAdmin)
