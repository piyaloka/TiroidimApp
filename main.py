from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
import os

# --- 1. EKRANLARI İÇE AKTARMA (Mürettebatı Çağır) ---
from screens.giris_ekrani import GirisEkrani, HosgeldinEkrani
from screens.onboarding_ekrani import OnboardingEkrani
from screens.hastalik_secme import HastalikSecmeEkrani
from screens.dashboard_ekrani import DashboardEkrani
from screens.takvim_ekrani import TakvimEkrani
from screens.grafik_ekrani import GrafikEkrani
from screens.artibutonu_ekrani import ArtiButonuEkrani
from screens.duzenleme_ekrani import DuzenlemeEkrani
from screens.ayarlar_ekrani import AyarlarEkrani  # <-- YENİ EKLENDİ

# Telefon boyutu simülasyonu
Window.size = (360, 640)

class TiroidimApp(MDApp):
    def build(self):
        # --- TEMA AYARLARI ---
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Green"
        self.theme_cls.material_style = "M3" # Modern Tasarım
        self.title = "Tiroidim"

        # --- YÖNETİCİ (ScreenManager) ---
        yonetici = ScreenManager()

        # --- EKRANLARI YÖNETİCİYE EKLE ---
        # Not: 'name' parametresi, geçiş yaparken kullandığımız kimliktir.
        
        yonetici.add_widget(GirisEkrani(name="giris"))
        yonetici.add_widget(HosgeldinEkrani(name="hosgeldin"))
        yonetici.add_widget(OnboardingEkrani(name="onboarding"))
        yonetici.add_widget(HastalikSecmeEkrani(name="hastalik_secme"))
        yonetici.add_widget(DashboardEkrani(name="dashboard"))
        yonetici.add_widget(TakvimEkrani(name="takvim"))
        yonetici.add_widget(GrafikEkrani(name="grafik"))
        yonetici.add_widget(ArtiButonuEkrani(name="arti_butonu"))
        yonetici.add_widget(DuzenlemeEkrani(name="duzenleme"))
        yonetici.add_widget(AyarlarEkrani(name="ayarlar")) # <-- YENİ EKLENDİ

        # --- BAŞLANGIÇ EKRANI ---
        yonetici.current = "giris"
        
        return yonetici

if __name__ == "__main__":
    TiroidimApp().run()