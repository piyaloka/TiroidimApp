import sys
import os

# --- KRİTİK DÜZELTME 1: YOL AYARI ---
# Python'un üst klasördeki 'database.py'yi görmesini sağlar
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)
# ------------------------------------

from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.behaviors import ButtonBehavior
from datetime import date
import calendar

# Database dosyasını çağır
try:
    from database import Database
except ImportError:
    # Eğer hala bulamazsa hata verip çökmesin diye geçici çözüm
    print("UYARI: Database dosyası bulunamadı, sahte veri kullanılıyor.")
    class Database:
        def gun_ikonunu_hesapla(self, tarih):
            return {"status": "NO_PLAN", "icon": ""}
        def dashboard_kartlarini_getir(self, tarih):
            return []

KV = """
<DayButton>:
    orientation: "vertical"
    size_hint: None, None
    size: "45dp", "65dp"
    radius: [10]
    md_bg_color: (0.42, 0, 0.95, 0.1) if self.selected else (1, 1, 1, 0)
    padding: "5dp"
    spacing: "2dp"
    elevation: 0

    MDLabel:
        text: root.day_num
        halign: "center"
        font_style: "Caption"
        theme_text_color: "Custom"
        text_color: (0.42, 0, 0.95, 1) if root.selected else (0, 0, 0, 1)
        bold: True

    MDLabel:
        text: root.status_icon
        halign: "center"
        font_size: "14sp"

<TakvimEkrani>:
    name: "takvim"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 1, 1, 1, 1

        MDTopAppBar:
            title: "Tedavi Uyumu"
            elevation: 0
            md_bg_color: 1, 1, 1, 1
            specific_text_color: 0.42, 0, 0.95, 1
            left_action_items: [['calendar-month', lambda x: None]]

        # Takvim Grid Alanı
        MDCard:
            size_hint_y: None
            height: "280dp"
            elevation: 1
            radius: [0, 0, 20, 20]
            md_bg_color: 0.98, 0.98, 1, 1
            margin: "10dp"
            
            MDGridLayout:
                id: calendar_grid
                cols: 7
                padding: "10dp"
                spacing: "5dp"

        MDLabel:
            text: "İlaçlar"
            font_style: "H6"
            bold: True
            size_hint_y: None
            height: "40dp"
            padding: ["20dp", 0]
            theme_text_color: "Custom"
            text_color: 0.2, 0.2, 0.2, 1

        ScrollView:
            MDBoxLayout:
                id: ilac_listesi
                orientation: "vertical"
                adaptive_height: True
                padding: "20dp"
                spacing: "15dp"
"""

# --- KRİTİK DÜZELTME 2: MRO HATASI GİDERİLDİ ---
# MDCard başa alındı
class DayButton(MDCard, ButtonBehavior):
    day_num = ""
    status_icon = ""
    selected = False
    
    def __init__(self, t, is_selected, icon, **kwargs):
        super().__init__(**kwargs)
        self.tarih = t
        self.day_num = str(t.day)
        self.selected = is_selected
        self.status_icon = icon

Builder.load_string(KV)

class TakvimEkrani(MDScreen):
    def on_enter(self):
        # Database sınıfını başlat
        if not hasattr(self, "db"):
            self.db = Database()
        
        self.secili_tarih = date.today()
        self.takvimi_ciz()
        self.gun_detayi_yukle(self.secili_tarih)

    def takvimi_ciz(self):
        self.ids.calendar_grid.clear_widgets()
        
        # Gün isimlerini ekle (P, S, Ç...)
        gunler = ["Pz", "Sa", "Çar", "Per", "Cu", "Cmt", "Paz"]
        for g in gunler:
            self.ids.calendar_grid.add_widget(
                MDLabel(text=g, halign="center", font_style="Caption", theme_text_color="Hint")
            )

        today = date.today()
        yil, ay = today.year, today.month
        ilk_gun, gun_sayisi = calendar.monthrange(yil, ay)

        # Ayın ilk gününe kadar boşluk
        for _ in range(ilk_gun):
            self.ids.calendar_grid.add_widget(MDLabel(text=""))

        for gun in range(1, gun_sayisi + 1):
            tarih = date(yil, ay, gun)
            
            # Veritabanından veri çekme denemesi
            try:
                ikon_verisi = self.db.gun_ikonunu_hesapla(str(tarih))
            except:
                ikon_verisi = {"status": "NO_PLAN", "icon": ""}

            ikon = ikon_verisi.get("icon", "") if ikon_verisi.get("status") != "NO_PLAN" else "·"
            
            is_selected = (tarih == self.secili_tarih)
            
            btn = DayButton(
                t=tarih, 
                is_selected=is_selected, 
                icon=ikon,
                on_release=lambda x: self.gun_sec(x.tarih)
            )
            self.ids.calendar_grid.add_widget(btn)

    def gun_sec(self, tarih):
        self.secili_tarih = tarih
        self.takvimi_ciz()
        self.gun_detayi_yukle(tarih)

    def gun_detayi_yukle(self, tarih):
        self.ids.ilac_listesi.clear_widgets()
        try:
            kartlar = self.db.dashboard_kartlarini_getir(str(tarih))
        except:
            kartlar = []

        if not kartlar:
            self.ids.ilac_listesi.add_widget(
                MDLabel(text="Bu gün için kayıtlı ilaç yok.", halign="center", theme_text_color="Hint")
            )
            return

        for k in kartlar:
            bg_color = (0.8, 0.95, 0.8, 1) if k["taken"] else (0.95, 0.95, 0.95, 1)
            durum_metni = "Alındı ✅" if k["taken"] else ("Atlandı ❌" if k["taken"] is False else "Bekliyor")

            card = MDCard(
                orientation="vertical",
                size_hint_y=None,
                height="100dp",
                radius=[20],
                md_bg_color=bg_color,
                padding="15dp",
                elevation=1
            )

            card.add_widget(MDLabel(text=k['ilac_adi'], bold=True, font_style="H6"))
            card.add_widget(MDLabel(text=f"{k['saat']} - {k['doz']}", theme_text_color="Secondary"))
            card.add_widget(MDLabel(text=durum_metni, halign="right", theme_text_color="Primary", bold=True))

            self.ids.ilac_listesi.add_widget(card)