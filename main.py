# --- EN TEPEYE BU KODLARI EKLE (Kivy importlarından ÖNCE) ---
import os
from kivy.config import Config

# Pencere boyutunu ve yeniden boyutlandırılmasını buradan sabitliyoruz
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '750')
Config.set('graphics', 'resizable', '0') # Boyutlandırmayı kapatalım ki sabit kalsın
Config.write()

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.metrics import Metrics
from database import Database

# Ekranlar
from screens.giris_ekrani import GirisEkrani, HosgeldinEkrani
from screens.onboarding_ekrani import OnboardingEkrani
from screens.hastalik_secme import HastalikSecmeEkrani
from screens.dashboard_ekrani import DashboardEkrani
from screens.takvim_ekrani import TakvimEkrani
from screens.grafik_ekrani import GrafikEkrani
from screens.artibutonu_ekrani import ArtiButonuEkrani, AlarmEkrani, TahlilEkrani
from screens.duzenleme_ekrani import DuzenlemeEkrani
from screens.ayarlar_ekrani import AyarlarEkrani

class TiroidimApp(MDApp):
    def build(self):
        # Bu ayar widgetların devasa olmasını engeller
        Metrics.density = 1.0 
        
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Green"
        self.theme_cls.material_style = "M3"
        self.title = "Tiroidim"

        # Veritabanı
        db = Database()

        # Yönetici
        yonetici = ScreenManager()

        # Ekran Ekleme
        yonetici.add_widget(GirisEkrani(name="giris"))
        yonetici.add_widget(HosgeldinEkrani(name="hosgeldin"))
        yonetici.add_widget(OnboardingEkrani(name="onboarding"))
        yonetici.add_widget(HastalikSecmeEkrani(name="hastalik_secme"))
        yonetici.add_widget(DashboardEkrani(name="dashboard"))
        yonetici.add_widget(TakvimEkrani(name="takvim"))
        yonetici.add_widget(GrafikEkrani(name="grafik"))
        
        yonetici.add_widget(ArtiButonuEkrani(name="arti_butonu"))
        yonetici.add_widget(AlarmEkrani(name="alarm_ekle"))
        yonetici.add_widget(TahlilEkrani(name="tahlil_ekle"))

        yonetici.add_widget(DuzenlemeEkrani(name="duzenleme"))
        yonetici.add_widget(AyarlarEkrani(name="ayarlar"))

        yonetici.current = "giris" 
        
        return yonetici

if __name__ == "__main__":
    TiroidimApp().run()