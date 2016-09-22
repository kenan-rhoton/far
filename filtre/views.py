from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.conf import settings

from datetime import timedelta

from lxml import html
import requests
import re
#import logging

from .models import Avis, Font

import django_rq

from django_rq import job

#logger = logging.getLogger(__name__)

def index(request):
    
    avisos = Avis.objects.order_by('-data')
    
    
    now = timezone.now()
    avui = Avis.objects.filter(data__year=now.year, data__month=now.month, data__day=now.day).order_by('-data')
    now = now - timedelta(1)
    ahir = Avis.objects.filter(data__year=now.year, data__month=now.month, data__day=now.day).order_by('-data')
    week = now - timedelta(30)
    abans = Avis.objects.filter(data__range=(week, now)).order_by('-data')

    avui_set = avisos_a_dict(avui)
    ahir_set = avisos_a_dict(ahir)
    abans_set = avisos_a_dict(abans)
    
    fonts = Font.objects.all()
    context = {'avisos': avisos, 'fonts':fonts, 'avui':avui_set, 'ahir':ahir_set, 'abans':abans_set,}
    return render(request, 'filtre/index.html', context)

def avisos_a_dict(avisos):
    ret_set = {}
    for a in avisos:
        if not a.font.nom in ret_set:
            ret_set[a.font.nom] = {'font':a.font, 'num':1}
        else:
            ret_set[a.font.nom]['num'] = ret_set[a.font.nom]['num'] + 1

    return ret_set

def test_view(request, text):
    return render(request, 'filtre/echo.html', {'text':text})


def detall_avis(request, avis_id):

    avis = get_object_or_404(Avis, pk=avis_id)
    return render(request, 'filtre/detall_avis.html', {'avis':avis, 'fonts': Font.objects.all()})


def detall_font(request, font_id):
    
    font = get_object_or_404(Font, pk=font_id)
    now = timezone.now()
    avisos = font.avis_set.order_by('data')

    dates = {}

    for a in avisos:

        catalegs = font.cataleg_set.all()
        keys = []
        paraules = []
        
        for cat in catalegs:
            keys += re.split('\r\n',cat.frases)

        match = False

        for key in keys:
            if a.coincidencia.lower().find(key) > -1:
                paraules.append(key)
        
        if not dates.get(a.data.date().isoformat()):
            dates[a.data.date().isoformat()] = {}
        if not dates[a.data.date().isoformat()].get(a.url):
            dates[a.data.date().isoformat()][a.url] = {}
        if not dates[a.data.date().isoformat()][a.url].get(a.pagina):
            dates[a.data.date().isoformat()][a.url][a.pagina] = []
        dates[a.data.date().isoformat()][a.url][a.pagina].extend(paraules)
        dates[a.data.date().isoformat()][a.url][a.pagina] = list(set(dates[a.data.date().isoformat()][a.url][a.pagina]))


    dates_ordenades = []

    for d in dates.items():
        for doc, pags in d[1].items():
            pags = list(pags.items())
            pags.sort()
            d[1][doc] = pags
            print(pags)
        dates_ordenades.insert(0,d)

    dates_ordenades.sort()
    dates_ordenades.reverse()

    return render(request, 'filtre/detall_font.html', {'font':font, 'dates':dates_ordenades, 'fonts': Font.objects.all() })

def comprova_font(request, font_id):
    """
    Li encasquetem la feina a un simpàtic Worker per evitar problemes de sincronització :)
    """
    f = get_object_or_404(Font, pk=font_id)

    if settings.TESTING:
        comprovar_font(font_id)
    else:
        django_rq.enqueue(comprovar_font, font_id)
    
    return HttpResponseRedirect(reverse('filtre:detall font', args=(f.id,)))

def actualitza_tot(request):
    for f in Font.objects.all():
        res= comprova_font(request, f.id)
    return res

def analitza_font(request, font_id):
    f = get_object_or_404(Font, pk=font_id)
    if settings.TESTING:
        analitzar_font(font_id)
    else:
        django_rq.enqueue(analitzar_font, font_id)
    return HttpResponseRedirect(reverse('filtre:detall font', args=(f.id,)))


