from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.button import MDFlatButton
import sqlite3

KV = """
<AyarlarEkrani>:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Ayarlar"
            left_action_items: [["arrow-left", lambda x: app.back()]]

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: "12dp"
                spacing: "12dp"
                adaptive_height: True

                MDCard:
                    radius: [20,20,20,20]
                    padding: "12dp"
                    elevation: 2

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "8dp"

                        MDLabel:
                            text: "💊 İlaç Takip Ayarları"
                            bold: True

                        OneLineListItem:
                            text: "İlacınızı Seçin"
                            secondary_text: root.secili_ilac
                            on_release: root.ilac_popup()

                        OneLineListItem:
                            text: "İlaç Saati"
                            secondary_text: root.secili_saat

                        MDRaisedButton:
                            text: "İlacı Sil"
                            md_bg_color: 0.9,0.2,0.3,1
                            on_release: root.ilac_sil()

                MDCard:
                    radius: [20,20,20,20]
                    padding: "12dp"
                    elevation: 2

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "8dp"

                        MDLabel:
                            text: "🔔 Bildirim Ayarları"
                            bold: True

                        MDBoxLayout:
                            spacing: "10dp"
                            MDLabel:
                                text: "Bildirimleri Aç"
                            MDSwitch:
                                id: bildirim_switch

                MDCard:
                    radius: [20,20,20,20]
                    padding: "12dp"
                    elevation: 2

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "8dp"

                        MDLabel:
                            text: "🧪 Tahlil Ayarları"
                            bold: True

                        OneLineListItem:
                            text: "Tahlilinizi Seçin"
                            secondary_text: root.secili_tahlil
                            on_release: root.tahlil_popup()

                        MDRaisedButton:
                            text: "Seçili Tahlili Sil"
                            md_bg_color: 0.85,0.1,0.2,1
                            on_release: root.tahlil_sil()

        MDFillRoundFlatButton:
            text: "Kaydet"
            size_hint_x: .9
            pos_hint: {"center_x": .5}
            on_release: root.kaydet()
"""

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("tiroid_takip.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS kullanici_ilaclari (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ilac_adi TEXT,
            doz TEXT,
            saat TEXT
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tahlil_sonuclari (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarih TEXT,
            tsh REAL
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY CHECK(id=1),
            bildirim_acik INTEGER
        )""")
        self.cursor.execute("INSERT OR IGNORE INTO settings (id,bildirim_acik) VALUES (1,1)")
        self.conn.commit()

    def ilaclar(self):
        self.cursor.execute("SELECT id, ilac_adi, doz, saat FROM kullanici_ilaclari")
        return self.cursor.fetchall()

    def ilac_sil(self, ilac_id):
        self.cursor.execute("DELETE FROM kullanici_ilaclari WHERE id=?", (ilac_id,))
        self.conn.commit()

    def tahliller(self):
        self.cursor.execute("SELECT id, tarih, tsh FROM tahlil_sonuclari")
        return self.cursor.fetchall()

    def tahlil_sil(self, tahlil_id):
        self.cursor.execute("DELETE FROM tahlil_sonuclari WHERE id=?", (tahlil_id,))
        self.conn.commit()

    def ayar_kaydet(self, acik):
        self.cursor.execute("UPDATE settings SET bildirim_acik=? WHERE id=1", (acik,))
        self.conn.commit()

class AyarlarEkrani(MDScreen):
    secili_ilac = StringProperty("Seçilmedi")
    secili_saat = StringProperty("-")
    secili_tahlil = StringProperty("Seçilmedi")

    secili_ilac_id = NumericProperty(0)
    secili_tahlil_id = NumericProperty(0)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.db = Database()
        self.ilac_dialog = None
        self.tahlil_dialog = None

    def ilac_popup(self):
        items = []
        for i, ad, doz, saat in self.db.ilaclar():
            items.append(
                OneLineListItem(
                    text=f"{ad} {doz}",
                    on_release=lambda x, i=i, a=ad, d=doz, s=saat: self.ilac_sec(i,a,d,s)
                )
            )
        self.ilac_dialog = MDDialog(title="İlaç Seç", type="simple", items=items)
        self.ilac_dialog.open()

    def ilac_sec(self, i, a, d, s):
        self.secili_ilac_id = i
        self.secili_ilac = f"{a} {d}"
        self.secili_saat = s
        self.ilac_dialog.dismiss()

    def ilac_sil(self):
        if self.secili_ilac_id:
            self.db.ilac_sil(self.secili_ilac_id)
            self.secili_ilac = "Seçilmedi"
            self.secili_saat = "-"
            self.secili_ilac_id = 0

    def tahlil_popup(self):
        items = []
        for i, t, tsh in self.db.tahliller():
            items.append(
                OneLineListItem(
                    text=f"{t} | TSH: {tsh}",
                    on_release=lambda x, i=i, t=t, tsh=tsh: self.tahlil_sec(i,t,tsh)
                )
            )
        self.tahlil_dialog = MDDialog(title="Tahlil Seç", type="simple", items=items)
        self.tahlil_dialog.open()

    def tahlil_sec(self, i, t, tsh):
        self.secili_tahlil_id = i
        self.secili_tahlil = f"{t} | TSH: {tsh}"
        self.tahlil_dialog.dismiss()

    def tahlil_sil(self):
        if self.secili_tahlil_id:
            self.db.tahlil_sil(self.secili_tahlil_id)
            self.secili_tahlil = "Seçilmedi"
            self.secili_tahlil_id = 0

    def kaydet(self):
        self.db.ayar_kaydet(int(self.ids.bildirim_switch.active))

class AppMain(MDApp):
    def build(self):
        Builder.load_string(KV)
        return AyarlarEkrani()

    def back(self):
        pass

AppMain().run()
