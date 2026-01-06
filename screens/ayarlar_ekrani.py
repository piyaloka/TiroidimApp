import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
from database import Database


KV_AYARLAR = """
<AyarlarEkrani>:
    md_bg_color: 1, 1, 1, 1

    MDBoxLayout:
        orientation: "vertical"

        # ÜST BAR
        MDBoxLayout:
            size_hint_y: None
            height: "70dp"
            padding: "10dp"
            spacing: "10dp"
            md_bg_color: app.theme_cls.primary_color

            MDIconButton:
                icon: "arrow-left"
                theme_icon_color: "Custom"
                icon_color: 1, 1, 1, 1
                on_release:
                    root.manager.current = "dashboard"
                    root.manager.transition.direction = "right"

            MDLabel:
                text: "Ayarlar & Düzenleme"
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                padding: "20dp"
                spacing: "20dp"

                # BİLDİRİM TERCIHLERİ
                MDCard:
                    orientation: "vertical"
                    adaptive_height: True
                    radius: [20]
                    padding: "15dp"
                    spacing: "10dp"
                    md_bg_color: 0.97, 0.97, 0.97, 1

                    MDLabel:
                        text: "Bildirim Tercihleri"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.48, 0.34, 0.82, 1

                    MDSeparator:

                    MDBoxLayout:
                        size_hint_y: None
                        height: "40dp"

                        MDLabel:
                            text: "İlaç hatırlatıcılarını aç"

                        MDSwitch:
                            id: switch_bildirim
                            active: True
                            on_active: root.bildirim_toggle(value)

                # İLAÇ SAATİ GÜNCELLE
                MDCard:
                    orientation: "vertical"
                    adaptive_height: True
                    radius: [20]
                    padding: "20dp"
                    spacing: "15dp"
                    md_bg_color: 0.97, 0.97, 0.97, 1

                    MDLabel:
                        text: "İlaç Saati Güncelle"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.48, 0.34, 0.82, 1

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
                        disabled: True

                    MDFillRoundFlatButton:
                        id: btn_saat_guncelle
                        text: "Saati Güncelle"
                        md_bg_color: 0.48, 0.34, 0.82, 1
                        disabled: True
                        pos_hint: {"center_x": 0.45}
                        on_release: root.saat_guncelle()

        AnchorLayout:
            anchor_x: "right"
            anchor_y: "bottom"
            size_hint_y: None
            height: "100dp"
            padding: [0, 0, "30dp", "30dp"]

            MDFillRoundFlatButton:
                text: "KAYDET VE DÖN"
                on_release:
                    root.manager.current = "dashboard"
                    root.manager.transition.direction = "right"
"""

Builder.load_string(KV_AYARLAR)


class AyarlarEkrani(MDScreen):
    menu = None
    secili_ilac_id = None
    bildirimler_acik = True

    def on_enter(self):
        self.verileri_yukle()

    def bildirim_toggle(self, value):
        if value:
            toast("İlaç hatırlatıcıları AÇIK")
            self.bildirimler_acik = True
        else:
            toast("İlaç hatırlatıcıları KAPALI")
            self.bildirimler_acik = False

    def verileri_yukle(self):
        db = Database()
        ilaclar = db.kullanici_ilaclarini_getir()

        if not ilaclar:
            toast("Kayıtlı ilaç bulunamadı")
            return

        menu_items = []
        for ilac in ilaclar:
            menu_items.append({
                "viewclass": "OneLineListItem",
                "text": f"{ilac[1]} ({ilac[2]}) - {ilac[3]}",
                "on_release": lambda x=ilac: self.ilac_secildi(x)
            })

        self.menu = MDDropdownMenu(
            caller=self.ids.secilen_ilac_kutusu,
            items=menu_items,
            width_mult=4
        )

    def menu_ac(self):
        self.ids.secilen_ilac_kutusu.focus = False
        if self.menu:
            self.menu.open()

    def ilac_secildi(self, ilac):
        self.secili_ilac_id = ilac[0]
        self.ids.secilen_ilac_kutusu.text = f"{ilac[1]} - {ilac[2]}"
        self.ids.yeni_saat_input.text = ilac[3]
        self.ids.yeni_saat_input.disabled = False
        self.ids.btn_saat_guncelle.disabled = False
        self.menu.dismiss()

    def saat_guncelle(self):
        if not self.secili_ilac_id:
            toast("Lütfen önce bir ilaç seçin")
            return

        yeni_saat = self.ids.yeni_saat_input.text
        if not yeni_saat:
            toast("Saat boş olamaz")
            return

        db = Database()
        conn = db.baglanti_ac()
        conn.execute(
            "UPDATE kullanici_ilaclari SET saat = ? WHERE id = ?",
            (yeni_saat, self.secili_ilac_id)
        )
        conn.commit()
        conn.close()

        toast("Saat güncellendi")

        self.ids.secilen_ilac_kutusu.text = ""
        self.ids.yeni_saat_input.text = ""
        self.ids.yeni_saat_input.disabled = True
        self.ids.btn_saat_guncelle.disabled = True
        self.secili_ilac_id = None
        self.verileri_yukle()
