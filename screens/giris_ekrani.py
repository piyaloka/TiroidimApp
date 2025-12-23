# ÖRNEK KODDUR SİLİP KENDİ KODUNU YAZABİLİRSİN

from kivymd.uix.screen import MDScreen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class GirisEkrani(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Şimdilik boş kalmasın diye ekrana basit bir yazı koyuyoruz
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Giriş Ekranı (Henüz Yapılmadı)", color=(0,0,0,1)))
        self.add_widget(layout)