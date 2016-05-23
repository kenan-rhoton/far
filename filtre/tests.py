import datetime

from django.utils import timezone
from django.test import TestCase

from django.core.urlresolvers import reverse

from .models import Font, Avis, Cataleg


class FontTests(TestCase):

    def test_es_crea_correctament(self):
        """
        Test innecessari per provar
        """
        f = Font(nom="Potato",url="www.google.com",horari=timezone.now())
        f.save()
        self.assertEqual(f, Font.objects.all()[0])

    def test_inicialitza_font_crea_arxiu_amb_informacio_de_la_url(self):
        f = Font(nom="Test", url=reverse('filtre:test', args=("potatoes",)), horari=timezone.now())
        f.save()
        c = Cataleg(frases="potatoes")
        c.save()

        response = self.client.get(reverse('filtre:inicialitza font', args=(f.id,)), follow=True)

        self.assertIsNotNone(f.webfile)

    def test_inicialitza_font_no_afegeix_avis_encara_que_hi_hagi_coincidencia(self):
        f = Font(nom="Test", url=reverse('filtre:test', args=("potatoes",)), horari=timezone.now())
        f.save()
        c = Cataleg(frases="potatoes")
        c.save()

        response = self.client.get(reverse('filtre:inicialitza font', args=(f.id,)), follow=True)

        self.assertEqual(0,len(Avis.objects.all()))
        #Crea font que sigui una url propia
        #Posem una dada a la url que "coincidiria"
        #Inicialitzem la font
        #Comprovem que no hi han avisos
        pass

    def test_comprova_font_dona_error_si_no_esta_inicialitzat(self):
        pass

    def test_comprova_font_no_afegeix_avis_si_esta_inicialitzat_pero_no_hi_ha_coincidencia(self):
        pass

    def test_comprova_font_afegeix_avis_si_esta_inicialitzat_i_hi_ha_coincidencia(self):
        pass
        #Crea font que sigui una url propia
        #Posem una dada a la url que "coincidiria"
        #Inicialitzem la font
        #Canviem la url i posem una altra dada que "coincidiria"
        #Comprovem la font
        #Hi ha un avis

    #def test_comprova_afegeix_avis_si_en_troba(self):
    #  """
    #  Actualitzar funciona quan troba una font
    #  """
    #  f = Font(nom="LHC",url="http://hasthelargehadroncolliderdestroyedtheworldyet.com/",horari=timezone.now())
    #  f.save()
    #  c = Cataleg(frases="nope")
    #  c.save()
    #  c.fonts.add(f)
    #  c.save()

    #  response = self.client.get(reverse('filtre:comprova font', args=(f.id,)), follow=True)

    #  self.assertContains(response, "<a href=\"/avis/1/\">NOPE.")
    #  self.assertEqual(1,len(Avis.objects.all()))

    def test_comprova_no_afegeix_url_si_no_troba_coincidencia(self):
      """
      Actualitzar funciona quan no troba una font
      """
      f = Font(nom="LHC",url="http://hasthelargehadroncolliderdestroyedtheworldyet.com/",horari=timezone.now())
      f.save()
      c = Cataleg(frases="potato")
      c.save()
      c.fonts.add(f)
      c.save()

      response = self.client.get(reverse('filtre:comprova font', args=(f.id,)), follow=True)

      self.assertNotContains(response, "<a href=\"/avis/1/\">")

    def test_comprova_no_afegeix_avis_si_no_troba_coincidencia(self):
      """
      Actualitzar funciona quan no troba una font
      """
      f = Font(nom="LHC",url="http://hasthelargehadroncolliderdestroyedtheworldyet.com/",horari=timezone.now())
      f.save()
      c = Cataleg(frases="potato")
      c.save()
      c.fonts.add(f)
      c.save()

      response = self.client.get(reverse('filtre:comprova font', args=(f.id,)), follow=True)

      self.assertEqual(0,len(Avis.objects.all()))

    def test_actualitza_avisa_si_no_es_conecta(self):
      """
      Actualitzar avisa quan no hi ha conectivitat o problema similar
      """
      f = Font(nom="LHC",url="http://Aquestanoesunawebrealoaixoespero.cat/",horari=timezone.now())
      f.save()
      c = Cataleg(frases="potato")
      c.save()
      c.fonts.add(f)
      c.save()

      response = self.client.get(reverse('filtre:comprova font', args=(f.id,)), follow=True)

      self.assertContains(response, "contacta amb un administrador")
