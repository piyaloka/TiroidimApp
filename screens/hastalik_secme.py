from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.properties import StringProperty
from database import Database

KV_DISEASE = """
<HastalikSecmeEkrani>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 1, 0.95, 0.95, 1  # Açık pembe arka plan
        padding: "20dp"
        spacing: "10dp"

        # ÜST İLERLEME ÇİZGİLERİ
        MDBoxLayout:
            size_hint_y: None
            height: "10dp"
            spacing: "5dp"
            MDBoxLayout:
                md_bg_color: 1, 0.6, 0.6, 0.3
            MDBoxLayout:
                md_bg_color: 1, 0.6, 0.6, 0.3
            MDBoxLayout:
                md_bg_color: 1, 0.6, 0.6, 1

        # ANA KART
        MDCard:
            orientation: "vertical"
            md_bg_color: 1, 1, 1, 1
            radius: [30,]
            padding: "20dp"
            spacing: "10dp"
            elevation: 2
            size_hint_y: 0.92
            pos_hint: {"center_x": 0.5}

            # --- [BOŞLUK 1] Aşağı İtici ---
            Widget:
                size_hint_y: 1  # Esnek boşluk

            # PROFİL VE BAŞLIK
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                spacing: "10dp"
                pos_hint: {"center_x": 0.5}

                # Profil İkonu
                MDRelativeLayout:
                    size_hint: None, None
                    size: "80dp", "80dp"
                    pos_hint: {"center_x": .5}
                    canvas.before:
                        Color:
                            rgba: 1, 0.9, 0.9, 1
                        Ellipse:
                            pos: self.pos
                            size: self.size
                    MDIcon:
                        icon: "account"
                        halign: "center"
                        font_size: "45sp"
                        theme_text_color: "Custom"
                        text_color: 1, 0.6, 0.6, 1
                        pos_hint: {"center_x": .5, "center_y": .5}

                # Başlık
                MDLabel:
                    text: "Hangi tiroid hastalığına\\nsahipsiniz?"
                    halign: "center"
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 0.4, 0.2, 0.2, 1
                    adaptive_height: True

            # SEÇENEKLER (Listeyi de biraz ayıralım)
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                spacing: "15dp"
                padding: [0, "20dp", 0, "20dp"]

                MDFillRoundFlatButton:
                    text: "Hipertiroidi"
                    font_size: "16sp"
                    size_hint_x: 1
                    height: "55dp"
                    radius: [15,]
                    md_bg_color: (1, 0.92, 0.92, 1) if root.secilen_kod != "Hipertiroidi" else (1, 0.7, 0.7, 1)
                    text_color: (0.4, 0.2, 0.2, 1) if root.secilen_kod != "Hipertiroidi" else (1, 1, 1, 1)
                    on_release: root.hastalik_sec("Hipertiroidi")

                MDFillRoundFlatButton:
                    text: "Hashimoto"
                    font_size: "16sp"
                    size_hint_x: 1
                    height: "55dp"
                    radius: [15,]
                    md_bg_color: (1, 0.92, 0.92, 1) if root.secilen_kod != "Hashimoto" else (1, 0.7, 0.7, 1)
                    text_color: (0.4, 0.2, 0.2, 1) if root.secilen_kod != "Hashimoto" else (1, 1, 1, 1)
                    on_release: root.hastalik_sec("Hashimoto")

                MDFillRoundFlatButton:
                    text: "Emin Değilim"
                    font_size: "16sp"
                    size_hint_x: 1
                    height: "55dp"
                    radius: [15,]
                    md_bg_color: (1, 0.92, 0.92, 1) if root.secilen_kod != "Belirsiz" else (1, 0.7, 0.7, 1)
                    text_color: (0.4, 0.2, 0.2, 1) if root.secilen_kod != "Belirsiz" else (1, 1, 1, 1)
                    on_release: root.hastalik_sec("Belirsiz")

            # --- [BOŞLUK 2] Yukarı İtici ---
            Widget:
                size_hint_y: 1 # Esnek boşluk

            # BUTON
            MDFillRoundFlatButton:
                text: "KAYDI TAMAMLA"
                font_size: "18sp"
                md_bg_color: 1, 0.6, 0.6, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.9
                pos_hint: {"center_x": 0.5}
                radius: [25,]
                height: "50dp"
                on_release: root.kaydi_bitir()
"""

Builder.load_string(KV_DISEASE)

class HastalikSecmeEkrani(MDScreen):
    secilen_kod = StringProperty("Belirsiz")

    def hastalik_sec(self, isim):
        self.secilen_kod = isim

    def kaydi_bitir(self):
        try:
            db = Database()
            conn = db.baglanti_ac()
            cursor = conn.cursor()
            cursor.execute("UPDATE kullanici SET tiroid_tipi = ? WHERE id = (SELECT MAX(id) FROM kullanici)", (self.secilen_kod,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Hastalık kayıt hatası: {e}")

        self.manager.current = "dashboard"