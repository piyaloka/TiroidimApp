from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.clock import Clock

# KV Tasarımı (Görünüm)
KV_WELCOME = """
<GirisEkrani>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 1, 1, 1, 1
        
        Image:
            source: "assets/tiroid_logo.png"
            size_hint: None, None
            size: "250dp", "250dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            allow_stretch: True

<HosgeldinEkrani>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 1, 1, 1, 1
        padding: "20dp"
        spacing: "20dp"

        # Renkli Çizgiler
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
            # Dashboard'a gönderiyoruz
            on_release: 
                root.manager.current = "onboarding" 
                root.manager.transition.direction = "left"

        Widget:
            size_hint_y: 0.1
"""

Builder.load_string(KV_WELCOME)

# Python Sınıfları (Mantık)
class GirisEkrani(MDScreen):
    def on_enter(self, *args):
        # 3 saniye sonra Hoşgeldin ekranına geç
        Clock.schedule_once(self.git_hosgeldin, 3)
    
    def git_hosgeldin(self, dt):
        self.manager.current = "hosgeldin"

class HosgeldinEkrani(MDScreen):
    pass