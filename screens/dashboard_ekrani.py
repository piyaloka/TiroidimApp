import sys
import os
#kodunuzda hata çıkmaması için
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, NumericProperty, BooleanProperty
from kivy.animation import Animation
from kivy.metrics import dp
import datetime as _dt
from database import Database

# --- YARDIMCI SINIFLAR (Arkadaşının yazdığı özel kartlar - DOKUNULMADI) ---
class WeekCalendar(MDCard):
    days = ListProperty([])
    selected_idx = NumericProperty(0) # 0=Bugün

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hazirla()

    def hazirla(self):
        # Basitçe bu haftanın günlerini oluştur
        self.days = []
        bugun = _dt.date.today()
        # Pazartesiye git
        start = bugun - _dt.timedelta(days=bugun.weekday())
        
        gun_isimleri = ["P", "S", "Ç", "P", "C", "C", "P"]
        
        for i in range(7):
            d = start + _dt.timedelta(days=i)
            self.days.append({
                "dow": gun_isimleri[i],
                "day": f"{d.day:02d}",
                "is_weekend": i >= 5
            })
        
        # Bugünü seçili yap (0-6 arası index)
        self.selected_idx = bugun.weekday()

    def select_day(self, idx):
        self.selected_idx = idx

class SymptomBtn(MDCard):
    text = StringProperty()
    icon = StringProperty()

class ActionBtn(MDCard):
    text = StringProperty()
    bg = ListProperty([1, 1, 1, 1])
    text_color = ListProperty([0, 0, 0, 1])

class MedicineCard(MDCard):
    time = StringProperty()
    pill = StringProperty()
    note = StringProperty()
    bg = ListProperty([1, 1, 1, 1])
    btn_color = ListProperty([1, 1, 1, 1])


