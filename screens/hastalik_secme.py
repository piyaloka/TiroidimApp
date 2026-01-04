from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.properties import StringProperty
from database import Database

#tasarım
KV_DISEASE = """
<HastalikSecmeEkrani>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 1, 0.95, 0.95, 1
        padding: "20dp"
        spacing: "10dp"

        # Üst İlerleme Çizgileri
        MDBoxLayout:
            size_hint_y: None
            height: "10dp"
            spacing: "5dp"
            MDBoxLayout:
                md_bg_color: 1, 0.7, 0.7, 0.5
            MDBoxLayout:
                md_bg_color: 1, 0.7, 0.7, 0.5
            MDBoxLayout:
                md_bg_color: 1, 0.6, 0.6, 1

        MDCard:
            orientation: "vertical"
            md_bg_color: 1, 1, 1, 1
            radius: [30,]
            padding: "30dp"
            spacing: "20dp"
            elevation: 1
            size_hint_y: 0.85
            pos_hint: {"center_x": 0.5}

            # İkon
            MDBoxLayout:
                size_hint: None, None
                size: "100dp", "100dp"
                pos_hint: {"center_x": 0.5}
                md_bg_color: 1, 0.9, 0.9, 1
                radius: [50,]
                MDIcon:
                    icon: "medical-bag"
                    halign: "center"
                    font_size: "50sp"
                    theme_text_color: "Custom"
                    text_color: 0.8, 0.4, 0.4, 1

            MDLabel:
                text: "Hangi tiroid hastalığına\\nsahipsiniz?"
                halign: "center"
                font_style: "H6"
                bold: True
                size_hint_y: None
                height: "60dp"

            # Seçilen Hastalık Göstergesi
            MDLabel:
                text: root.selected_name
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.8, 0.2, 0.2, 1
                bold: True
                size_hint_y: None
                height: "20dp"

            # Seçenekler
            ScrollView:
                MDBoxLayout:
                    orientation: "vertical"
                    adaptive_height: True
                    spacing: "10dp"
                    
                    MDRectangleFlatButton:
                        text: "Hipertiroidi"
                        size_hint_x: 1
                        on_release: root.hastalik_sec("Hipertiroidi")
                    
                    MDRectangleFlatButton:
                        text: "Hashimoto"
                        size_hint_x: 1
                        on_release: root.hastalik_sec("Hashimoto")

                    MDRectangleFlatButton:
                        text: "Emin Değilim"
                        size_hint_x: 1
                        on_release: root.hastalik_sec("Belirsiz")

            MDFillRoundFlatButton:
                text: "KAYDI TAMAMLA"
                font_size: "20sp"
                md_bg_color: 1, 0.7, 0.7, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.9
                on_release: root.kaydi_bitir()
"""

Builder.load_string(KV_DISEASE)

# DÜZELTİLMİŞ SINIF İSMİ: HastalikSecmeEkrani 

class HastalikSecmeEkrani(MDScreen):
    selected_name = StringProperty("Henüz seçim yapılmadı")
    secilen_kod = "Belirsiz"

    def hastalik_sec(self, isim):
        self.selected_name = f"Seçilen: {isim}"
        self.secilen_kod = isim

    def kaydi_bitir(self):
        # Veritabanına güncelleme
        try:
            db = Database()
            conn = db.baglanti_ac()
            cursor = conn.cursor()
            cursor.execute("UPDATE kullanici SET tiroid_tipi = ? WHERE id = (SELECT MAX(id) FROM kullanici)", (self.secilen_kod,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Hastalık kayıt hatası: {e}")

        # Dashboard'a geç
        self.manager.current = "dashboard"