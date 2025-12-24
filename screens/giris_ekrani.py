from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout

# --- GİRİŞ VE HOŞGELDİN EKRANI TASARIMI ---
KV_WELCOME = """
<GirisEkrani>:
    md_bg_color: 1, 1, 1, 1 
    
    AnchorLayout:
        anchor_x: "center"
        anchor_y: "center"

        # Logo ve Yazıyı tutan kutu
        MDBoxLayout:
            orientation: "vertical"
            # adaptive_size: True  <-- BUNU SİLDİK (Sorun buydu)
            adaptive_height: True  # Sadece yüksekliği otomatik yap
            size_hint_x: None      # Genişliği biz belirleyeceğiz
            width: "300dp"         # Yazının rahat sığacağı genişlik
            spacing: "10dp"        # Logo ve yazı arası boşluk
            pos_hint: {"center_x": 0.5, "center_y": 0.55}

            # --- LOGO RESMİ ---
            Image:
                source: "assets/logo_mor.png"
                size_hint: None, None
                size: "75dp", "75dp"   # Senin istediğin küçük boyut
                pos_hint: {"center_x": 0.5}
                allow_stretch: True

            # --- BAŞLIK YAZISI ---
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
        md_bg_color: 1, 1, 1, 1
        padding: "20dp"
        spacing: "20dp"

        MDBoxLayout:
            size_hint_y: None
            height: "10dp"
            spacing: "5dp"
            MDBoxLayout:
                md_bg_color: 0.42, 0, 0.95, 1
                size_hint_x: 0.3
            MDBoxLayout:
                md_bg_color: 0.9, 0.9, 0.9, 1
            MDBoxLayout:
                md_bg_color: 0.9, 0.9, 0.9, 1

        Widget:
            size_hint_y: 0.2

        MDLabel:
            text: "Merhaba,\\nHoş Geldin!"
            halign: "center"
            font_style: "H4"
            bold: True
            theme_text_color: "Custom"
            text_color: 0.42, 0, 0.95, 1

        Widget:
            size_hint_y: 0.2

        MDFillRoundFlatButton:
            text: "İlerle"
            font_size: "20sp"
            md_bg_color: 0.42, 0, 0.95, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}
            on_release: 
                root.manager.current = "onboarding" 
                root.manager.transition.direction = "left"

        Widget:
            size_hint_y: 0.1
"""

Builder.load_string(KV_WELCOME)

class GirisEkrani(MDScreen):
    def on_enter(self, *args):
        Clock.schedule_once(self.git_hosgeldin, 3)
    
    def git_hosgeldin(self, dt):
        self.manager.current = "hosgeldin"

class HosgeldinEkrani(MDScreen):
    pass