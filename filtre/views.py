from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone

from lxml import html
import requests
import re
#import logging

from .models import Noticia, Font

#logger = logging.getLogger(__name__)

def index(request):
    
    noticies = Noticia.objects.order_by('-data')
    fonts = Font.objects.all()
    context = {'noticies': noticies, 'fonts':fonts,}
    return render(request, 'filtre/index.html', context)



def detall_noticia(request, noticia_id):

    noticia = get_object_or_404(Noticia, pk=noticia_id)
    return render(request, 'filtre/detall_noticia.html', {'noticia':noticia, 'fonts': Font.objects.all()})

def detall_avis(request, avis_id):

    avis = get_object_or_404(Avis, pk=avis_id)
    return render(request, 'filtre/detall_avis.html', {'avis':avis, 'fonts': Font.objects.all()})


def detall_font(request, font_id):
    
    font = get_object_or_404(Font, pk=font_id)
    avisos = font.avis_set.all()
    frases = ""

    for cat in font.cataleg_set.all():
        frases += cat.frases + ";"
    return render(request, 'filtre/detall_font.html', {'font':font, 'avisos': avisos, 'fonts': Font.objects.all(), 'frases': frases })

def comprova_font(request, font_id):
    f = get_object_or_404(Font, pk=font_id)

    import urllib.request
    import shutil
    import django.utils.text
    
    with urllib.request.urlopen(f.url) as response, open(django.utils.text.get_valid_filename(f.url + "1"), 'wb') as out_file:
        shutil.copyfileobj(response,out_file)

    oldfile = open(django.utils.text.get_valid_filename(f.url), 'U', encoding='utf-8', errors='ignore')
    newfile = open(django.utils.text.get_valid_filename(f.url + "1"), 'U', encoding='utf-8', errors='ignore')

    import difflib

    diff = difflib.unified_diff(oldfile.readlines(),newfile.readlines())

    import re

    diffregex = re.compile('\+[^+].*')
    docregex = re.compile('<a href="[^ ]*pdf')
    
    catalegs = f.cataleg_set.all()
    keys = []
    
    for cat in catalegs:
        keys += re.split('[;:, \n]',cat.frases)

    for d in diff:
        if diffregex.match(d): #Do the cataleg search
            
            for key in keys:
                if d.lower().find(key) > -1:
                    #Falta purgar la coincidencia de la d
                    n = Avis(coincidencia=d,tipus='Web',url=f.url,data=timezone.now(),font=f)
                    n.save()
                    break

            res = docregex.search(d)
            
            if res: #Do the doc search
                docurl=res.group()[9:]
                if not (re.match("http://", docurl) or re.match("www", docurl)):
                    docurl = f.url + docurl
                import PyPDF2
                with urllib.request.urlopen(docurl) as response, open('tmp.pdf', 'wb') as out_file:
                    shutil.copyfileobj(response,out_file)

                fp = open("tmp.pdf", 'rb')
                pdfReader = PyPDF2.PdfFileReader(fp)

                for i in range(0,pdfReader.numPages-1):
                    pageObj = pdfReader.getPage(i)
                    txtlines = pageObj.extractText().splitlines()
                    for line in txtlines:
                        for key in keys:
                            if line.lower().find(key) > -1:
                                #Mejorar las coincidencias
                                n = Avis(coincidencia=line,tipus="Document",pagina=i,url=docurl,data=timezone.now(),font=f)
                                n.save()
                                break

    return HttpResponseRedirect(reverse('filtre:detall font', args=(f.id,)))


def actualitza_font(request, font_id):

    f = get_object_or_404(Font, pk=font_id)
    
    try:
        page = requests.get(f.url)
    except:
        f.haserror = True
        return HttpResponseRedirect(reverse('filtre:detall font', args=(f.id,)))
    
    if page.status_code != 200:
        f.haserror = True
        return HttpResponseRedirect(reverse('filtre:detall font', args=(f.id,)))
    
    tree = html.fromstring(page.text)
    dataset = tree.xpath(f.path)
    catalegs = f.cataleg_set.all()
    keys = []
    
    for cat in catalegs:
        keys += re.split('[;:, \n]',cat.frases)
    
    #FUTURE WORK:
    #añadir texto y url
    #Comprobar errores (no fallar si no hay internet)
    
    for dat in dataset:
        if not f.noticia_set.filter(titol__exact = dat).exists():
            for key in keys:
                if dat.lower().find(key) > -1:
                    n = Noticia(titol=dat,data=timezone.now(),font=f)
                    n.save()
                    break

    return HttpResponseRedirect(reverse('filtre:detall font', args=(f.id,)))
