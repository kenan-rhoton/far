## Aquí es defineixen els models de dades, quedarán reflectits a la Bases de Dades

from django.db import models

# Aquest model conté informació sobre les Font's d'informació.
# -   nom: conté el nom donat per l'administrador a la font
# -   url: conté la adreça web de la font
# -   webfile: conté el contingut de la font a la última actualització
# -   horari: conté la hora del servidor en la que s'actualitzará la font
class Font(models.Model):
    nom = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    webfile = models.FileField(upload_to='filtre.WebFileModel/dades/nom/mimetype', blank=True, null=True)
    horari = models.TimeField('Hora d\'actualització')
    def __str__(self):
        return self.nom

# Aquest model conté informació sobre els Catàlegs de paraules d'interés
# -   nom: conté el nom donat per l'administrador al Catàleg
# -   frases: conté les frases que conformen el Catàleg
# -   fonts: conté les asociacions a les Fonts que fan servir el Catàleg
class Cataleg(models.Model):
    nom = models.CharField(max_length=200)
    frases = models.TextField()
    fonts = models.ManyToManyField(Font)
    def __str__(self):
        return self.nom

# Aquest model conté informació sobre els Avisos
# -   coincidencia: Part del document que ha fet saltar l'Avís
# -   tipus: Indica si l'Avís ha saltat en un Document o a una Web
# -   pagina: En cas de ser tipus Document, conté la pàgina que ha provocat l'Avís
# -   url: adreça electrónica on hi ha el document o web
# -   data: conté la data en que va saltar l'Avís
# -   font: conté la font on va saltar l'Avís
class Avis(models.Model):
    coincidencia = models.CharField(max_length=2000)
    tipus = models.CharField(max_length=20) #Pot ser Document o Web
    pagina = models.IntegerField(null=True)
    url = models.URLField(max_length=2000) #Potencialment no és el mateix que el de la Font (si es d'un document intern)
    data = models.DateTimeField("Data de l'avís")
    font = models.ForeignKey(Font)
    def __str__(self):
        return self.coincidencia
    class Meta:
        verbose_name = "avís"
        verbose_name_plural = "avisos"

## FOR DB FILE STORAGE

# Aquest model conté informació sobre els Arxius de contingut de les Fonts (ja que Heroku no ens dona llibertat amb el disc dur)
# -   dades: conté les dades en format Unicode
# -   nom: nom de l'arxiu
# -   mimetype: tipus MIME de l'arxiu
class WebFileModel(models.Model):
    dades = models.TextField()
    nom = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)
