import sys
import os
#kodunuzda hata çıkmaması için eklendi
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp # Tema değişimi için gerekli
from kivymd.toast import toast # Kullanıcıya uyarı vermek için
from database import Database

# --- TASARIM (KV) ---
KV_AYARLAR = """
<AyarlarEkrani>:
    md_bg_color: self.theme_cls.bg_normal # Tema ile uyumlu arka plan

    MDBoxLayout:
        orientation: "vertical"
        
        # --- ÜST BAR ---
        MDBoxLayout:
            size_hint_y: None
            height: "70dp"
            padding: "10dp"
            spacing: "10dp"
            md_bg_color: self.theme_cls.primary_color # Dinamik tema rengi
            elevation: 2
            
            MDIconButton:
                icon: "arrow-left"
                theme_icon_color: "Custom"
                icon_color: 1, 1, 1, 1
                on_release: 
                    root.manager.current = "dashboard"
                    root.manager.transition.direction = "right"
                pos_hint: {"center_y": 0.5}

            MDLabel:
                text: "Ayarlar & Düzenleme"
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                pos_hint: {"center_y": 0.5}

        # --- İÇERİK ---
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                padding: "20dp"
                spacing: "20dp"

                # 1. BİLDİRİM VE TEMA AYARLARI KARTI
                MDCard:
                    orientation: "vertical"
                    size_hint_y: None
                    adaptive_height: True
                    radius: [20,]
                    padding: "15dp"
                    spacing: "10dp"
                    elevation: 1
                    
                    MDLabel:
                        text: "Uygulama Tercihleri"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Primary"

                    MDSeparator:

                    # Bildirim Switch (Hizalanmış)
                    MDBoxLayout:
                        size_hint_y: None
                        height: "40dp"
                        MDLabel:
                            text: "İlaç hatırlatıcılarını aç"
                            halign: "left"
                        MDSwitch:
                            id: switch_bildirim
                            active: True
                            on_active: root.bildirim_ayarini_degistir(*args)
                    
                    # Tema Switch (Yeni Eklendi)
                    MDBoxLayout:
                        size_hint_y: None
                        height: "40dp"
                        MDLabel:
                            text: "Karanlık Mod"
                            halign: "left"
                        MDSwitch:
                            id: switch_tema
                            active: False
                            on_active: root.tema_degistir(*args)

                # 2. İLAÇ SAATİ DÜZENLEME KARTI
                MDCard:
                    orientation: "vertical"
                    size_hint_y: None
                    adaptive_height: True
                    radius: [20,]
                    padding: "20dp"
                    spacing: "15dp"
                    elevation: 1

                    MDLabel:
                        text: "İlaç Saati Güncelle"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Primary"

                    MDTextField:
                        id: secilen_ilac_kutusu
                        hint_text: "Düzenlenecek ilacı seçin"
                        mode: "rectangle"
                        icon_right: "chevron-down"
                        readonly: True
                        on_focus: if self.focus: root.menu_ac()

                    MDTextField:
                        id: yeni_saat_input
                        hint_text: "Yeni Saat (Seçim yapmadan aktif olmaz)"
                        mode: "rectangle"
                        disabled: True # Başlangıçta kapalı
                        input_filter: "float"
                    
                    MDFillRoundFlatButton:
                        text: "Saati Güncelle"
                        size_hint_x: 1
                        on_release: root.saat_guncelle()

                Widget:
                    size_hint_y: None
                    height: "50dp"
"""

Builder.load_string(KV_AYARLAR)

class AyarlarEkrani(MDScreen):
    menu = None
    secili_ilac_id = None

    def on_enter(self):
        self.verileri_yukle()
        self.bildirim_durumunu_getir()
        # Tema switch durumunu mevcut temaya göre ayarla
        self.ids.switch_tema.active = (MDApp.get_running_app().theme_cls.theme_style == "Dark")

    def verileri_yukle(self):
        try:
            db = Database()
            ilaclar = db.kullanici_ilaclarini_getir()
            menu_items = []
            for ilac in ilaclar:
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
        except Exception as e:
            print(f"Veri yükleme hatası: {e}")

    def menu_ac(self):
        self.ids.secilen_ilac_kutusu.focus = False
        if self.menu:
            self.menu.open()

    def ilac_secildi(self, ilac_tuple):
        self.secili_ilac_id = ilac_tuple[0]
        self.ids.secilen_ilac_kutusu.text = f"{ilac_tuple[1]} - {ilac_tuple[2]}"
        self.ids.yeni_saat_input.text = ilac_tuple[3]
        self.ids.yeni_saat_input.disabled = False # İlaç seçilince saati aktif et
        self.menu.dismiss()

    def saat_guncelle(self):
        # Önce ilaç seçilmiş mi kontrol et
        if not self.secili_ilac_id:
            toast("Lütfen önce bir ilaç seçin!")
            return

        yeni_saat = self.ids.yeni_saat_input.text
        if yeni_saat:
            db = Database()
            conn = db.baglanti_ac()
            conn.execute("UPDATE kullanici_ilaclari SET saat = ? WHERE id = ?", (yeni_saat, self.secili_ilac_id))
            conn.commit()
            conn.close()
            
            toast(f"Saat {yeni_saat} olarak güncellendi.")
            
            # Temizlik
            self.ids.secilen_ilac_kutusu.text = ""
            self.ids.yeni_saat_input.text = ""
            self.ids.yeni_saat_input.disabled = True # Tekrar kilitle
            self.secili_ilac_id = None
            self.verileri_yukle()

    def bildirim_durumunu_getir(self):
        db = Database()
        ayarlar = db.ayarlari_getir()
        if ayarlar:
            self.ids.switch_bildirim.active = bool(ayarlar.get("bildirim_acik", 1))

    def bildirim_ayarini_degistir(self, instance, value):
        durum = 1 if value else 0
        db = Database()
        db.ayar_guncelle("bildirim_acik", durum)

    def tema_degistir(self, instance, value):
        app = MDApp.get_running_app()
        if value:
            app.theme_cls.theme_style = "Dark"
        else:
            app.theme_cls.theme_style = "Light"
