import calendar
from datetime import date
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from database import Database

KV_TAKVIM = """
<DayButton>:
    orientation: "vertical"
    size_hint: None, None
    size: "45dp", "70dp"
    radius: [15]
    # Seçili gün için fıstık yeşili vurgusu
    md_bg_color: (0.67, 0.85, 0.28, 0.2) if self.selected else (1, 1, 1, 0)
    line_color: (0.67, 0.85, 0.28, 1) if self.selected else (0, 0, 0, 0)
    padding: "5dp"
    elevation: 0

    MDLabel:
        text: root.day_num
        halign: "center"
        font_style: "Button"
        theme_text_color: "Custom"
        # Hafta sonu ise kırmızı (Görseldeki gibi)
        text_color: (0.8, 0.2, 0.2, 1) if root.is_weekend and not root.selected else (0, 0, 0, 1)
        bold: True

    MDLabel:
        text: root.status_icon
        halign: "center"
        font_size: "18sp"
        theme_text_color: "Custom"
        text_color: (0.67, 0.85, 0.28, 1)

<TakvimEkrani>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 1, 1, 1, 1

        MDTopAppBar:
            title: "Tedavi Uyumu"
            elevation: 0
            md_bg_color: 1, 1, 1, 1
            specific_text_color: 0, 0, 0, 1
            left_action_items: [['chevron-left', lambda x: setattr(app.root, 'current', 'dashboard')]]

        MDCard:
            size_hint_y: None
            height: "320dp"
            elevation: 0
            radius: [0, 0, 30, 30]
            md_bg_color: 0.98, 0.99, 0.96, 1
            
            MDBoxLayout:
                orientation: "vertical"
                padding: "15dp"
                
                MDGridLayout:
                    id: calendar_grid
                    cols: 7
                    spacing: "4dp"

        MDLabel:
            text: "Günlük İlaç Özeti"
            font_style: "H6"
            bold: True
            size_hint_y: None
            height: "60dp"
            padding: ["20dp", 0]

        ScrollView:
            MDBoxLayout:
                id: ilac_listesi
                orientation: "vertical"
                adaptive_height: True
                padding: ["20dp", "10dp"]
                spacing: "12dp"
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

    def takvimi_ciz(self):
        grid = self.ids.calendar_grid
        grid.clear_widgets()

        # Gün başlıkları (Pzt, Sal...)
        gun_adlari = ["Pz", "Sa", "Ça", "Pe", "Cu", "Ct", "Pa"]
        for g in gun_adlari:
            grid.add_widget(MDLabel(text=g, halign="center", font_style="Caption", theme_text_color="Hint"))

        yil, ay = self.secili_tarih.year, self.secili_tarih.month
        ilk_gun, gun_sayisi = calendar.monthrange(yil, ay)

        # Ay başındaki boşluklar
        for _ in range(ilk_gun):
            grid.add_widget(MDLabel(text=""))

        for gun in range(1, gun_sayisi + 1):
            tarih = date(yil, ay, gun)
            # Veritabanından o günün ikonunu hesapla
            ikon_data = self.db.gun_ikonunu_hesapla(str(tarih))
            ikon = ikon_data["icon"] if ikon_data["status"] != "NO_PLAN" else "·"
            
            is_weekend = tarih.weekday() >= 5 

            btn = DayButton(
                tarih=tarih,
                selected=(tarih == self.secili_tarih),
                icon=ikon,
                is_weekend=is_weekend,
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

        # Database üzerinden o günün kartlarını çek
        kartlar = self.db.dashboard_kartlarini_getir(str(tarih))

        if not kartlar:
            box.add_widget(MDLabel(text="Bu tarihte ilaç kaydı bulunamadı.", halign="center", theme_text_color="Hint"))
            return

        for k in kartlar:
            # Onboarding ile uyumlu fıstık yeşili (0.67, 0.85, 0.28)
            bg_color = (0.67, 0.85, 0.28, 0.1) if k["taken"] else (0.96, 0.96, 0.96, 1)
            durum_metni = "Alındı ✅" if k["taken"] else ("Atlandı ❌" if k["taken"] is False else "Bekliyor ⏳")

            card = MDCard(
                orientation="horizontal",
                size_hint_y=None,
                height="85dp",
                radius=[20],
                md_bg_color=bg_color,
                padding="15dp",
                elevation=0
            )

            info_box = MDBoxLayout(orientation="vertical")
            info_box.add_widget(MDLabel(text=k["ilac_adi"], bold=True, font_style="Subtitle1"))
            info_box.add_widget(MDLabel(text=f"{k['saat']} | {k['doz']}", font_style="Caption", theme_text_color="Secondary"))
            
            card.add_widget(info_box)
            card.add_widget(MDLabel(text=durum_metni, halign="right", bold=True, theme_text_color="Primary"))

            box.add_widget(card)

Builder.load_string(KV_TAKVIM)
