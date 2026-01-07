from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder
from database import Database

KV = """
<AyarlarEkrani>:
    name: "ayarlar"
    md_bg_color: 1, 1, 1, 1

    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "15dp"

        MDLabel:
            text: "Ayarlar & Düzenleme"
            halign: "center"
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: 0.5, 0.2, 0.8, 1

        MDCard:
            padding: "16dp"
            size_hint_y: None
            height: "80dp"
            radius: [15,]
            elevation: 1

            MDBoxLayout:
                orientation: "horizontal"
                spacing: "10dp"

                MDLabel:
                    text: "İlaç hatırlatıcılarını aç"
                    halign: "left"

                MDSwitch:
                    id: bildirim_switch
                    on_active: root.bildirim_kaydet(self.active)

        MDCard:
            orientation: "vertical"
            padding: "20dp"
            spacing: "10dp"
            size_hint_y: None
            height: "250dp"
            radius: [15,]
            elevation: 1

            MDTextField:
                id: ilac_secimi
                hint_text: "Düzenlenecek ilacı seçin"
                readonly: True
                on_focus: if self.focus: root.menu_ac()

            MDTextField:
                id: yeni_saat
                hint_text: "Yeni Saat (Örn: 08:30)"

            MDRaisedButton:
                text: "Saati Güncelle"
                md_bg_color: 0.5, 0.2, 0.8, 1
                on_release: root.saat_guncelle()

        Widget:
            size_hint_y: 1

        MDFlatButton:
            text: "Geri Dön"
            pos_hint: {"center_x": 0.5}
            on_release: app.root.current = "dashboard"
"""

Builder.load_string(KV)

class AyarlarEkrani(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.menu = None
        self.secili_id = None

    def on_enter(self):
        ayar = self.db.ayarlari_getir()
        if ayar:
            self.ids.bildirim_switch.active = bool(ayar["bildirim_acik"])

        ilaclar = self.db.kullanici_ilaclarini_getir()
        items = [{
            "viewclass": "OneLineListItem",
            "text": i[1],
            "on_release": lambda x=i: self.ilac_sec(x),
        } for i in ilaclar]

        self.menu = MDDropdownMenu(caller=self.ids.ilac_secimi, items=items, width_mult=4)

    def menu_ac(self):
        if self.menu:
            self.menu.open()

    def ilac_sec(self, ilac):
        self.secili_id = ilac[0]
        self.ids.ilac_secimi.text = ilac[1]
        self.ids.yeni_saat.text = ilac[3]
        self.menu.dismiss()

    def bildirim_kaydet(self, aktif):
        self.db.ayar_guncelle("bildirim_acik", 1 if aktif else 0)

    def saat_guncelle(self):
        if self.secili_id:
            self.db.ilac_saati_guncelle(self.secili_id, self.ids.yeni_saat.text)
            self.ids.ilac_secimi.text = "Güncellendi!"
