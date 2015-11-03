from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone

from lxml import html
import requests
import re

from .models import Noticia, Font

def index(request):
    noticies = Noticia.objects.order_by('-data')
    fonts = Font.objects.all()
    context = {'noticies': noticies, 'fonts':fonts,}
    return render(request, 'filtre/index.html', context)

def detall_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    return render(request, 'filtre/detall_noticia.html', {'noticia':noticia, 'fonts': Font.objects.all()})


def detall_font(request, font_id):
    font = get_object_or_404(Font, pk=font_id)
    noticies = font.noticia_set.all()
    frases = ""
    for cat in font.cataleg_set.all():
        frases += cat.nom + "\n"
    error = font.haserror
    font.haserror = False
    return render(request, 'filtre/detall_font.html', {'font':font, 'noticies': noticies, 'fonts': Font.objects.all(), 'frases': frases, 'error': error })

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