# --- TASARIM KODLARI (KV) ---
KV_DASHBOARD = '''
<WeekCalendar>:
    size_hint_y: None
    height: "90dp"
    radius: [20,]
    elevation: 0
    md_bg_color: [1, 1, 1, 0] # Şeffaf olsun
    padding: ["0dp", "10dp", "0dp", "10dp"]

    MDGridLayout:
        cols: 7
        adaptive_height: True
        spacing: "8dp"
        
        # 7 Gün İçin Döngü Yapılamadığı İçin Tek Tek Yazıyoruz (Kivy Kısıtı)
        # --- PAZARTESİ ---
        MDCard:
            size_hint: None, None
            size: "38dp", "65dp"
            radius: [15,]
            md_bg_color: [0.5, 0.3, 0.9, 1] if root.selected_idx == 0 else [1, 1, 1, 1]
            on_release: root.select_day(0)
            elevation: 1
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: root.days[0]["dow"] if root.days else ""
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: [1,1,1,1] if root.selected_idx == 0 else [0,0,0,0.5]
                MDLabel:
                    text: root.days[0]["day"] if root.days else ""
                    halign: "center"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1,1,1,1] if root.selected_idx == 0 else [0,0,0,1]

        # --- SALI ---
        MDCard:
            size_hint: None, None
            size: "38dp", "65dp"
            radius: [15,]
            md_bg_color: [0.5, 0.3, 0.9, 1] if root.selected_idx == 1 else [1, 1, 1, 1]
            on_release: root.select_day(1)
            elevation: 1
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: root.days[1]["dow"] if root.days else ""
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: [1,1,1,1] if root.selected_idx == 1 else [0,0,0,0.5]
                MDLabel:
                    text: root.days[1]["day"] if root.days else ""
                    halign: "center"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1,1,1,1] if root.selected_idx == 1 else [0,0,0,1]
        
        # --- ÇARŞAMBA ---
        MDCard:
            size_hint: None, None
            size: "38dp", "65dp"
            radius: [15,]
            md_bg_color: [0.5, 0.3, 0.9, 1] if root.selected_idx == 2 else [1, 1, 1, 1]
            on_release: root.select_day(2)
            elevation: 1
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: root.days[2]["dow"] if root.days else ""
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: [1,1,1,1] if root.selected_idx == 2 else [0,0,0,0.5]
                MDLabel:
                    text: root.days[2]["day"] if root.days else ""
                    halign: "center"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1,1,1,1] if root.selected_idx == 2 else [0,0,0,1]

        # --- PERŞEMBE ---
        MDCard:
            size_hint: None, None
            size: "38dp", "65dp"
            radius: [15,]
            md_bg_color: [0.5, 0.3, 0.9, 1] if root.selected_idx == 3 else [1, 1, 1, 1]
            on_release: root.select_day(3)
            elevation: 1
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: root.days[3]["dow"] if root.days else ""
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: [1,1,1,1] if root.selected_idx == 3 else [0,0,0,0.5]
                MDLabel:
                    text: root.days[3]["day"] if root.days else ""
                    halign: "center"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1,1,1,1] if root.selected_idx == 3 else [0,0,0,1]

        # --- CUMA ---
        MDCard:
            size_hint: None, None
            size: "38dp", "65dp"
            radius: [15,]
            md_bg_color: [0.5, 0.3, 0.9, 1] if root.selected_idx == 4 else [1, 1, 1, 1]
            on_release: root.select_day(4)
            elevation: 1
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: root.days[4]["dow"] if root.days else ""
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: [1,1,1,1] if root.selected_idx == 4 else [0,0,0,0.5]
                MDLabel:
                    text: root.days[4]["day"] if root.days else ""
                    halign: "center"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1,1,1,1] if root.selected_idx == 4 else [0,0,0,1]

        # --- CUMARTESİ ---
        MDCard:
            size_hint: None, None
            size: "38dp", "65dp"
            radius: [15,]
            md_bg_color: [0.5, 0.3, 0.9, 1] if root.selected_idx == 5 else [1, 1, 1, 1]
            on_release: root.select_day(5)
            elevation: 1
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: root.days[5]["dow"] if root.days else ""
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: [1,1,1,1] if root.selected_idx == 5 else [0,0,0,0.5]
                MDLabel:
                    text: root.days[5]["day"] if root.days else ""
                    halign: "center"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1,1,1,1] if root.selected_idx == 5 else [0,0,0,1]

        # --- PAZAR ---
        MDCard:
            size_hint: None, None
            size: "38dp", "65dp"
            radius: [15,]
            md_bg_color: [0.5, 0.3, 0.9, 1] if root.selected_idx == 6 else [1, 1, 1, 1]
            on_release: root.select_day(6)
            elevation: 1
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: root.days[6]["dow"] if root.days else ""
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: [1,1,1,1] if root.selected_idx == 6 else [0,0,0,0.5]
                MDLabel:
                    text: root.days[6]["day"] if root.days else ""
                    halign: "center"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1,1,1,1] if root.selected_idx == 6 else [0,0,0,1]

<SymptomBtn>:
    size_hint: None, None
    size: "100dp", "40dp"
    radius: [20,]
    elevation: 0
    md_bg_color: [1, 1, 1, 1]
    on_release: root.parent.parent.parent.parent.parent.symptom_callback(root.text)
    MDBoxLayout:
        padding: ["10dp", 0]
        spacing: "5dp"
        MDIcon:
            icon: root.icon
            font_size: "18sp"
            theme_text_color: "Custom"
            text_color: [0.5, 0.3, 0.9, 1]
            pos_hint: {"center_y": .5}
        MDLabel:
            text: root.text
            font_size: "10sp"
            bold: True

<MedicineCard>:
    orientation: "vertical"
    size_hint_y: None
    height: "100dp"
    padding: "15dp"
    radius: [20,]
    md_bg_color: root.bg
    MDLabel:
        text: root.time
        bold: True
        theme_text_color: "Custom"
        text_color: [0.2, 0.2, 0.2, 1]
    MDLabel:
        text: root.pill
        font_style: "H6"
        bold: True
        theme_text_color: "Custom"
        text_color: [0.5, 0.3, 0.9, 1]
    MDLabel:
        text: root.note
        font_size: "12sp"
        theme_text_color: "Secondary"

<DashboardEkrani>:
    md_bg_color: 0.97, 0.97, 0.99, 1

    MDBoxLayout:
        orientation: "vertical"
        
        # --- ÜST BAR (Profil ve Logo) ---
        MDBoxLayout:
            size_hint_y: None
            height: "70dp"
            padding: ["20dp", "10dp"]
            spacing: "15dp"
            
            # Profil İkonu
            MDIconButton:
                icon: "account-circle"
                icon_size: "40sp"
                theme_text_color: "Custom"
                text_color: [0.5, 0.3, 0.9, 1]
                on_release: 
                    root.manager.current = "duzenleme"
                    root.manager.transition.direction = "left"

            Widget: # Boşluk

            # Logo
            Image:
                source: "assets/logo_mor.png"
                size_hint: None, None
                size: "40dp", "40dp"
            
            Widget: # Boşluk
            
            # Ayarlar İkonu
            MDIconButton:
                icon: "cog"
                theme_text_color: "Custom"
                text_color: [0.5, 0.5, 0.5, 1]
                on_release: 
                    root.manager.current = "ayarlar"
                    root.manager.transition.direction = "left"

        # --- SCROLL İÇERİK ---
        MDScrollView:
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                padding: ["20dp", "10dp", "20dp", "100dp"] # Altta boşluk (Menü için)
                spacing: "20dp"

                # Tarih
                MDLabel:
                    id: month_label
                    text: "Aralık 2025"
                    font_style: "H5"
                    bold: True
                
                # Takvim
                WeekCalendar:
                    id: week_calendar
                
                # Semptomlar Başlık
                MDLabel:
                    text: "Bugün nasıl hissediyorsun?"
                    bold: True
                
                MDGridLayout:
                    cols: 3
                    adaptive_height: True
                    spacing: "10dp"
                    SymptomBtn:
                        text: "Mutlu"
                        icon: "emoticon-happy-outline"
                    SymptomBtn:
                        text: "Yorgun"
                        icon: "emoticon-confused-outline"
                    SymptomBtn:
                        text: "Enerjik"
                        icon: "lightning-bolt"

                # İlaçlar Başlık
                MDLabel:
                    text: "Sıradaki İlaçlar"
                    bold: True
                
                MedicineCard:
                    time: "09:00"
                    pill: "Levotiron"
                    note: "Aç karnına"
                    bg: [0.9, 0.9, 1, 1]

                MedicineCard:
                    time: "14:00"
                    pill: "Vitamin D"
                    note: "Tok karnına"
                    bg: [1, 0.95, 0.8, 1]

    # --- ALT MENÜ KARTI (Gizli - BURASI DÜZENLENDİ) ---
    MDCard:
        id: menu_card
        size_hint: None, None
        width: "200dp"
        height: "0dp" # Başlangıçta kapalı
        pos_hint: {"x": .2, "y": .13}
        radius: [20, 20, 0, 20]
        md_bg_color: [1, 1, 1, 1]
        elevation: 4
        opacity: 0
        orientation: "vertical"
        padding: "10dp"
        spacing: "10dp"
        
        # 1. BUTON: İLAÇ EKLE
        MDFillRoundFlatButton:
            text: "İlaç Ekle"
            size_hint_x: 1
            md_bg_color: [0.5, 0.3, 0.9, 1]
            on_release: root.menu_action("arti_butonu") # Bu isim Main.py ile uyumlu
        
        # 2. BUTON: ALARM EKLE
        MDFillRoundFlatButton:
            text: "Alarm Ekle"
            size_hint_x: 1
            md_bg_color: [0.5, 0.3, 0.9, 1]
            on_release: root.menu_action("alarm_ekle")
        
        # 3. BUTON: TAHLİL EKLE
        MDFillRoundFlatButton:
            text: "Tahlil Ekle"
            size_hint_x: 1
            md_bg_color: [0.5, 0.3, 0.9, 1]
            on_release: root.menu_action("tahlil_ekle")

    # --- ALT SABİT BAR ---
    MDCard:
        size_hint: 0.9, None
        height: "60dp"
        radius: [30,]
        pos_hint: {"center_x": .5, "bottom": .02}
        md_bg_color: [1, 1, 1, 1]
        elevation: 2
        padding: ["30dp", 0, "100dp", 0] # Sağ tarafı boş bırak (Artı butonu için)
        
        MDIconButton:
            icon: "home"
            theme_text_color: "Custom"
            text_color: [0.5, 0.3, 0.9, 1]
            pos_hint: {"center_y": .5}
        
        Widget: 

        MDIconButton:
            icon: "calendar"
            pos_hint: {"center_y": .5}
            on_release: root.manager.current = "takvim"

    # --- ARTI BUTONU (FAB) ---
    MDFloatingActionButton:
        icon: "plus"
        md_bg_color: [0.5, 0.3, 0.9, 1]
        icon_color: [1, 1, 1, 1]
        pos_hint: {"right": .9, "bottom": .05}
        elevation: 4
        on_release: root.toggle_menu()
'''

Builder.load_string(KV_DASHBOARD)

class DashboardEkrani(MDScreen):
    menu_open = BooleanProperty(False)

    def on_enter(self):
        # Tarihi güncelle
        today = _dt.date.today()
        aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", 
                 "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
        self.ids.month_label.text = f"{aylar[today.month-1]} {today.year}"

    def toggle_menu(self):
        self.menu_open = not self.menu_open
        menu = self.ids.menu_card
        
        if self.menu_open:
            # Burayı dp(190) yaptık ki 3 buton sığsın
            Animation(height=dp(190), opacity=1, d=0.2).start(menu)
        else:
            Animation(height=0, opacity=0, d=0.2).start(menu)

    def menu_action(self, screen_name):
        self.toggle_menu() # Menüyü kapat
        self.manager.current = screen_name # Sayfaya git

    def symptom_callback(self, text):
        print(f"Semptom seçildi: {text}")
        # Buraya veritabanı kayıt kodu eklenebilir