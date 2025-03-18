import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.paate = Kassapaate()

    def test_alustus_antaa_oikeat_arvot(self):
        self.assertEqual(self.paate.kassassa_rahaa, 100000)
        self.assertEqual(self.paate.maukkaat, 0)
        self.assertEqual(self.paate.edulliset, 0)

    def test_kateisosto_maukkailla_oikein_toimii(self):
        self.assertEqual(self.paate.syo_maukkaasti_kateisella(500), 100)
        self.assertEqual(self.paate.maukkaat, 1)
        self.assertEqual(self.paate.kassassa_rahaa, 100400)

    def test_kateisosto_maukkailla_liian_vahan_rahaa_ei_osta(self):
        self.assertEqual(self.paate.syo_maukkaasti_kateisella(300), 300)
        self.assertEqual(self.paate.maukkaat, 0)
        self.assertEqual(self.paate.kassassa_rahaa, 100000)

    def test_korttiosto_maukkailla_oikein_toimii(self):
        kortti = Maksukortti(100000)
        self.assertEqual(self.paate.syo_maukkaasti_kortilla(kortti), True)
        self.assertEqual(self.paate.maukkaat, 1)
        self.assertEqual(self.paate.kassassa_rahaa, 100000)

    def test_korttiosto_maukkailla_liian_vahan_rahaa_ei_osta(self):
        kortti = Maksukortti(100)
        self.assertEqual(self.paate.syo_maukkaasti_kortilla(kortti), False)
        self.assertEqual(self.paate.maukkaat, 0)
        self.assertEqual(self.paate.kassassa_rahaa, 100000)

    def test_kateisosto_edullisilla_oikein_toimii(self):
        self.assertEqual(self.paate.syo_edullisesti_kateisella(500), 260)
        self.assertEqual(self.paate.edulliset, 1)
        self.assertEqual(self.paate.kassassa_rahaa, 100240)

    def test_kateisosto_edullisilla_liian_vahan_rahaa_ei_osta(self):
        self.assertEqual(self.paate.syo_edullisesti_kateisella(200), 200)
        self.assertEqual(self.paate.edulliset, 0)
        self.assertEqual(self.paate.kassassa_rahaa, 100000)

    def test_korttiosto_edullisilla_oikein_toimii(self):
        kortti = Maksukortti(100000)
        self.assertEqual(self.paate.syo_edullisesti_kortilla(kortti), True)
        self.assertEqual(self.paate.edulliset, 1)
        self.assertEqual(self.paate.kassassa_rahaa, 100000)

    def test_korttiosto_edullisilla_liian_vahan_rahaa_ei_osta(self):
        kortti = Maksukortti(100)
        self.assertEqual(self.paate.syo_edullisesti_kortilla(kortti), False)
        self.assertEqual(self.paate.edulliset, 0)
        self.assertEqual(self.paate.kassassa_rahaa, 100000)

    def test_rahan_lataaminen_kortille_positiivinen_toimii(self):
        kortti = Maksukortti(100)
        self.paate.lataa_rahaa_kortille(kortti, 200)
        self.assertEqual(kortti.saldo_euroina(), 3.0)
        self.assertEqual(self.paate.kassassa_rahaa, 100200)

    def test_rahan_lataaminen_kortille_negatiivinen_ei_toimi(self):
        kortti = Maksukortti(100)
        self.paate.lataa_rahaa_kortille(kortti, -200)
        self.assertEqual(kortti.saldo_euroina(), 1.0)
        self.assertEqual(self.paate.kassassa_rahaa, 100000)

    def test_kassassa_rahaa_euroina(self):
        self.assertEqual(self.paate.kassassa_rahaa_euroina(), 1000.0)