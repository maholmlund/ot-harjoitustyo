import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    # itse tehdyt testit
    def test_kortin_alkusaldo_on_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)
    
    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(200)

        self.assertEqual(self.maksukortti.saldo_euroina(), 12.0)
    
    def test_raha_vahenee_jos_sita_on_tarpeeksi(self):
        self.assertTrue(self.maksukortti.ota_rahaa(200))
        self.assertEqual(self.maksukortti.saldo_euroina(), 8.0)
    
    def test_raha_ei_vahene_jos_otetaan_liikaa(self):
        self.assertTrue(not self.maksukortti.ota_rahaa(1200))
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)