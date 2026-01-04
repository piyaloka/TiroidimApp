from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from database import Database
import calendar
from datetime import date

# --- TASARIM (KV) ---
KV_TAKVIM = """
<DayButton>:
    orientation: "vertical"
    size_hint: None, None
    size: "45dp", "75dp"
    radius: [15]
    md_bg_color: (0.42, 0, 0.95, 0.1) if self.selected else (1, 1, 1, 0)
    line_color: (0.42, 0, 0.95, 0.5) if self.selected else (0, 0, 0, 0.05)
    line_width: 1.2
    padding: "4dp"
    spacing: "2dp"
    on_release: root.tiklandi()

    MDLabel:
        text: root.day_num
        halign: "center"
        font_style: "Button"
        theme_text_color: "Custom"
        text_color: (0.42, 0, 0.95, 1) if root.selected else (0, 0, 0, 0.8)
        bold: True

    MDLabel:
        text: root.status_icon
        halign: "center"
        font_size: "18sp"
        theme_text_color: "Custom"
        text_color: (0.67, 0.85, 0.28, 1) # Yeşil tonu

<TakvimEkrani>:
    md_bg_color: 0.98, 0.98, 0.98, 1

    MDBoxLayout:
        orientation: "vertical"

        # --- ÜST PANEL ---
        MDBoxLayout:
            size_hint_y: None
            height: "65dp"
            padding: ["10dp", 0]
            md_bg_color: 1, 1, 1, 1
            
            MDIconButton:
                icon: "chevron-left"
                pos_hint: {"center_y": 0.5}
                on_release: 
                    root.manager.current = "dashboard"
                    root.manager.transition.direction = "right"

            MDLabel:
                text: "Tedavi Takvimi"
                font_style: "H6"
                bold: True
                halign: "center"
                pos_hint: {"center_y": 0.5}
            
            Widget:
                size_hint_x: None
                width: "48dp"

        # --- TAKVİM ŞERİDİ (YATAY KART) ---
        MDCard:
            size_hint_y: None
            height: "160dp"
            elevation: 0
            radius: [0, 0, 30, 30]
            md_bg_color: 1, 1, 1, 1
            padding: ["10dp", "5dp"]
            
            MDGridLayout:
                id: calendar_grid
                cols: 7
                spacing: "2dp"
                adaptive_height: True
                pos_hint: {"top": 1}

        # --- SEÇİLİ GÜN BİLGİSİ ---
        MDBoxLayout:
            size_hint_y: None
            height: "60dp"
            padding: ["20dp", "10dp"]
            
            MDLabel:
                id: secili_gun_baslik
                text: "Bugünün İlaçları"
                font_style: "Subtitle1"
                bold: True
                theme_text_color: "Primary"

        # --- İLAÇ LİSTESİ (KARTLAR) ---
        ScrollView:
            do_scroll_x: False
            MDBoxLayout:
                id: ilac_listesi
                orientation: "vertical"
                adaptive_height: True
                padding: ["20dp", "5dp"]
                spacing: "12dp"
"""

Builder.load_string(KV_TAKVIM)

class DayButton(MDCard, ButtonBehavior):
    day_num = StringProperty()
    status_icon = StringProperty()
    selected = BooleanProperty(False)
    is_weekend = BooleanProperty(False)
    
    def __init__(self, tarih, selected, icon, is_weekend, callback, **kwargs):
        super().__init__(**kwargs)
        self.tarih = tarih
        self.day_num = str(tarih.day)
        self.selected = selected
        self.status_icon = icon
        self.is_weekend = is_weekend
        self.callback = callback

    def tiklandi(self):
        self.callback(self.tarih)

class TakvimEkrani(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.secili_tarih = date.today()

    def on_enter(self):
        """Ekran her açıldığında verileri tazeler"""
        self.takvimi_ciz()
        self.gun_detayi_yukle(self.secili_tarih)

    def takvimi_ciz(self):
        grid = self.ids.calendar_grid
        grid.clear_widgets()

        # 1. Gün Başlıkları (Pazartesi'den başlar)
        gunler = ["Pt", "Sa", "Ça", "Pe", "Cu", "Ct", "Pz"]
        for g in gunler:
            grid.add_widget(MDLabel(
                text=g, 
                halign="center", 
                font_style="Caption", 
                theme_text_color="Hint",
                size_hint_y=None,
                height="30dp"
            ))

        # 2. Takvim Hesaplamaları
        yil, ay = self.secili_tarih.year, self.secili_tarih.month
        ilk_gun_indeksi, gun_sayisi = calendar.monthrange(yil, ay)

        # Ayın ilk gününe kadar boşluk ekle
        for _ in range(ilk_gun_indeksi):
            grid.add_widget(MDLabel(text=""))

        # 3. Günleri Ekle
        for gun in range(1, gun_sayisi + 1):
            tarih = date(yil, ay, gun)
            
            # Veritabanından durum bilgisini al
            durum_verisi = self.db.gun_ikonunu_hesapla(str(tarih))
            ikon = durum_verisi["icon"] if durum_verisi["status"] != "NO_PLAN" else ""

            btn = DayButton(
                tarih=tarih,
                selected=(tarih == self.secili_tarih),
                icon=ikon,
                is_weekend=(tarih.weekday() >= 5),
                callback=self.gun_sec
            )
            grid.add_widget(btn)

    def gun_sec(self, tarih):
        self.secili_tarih = tarih
        self.ids.secili_gun_baslik.text = f"{tarih.strftime('%d.%m.%Y')} İlaçları"
        self.takvimi_ciz()
        self.gun_detayi_yukle(tarih)

    def gun_detayi_yukle(self, tarih):
        box = self.ids.ilac_listesi
        box.clear_widgets()

        # O güne ait ilaç kartlarını getir
        kartlar = self.db.dashboard_kartlarini_getir(str(tarih))

        if not kartlar:
            box.add_widget(MDLabel(
                text="Bu gün için planlanmış ilaç yok.", 
                halign="center", 
                padding=[0, "50dp"],
                theme_text_color="Hint"
            ))
            return

        for k in kartlar:
            # Duruma göre renk ve metin belirle
            if k["taken"] is True:
                renk, durum_metni, bg = (0, 0.6, 0, 1), "ALINDI ✅", (0.9, 1, 0.9, 1)
            elif k["taken"] is False:
                renk, durum_metni, bg = (0.8, 0, 0, 1), "ATLANDI ❌", (1, 0.9, 0.9, 1)
            else:
                renk, durum_metni, bg = (0.5, 0.5, 0.5, 1), "BEKLİYOR ⏳", (1, 1, 1, 1)

            card = MDCard(
                orientation="horizontal",
                size_hint_y=None, height="85dp",
                radius=[15], padding="15dp", elevation=1,
                md_bg_color=bg
            )

            vbox = MDBoxLayout(orientation="vertical")
            vbox.add_widget(MDLabel(text=k["ilac_adi"], bold=True, font_style="Subtitle1"))
            vbox.add_widget(MDLabel(text=f"{k['doz']} • Saat: {k['saat']}", font_style="Caption"))
            
            card.add_widget(vbox)
            card.add_widget(MDLabel(
                text=durum_metni, halign="right", 
                theme_text_color="Custom", text_color=renk, bold=True
            ))
            box.add_widget(card)
