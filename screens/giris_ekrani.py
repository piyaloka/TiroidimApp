from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout

KV_WELCOME = """
<GirisEkrani>:
    md_bg_color: 1, 1, 1, 1 
    
    AnchorLayout:
        anchor_x: "center"
        anchor_y: "center"

        # Logo ve Yazıyı tutan kutu
        MDBoxLayout:
            orientation: "vertical"
            adaptive_height: True 
            size_hint_x: None 
            width: "300dp" 
            spacing: "10dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.55}

            Image:
                source: "assets/logo_mor.png"
                size_hint: None, None
                size: "75dp", "75dp"
                pos_hint: {"center_x": 0.5}
                allow_stretch: True
            
            MDLabel:
                text: "Tiroidim"
                halign: "center"
                font_style: "H4"
                bold: True
                theme_text_color: "Custom"
                text_color: 0.42, 0, 0.95, 1
                adaptive_height: True

<HosgeldinEkrani>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0.96, 0.93, 1, 1  # Arka Plan: Çok açık mor
        padding: "20dp"
        spacing: "10dp"

        # ÜST İLERLEME ÇİZGİLERİ
        MDBoxLayout:
            size_hint_y: None
            height: "10dp"
            spacing: "5dp"
            # 1.Çizgi (Aktif - Koyu Mor)
            MDBoxLayout:
                md_bg_color: 0.42, 0, 0.95, 1
            # 2.Çizgi (Pasif - Soluk Mor)
            MDBoxLayout:
                md_bg_color: 0.42, 0, 0.95, 0.2
            # 3.Çizgi (Pasif - Soluk Mor)
            MDBoxLayout:
                md_bg_color: 0.42, 0, 0.95, 0.2

        # KART YAPISI
        MDCard:
            orientation: "vertical"
            md_bg_color: 1, 1, 1, 1
            radius: [30,]
            padding: "20dp"
            spacing: "20dp"
            elevation: 2
            size_hint_y: 0.92
            pos_hint: {"center_x": 0.5}

            Widget: # Üst boşluk

            MDLabel:
                text: "Merhaba,\\nHoş Geldin!"
                halign: "center"
                font_style: "H4"
                bold: True
                theme_text_color: "Custom"
                text_color: 0.42, 0, 0.95, 1
            
            Widget: # Alt boşluk

            # BUTON (Kartın içinde, en altta)
            MDFillRoundFlatButton:
                text: "İLERLE"
                font_size: "18sp"
                md_bg_color: 0.42, 0, 0.95, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.9
                pos_hint: {"center_x": 0.5}
                radius: [25,]
                height: "50dp"
                on_release: 
                    root.manager.current = "onboarding" 
                    root.manager.transition.direction = "left"
"""

Builder.load_string(KV_WELCOME)

class GirisEkrani(MDScreen):
    def on_enter(self, *args):
        # 3 saniye sonra otomatik geçiş
        Clock.schedule_once(self.git_hosgeldin, 3)
    
    def git_hosgeldin(self, dt):
        self.manager.current = "hosgeldin"

class HosgeldinEkrani(MDScreen):
    pass