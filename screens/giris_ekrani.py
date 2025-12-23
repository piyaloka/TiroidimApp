from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.uix.button import MDFillRoundFlatButton

KV_WELCOME = """
<giris_ekrani1>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 1, 1, 1, 1
        Image:
            source: "tiroid_logo.png"
            size_hint: None, None
            size: "250dp", "250dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}

<giris_ekrani2>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 1, 1, 1, 1
        padding: "20dp"
        spacing: "20dp"

        # Üstteki ilerleme çizgileri
        MDBoxLayout:
            size_hint_y: None
            height: "4dp"
            spacing: "10dp"
            padding: ["20dp", "20dp", "20dp", 0]
            MDBoxLayout:
                md_bg_color: 0.42, 0, 0.95, 1
            MDBoxLayout:
                md_bg_color: 0.8, 0.7, 0.9, 1
            MDBoxLayout:
                md_bg_color: 0.8, 0.7, 0.9, 1

        Widget:
            size_hint_y: 0.1

        Image:
            source: "tiroid_logo.png"
            size_hint: None, None
            size: "100dp", "100dp"
            pos_hint: {"center_x": 0.5}

        Widget:
            size_hint_y: 0.1

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
            on_release: root.manager.current = "onboarding"

        Widget:
            size_hint_y: 0.1
"""

class giris_ekrani1(Screen):
    def on_enter(self, *args):
        # 3 saniye sonra WelcomeScreen'e (yazılı ekran) geç
        Clock.schedule_once(self.go_to_welcome, 3)
    
    def go_to_welcome(self, dt):
        self.manager.current = "welcome_text"

class giris_ekrani2(Screen):
    pass

# Tasarımı tek seferde yüklüyoruz
Builder.load_string(KV_WELCOME)
