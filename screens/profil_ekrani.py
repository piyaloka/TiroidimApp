from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

# Ortak veri yapısı
user_profile = {
    "isim": "",
    "soyisim": "",
    "dogum_tarihi": "",
    "cinsiyet": "",
    "mail": "",
    "boy": "",
    "kilo": "",
    "foto_yolu": "default_avatar.png" # Varsayılan resim
}

KV_ONBOARDING = """
<OnboardingScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 1, 1, 1, 1
        padding: "20dp"
        spacing: "15dp"

        # Üst İlerleme Çizgileri
        MDBoxLayout:
            size_hint_y: None
            height: "4dp"
            spacing: "10dp"
            padding: ["10dp", "20dp", "10dp", 0]
            MDBoxLayout:
                md_bg_color: 0.67, 0.85, 0.28, 1
            MDBoxLayout:
                md_bg_color: 0.67, 0.85, 0.28, 1
            MDBoxLayout:
                md_bg_color: 0.9, 0.9, 0.9, 1

        Widget:
            size_hint_y: 0.05

        MDLabel:
            text: "Seni tanıyalım!"
            font_style: "H5"
            bold: True
            halign: "left"
            padding_x: "20dp"
            size_hint_y: None
            height: "40dp"

        # Profil Fotoğrafı ve İsim/Soyisim Alanı
        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: "120dp"
            spacing: "15dp"
            padding: ["10dp", 0, "10dp", 0]

            # Tıklanabilir Fotoğraf Ekleme Alanı
            MDRelativeLayout:
                size_hint: None, None
                size: "100dp", "100dp"
                
                # Yeşil Yuvarlak Arka Plan
                canvas.before:
                    Color:
                        rgba: 0.88, 0.94, 0.75, 1
                    Ellipse:
                        pos: self.pos
                        size: self.size
                
                MDBoxLayout:
                    orientation: "vertical"
                    adaptive_size: True
                    pos_hint: {"center_x": .5, "center_y": .5}
                    
                    MDIconButton:
                        icon: "camera"
                        pos_hint: {"center_x": .5}
                        on_release: root.foto_sec()
                    
                    MDLabel:
                        text: "Fotoğraf ekle"
                        font_style: "Caption"
                        halign: "center"
                        adaptive_height: True

            # İsim ve Soyisim
            MDBoxLayout:
                orientation: "vertical"
                spacing: "10dp"
                MDTextField:
                    id: isim
                    hint_text: "İsim"
                    mode: "round"
                    fill_color_normal: 0.88, 0.94, 0.75, 1
                MDTextField:
                    id: soyisim
                    hint_text: "Soyisim"
                    mode: "round"
                    fill_color_normal: 0.88, 0.94, 0.75, 1

        # Diğer Bilgiler
        MDBoxLayout:
            orientation: "vertical"
            spacing: "12dp"
            padding: ["10dp", 0, "10dp", 0]

            MDTextField:
                id: dogum
                hint_text: "Doğum Tarihi"
                icon_left: "cake-variant"
                mode: "round"
                fill_color_normal: 0.88, 0.94, 0.75, 1

            MDTextField:
                id: cinsiyet
                hint_text: "Cinsiyet"
                icon_left: "gender-male-female"
                mode: "round"
                fill_color_normal: 0.88, 0.94, 0.75, 1

            MDTextField:
                id: mail
                hint_text: "E-posta Adresi"
                icon_left: "email-outline"
                mode: "round"
                fill_color_normal: 0.88, 0.94, 0.75, 1

            MDBoxLayout:
                orientation: "horizontal"
                spacing: "15dp"
                MDTextField:
                    id: boy
                    hint_text: "Boy"
                    mode: "round"
                    fill_color_normal: 0.88, 0.94, 0.75, 1
                MDTextField:
                    id: kilo
                    hint_text: "Kilo"
                    mode: "round"
                    fill_color_normal: 0.88, 0.94, 0.75, 1

        Widget:
            size_hint_y: 0.1

        MDFillRoundFlatButton:
            text: "İlerle"
            md_bg_color: 0.67, 0.85, 0.28, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            on_release: root.save_and_next()

        Widget:
            size_hint_y: 0.05
"""

class OnboardingScreen(Screen):
    def __init__(self, **kwargs):
        Builder.load_string(KV_ONBOARDING)
        super().__init__(**kwargs)

    def foto_sec(self):
        print("Fotoğraf seçme galerisi açılıyor...")
        

    def save_and_next(self):
        user_profile["isim"] = self.ids.isim.text
        user_profile["soyisim"] = self.ids.soyisim.text
        user_profile["dogum_tarihi"] = self.ids.dogum.text
        user_profile["cinsiyet"] = self.ids.cinsiyet.text
        user_profile["mail"] = self.ids.mail.text
        user_profile["boy"] = self.ids.boy.text
        user_profile["kilo"] = self.ids.kilo.text
        self.manager.current = "disease_select"
