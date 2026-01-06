from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.properties import StringProperty
from database import Database
from datetime import datetime

KV_ONBOARDING = """
<OnboardingEkrani>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0.94, 0.98, 0.90, 1  # Arka plan: Çok açık yeşil
        padding: "20dp"
        spacing: "10dp"

        # ÜST İLERLEME ÇİZGİLERİ
        MDBoxLayout:
            size_hint_y: None
            height: "10dp"
            spacing: "5dp"
            MDBoxLayout:
                md_bg_color: 0.67, 0.85, 0.28, 0.3
            MDBoxLayout:
                md_bg_color: 0.67, 0.85, 0.28, 1
            MDBoxLayout:
                md_bg_color: 0.67, 0.85, 0.28, 0.3

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

            # --- [BOŞLUK 1] ---
            Widget:
                size_hint_y: 0.5

            MDLabel:
                text: "Seni tanıyalım!"
                font_style: "H5"
                bold: True
                halign: "center"
                size_hint_y: None
                height: "80dp"
                theme_text_color: "Custom"
                text_color: 0.2, 0.3, 0.1, 1

            # FOTOĞRAF VE İSİM ALAN
            MDBoxLayout:
                orientation: "horizontal"
                size_hint_y: None
                height: "90dp"
                spacing: "15dp"

                MDRelativeLayout:
                    size_hint: None, None
                    size: "80dp", "80dp"
                    pos_hint: {"center_y": .5}
                    canvas.before:
                        Color:
                            rgba: 0.88, 0.94, 0.75, 1
                        Ellipse:
                            pos: self.pos
                            size: self.size
                    MDIconButton:
                        icon: "camera"
                        theme_text_color: "Custom"
                        text_color: 0.4, 0.5, 0.2, 1
                        pos_hint: {"center_x": .5, "center_y": .6}
                    MDLabel:
                        text: "Fotoğraf"
                        font_style: "Caption"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 0.4, 0.5, 0.2, 1
                        pos_hint: {"center_x": .5, "center_y": .3}

                MDBoxLayout:
                    orientation: "vertical"
                    spacing: "8dp"
                    pos_hint: {"center_y": 0.5}
                    MDTextField:
                        id: isim
                        hint_text: "İsim"
                        mode: "fill"
                        fill_color_normal: 0.96, 0.98, 0.92, 1
                        line_color_focus: 0.67, 0.85, 0.28, 1
                        radius: [15, 15, 15, 15]
                        on_text: root.filter_text(self)
                        
                    MDTextField:
                        id: soyisim
                        hint_text: "Soyisim"
                        mode: "fill"
                        fill_color_normal: 0.96, 0.98, 0.92, 1
                        line_color_focus: 0.67, 0.85, 0.28, 1
                        radius: [15, 15, 15, 15]
                        on_text: root.filter_text(self)

            # DİĞER BİLGİLER
            MDBoxLayout:
                orientation: "vertical"
                spacing: "12dp"  
                adaptive_height: True
                padding: [0, "5dp", 0, "5dp"] 

                # DOĞUM TARİHİ ALANI (GÜNCELLENDİ)
                MDTextField:
                    id: dogum
                    hint_text: "Doğum Tarihi (GG/AA/YYYY)"
                    icon_left: "calendar"
                    mode: "fill"
                    fill_color_normal: 0.96, 0.98, 0.92, 1
                    line_color_focus: 0.67, 0.85, 0.28, 1
                    radius: [15, 15, 15, 15]
                    # Readonly ve on_focus kaldırıldı, manuel girişe açıldı.
                    base_direction: "ltr"  # İmleç kaymasını önlemek için eklendi
                    multiline: False
                    max_text_length: 10

                # Cinsiyet Butonları
                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: "10dp"
                    size_hint_y: None
                    height: "40dp"
                    
                    MDFillRoundFlatButton:
                        text: "Kadın"
                        font_size: "12sp"
                        size_hint_x: 1
                        md_bg_color: (0.67, 0.85, 0.28, 1) if root.secilen_cinsiyet == "Kadın" else (0.96, 0.98, 0.92, 1)
                        text_color: (1, 1, 1, 1) if root.secilen_cinsiyet == "Kadın" else (0.4, 0.5, 0.2, 1)
                        on_release: root.cinsiyet_sec("Kadın")
                    
                    MDFillRoundFlatButton:
                        text: "Erkek"
                        font_size: "12sp"
                        size_hint_x: 1
                        md_bg_color: (0.67, 0.85, 0.28, 1) if root.secilen_cinsiyet == "Erkek" else (0.96, 0.98, 0.92, 1)
                        text_color: (1, 1, 1, 1) if root.secilen_cinsiyet == "Erkek" else (0.4, 0.5, 0.2, 1)
                        on_release: root.cinsiyet_sec("Erkek")

                    MDFillRoundFlatButton:
                        text: "Diğer"
                        font_size: "12sp"
                        size_hint_x: 0.8
                        md_bg_color: (0.67, 0.85, 0.28, 1) if root.secilen_cinsiyet == "Diğer" else (0.96, 0.98, 0.92, 1)
                        text_color: (1, 1, 1, 1) if root.secilen_cinsiyet == "Diğer" else (0.4, 0.5, 0.2, 1)
                        on_release: root.cinsiyet_sec("Diğer")

                # Boy - Kilo
                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: "15dp"
                    size_hint_y: None  
                    height: "55dp"
                    
                    MDTextField:
                        id: boy
                        hint_text: "Boy (cm)"
                        mode: "fill"
                        input_filter: "int"
                        fill_color_normal: 0.96, 0.98, 0.92, 1
                        line_color_focus: 0.67, 0.85, 0.28, 1
                        radius: [15, 15, 15, 15]
                    MDTextField:
                        id: kilo
                        hint_text: "Kilo (kg)"
                        mode: "fill"
                        input_filter: "int"
                        fill_color_normal: 0.96, 0.98, 0.92, 1
                        line_color_focus: 0.67, 0.85, 0.28, 1
                        radius: [15, 15, 15, 15]

            # --- [BOŞLUK 2] ---
            Widget:
                size_hint_y: 0.5

            # Buton (En altta sabit)
            MDFillRoundFlatButton:
                text: "İLERLE"
                font_size: "18sp"
                md_bg_color: 0.67, 0.85, 0.28, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.9
                pos_hint: {"center_x": 0.5}
                radius: [25,]
                height: "50dp"
                on_release: root.kaydet_ve_ilerle()
"""

