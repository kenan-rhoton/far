import datetime

from django.utils import timezone
from django.test import LiveServerTestCase

from django.core.urlresolvers import reverse

from .models import Font, Avis, Cataleg

import time

class FontTests(LiveServerTestCase):

    def tearDown(self):
        pass

    def test_es_crea_correctament(self):
        """
        Test innecessari per provar
        """
        f = Font(nom="Potato",url="http://www.google.com",horari=timezone.now())
        f.save()

        self.assertEqual(f, Font.objects.latest('id'))

    def test_es_mostra_correctament(self):
        f = Font(nom="Potato",url="http://www.google.com",horari=timezone.now())
        f.save()

        response = self.client.get(reverse('filtre:index'))

        self.assertContains(response, "Potato")

    def test_comprova_font_te_arxiu_none_inicialment(self):
        f = Font(nom="Test", url="http://www.google.com", horari=timezone.now())
        f.save()

        self.assertRaises(ValueError, f.webfile.name)

    def test_comprova_font_crea_arxiu_si_es_el_primer_cop(self):
        f = Font(nom="Test", url=self.live_server_url+reverse('filtre:test', args=("cabbages",)), horari=timezone.now())
        f.save()
        c = Cataleg(frases="google")
        c.save()
        c.fonts.add(f)
        c.save()

        response = self.client.get(reverse('filtre:comprova font', args=(f.id,)), follow=True)

        f.refresh_from_db()

        self.assertNotEquals(f.webfile.file.size,0)

    def test_comprova_font_no_afegeix_avis_encara_que_hi_hagi_coincidencia_si_es_el_primer_cop(self):

        size = len(Avis.objects.all())

        f = Font(nom="Potatoes", url="http://www.google.com", horari=timezone.now())
        f.save()
        c = Cataleg(frases="potatoes")
        c.save()
        c.fonts.add(f)
        c.save()

        response = self.client.get(reverse('filtre:comprova font', args=(f.id,)), follow=True)

        self.assertEqual(size,len(Avis.objects.all()))

    def test_comprova_font_no_afegeix_avis_si_esta_inicialitzat_pero_no_hi_ha_coincidencia(self):

        f = Font(nom="Test", url=self.live_server_url+reverse('filtre:test', args=("cabbages",)), horari=timezone.now())
        f.save()
        c = Cataleg(frases="potatoes")
        c.save()
        c.fonts.add(f)
        c.save()

        response = self.client.get(reverse('filtre:comprova font', args=(f.id,)), follow=True)

        f.url=(self.live_server_url+reverse('filtre:test', args=("soup",)))
        f.save()

        response = self.client.get(reverse('filtre:comprova font', args=(f.id,)), follow=True)

        self.assertEqual(0,len(Avis.objects.all()))

    def test_comprova_font_afegeix_avis_si_esta_inicialitzat_i_hi_ha_coincidencia(self):
        size = len(Avis.objects.all())
        f = Font(nom="Test", url=self.live_server_url+reverse('filtre:test', args=("cabbages",)), horari=timezone.now())
        f.save()
        c = Cataleg(frases="potatoes")
        c.save()
        c.fonts.add(f)
        c.save()

        response = self.client.get(reverse('filtre:comprova font', args=(f.id,)), follow=True)

        f.refresh_from_db()
        f.url = self.live_server_url+reverse('filtre:test', args=("potatoes\n<br\>potatoes\n<br\>cabbages\n<br\>soup potato",))
        f.save()

        response = self.client.get(reverse('filtre:comprova font', args=(f.id,)), follow=True)

        f.refresh_from_db()

        self.assertEqual(len(Avis.objects.all()), 2)

    def test_comprova_font_caracters_extranys_no_la_lien(self):
        size = len(Avis.objects.all())
        f = Font(nom="Test", url=self.live_server_url+reverse('filtre:test', args=("cabbages",)), horari=timezone.now())
        f.save()
        c = Cataleg(frases="Llei Orgànica 1/2004\nLlei catalana 5/2008\nviolència masclista\nviolència de genere\ndones assassinades\nvíctimes de violència de gènere\nsupervivents de violència\ndones immigrants\ntràfic de persones\nexplotació sexual\nintèrprets judicials\ntorns d'ofici amb especialització en matèria de violència de gènere\nviolència sexual\nformació i disponibilitat d'intèrprets\ndones refugiades\nesclavitud\ndenúncies de víctimes\nProtocol de Protecció de les Víctimes de Tràfic d'éssers Humans a Catalunya\nagressions sexuals\natenció sanitària\navortament")
        c.save()
        c.fonts.add(f)
        c.save()

        response = self.client.get(reverse('filtre:comprova font', args=(f.id,)), follow=True)

        f.refresh_from_db()
        f.url = self.live_server_url+reverse('filtre:test', args=("Llei Orgànica \n<br\>violència masclista\n<br\>denúncies\n<br\>avortament",))
        f.save()

        response = self.client.get(reverse('filtre:comprova font', args=(f.id,)), follow=True)

        f.refresh_from_db()

        self.assertEqual(len(Avis.objects.all()), 2)



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
      size = len(Avis.objects.all())
      f = Font(nom="LHC",url="http://hasthelargehadroncolliderdestroyedtheworldyet.com/",horari=timezone.now())
      f.save()
      c = Cataleg(frases="potato")
      c.save()
      c.fonts.add(f)
      c.save()

      response = self.client.get(reverse('filtre:comprova font', args=(f.id,)), follow=True)

      self.assertEqual(size,len(Avis.objects.all()))

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

      #self.assertContains(response, "contacta amb un administrador")
