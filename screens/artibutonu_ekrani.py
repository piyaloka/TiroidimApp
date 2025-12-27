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

KV = '''
MDScreen:
    md_bg_color: 1, 1, 1, 1

   # --- 1. MİNİ PENCERE (KONUMU YUKARI ALINDI) ---
   MDCard:
        id: mini_menu
        size_hint: None, None
        size: "240dp", "250dp"
        # "+" butonunun tam üstüne gelmemesi için y ekseni artırıldı
        pos_hint: {"center_x": 0.4, "center_y": 0.35} 
        opacity: 0
        disabled: True
        elevation: 10
        radius: [50, 50, 10, 50]
        line_color: 0.5, 0.2, 0.8, 1
        line_width: 1.5

        MDBoxLayout:
            orientation: 'vertical'
            padding: "20dp"
            spacing: "15dp"
            MDFillRoundFlatButton:
                text: "İlaç ekle"
                size_hint_x: 1
                on_release: app.open_form("ilaç")
            MDFillRoundFlatButton:
                text: "Alarm ekle"
                size_hint_x: 1
                on_release: app.open_form("alarm")
            MDFillRoundFlatButton:
                text: "Tahlil ekle"
                size_hint_x: 1
                on_release: app.open_form("tahlil") 

       # ANA ARTI (+) BUTONU
    MDFloatingActionButton:
        id: main_fab
        icon: "plus"
        md_bg_color: 0.4, 0.1, 0.9, 1
        pos_hint: {"center_x": .85, "center_y": .1}
        on_release: app.toggle_menu()   

class MedApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"
        return Builder.load_string(KV)

    def toggle_menu(self):
        menu = self.root.ids.mini_menu
        is_open = menu.opacity > 0
        Animation(opacity=0 if is_open else 1, duration=0.2).start(menu)
        menu.disabled = is_open      

    def open_form(self, mode):
        print(f"{mode} formu açılıyor...")

if __name__ == '__main__':
    MedApp().run() 
