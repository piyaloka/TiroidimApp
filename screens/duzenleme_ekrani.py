from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from database import Database

# TASARIM (KV)
KV_PROFIL_GUNCEL = """
<DuzenlemeEkrani>:
    md_bg_color: 1, 1, 1, 1
    
    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "10dp"

        # ÜST KISIM: Profil Fotoğrafı Alanı
        MDRelativeLayout:
            size_hint_y: None
            height: "160dp"
            
            MDIcon:
                id: profil_ikonu
                icon: "account-circle"
                font_size: "120sp"
                pos_hint: {"center_x": .5, "center_y": .6}
                theme_text_color: "Custom"
                text_color: 0.67, 0.85, 0.28, 1

            MDIconButton:
                icon: "camera"
                pos_hint: {"center_x": .62, "center_y": .35}
                md_bg_color: 0.67, 0.85, 0.28, 1
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                on_release: root.galeri_uyarisi()

        # GİRİŞ ALANLARI
        MDTextField:
            id: full_name
            hint_text: "Ad Soyad"
            mode: "fill"
            icon_left: "account"

        MDBoxLayout:
            spacing: "10dp"
            size_hint_y: None
            height: "80dp"
            MDTextField:
                id: user_age
                hint_text: "Yaş"
                mode: "fill"
            MDTextField:
                id: user_weight
                hint_text: "Kilo"
                mode: "fill"
            MDTextField:
                id: user_height
                hint_text: "Boy"
                mode: "fill"

        # HASTALIK TİPİ SEÇİM ALANI (Kritik Bölge)
        MDRelativeLayout:
            size_hint_y: None
            height: "60dp"
            
            MDTextField:
                id: tiroid_tipi_input
                hint_text: "Tiroid Hastalık Tipi"
                mode: "fill"
                icon_left: "medical-bag"
                readonly: True
                pos_hint: {"center_x": .5, "center_y": .5}

            # TextField'ın üzerine tam oturan şeffaf buton
            MDIconButton:
                icon: ""
                size_hint: 1, 1
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root.hastalik_ekranina_git()

        Widget:
            size_hint_y: 1

        # İŞLEM BUTONLARI
        MDFillRoundFlatButton:
            text: "BİLGİLERİ KAYDET"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.67, 0.85, 0.28, 1
            on_release: root.bilgileri_veritabanina_kaydet()

        MDFlatButton:
            text: "Geri Dön"
            pos_hint: {"center_x": 0.5}
            on_release: app.root.current = "dashboard"
"""

Builder.load_string(KV_PROFIL_GUNCEL)

class DuzenlemeEkrani(MDScreen):
    def galeri_uyarisi(self):
        """Pydroid'de kütüphane çakışmasını önlemek için basit uyarı."""
        print("Galeri şu an devre dışı (Pydroid kısıtlaması).")

    def hastalik_ekranina_git(self):
        """Hastalık seçme ekranına yönlendirir."""
        if self.manager:
            self.manager.current = "hastalik_secme"
        else:
            print("Hata: ScreenManager bulunamadı!")

    def on_enter(self):
        """Ekran her açıldığında verileri tazeler."""
        self.verileri_yukle()

    def verileri_yukle(self):
        try:
            db = Database()
            conn = db.baglanti_ac()
            cursor = conn.cursor()
            # Veritabanından mevcut kullanıcı bilgilerini çek
            cursor.execute("SELECT ad_soyad, yas, boy, kilo, tiroid_tipi FROM kullanici LIMIT 1")
            row = cursor.fetchone()
            conn.close()

            if row:
                self.ids.full_name.text = str(row[0] if row[0] else "")
                self.ids.user_age.text = str(row[1] if row[1] else "")
                self.ids.user_height.text = str(row[2] if row[2] else "")
                self.ids.user_weight.text = str(row[3] if row[3] else "")
                self.ids.tiroid_tipi_input.text = str(row[4] if row[4] else "Seçmek için tıkla")
        except Exception as e:
            print(f"Veri yükleme hatası: {e}")

    def bilgileri_veritabanina_kaydet(self):
        try:
            db = Database()
            conn = db.baglanti_ac()
            cursor = conn.cursor()
            
            # Sadece profil bilgilerini güncelle (Hastalık tipi zaten diğer ekrandan güncelleniyor)
            cursor.execute("""
                UPDATE kullanici SET 
                ad_soyad = ?, yas = ?, boy = ?, kilo = ?
                WHERE id = (SELECT id FROM kullanici LIMIT 1)
            """, (
                self.ids.full_name.text,
                self.ids.user_age.text,
                self.ids.user_height.text,
                self.ids.user_weight.text
            ))
            
            conn.commit()
            conn.close()
            # Başarılı kayıttan sonra ana ekrana dön
            self.manager.current = "dashboard"
        except Exception as e:
            print(f"Kaydetme hatası: {e}")
