from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from profil_ekrani import user_profile

class DiseaseScreen(Screen):
    # Seçilen hastalığı ekranda dinamik olarak göstermek için
    selected_name = StringProperty("Henüz seçim yapılmadı")

    def select_disease(self, disease_name):
        """Hastalığı kaydeder ve kullanıcıya görsel geri bildirim verir."""
        user_profile["hastalik"] = disease_name
        self.selected_name = f"Seçilen: {disease_name}"

    def finish_onboarding(self):
        """Profil özet ekranına geçiş yapar."""
        self.manager.current = "profile_edit"

KV_DISEASE = """
<DiseaseScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 1, 0.88, 0.88, 1  # Görseldeki o yumuşak pembe arka plan
        padding: "20dp"
        spacing: "15dp"

        # Üst İlerleme Çubuğu (Görseldeki gibi ince ve soft)
        MDBoxLayout:
            size_hint_y: None
            height: "4dp"
            spacing: "10dp"
            padding: ["40dp", "10dp", "40dp", 0]
            MDBoxLayout:
                md_bg_color: 1, 0.7, 0.7, 0.5
            MDBoxLayout:
                md_bg_color: 1, 0.7, 0.7, 0.5
            MDBoxLayout:
                md_bg_color: 1, 0.6, 0.6, 1 # Koyu Pembe Aktif

        Widget:
            size_hint_y: 0.1

        # Ana Beyaz Kart (Yumuşatılmış köşeler)
        MDCard:
            orientation: "vertical"
            md_bg_color: 1, 1, 1, 1
            radius: [40,]
            padding: "30dp"
            spacing: "20dp"
            elevation: 0
            size_hint_y: 0.75
            pos_hint: {"center_x": 0.5}

            # Profil Fotoğraf Alanı (Daire içinde kamera ikonu)
            MDBoxLayout:
                size_hint: None, None
                size: "120dp", "120dp"
                pos_hint: {"center_x": 0.5}
                md_bg_color: 1, 0.9, 0.9, 1
                radius: [60,]
                MDIcon:
                    icon: "camera"
                    halign: "center"
                    font_size: "40sp"
                    theme_text_color: "Custom"
                    text_color: 0, 0, 0, 1

            MDLabel:
                text: "Hangi tiroid hastalığına\\nsahipsiniz?"
                halign: "center"
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: 0.1, 0.1, 0.1, 1

            # Seçilen Hastalık Yazısı (Kırmızı Vurgu)
            MDLabel:
                text: root.selected_name
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.8, 0.2, 0.2, 1
                bold: True

            # Hastalık Seçenekleri (Sade ve Çizgili)
            MDBoxLayout:
                orientation: "vertical"
                spacing: "2dp"
                adaptive_height: True
                
                MDFlatButton:
                    text: "Hipertiroidi"
                    size_hint_x: 1
                    font_size: "18sp"
                    on_release: root.select_disease("Hipertiroidi")
                
                MDSeparator:
                    height: "1dp"
                    color: 0.9, 0.9, 0.9, 1
                
                MDFlatButton:
                    text: "Hashimoto"
                    size_hint_x: 1
                    font_size: "18sp"
                    on_release: root.select_disease("Hashimoto")

        Widget:
            size_hint_y: 0.1

        # KAYDI TAMAMLA Butonu (Görseldeki pembe buton)
        MDFillRoundFlatButton:
            text: "KAYDI TAMAMLA"
            font_size: "18sp"
            md_bg_color: 1, 0.7, 0.7, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            on_release: root.finish_onboarding()

        Widget:
            size_hint_y: 0.05
"""
Builder.load_string(KV_DISEASE)