@job
def analitzar_font(font_id):
    f = get_object_or_404(Font, pk=font_id)

    import urllib.request
    import shutil
    from django.utils.text import get_valid_filename
    from django.core.files import File


    try:
        with urllib.request.urlopen(f.url) as response, open(get_valid_filename(f.url), 'wb') as out_file:
            shutil.copyfileobj(response,out_file)
    except Exception as e:
        return "There was an error with the request"

    newfile = open(get_valid_filename(f.url), 'U', encoding='utf-8', errors='ignore')

    diff = newfile.readlines()

    import re

    docregex = re.compile('<a href="[^ ]*pdf')
    
    catalegs = f.cataleg_set.all()
    keys = []
    
    for cat in catalegs:
        keys += re.split('\r\n',cat.frases)

    match = False

    for d in diff:
        for key in keys:
            if d.lower().find(key) > -1:
                #Falta purgar la coincidencia de la d
                n = Avis(coincidencia=d.replace("™", "'"),tipus='Web',url=f.url,data=timezone.now(),font=f)
                n.save()
                break

        res = docregex.search(d)
        
        if res: #Do the doc search
            docurl=res.group()[9:]
            if not (re.match("http://", docurl) or re.match("www", docurl)):

                cleanUrl = re.match('http://[^/]*', f.url)
                if cleanUrl is None:
                    cleanUrl = re.match('[^/]*', f.url)
                
                trueUrl = cleanUrl.group()
                docurl = trueUrl + docurl
            
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
                            n = Avis(coincidencia=line.replace("™", "'"),tipus="Document",pagina=i,url=docurl,data=timezone.now(),font=f)
                            n.save()
                            break

    return "OK"

@job
def comprovar_font(font_id):
    f = get_object_or_404(Font, pk=font_id)

    import urllib.request
    import shutil
    from django.utils.text import get_valid_filename
    from django.core.files import File


    try:
        with urllib.request.urlopen(f.url) as response, open(get_valid_filename(f.url), 'wb') as out_file:
            shutil.copyfileobj(response,out_file)
    except Exception as e:
        return "There was an error with the request"

    try:
        f.webfile.open('U')
    except ValueError as v:
        with open(get_valid_filename(f.url), 'rb') as new_file:
            f.webfile = File(new_file)
            f.save()

        return "Saved: " + get_valid_filename(f.url)
        #oldfile = open("tmpfile.tmp", 'U', encoding='utf-8', errors='ignore')
        
    newfile = open(get_valid_filename(f.url), 'U', encoding='utf-8', errors='ignore')

    import difflib

    data = []

    for line in f.webfile.readlines():
        data.append(line.decode('utf-8', 'ignore'))

    diff = difflib.unified_diff(data,newfile.readlines())

    import re

    diffregex = re.compile('\+[^+].*')
    docregex = re.compile('<a href="[^ ]*pdf')
    
    catalegs = f.cataleg_set.all()
    keys = []
    
    for cat in catalegs:
        keys += re.split('\r\n',cat.frases)

    match = False

    for d in diff:
        if diffregex.match(d): #Do the cataleg search

            match = True

            for key in keys:
                if d.lower().find(key) > -1:
                    #Falta purgar la coincidencia de la d
                    n = Avis(coincidencia=d.replace("™", "'"),tipus='Web',url=f.url,data=timezone.now(),font=f)
                    n.save()
                    break

            res = docregex.search(d)
            
            if res: #Do the doc search
                docurl=res.group()[9:]
                if not (re.match("http://", docurl) or re.match("www", docurl)):

                    cleanUrl = re.match('http://[^/]*', f.url)
                    if cleanUrl is None:
                        cleanUrl = re.match('[^/]*', f.url)
                    
                    trueUrl = cleanUrl.group()
                    docurl = trueUrl + docurl
                
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
                                n = Avis(coincidencia=line.replace("™", "'"),tipus="Document",pagina=i,url=docurl,data=timezone.now(),font=f)
                                n.save()
                                break
    if match == True:
        newfile.close()
        newfile = open(get_valid_filename(f.url), 'rb')
        tmpfile = File(newfile)
        f.webfile.save(get_valid_filename(f.url), tmpfile)

    return "Found match: " + str(match)