Builder.load_string(KV_ONBOARDING)

class OnboardingEkrani(MDScreen):
    secilen_cinsiyet = StringProperty("")

    def cinsiyet_sec(self, cinsiyet):
        self.secilen_cinsiyet = cinsiyet

    def filter_text(self, instance):
        if not instance.text.isalpha() and instance.text != "":
            filtered = ''.join([c for c in instance.text if c.isalpha() or c.isspace()])
            if instance.text != filtered:
                instance.text = filtered
                instance.cursor = (len(instance.text), 0)

    # DatePicker ile ilgili open/close/save fonksiyonları SİLİNDİ.

    def kaydet_ve_ilerle(self):
        isim = self.ids.isim.text
        soyisim = self.ids.soyisim.text
        boy_text = self.ids.boy.text
        kilo_text = self.ids.kilo.text
        dogum_tarihi = self.ids.dogum.text # Artık tarihi buradan text olarak alıyoruz
        
        # Basit validasyon: İsim yoksa geçirme (opsiyonel)
        # if not isim: return 

        try:
            db = Database()
            conn = db.baglanti_ac()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM kullanici")
            boy = int(boy_text) if boy_text and boy_text.isdigit() else 0
            kilo = int(kilo_text) if kilo_text and kilo_text.isdigit() else 0
            
            # NOT: Yaş hesaplaması için tarihi parse etmemiz gerekebilir.
            # Şimdilik eski kodundaki gibi hardcoded 25 bıraktım, 
            # ancak istersen doğum tarihinden yaş hesaplayan bir kod ekleyebilirim.
            yas = 25 
            
            cursor.execute("""
                INSERT INTO kullanici (ad_soyad, yas, boy, kilo, tiroid_tipi) 
                VALUES (?, ?, ?, ?, ?)
            """, (f"{isim} {soyisim}", yas, boy, kilo, "Belirsiz"))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Kayıt hatası: {e}")

        self.manager.current = "hastalik_secme"