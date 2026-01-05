from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.behaviors import ButtonBehavior
from datetime import date
import calendar

from database import Database

KV_TAKVIM = """
<DayButton>:
    orientation: "vertical"
    size_hint: None, None
    size: "42dp", "65dp"
    radius: [12]
    md_bg_color: (0.42, 0, 0.95, 0.1) if self.selected else (1, 1, 1, 0)
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
        font_size: "14sp"
        theme_text_color: "Custom"
        text_color: (0.42, 0, 0.95, 1)

<TakvimEkrani>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 1, 1, 1, 1

        # Header ve Takvim Kartı Alanı (Görseldeki gibi)
        MDBoxLayout:
            size_hint_y: None
            height: "70dp"
            padding: ["20dp", "10dp"]
            MDIconButton:
                icon: "account-circle"
                text_color: 0.42, 0, 0.95, 1
            Widget:
            MDIcon:
                icon: "butterfly"
                text_color: 0.42, 0, 0.95, 1
            Widget:
            MDIconButton:
                icon: "cog"

        MDLabel:
            text: "Tedavi Uyumu"
            font_style: "H6"
            bold: True
            padding: ["20dp", 0]
            size_hint_y: None
            height: "40dp"

        MDCard:
            size_hint: 0.9, None
            height: "260dp"
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
                padding: "20dp"
                spacing: "15dp"
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
        # İlaç kontrolü burada yapılır
        self.takvimi_ciz()
        self.gun_detayi_yukle(self.secili_tarih)

    def takvimi_ciz(self):
        grid = self.ids.calendar_grid
        grid.clear_widgets()

        # İlaç listesi boş mu kontrol et
        ilac_plani_var_mi = len(self.db.kullanici_ilaclarini_getir()) > 0

        yil, ay = self.secili_tarih.year, self.secili_tarih.month
        ilk_gun, gun_sayisi = calendar.monthrange(yil, ay)

        # Gün başlıklarını ekle
        for g in ["Pz", "Sa", "Ça", "Pe", "Cu", "Ct", "Pa"]:
            grid.add_widget(MDLabel(text=g, halign="center", font_style="Caption"))

        for _ in range(ilk_gun):
            grid.add_widget(MDLabel(text=""))

        for gun in range(1, gun_sayisi + 1):
            tarih = date(yil, ay, gun)
            
            # Eğer ilaç planı yoksa ikon her zaman boş kalır
            if not ilac_plani_var_mi:
                ikon = ""
            else:
                # İlaç varsa durumuna göre ikon hesaplanır
                ikon_data = self.db.gun_ikonunu_hesapla(str(tarih))
                ikon = ikon_data["icon"] if ikon_data["status"] != "NO_PLAN" else "·"

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
            box.add_widget(MDLabel(text="İlaç eklenmedi.", halign="center", theme_text_color="Hint"))
            return

        for k in kartlar:
            # Kart tasarımı ve seçim kutucukları buraya gelecek
            card = MDCard(size_hint_y=None, height="100dp", radius=[20], md_bg_color=(0.9, 0.9, 0.9, 1))
            card.add_widget(MDLabel(text=f"{k['ilac_adi']} - {k['saat']}", halign="center"))
            box.add_widget(card)

Builder.load_string(KV_TAKVIM)
