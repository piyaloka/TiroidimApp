import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivy.lang import Builder
from kivy.metrics import dp
from database import Database

KV = '''
<AyarlarEkrani>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.98, 0.98, 0.98, 1  # Hafif gri arka plan

        MDTopAppBar:
            title: "Ayarlar & Düzenleme"
            elevation: 0
            pos_hint: {"top": 1}
            left_action_items: [["arrow-left", lambda x: root.dashboard_git()]]
            md_bg_color: 1, 1, 1, 1
            specific_text_color: 0, 0, 0, 1

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                padding: "20dp"
                spacing: "20dp"

                # BİLDİRİM TERCİHLERİ KARTI
                MDCard:
                    orientation: "vertical"
                    size_hint_y: None
                    height: "120dp"
                    padding: "16dp"
                    radius: [20, 20, 20, 20]
                    elevation: 1
                    shadow_softness: 2

                    MDLabel:
                        text: "Bildirim Tercihleri"
                        theme_text_color: "Custom"
                        text_color: self.theme_cls.primary_color
                        bold: True
                        font_style: "Subtitle1"

                    MDBoxLayout:
                        orientation: "horizontal"
                        MDLabel:
                            text: "İlaç hatırlatıcılarını aç"
                            theme_text_color: "Secondary"
                        MDSwitch:
                            id: bildirim_switch
                            active: True
                            on_active: root.bildirim_guncelle(self.active)

                # İLAÇ SAATİ GÜNCELLEME KARTI
                MDCard:
                    orientation: "vertical"
                    size_hint_y: None
                    height: "240dp"
                    padding: "16dp"
                    spacing: "12dp"
                    radius: [20, 20, 20, 20]
                    elevation: 1

                    MDLabel:
                        text: "İlaç Saati Güncelle"
                        theme_text_color: "Custom"
                        text_color: self.theme_cls.primary_color
                        bold: True
                        font_style: "Subtitle1"

                    MDTextField:
                        id: ilac_secimi
                        hint_text: "Düzenlenecek ilacı seçin"
                        readonly: True
                        on_focus: if self.focus: root.menu_ac()
                        mode: "outline"

                    MDTextField:
                        id: yeni_saat
                        hint_text: "Yeni Saat (Örn: 08:30)"
                        mode: "outline"
                        helper_text: "24 saat formatında giriniz"
                        helper_text_mode: "on_error"

                    MDRaisedButton:
                        text: "Saati Güncelle"
                        size_hint_x: 1
                        md_bg_color: self.theme_cls.primary_color
                        on_release: root.ilac_saati_kaydet()

                # PROFİL VE HAKKINDA (EKSTRA)
                MDCard:
                    orientation: "vertical"
                    size_hint_y: None
                    height: "130dp"
                    padding: "16dp"
                    radius: [20, 20, 20, 20]
                    elevation: 1
                    
                    MDLabel:
                        text: "Diğer"
                        theme_text_color: "Custom"
                        text_color: self.theme_cls.primary_color
                        bold: True
                        font_style: "Subtitle1"
                    
                    OneLineIconListItem:
                        text: "Profilimi Düzenle"
                        on_release: root.manager.current = "duzenleme"
                        IconLeftWidget:
                            icon: "account-edit"
                    
                    OneLineIconListItem:
                        text: "Hakkında"
                        on_release: root.hakkinda_mesaji()
                        IconLeftWidget:
                            icon: "information"
'''

class AyarlarEkrani(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.db = Database()
        Builder.load_string(KV)
        self.menu = None
        self.secili_ilac_id = None

    def on_enter(self):
        """Ekran açıldığında verileri tazeler."""
        # Bildirim ayarını yükle
        ayarlar = self.db.ayarlari_getir()
        self.ids.bildirim_switch.active = bool(ayarlar["bildirim_acik"])
        self.menu_olustur()

    def menu_olustur(self):
        """İlaç listesini dropdown menüye yükler."""
        ilaclar = self.db.kullanici_ilaclarini_getir() #
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i[1]} ({i[2]})",
                "on_release": lambda x=i: self.menu_secim_yap(x),
            } for i in ilaclar
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.ilac_secimi,
            items=menu_items,
            width_mult=4,
        )

    def menu_ac(self):
        if self.menu:
            self.menu.open()

    def menu_secim_yap(self, ilac_verisi):
        self.secili_ilac_id = ilac_verisi[0]
        self.ids.ilac_secimi.text = ilac_verisi[1]
        self.ids.yeni_saat.text = ilac_verisi[3]
        self.menu.dismiss()

    def bildirim_guncelle(self, durum):
        # sqlite3 için 1 veya 0 olarak kaydet
        self.db.ayar_guncelle("bildirim_acik", 1 if durum else 0)

    def ilac_saati_kaydet(self):
        if not self.secili_ilac_id or not self.ids.yeni_saat.text:
            return

        # Veritabanında güncelleme (Yeni bir fonksiyon eklemelisin veya mevcut olanı kullanmalısın)
        conn = self.db.baglanti_ac()
        cursor = conn.cursor()
        cursor.execute("UPDATE kullanici_ilaclari SET saat = ? WHERE id = ?", 
                       (self.ids.yeni_saat.text, self.secili_ilac_id))
        conn.commit()
        conn.close()
        
        # Temizlik ve geri bildirim
        self.ids.ilac_secimi.text = ""
        self.ids.yeni_saat.text = ""
        self.secili_ilac_id = None
        print("İlaç saati güncellendi.")

    def hakkinda_mesaji(self):
        MDDialog(
            title="Hakkında",
            text="Tiroidim v1.0\nSağlıklı günler dileriz.",
            buttons=[MDFlatButton(text="Kapat")]
        ).open()

    def dashboard_git(self):
        self.manager.current = "dashboard"
