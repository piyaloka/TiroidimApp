# ÖRNEK KODDUR SİLİP KENDİ KODUNU YAZABİLİRSİN
# 

from kivymd.uix.screen import MDScreen
from kivy.uix.label import Label

class TakvimEkrani(MDScreen):  # <--- Main.py bu ismi arıyor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Takvim Ekranı (Yapım Aşamasında)"))