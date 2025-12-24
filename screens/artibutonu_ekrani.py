""" 
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
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from database import Database

class ArtiButonuEkrani(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.md_bg_color = (1, 1, 1, 1)

        layout = MDBoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20,
            pos_hint={"top": 1}
        )

        layout.add_widget(MDLabel(text="Yeni İlaç Ekle", halign="center", font_style="H5", size_hint_y=None, height=50))

        self.drug_name = MDTextField(hint_text="İlaç Adı", mode="rectangle")
        self.dosage = MDTextField(hint_text="Dozaj (ör: 500 mg)", mode="rectangle")
        self.frequency = MDTextField(hint_text="Kullanım Sıklığı", mode="rectangle")

        save_button = MDRaisedButton(
            text="KAYDET",
            md_bg_color=(0.42, 0, 0.95, 1),
            pos_hint={"center_x": 0.5},
            on_release=self.ilac_kaydet
        )

        layout.add_widget(self.drug_name)
        layout.add_widget(self.dosage)
        layout.add_widget(self.frequency)
        layout.add_widget(save_button)
        layout.add_widget(MDLabel()) # Boşluk

        self.add_widget(layout)

    def ilac_kaydet(self, instance):
        # Şimdilik sadece Dashboard'a dönelim
        print(f"Kaydediliyor: {self.drug_name.text}")
        self.manager.current = "dashboard"