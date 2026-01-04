import sys
import os
#kodunuzda hata çıkmaması için eklendi
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from database import Database

# --- TASARIM (KV) ---
KV_AYARLAR = """
<AyarlarEkrani>:
    md_bg_color: 0.98, 0.98, 0.98, 1

    MDBoxLayout:
        orientation: "vertical"
        
        # --- ÜST BAR ---
        MDBoxLayout:
            size_hint_y: None
            height: "70dp"
            padding: "10dp"
            spacing: "10dp"
            md_bg_color: 1, 1, 1, 1
            elevation: 1
            
            MDIconButton:
                icon: "arrow-left"
                on_release: 
                    root.manager.current = "dashboard"
                    root.manager.transition.direction = "right"
                pos_hint: {"center_y": 0.5}

            MDLabel:
                text: "Ayarlar & Düzenleme"
                font_style: "H6"
                bold: True
                pos_hint: {"center_y": 0.5}

        # --- İÇERİK ---
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                padding: "20dp"
                spacing: "20dp"

                # 1. BİLDİRİM AYARLARI KARTI
                MDCard:
                    orientation: "vertical"
                    size_hint_y: None
                    height: "120dp"
                    radius: [20,]
                    padding: "15dp"
                    md_bg_color: 1, 1, 1, 1
                    elevation: 1
                    
                    MDLabel:
                        text: "Bildirim Tercihleri"
                        font_style: "Subtitle1"
                        bold: True
                        size_hint_y: None
                        height: "30dp"
                        theme_text_color: "Custom"
                        text_color: 0.5, 0.3, 0.9, 1

                    MDSeparator:
                        height: "1dp"

                    MDBoxLayout:
                        spacing: "10dp"
                        MDLabel:
                            text: "İlaç hatırlatıcılarını aç"
                            pos_hint: {"center_y": 0.5}
                        
                        MDSwitch:
                            id: switch_bildirim
                            pos_hint: {"center_y": 0.5}
                            active: True
                            on_active: root.bildirim_ayarini_degistir(*args)

                # 2. İLAÇ SAATİ DÜZENLEME KARTI
                MDCard:
                    orientation: "vertical"
                    size_hint_y: None
                    adaptive_height: True
                    radius: [20,]
                    padding: "20dp"
                    spacing: "15dp"
                    md_bg_color: 1, 1, 1, 1
                    elevation: 1

                    MDLabel:
                        text: "İlaç Saati Güncelle"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.5, 0.3, 0.9, 1
                        size_hint_y: None
                        height: "30dp"

                    # İlaç Seçimi (Dropdown Tetikleyici)
                    MDTextField:
                        id: secilen_ilac_kutusu
                        hint_text: "Düzenlenecek ilacı seçin"
                        mode: "rectangle"
                        icon_right: "chevron-down"
                        readonly: True
                        on_focus: if self.focus: root.menu_ac()

                    MDTextField:
                        id: yeni_saat_input
                        hint_text: "Yeni Saat (Örn: 08:30)"
                        mode: "rectangle"
                        input_filter: "float" # Basit filtre, saat formatı için geliştirilebilir
                    
                    MDFillRoundFlatButton:
                        text: "Saati Güncelle"
                        size_hint_x: 1
                        md_bg_color: 0.5, 0.3, 0.9, 1
                        on_release: root.saat_guncelle()

                Widget: # Boşluk
"""

Builder.load_string(KV_AYARLAR)

class AyarlarEkrani(MDScreen):
    menu = None
    secili_ilac_id = None

    def on_enter(self):
        """Ekran açılınca verileri yükle"""
        self.verileri_yukle()
        self.bildirim_durumunu_getir()

    def verileri_yukle(self):
        # Dropdown menüyü hazırla
        db = Database()
        ilaclar = db.kullanici_ilaclarini_getir()
        
        menu_items = []
        for ilac in ilaclar:
            # ilac yapısı: (id, ad, doz, saat, periyot)
            text = f"{ilac[1]} ({ilac[2]}) - Şu an: {ilac[3]}"
            menu_items.append({
                "viewclass": "OneLineListItem",
                "text": text,
                "on_release": lambda x=ilac: self.ilac_secildi(x),
            })

        self.menu = MDDropdownMenu(
            caller=self.ids.secilen_ilac_kutusu,
            items=menu_items,
            width_mult=4,
        )

    def menu_ac(self):
        self.ids.secilen_ilac_kutusu.focus = False # Klavyeyi kapat
        if self.menu:
            self.menu.open()

    def ilac_secildi(self, ilac_tuple):
        """Dropdown'dan seçim yapılınca"""
        self.secili_ilac_id = ilac_tuple[0]
        self.ids.secilen_ilac_kutusu.text = f"{ilac_tuple[1]} - {ilac_tuple[2]}"
        self.ids.yeni_saat_input.text = ilac_tuple[3] # Mevcut saati yaz
        self.menu.dismiss()

    def saat_guncelle(self):
        yeni_saat = self.ids.yeni_saat_input.text
        if self.secili_ilac_id and yeni_saat:
            db = Database()
            conn = db.baglanti_ac()
            conn.execute("UPDATE kullanici_ilaclari SET saat = ? WHERE id = ?", (yeni_saat, self.secili_ilac_id))
            conn.commit()
            conn.close()
            print(f"İlaç {self.secili_ilac_id} saati {yeni_saat} olarak güncellendi.")
            
            # Geri bildirim ve temizlik
            self.ids.secilen_ilac_kutusu.text = ""
            self.ids.yeni_saat_input.text = ""
            self.verileri_yukle() # Listeyi güncelle

    def bildirim_durumunu_getir(self):
        db = Database()
        ayarlar = db.ayarlari_getir()
        if ayarlar:
            # 1 ise True, 0 ise False
            self.ids.switch_bildirim.active = bool(ayarlar["bildirim_acik"])

    def bildirim_ayarini_degistir(self, instance, value):
        durum = 1 if value else 0
        db = Database()
        db.ayar_guncelle("bildirim_acik", durum)
        print(f"Bildirim ayarı değiştirildi: {durum}")