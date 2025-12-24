from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
import os

Builder.load_file("assets/dashboard.kv")  
#Builder.load_file("assets/giris.kv")      
Builder.load_file("assets/takvim.kv")     
Builder.load_file("assets/grafik.kv")    

from screens.giris_ekrani import GirisEkrani, HosgeldinEkrani
from screens.dashboard_ekrani import DashboardEkrani
from screens.takvim_ekrani import TakvimEkrani
from screens.grafik_ekrani import GrafikEkrani
from screens.artibutonu_ekrani import ArtiButonuEkrani
from screens.duzenleme_ekrani import DuzenlemeEkrani


# Telefon boyutu
Window.size = (360, 640)

class TiroidimApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Green"
        self.title = "Tiroidim"

        # Yöneticiyi (ScreenManager) oluşturuyoruz
        yonetici = ScreenManager()

        # Ekranları yöneticiye ekliyoruz
        # (GirisEkrani vb.) kullanıyoruz
        yonetici.add_widget(GirisEkrani(name="giris"))
        yonetici.add_widget(HosgeldinEkrani(name="hosgeldin"))
        yonetici.add_widget(DashboardEkrani(name="dashboard"))
        yonetici.add_widget(TakvimEkrani(name="takvim"))
        yonetici.add_widget(GrafikEkrani(name="grafik"))
        yonetici.add_widget(ArtiButonuEkrani(name="arti_butonu"))
        yonetici.add_widget(DuzenlemeEkrani(name="duzenleme"))

        # İlk açılacak ekran
        yonetici.current = "giris"
        
        return yonetici

if __name__ == "__main__":
    TiroidimApp().run()
