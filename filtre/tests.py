import datetime

from django.utils import timezone
from django.test import LiveServerTestCase

from django.core.urlresolvers import reverse

from .models import Font, Avis, Cataleg

import time

class FontTests(LiveServerTestCase):

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

    def test_analitza_font_afegeix_avis_si_hi_ha_coincidencia(self):
        size = len(Avis.objects.all())
        f = Font(nom="Test", url=self.live_server_url+reverse('filtre:test', args=("potatoes\r\n<br\>potatoes\r\n<br\>cabbages\r\n<br\>soup potato",)), horari=timezone.now())
        f.save()
        c = Cataleg(frases="potatoes")
        c.save()
        c.fonts.add(f)
        c.save()

        response = self.client.get(reverse('filtre:analitza font', args=(f.id,)), follow=True)

        f.refresh_from_db()

        self.assertEqual(len(Avis.objects.all()), 2)

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
        f.url = self.live_server_url+reverse('filtre:test', args=("potatoes\r\n<br\>potatoes\r\n<br\>cabbages\r\n<br\>soup potato",))
        f.save()

        response = self.client.get(reverse('filtre:comprova font', args=(f.id,)), follow=True)

        f.refresh_from_db()

        self.assertEqual(len(Avis.objects.all()), 2)

    def test_comprova_font_caracters_extranys_no_la_lien(self):
        size = len(Avis.objects.all())
        f = Font(nom="Test", url=self.live_server_url+reverse('filtre:test', args=("cabbages",)), horari=timezone.now())
        f.save()
        c = Cataleg(frases="Llei Orgànica 1/2004\r\nLlei catalana 5/2008\r\nviolència masclista\r\nviolència de genere\r\ndones assassinades\r\nvíctimes de violència de gènere\r\nsupervivents de violència\r\ndones immigrants\r\ntràfic de persones\r\nexplotació sexual\r\nintèrprets judicials\r\ntorns d'ofici amb especialització en matèria de violència de gènere\r\nviolència sexual\r\nformació i disponibilitat d'intèrprets\r\ndones refugiades\r\nesclavitud\r\ndenúncies de víctimes\r\nProtocol de Protecció de les Víctimes de Tràfic d'éssers Humans a Catalunya\r\nagressions sexuals\r\natenció sanitària\r\navortament")
        c.save()
        c.fonts.add(f)
        c.save()

        response = self.client.get(reverse('filtre:comprova font', args=(f.id,)), follow=True)

        f.refresh_from_db()
        f.url = self.live_server_url+reverse('filtre:test', args=("Llei Orgànica \r\n<br\>violència masclista\r\n<br\>denúncies\r\n<br\>avortament",))
        f.save()

        response = self.client.get(reverse('filtre:comprova font', args=(f.id,)), follow=True)

        f.refresh_from_db()

        self.assertEqual(len(Avis.objects.all()), 2)

    def test_comprova_actualitza_tot_crea_arxius_correctament(self):
        f1 = Font(nom="Test", url=self.live_server_url+reverse('filtre:test', args=("cabbages",)), horari=timezone.now())
        f2 = Font(nom="Test", url=self.live_server_url+reverse('filtre:test', args=("cabbages",)), horari=timezone.now())
        f3 = Font(nom="Test", url=self.live_server_url+reverse('filtre:test', args=("cabbages",)), horari=timezone.now())
        f1.save()
        f2.save()
        f3.save()
        c = Cataleg(frases="google")
        c.save()
        c.fonts.add(f1)
        c.fonts.add(f2)
        c.fonts.add(f3)
        c.save()

        response = self.client.get(reverse('filtre:actualitza tot'), follow=True)

        f1.refresh_from_db()
        f2.refresh_from_db()
        f3.refresh_from_db()

        self.assertNotEquals(f1.webfile.file.size,0)
        self.assertNotEquals(f2.webfile.file.size,0)
        self.assertNotEquals(f3.webfile.file.size,0)


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

    def test_avisos_generats_tenen_data(self):
        size = len(Avis.objects.all())
        f = Font(nom="Test", url=self.live_server_url+reverse('filtre:test', args=("potatoes\r\n<br\>potatoes\r\n<br\>cabbages\r\n<br\>soup potato",)), horari=timezone.now())
        f.save()
        c = Cataleg(frases="potatoes")
        c.save()
        c.fonts.add(f)
        c.save()

        response = self.client.get(reverse('filtre:analitza font', args=(f.id,)), follow=True)

        f.refresh_from_db()

        self.assertIsNotNone(Avis.objects.all()[0].data)

    def test_avis_amb_data_apareix_al_detall_avis(self):
        size = len(Avis.objects.all())
        f = Font(nom="Test", url=self.live_server_url+reverse('filtre:test', args=("potatoes\r\n<br\>potatoes\r\n<br\>cabbages\r\n<br\>soup potato",)), horari=timezone.now())
        f.save()
        c = Cataleg(frases="potatoes")
        c.save()
        c.fonts.add(f)
        c.save()

        response = self.client.get(reverse('filtre:analitza font', args=(f.id,)), follow=True)
        response = self.client.get(reverse('filtre:detall avis', args=(Avis.objects.all()[0].id,)), follow=True)

        self.assertContains(response, "Data:")

    def test_avis_amb_data_apareix_al_detall_font(self):
        size = len(Avis.objects.all())
        f = Font(nom="Test", url=self.live_server_url+reverse('filtre:test', args=("potatoes\r\n<br\>potatoes\r\n<br\>cabbages\r\n<br\>soup potato",)), horari=timezone.now())
        f.save()
        c = Cataleg(frases="potatoes")
        c.save()
        c.fonts.add(f)
        c.save()

        response = self.client.get(reverse('filtre:analitza font', args=(f.id,)), follow=True)
        response = self.client.get(reverse('filtre:detall font', args=(f.id,)), follow=True)

        self.assertContains(response, "Avu&iacute;")

    def test_avisos_generen_font_i_num_avisos_al_index(self):
        size = len(Avis.objects.all())
        f = Font(nom="Test", url=self.live_server_url+reverse('filtre:test', args=("potatoes\r\n<br\>potatoes\r\n<br\>cabbages\r\n<br\>soup potato",)), horari=timezone.now())
        f.save()
        c = Cataleg(frases="potatoes")
        c.save()
        c.fonts.add(f)
        c.save()

        response = self.client.get(reverse('filtre:analitza font', args=(f.id,)), follow=True)
        response = self.client.get(reverse('filtre:index'), follow=True)

        self.assertContains(response, '<b>Test</b> (2)')

    def test_avisos_soluciona_caracters_extranys(self):
        pass
