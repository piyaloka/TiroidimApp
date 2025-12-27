""" 
 
******** DUZENLEME YAPILDI *******


from kivymd.uix.screen import MDScreen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from database import Database  # database.py dosyasını içe aktar
from datetime import datetime

class ArtiButonuEkrani(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database() # Veritabanı sınıfını başlat
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Görevin: "Aldım" Butonu
        self.btn_aldim = Button(
            text="Aldım",
            size_hint=(None, None),
            size=(200, 60),
            pos_hint={'center_x': 0.5},
            background_normal='' # Renk değişimi için gerekli
        )
        self.btn_aldim.bind(on_release=self.aldim_islemi) # on_release olayı
        
        # Görevin: "Atladım" Butonu
        self.btn_atladim = Button(
            text="Atladım",
            size_hint=(None, None),
            size=(200, 60),
            pos_hint={'center_x': 0.5},
            background_color=(0.7, 0.7, 0.7, 1) # Gri
        )
        self.btn_atladim.bind(on_release=self.atladim_islemi)

        layout.add_widget(self.btn_aldim)
        layout.add_widget(self.btn_atladim)
        self.add_widget(layout)

    def aldim_islemi(self, instance):
        # 1. Butonu Mor Yap
        instance.background_color = (0.5, 0, 0.5, 1) 
        
        # 2. Veritabanına "ALINDI" bilgisini işle
        bugun = datetime.now().strftime('%Y-%m-%d')
        # Örnek ilac_id: 1 (Normalde seçilen ilaçtan gelir)
        self.db.ilac_logla(1, bugun, "ALINDI") 
        print(f"{bugun} tarihi için ilaç alındı olarak kaydedildi.")

    def atladim_islemi(self, instance):
        # Atladım kaydı yap
        bugun = datetime.now().strftime('%Y-%m-%d')
        self.db.ilac_logla(1, bugun, "ATLADI")
        print("İlaç atlandı.")

"""
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.animation import Animation

MDFloatingActionButton:
        id: main_fab
        icon: "plus"
        md_bg_color: 0.4, 0.1, 0.9, 1
        pos_hint: {"center_x": .85, "center_y": .1}
        on_release: app.toggle_menu()

    # --- DİNAMİK FORM SAYFASI ---
    MDCard:
        id: form_page
        pos_hint: {"center_x": 0.5, "center_y": -1} # Ekranın çok dışında başlar
        size_hint: 0.95, 0.8
        radius: [30, 30, 30, 30]
        elevation: 12
        padding: "20dp"
        orientation: 'vertical'
