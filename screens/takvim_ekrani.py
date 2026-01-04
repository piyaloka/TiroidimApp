from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from database import Database
import calendar
from datetime import date

# --- TASARIM (KV) ---
KV_TAKVIM = """
<DayButton>:
    orientation: "vertical"
    size_hint: None, None
    size: "40dp", "65dp"
    radius: [15]
    # Seçili ise Yeşil, değilse şeffaf
    md_bg_color: (0.67, 0.85, 0.28, 0.3) if self.selected else (1, 1, 1, 0)
    line_color: (0.67, 0.85, 0.28, 1) if self.selected else (0, 0, 0, 0)
    padding: "5dp"
    elevation: 0
    on_release: root.tiklandi()

    MDLabel:
        text: root.day_num
        halign: "center"
        font_style: "Body2"
        theme_text_color: "Custom"
        # Hafta sonu kırmızı, değilse siyah
        text_color: (0.8, 0.2, 0.2, 1) if root.is_weekend and not root.selected else (0, 0, 0, 1)
        bold: True

    MDLabel:
        text: root.status_icon
        halign: "center"
        font_size: "16sp"
        theme_text_color: "Custom"
        text_color: (0.67, 0.85, 0.28, 1)

<TakvimEkrani>:
    md_bg_color: 0.98, 0.98, 0.98, 1

    MDBoxLayout:
        orientation: "vertical"

        # --- ÜST BAR ---
        MDBoxLayout:
            size_hint_y: None
            height: "70dp"
            padding: "10dp"
            md_bg_color: 1, 1, 1, 1
            elevation: 1
            
            MDIconButton:
                icon: "arrow-left"
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
            
            Widget: # Hizalama için boşluk
                size_hint_x: None
                width: "48dp"

        # --- TAKVİM KARTI ---
        MDCard:
            size_hint_y: None
            height: "140dp"
            elevation: 0
            radius: [0, 0, 25, 25]
            md_bg_color: 1, 1, 1, 1
            padding: "10dp"
            
            MDGridLayout:
                id: calendar_grid
                cols: 7
                spacing: "5dp"
                adaptive_height: True
                pos_hint: {"center_y": 0.5}

        # --- LİSTE BAŞLIĞI ---
        MDLabel:
            id: secili_gun_baslik
            text: "Bugünün İlaçları"
            font_style: "Subtitle1"
            bold: True
            size_hint_y: None
            height: "50dp"
            padding: ["20dp", "10dp"]
            theme_text_color: "Custom"
            text_color: 0.42, 0, 0.95, 1

        # --- İLAÇ LİSTESİ ---
        ScrollView:
            MDBoxLayout:
                id: ilac_listesi
                orientation: "vertical"
                adaptive_height: True
                padding: ["20dp", "10dp"]
                spacing: "15dp"
"""

Builder.load_string(KV_TAKVIM)

# --- ÖZEL GÜN BUTONU ---
class DayButton(MDCard, ButtonBehavior):
    def __init__(self, tarih, selected, icon, is_weekend, callback, **kwargs):
        super().__init__(**kwargs)
        self.tarih = tarih
        self.day_num = str(tarih.day)
        self.selected = selected
        self.status_icon = icon
        self.is_weekend = is_weekend
        self.callback = callback # Tıklanınca çalışacak fonksiyon

    def tiklandi(self):
        self.callback(self.tarih)

# --- TAKVİM EKRANI ---
class TakvimEkrani(MDScreen):
    secili_tarih = None

    def on_enter(self):
        """Ekran açılınca çalışır"""
        self.db = Database()
        if not self.secili_tarih:
            self.secili_tarih = date.today()
        
        self.takvimi_ciz()
        self.gun_detayi_yukle(self.secili_tarih)

    def takvimi_ciz(self):
        grid = self.ids.calendar_grid
        grid.clear_widgets()

        # Gün başlıkları
        gun_adlari = ["Pz", "Sa", "Ça", "Pe", "Cu", "Ct", "Pa"]
        for g in gun_adlari:
            grid.add_widget(MDLabel(text=g, halign="center", font_style="Caption", theme_text_color="Hint"))

        yil, ay = self.secili_tarih.year, self.secili_tarih.month
        ilk_gun_indeksi, gun_sayisi = calendar.monthrange(yil, ay)

        # Boşluklar (Ayın ilk günü hangi güne denk geliyorsa)
        for _ in range(ilk_gun_indeksi):
            grid.add_widget(MDLabel(text=""))

        # Günleri Buton Olarak Ekle
        for gun in range(1, gun_sayisi + 1):
            tarih = date(yil, ay, gun)
            
            # Veritabanından ikon çek (✅, ❌, ⚠️ veya ➖)
            durum = self.db.gun_ikonunu_hesapla(str(tarih))
            ikon = durum["icon"]
            if durum["status"] == "NO_PLAN":
                ikon = "" # Plan yoksa boş görünsün

            is_weekend = tarih.weekday() >= 5 
            is_selected = (tarih == self.secili_tarih)

            btn = DayButton(
                tarih=tarih,
                selected=is_selected,
                icon=ikon,
                is_weekend=is_weekend,
                callback=self.gun_sec
            )
            grid.add_widget(btn)

    def gun_sec(self, tarih):
        """Takvimden bir güne tıklanınca"""
        self.secili_tarih = tarih
        self.ids.secili_gun_baslik.text = f"{tarih.day}.{tarih.month}.{tarih.year} İlaçları"
        self.takvimi_ciz() # Seçimi güncellemek için yeniden çiz
        self.gun_detayi_yukle(tarih)

    def gun_detayi_yukle(self, tarih):
        """Seçilen günün ilaçlarını listeler"""
        box = self.ids.ilac_listesi
        box.clear_widgets()

        kartlar = self.db.dashboard_kartlarini_getir(str(tarih))

        if not kartlar:
            box.add_widget(MDLabel(
                text="Bu tarih için kayıtlı ilaç planı yok.", 
                halign="center", 
                theme_text_color="Hint"
            ))
            return

        for k in kartlar:
            # Renklendirme
            if k["taken"] is True:
                bg_color = (0.9, 1, 0.9, 1) # Açık Yeşil
                durum = "ALINDI ✅"
                renk = (0, 0.5, 0, 1)
            elif k["taken"] is False:
                bg_color = (1, 0.9, 0.9, 1) # Açık Kırmızı
                durum = "ATLANDI ❌"
                renk = (0.8, 0, 0, 1)
            else:
                bg_color = (1, 1, 1, 1) # Beyaz
                durum = "BEKLİYOR ⏳"
                renk = (0.5, 0.5, 0.5, 1)

            card = MDCard(
                orientation="horizontal",
                size_hint_y=None,
                height="80dp",
                radius=[15],
                md_bg_color=bg_color,
                padding="15dp",
                elevation=1
            )

            # Sol taraf: İlaç Bilgisi
            info = MDBoxLayout(orientation="vertical", spacing="5dp")
            info.add_widget(MDLabel(text=k["ilac_adi"], bold=True))
            info.add_widget(MDLabel(text=f"{k['doz']} - {k['saat']}", font_style="Caption"))
            
            # Sağ taraf: Durum
            durum_lbl = MDLabel(text=durum, halign="right", bold=True, theme_text_color="Custom", text_color=renk)

            card.add_widget(info)
            card.add_widget(durum_lbl)
            box.add_widget(card)