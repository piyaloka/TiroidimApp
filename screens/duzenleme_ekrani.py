from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from profil_ekrani import user_profile

class duzenleme_ekrani(Screen):
    def on_enter(self):
        # Onboarding ekranında girilen verileri kart üzerine yansıtıyoruz
        self.ids.full_name.text = f"{user_profile['isim']} {user_profile['soyisim']}"
        self.ids.user_mail.text = user_profile['mail']
        self.ids.user_stats.text = f"Boy: {user_profile['boy']} cm   |   Kilo: {user_profile['kilo']} kg"
        self.ids.user_birthday.text = f"Doğum Tarihi: {user_profile['dogum_tarihi']}"

KV_PROFILE = """
<duzenleme_ekrani>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 1, 1, 1, 1 # Temiz beyaz arka plan
        padding: "20dp"
        spacing: "15dp"

        MDLabel:
            text: "Profil Bilgilerim"
            halign: "center"
            font_style: "H5"
            bold: True
            size_hint_y: None
            height: "60dp"
            theme_text_color: "Custom"
            text_color: 0.2, 0.2, 0.2, 1

        # Modern Profil Kartı (Yeşil Temalı)
        MDCard:
            orientation: "vertical"
            size_hint: 0.95, None
            height: "260dp"
            padding: "20dp"
            spacing: "10dp"
            pos_hint: {"center_x": 0.5}
            radius: [25,]
            md_bg_color: 0.88, 0.94, 0.75, 0.6  # Görseldeki açık yeşil (şeffaflık eklendi)
            elevation: 1

            # Profil Resmi Alanı (Küçük Daire)
            MDBoxLayout:
                size_hint: None, None
                size: "70dp", "70dp"
                pos_hint: {"center_x": 0.5}
                md_bg_color: 1, 1, 1, 0.8
                radius: [35,]
                MDIcon:
                    icon: "account"
                    halign: "center"
                    font_size: "40sp"
                    theme_text_color: "Custom"
                    text_color: 0.67, 0.85, 0.28, 1

            MDLabel:
                id: full_name
                text: "İsim Soyisim"
                halign: "center"
                font_style: "H6"
                bold: True
            
            MDLabel:
                id: user_mail
                text: "E-posta Adresi"
                halign: "center"
                theme_text_color: "Secondary"
                font_style: "Body1"

            MDSeparator:
                height: "1dp"
                color: 0.67, 0.85, 0.28, 0.3

            MDLabel:
                id: user_birthday
                text: "Doğum Tarihi"
                halign: "center"
                font_style: "Caption"

            MDLabel:
                id: user_stats
                text: "Boy: - | Kilo: -"
                halign: "center"
                bold: True
                theme_text_color: "Custom"
                text_color: 0.4, 0.6, 0.2, 1

        Widget:
            size_hint_y: 1 # Esnek boşluk

        # İşlem Butonları
        MDBoxLayout:
            orientation: "vertical"
            spacing: "10dp"
            size_hint_y: None
            height: "120dp"

            MDFillRoundFlatButton:
                text: "Bilgileri Güncelle"
                size_hint_x: 0.8
                pos_hint: {"center_x": 0.5}
                md_bg_color: 0.67, 0.85, 0.28, 1 # Canlı Yeşil
                on_release: root.manager.current = "onboarding"

            MDFlatButton:
                text: "Çıkış Yap"
                pos_hint: {"center_x": 0.5}
                theme_text_color: "Custom"
                text_color: 0.6, 0.1, 0.1, 1
                on_release: app.stop()

        Widget:
            size_hint_y: 0.05
"""

Builder.load_string(KV_PROFILE)
