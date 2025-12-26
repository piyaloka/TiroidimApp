from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from datetime import date
import calendar

from database import Database   # DOSYA ADINI database.py YAP

db = Database()

KV = """
<TakvimEkrani>:
    name: "takvim"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 1,1,1,1

        MDTopAppBar:
            title: "Tedavi Uyumu"
            elevation: 0
            md_bg_color: 1,1,1,1
            specific_text_color: 0.42, 0, 0.95, 1

        ScrollView:
            MDGridLayout:
                id: calendar_grid
                cols: 7
                adaptive_height: True
                padding: "10dp"
                spacing: "5dp"

        MDSeparator:

        ScrollView:
            MDBoxLayout:
                id: ilac_listesi
                orientation: "vertical"
                adaptive_height: True
                padding: "10dp"
                spacing: "10dp"
"""

Builder.load_string(KV)


class TakvimEkrani(MDScreen):
    def on_enter(self):
        self.secili_tarih = date.today()
        self.takvimi_ciz()
        self.gun_detayi_yukle(self.secili_tarih)

    def takvimi_ciz(self):
        self.ids.calendar_grid.clear_widgets()

        today = date.today()
        yil, ay = today.year, today.month
        gun_sayisi = calendar.monthrange(yil, ay)[1]

        for gun in range(1, gun_sayisi + 1):
            tarih = date(yil, ay, gun)
            ikon = db.gun_ikonunu_hesapla(str(tarih))["icon"]

            btn = MDFlatButton(
                text=f"{gun}\n{ikon}",
                on_release=lambda x, t=tarih: self.gun_sec(t)
            )
            self.ids.calendar_grid.add_widget(btn)

    def gun_sec(self, tarih):
        self.secili_tarih = tarih
        self.gun_detayi_yukle(tarih)

    def gun_detayi_yukle(self, tarih):
        self.ids.ilac_listesi.clear_widgets()
        kartlar = db.dashboard_kartlarini_getir(str(tarih))

        for k in kartlar:
            durum = "—"
            if k["taken"] is True:
                durum = "✅"
            elif k["taken"] is False:
                durum = "❌"

            card = MDCard(
                size_hint_y=None,
                height="70dp",
                radius=[16],
                md_bg_color=(0.95, 0.95, 0.95, 1),
                padding="10dp"
            )

            card.add_widget(
                MDLabel(
                    text=f"{k['saat']}  {k['ilac_adi']} {k['doz']}   {durum}",
                    halign="left"
                )
            )

            self.ids.ilac_listesi.add_widget(card)

