from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from database import Database

KV_ONBOARDING = """
<OnboardingEkrani>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 1, 1, 1, 1
        padding: "20dp"
        spacing: "10dp"

        # ÜST İLERLEME ÇİZGİLERİ
        
        MDBoxLayout:
            size_hint_y: None
            height: "10dp"
            spacing: "5dp"
            # 1. Çizgi 
            MDBoxLayout:
                md_bg_color: 0.67, 0.85, 0.28, 0.3
            # 2. Çizgi 
            MDBoxLayout:
                md_bg_color: 0.67, 0.85, 0.28, 1
            # 3. Çizgi
            MDBoxLayout:
                md_bg_color: 0.67, 0.85, 0.28, 0.3

        MDLabel:
            text: "Seni tanıyalım!"
            font_style: "H5"
            bold: True
            size_hint_y: None
            height: "50dp"
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 1

        # FOTOĞRAF VE İSİM ALAN
        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: "120dp"
            spacing: "15dp"

            MDRelativeLayout:
                size_hint: None, None
                size: "100dp", "100dp"
                canvas.before:
                    Color:
                        rgba: 0.88, 0.94, 0.75, 1
                    Ellipse:
                        pos: self.pos
                        size: self.size
                MDIconButton:
                    icon: "camera"
                    pos_hint: {"center_x": .5, "center_y": .6}
                MDLabel:
                    text: "Fotoğraf"
                    font_style: "Caption"
                    halign: "center"
                    pos_hint: {"center_x": .5, "center_y": .3}

            MDBoxLayout:
                orientation: "vertical"
                spacing: "10dp"
                pos_hint: {"center_y": 0.5}
                MDTextField:
                    id: isim
                    hint_text: "İsim"
                    mode: "round"
                    fill_color_normal: 0.88, 0.94, 0.75, 0.5
                MDTextField:
                    id: soyisim
                    hint_text: "Soyisim"
                    mode: "round"
                    fill_color_normal: 0.88, 0.94, 0.75, 0.5

        # DİĞER 
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
             
                spacing: "15dp"  
                adaptive_height: True
                
                padding: [0, "10dp", 0, "20dp"] 

                MDTextField:
                    id: dogum
                    hint_text: "Doğum Tarihi (Gün.Ay.Yıl)"
                    icon_left: "cake-variant"
                    mode: "round"
                    fill_color_normal: 0.88, 0.94, 0.75, 0.5
                    size_hint_y: None
                    height: "50dp" 

                MDTextField:
                    id: cinsiyet
                    hint_text: "Cinsiyet"
                    icon_left: "gender-male-female"
                    mode: "round"
                    fill_color_normal: 0.88, 0.94, 0.75, 0.5
                    size_hint_y: None
                    height: "50dp"

               

                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: "15dp"
                    size_hint_y: None  
                    height: "50dp" # Buranın yüksekliğini de diğerleri gibi yaptım
                    
                    MDTextField:
                        id: boy
                        hint_text: "Boy (cm)"
                        mode: "round"
                        fill_color_normal: 0.88, 0.94, 0.75, 0.5
                    MDTextField:
                        id: kilo
                        hint_text: "Kilo (kg)"
                        mode: "round"
                        fill_color_normal: 0.88, 0.94, 0.75, 0.5

        # Butonu en alta sabitledik
        MDFillRoundFlatButton:
            text: "İlerle"
            md_bg_color: 0.67, 0.85, 0.28, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            on_release: root.kaydet_ve_ilerle()
"""

Builder.load_string(KV_ONBOARDING)

class OnboardingEkrani(MDScreen):
    def kaydet_ve_ilerle(self):
        isim = self.ids.isim.text
        soyisim = self.ids.soyisim.text
        yas_text = self.ids.dogum.text
        boy_text = self.ids.boy.text
        kilo_text = self.ids.kilo.text
        
        try:
            db = Database()
            conn = db.baglanti_ac()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM kullanici")
            
            boy = int(boy_text) if boy_text.isdigit() else 0
            kilo = int(kilo_text) if kilo_text.isdigit() else 0
            
            cursor.execute("""
                INSERT INTO kullanici (ad_soyad, yas, boy, kilo, tiroid_tipi) 
                VALUES (?, ?, ?, ?, ?)
            """, (f"{isim} {soyisim}", 25, boy, kilo, "Belirsiz"))
            
            conn.commit()
            conn.close()
            print("Kullanıcı kaydedildi.")
        except Exception as e:
            print(f"Kayıt hatası: {e}")

        self.manager.current = "hastalik_secme"