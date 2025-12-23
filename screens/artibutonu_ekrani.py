# ÖRNEK KODDUR SİLİP KENDİ KODUNU YAZABİLİRSİN
from kivymd.uix.screen import MDScreen
from kivy.uix.label import Label

class ArtiButonuEkrani(MDScreen): # <--- İsmi değiştirdik
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Ekleme Ekranı (Yapım Aşamasında)"))