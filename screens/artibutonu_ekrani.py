import sys
import os
#kodunuzda hata çıkmaması için eklendi
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from kivymd.uix.screen import MDScreen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from database import Database 
from datetime import datetime

class ArtiButonuEkrani(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Veritabanı bağlantısı
        self.db = Database() 
        
        # Dikey bir düzen oluştur
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # --- "Aldım" Butonu ---
        self.btn_aldim = Button(
            text="Aldım",
            size_hint=(None, None),
            size=(200, 60),
            pos_hint={'center_x': 0.5},
            background_normal='' 
        )
        self.btn_aldim.bind(on_release=self.aldim_islemi) 
        
        # --- "Atladım" Butonu ---
        self.btn_atladim = Button(
            text="Atladım",
            size_hint=(None, None),
            size=(200, 60),
            pos_hint={'center_x': 0.5},
            background_color=(0.7, 0.7, 0.7, 1) # Gri renk
        )
        self.btn_atladim.bind(on_release=self.atladim_islemi)

        # Butonları düzene ekle
        layout.add_widget(self.btn_aldim)
        layout.add_widget(self.btn_atladim)
        
        # Düzeni ekrana ekle
        self.add_widget(layout)

    def aldim_islemi(self, instance):
        # 1. Butonu Mor Yap
        instance.background_color = (0.5, 0, 0.5, 1) 
        
        # 2. Veritabanına "ALINDI" bilgisini işle
        bugun = datetime.now().strftime('%Y-%m-%d')
        # Not: Buradaki '1' ilaç ID'sidir. İleride bunu dinamik yapacağız.
        self.db.ilac_logla(1, bugun, "ALINDI") 
        print(f"{bugun} tarihi için ilaç alındı olarak kaydedildi.")

    def atladim_islemi(self, instance):
        # Atladım kaydı yap
        bugun = datetime.now().strftime('%Y-%m-%d')
        self.db.ilac_logla(1, bugun, "ATLADI")
        print("İlaç atlandı.")