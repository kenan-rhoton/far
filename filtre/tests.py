import datetime

from django.utils import timezone
from django.test import TestCase

from django.core.urlresolvers import reverse

from .models import Font, Noticia, Cataleg


class FontTests(TestCase):

    def test_es_crea_correctament(self):
        """
        Test innecessari per provar
        """
        f = Font(nom="Potato",url="www.google.com",path="//h1.text()",horari=timezone.now())
        f.save()
        self.assertEqual(f, Font.objects.all()[0])

    def test_actualitza_afegeix_noticia_si_en_troba(self):
      """
      Actualitzar funciona quan troba una font
      """
      f = Font(nom="LHC",url="http://hasthelargehadroncolliderdestroyedtheworldyet.com/",path="//noscript/text()",horari=timezone.now())
      f.save()
      c = Cataleg(frases="nope")
      c.save()
      c.fonts.add(f)
      c.save()

      response = self.client.get(reverse('filtre:actualitza font', args=(f.id,)), follow=True)

      self.assertContains(response, "<a href=\"/noticia/1/\">NOPE.")
      self.assertEqual(1,len(Noticia.objects.all()))

    def test_actualitza_no_afegeix_noticia_si_no_en_troba(self):
      """
      Actualitzar funciona quan no troba una font
      """
      f = Font(nom="LHC",url="http://hasthelargehadroncolliderdestroyedtheworldyet.com/",path="//noscript/text()",horari=timezone.now())
      f.save()
      c = Cataleg(frases="potato")
      c.save()
      c.fonts.add(f)
      c.save()

      response = self.client.get(reverse('filtre:actualitza font', args=(f.id,)), follow=True)

      self.assertNotContains(response, "<a href=\"/noticia/1/\">")
      self.assertEqual(0,len(Noticia.objects.all()))

    def test_actualitza_avisa_si_no_es_conecta(self):
      """
      Actualitzar avisa quan no hi ha conectivitat o problema similar
      """
      f = Font(nom="LHC",url="http://Aquestanoesunawebrealoaixoespero.cat/",path="//noscript/text()",horari=timezone.now())
      f.save()
      c = Cataleg(frases="potato")
      c.save()
      c.fonts.add(f)
      c.save()

      response = self.client.get(reverse('filtre:actualitza font', args=(f.id,)), follow=True)

      self.assertContains(response, "contacta amb un administrador")
      self.assertEqual(0,len(Noticia.objects.all()))
