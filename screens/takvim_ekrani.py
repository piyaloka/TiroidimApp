from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from datetime import date
import calendar

from database import Database


KV_TAKVIM = """
<DayButton>:
    orientation: "vertical"
    size_hint: None, None
    size: "42dp", "68dp"
    radius: [15]
    md_bg_color: (0.42, 0, 0.95, 0.15) if self.selected else (1, 1, 1, 0)
    padding: "4dp"
    spacing: "2dp"

    MDLabel:
        text: root.day_num
        halign: "center"
        font_style: "Caption"
        bold: True
        theme_text_color: "Custom"
        text_color: (1, 0, 0, 1) if root.is_weekend and not root.selected else (0, 0, 0, 1)

    MDLabel:
        text: root.status_icon
        halign: "center"
        font_size: "16sp"
        theme_text_color: "Custom"
        text_color: (0.42, 0, 0.95, 1)


<IlacKartKutucugu@MDCard>:
    text: ""
    size_hint: None, None
    height: "35dp"
    radius: [10]
    md_bg_color: 1, 1, 1, 1
    elevation: 0
    padding: ["8dp", 0]
    MDBoxLayout:
        MDLabel:
            text: root.text
            font_style: "Caption"
        MDIcon:
            icon: "chevron-down"
            font_size: "16sp"


<TakvimEkrani>:
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1

        MDBoxLayout:
            orientation: "vertical"
            pos_hint: {"top": 1}

            # ÜST BAR
            MDBoxLayout:
                size_hint_y: None
                height: "70dp"
                padding: ["20dp", "10dp"]
                MDIconButton:
                    icon: "account-circle"
                    theme_text_color: "Custom"
                    text_color: 0.42, 0, 0.95, 1
                Widget:
                MDIcon:
                    icon: "butterfly"
                    theme_text_color: "Custom"
                    text_color: 0.42, 0, 0.95, 1
                Widget:
                MDIconButton:
                    icon: "cog"
                    on_release: app.root.current = "ayarlar"

            MDLabel:
                text: "Tedavi Uyumu"
                font_style: "H6"
                bold: True
                padding: ["20dp", 0]
                size_hint_y: None
                height: "40dp"

            # TAKVİM
            MDCard:
                size_hint: 0.9, None
                height: "280dp"
                pos_hint: {"center_x": .5}
                radius: [25]
                elevation: 1
                md_bg_color: 0.98, 0.98, 1, 1
                MDGridLayout:
                    id: calendar_grid
                    cols: 7
                    padding: "10dp"
                    spacing: "2dp"

            MDLabel:
                text: "İlaçlar"
                font_style: "H6"
                bold: True
                padding: ["20dp", "15dp"]
                size_hint_y: None
                height: "50dp"

            ScrollView:
                MDBoxLayout:
                    id: ilac_listesi
                    orientation: "vertical"
                    adaptive_height: True
                    padding: ["20dp", 0, "20dp", "100dp"]
                    spacing: "15dp"

        # 🔗 MEVCUT + BUTONU (SADECE ENTEGRE EDİLDİ)
        MDFloatingActionButton:
            icon: "plus"
            md_bg_color: 0.42, 0, 0.95, 1
            pos_hint: {"center_x": .85, "center_y": .15}
            on_release: root.arti_butonuna_git()

        # ALT NAV
        MDCard:
            size_hint: 0.9, None
            height: "65dp"
            radius: [30]
            elevation: 2
            pos_hint: {"center_x": .5, "center_y": .06}
            md_bg_color: 1, 1, 1, 1
            MDBoxLayout:
                padding: ["25dp", 0]
                MDIconButton:
                    icon: "home-outline"
                    on_release: app.root.current = "dashboard"
                Widget:
                MDIconButton:
                    icon: "calendar-month"
                    theme_text_color: "Custom"
                    text_color: 0.42, 0, 0.95, 1
                Widget:
                MDIconButton:
                    icon: "chart-line"
                    on_release: app.root.current = "grafik"
"""


class DayButton(MDCard, ButtonBehavior):
    def __init__(self, tarih, selected, icon, is_weekend, **kwargs):
        super().__init__(**kwargs)
        self.tarih = tarih
        self.day_num = str(tarih.day)
        self.selected = selected
        self.status_icon = icon
        self.is_weekend = is_weekend


class TakvimEkrani(MDScreen):

    def on_enter(self):
        self.db = Database()
        self.secili_tarih = date.today()
        self.takvimi_ciz()
        self.gun_detayi_yukle(self.secili_tarih)

    # ➕ BUTON ENTEGRASYONU
    def arti_butonuna_git(self):
        self.manager.current = "arti_butonu"

    def takvimi_ciz(self):
        grid = self.ids.calendar_grid
        grid.clear_widgets()

        for g in ["Pz", "Sa", "Ça", "Pe", "Cu", "Ct", "Pa"]:
            grid.add_widget(
                MDLabel(text=g, halign="center", font_style="Caption", theme_text_color="Hint")
            )

        yil, ay = self.secili_tarih.year, self.secili_tarih.month
        ilk_gun, gun_sayisi = calendar.monthrange(yil, ay)

        kullanici_ilaclari = self.db.kullanici_ilaclarini_getir()

        for _ in range(ilk_gun):
            grid.add_widget(MDLabel(text=""))

        for gun in range(1, gun_sayisi + 1):
            tarih = date(yil, ay, gun)

            if kullanici_ilaclari:
                ikon_data = self.db.gun_ikonunu_hesapla(str(tarih))
                ikon = ikon_data["icon"] if ikon_data["status"] != "NO_PLAN" else "·"
            else:
                ikon = ""

            btn = DayButton(
                tarih=tarih,
                selected=(tarih == self.secili_tarih),
                icon=ikon,
                is_weekend=(tarih.weekday() >= 5),
                on_release=lambda x, t=tarih: self.gun_sec(t)
            )
            grid.add_widget(btn)

    def gun_sec(self, tarih):
        self.secili_tarih = tarih
        self.takvimi_ciz()
        self.gun_detayi_yukle(tarih)

    def gun_detayi_yukle(self, tarih):
        box = self.ids.ilac_listesi
        box.clear_widgets()

        kartlar = self.db.dashboard_kartlarini_getir(str(tarih))

        if not kartlar:
            return

        for k in kartlar:
            bg = (0.88, 0.94, 0.75, 1) if k["taken"] else (1, 1, 0.9, 1)

            card = MDCard(
                orientation="vertical",
                size_hint_y=None,
                height="120dp",
                radius=[20],
                md_bg_color=bg,
                padding="15dp",
                elevation=0
            )

            card.add_widget(MDLabel(text=k["ilac_adi"], bold=True, font_style="H6"))
            card.add_widget(MDLabel(text=tarih.strftime("%d/%m/%Y"), font_style="Caption"))

            row = Builder.template("IlacKartKutucugu", text=k["doz"], width=dp(110))
            row2 = Builder.template("IlacKartKutucugu", text="adet", width=dp(70))
            row3 = Builder.template("IlacKartKutucugu", text="gün", width=dp(70))

            line = Builder.load_string("""
MDBoxLayout:
    spacing: "10dp"
    size_hint_y: None
    height: "40dp"
""")

            line.add_widget(row)
            line.add_widget(row2)
            line.add_widget(row3)

            card.add_widget(line)
            box.add_widget(card)


Builder.load_string(KV_TAKVIM)

