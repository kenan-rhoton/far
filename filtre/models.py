from django.db import models



class Font(models.Model):
    nom = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    path = models.CharField(max_length=200) #Deprecated
    #FUTURE WORK
    #¿Find a better method than XPath selection?
    #textpath = models.CharField(max_length=200)
    #urlpath = models.URLField(max_length=200)
    #tipus: HTML o PDF
    horari = models.TimeField('Hora d\'actualització')
    haserror = models.BooleanField(default=False)
    #frases = models.TextField()
    def __str__(self):
        return self.nom
    def noerror(self):
        self.haserror = False

class Noticia(models.Model):
    titol = models.CharField(max_length=200)
    data = models.DateTimeField('Data de publicació')
    #FUTURE WORK
    #text = models.CharField(max_length=200)
    #link = models.URLField(max_length=200)
    font = models.ForeignKey(Font)
    def __str__(self):
        return self.titol

class Cataleg(models.Model):
    nom = models.CharField(max_length=200)
    frases = models.TextField()
    fonts = models.ManyToManyField(Font)
    def __str__(self):
        return self.nom

class Avis(models.Model):
    coincidencia = models.CharField(max_length=2000)
    tipus = models.CharField(max_length=20) #Pot ser Document o Web
    pagina = models.IntegerField()
    url = models.URLField(max_length=2000) #Potencialment no és el mateix que el de la Font (si es d'un document intern)
    data = models.DateTimeField("Data de l'avís")
    font = models.ForeignKey(Font)
    def __str__(self):
        return self.coincidencia
