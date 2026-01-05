from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, BooleanProperty, ColorProperty
from datetime import date
import calendar

from database import Database

class DayButton(MDCard, ButtonBehavior):
    day_num = StringProperty()
    selected = BooleanProperty(False)
    is_weekend = BooleanProperty(False)
    status_color = ColorProperty([1, 1, 1, 0])
    tarih = None

class TakvimEkrani(MDScreen):
    menu_open = BooleanProperty(False)
    current_view_date = date.today().replace(day=1)

    def on_enter(self):
        self.db = Database()
        self.secili_tarih = date.today()
        self.takvimi_yenile()
        self.gun_detayi_yukle(self.secili_tarih)

    def ay_degistir(self, yon):
        yeni_ay = self.current_view_date.month + yon
        yeni_yil = self.current_view_date.year
        if yeni_ay > 12:
            yeni_ay = 1
            yeni_yil += 1
        elif yeni_ay < 1:
            yeni_ay = 12
            yeni_yil -= 1
        self.current_view_date = date(yeni_yil, yeni_ay, 1)
        self.takvimi_yenile()

    def takvimi_yenile(self):
        grid = self.ids.calendar_grid
        grid.clear_widgets()
        aylar_tr = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", 
                    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
        self.ids.ay_yil_label.text = f"{aylar_tr[self.current_view_date.month-1]} {self.current_view_date.year}"

        for g in ["Pz", "Sa", "Ça", "Pe", "Cu", "Ct", "Pa"]:
            grid.add_widget(MDLabel(text=g, halign="center", font_style="Caption", theme_text_color="Hint"))

        yil, ay = self.current_view_date.year, self.current_view_date.month
        ilk_gun, gun_sayisi = calendar.monthrange(yil, ay)
        bugun = date.today()

        for _ in range(ilk_gun):
            grid.add_widget(MDLabel(text=""))

        for gun in range(1, gun_sayisi + 1):
            tarih = date(yil, ay, gun)
            tarih_str = tarih.strftime('%Y-%m-%d')
            
            bg_renk = [1, 1, 1, 0] # Varsayılan: Gri/Şeffaf

            # Sadece BUGÜN ve GEÇMİŞ günleri, kullanıcı girişine göre renklendir
            if tarih <= bugun:
                ikon_data = self.db.gun_ikonunu_hesapla(tarih_str)
                if ikon_data["status"] == "ALL_TAKEN":
                    bg_renk = [0.2, 0.8, 0.2, 0.4] # Yeşil (Alındı)
                elif ikon_data["status"] in ["NONE_TAKEN", "PARTIAL"]:
                    bg_renk = [0.8, 0.2, 0.2, 0.4] # Kırmızı (Atlandı/Eksik)
            
            btn = DayButton(
                day_num=str(gun),
                selected=(tarih == self.secili_tarih),
                status_color=bg_renk,
                is_weekend=(tarih.weekday() >= 5)
            )
            btn.tarih = tarih
            btn.bind(on_release=lambda x, t=tarih: self.gun_sec(t))
            grid.add_widget(btn)

    def gun_sec(self, tarih):
        self.secili_tarih = tarih
        self.takvimi_yenile()
        self.gun_detayi_yukle(tarih)

    def gun_detayi_yukle(self, tarih):
        box = self.ids.ilac_listesi
        box.clear_widgets()
        kartlar = self.db.dashboard_kartlarini_getir(tarih.strftime('%Y-%m-%d'))
        
        for k in kartlar:
            bg = [0.88, 0.94, 0.75, 1] if k["taken"] else [1, 0.9, 0.9, 1]
            card = MDCard(
                orientation="vertical", 
                adaptive_height=True, 
                padding="20dp", 
                radius=[30], 
                md_bg_color=bg, 
                spacing="10dp", 
                elevation=0
            )
            card.add_widget(MDLabel(text=k["ilac_adi"], bold=True, font_style="H6"))
            card.add_widget(MDLabel(text=tarih.strftime("%d/%m/%Y"), font_style="Caption", theme_text_color="Secondary"))
            
            # Görseldeki alt kutucuklar (doz, adet, gün)
            row = Builder.load_string(f'''
MDBoxLayout:
    spacing: "10dp"
    size_hint_y: None
    height: "40dp"
    MDCard:
        radius: [15]
        md_bg_color: 1, 1, 1, 1
        padding: ["10dp", 0]
        MDLabel:
            text: "{k['doz']}"
            font_style: "Caption"
            halign: "center"
        MDIcon:
            icon: "chevron-down"
            font_size: "16sp"
            pos_hint: {{"center_y": .5}}
    MDCard:
        radius: [15]
        md_bg_color: 1, 1, 1, 1
        padding: ["10dp", 0]
        MDLabel:
            text: "adet"
            font_style: "Caption"
            halign: "center"
    MDCard:
        radius: [15]
        md_bg_color: 1, 1, 1, 1
        padding: ["10dp", 0]
        MDLabel:
            text: "gün"
            font_style: "Caption"
            halign: "center"
''')
            card.add_widget(row)
            box.add_widget(card)

    def toggle_menu(self):
        self.menu_open = not self.menu_open
        self.ids.menu_card.opacity = 1 if self.menu_open else 0
        self.ids.menu_card.disabled = not self.menu_open

Builder.load_string("""
<DayButton>:
    orientation: "vertical"
    size_hint: None, None
    size: "42dp", "55dp"
    radius: [12]
    md_bg_color: (0.5, 0.3, 0.9, 1) if self.selected else root.status_color
    padding: "2dp"
    MDLabel:
        text: root.day_num
        halign: "center"
        font_style: "Button"
        bold: True
        theme_text_color: "Custom"
        text_color: (1, 1, 1, 1) if root.selected else ((0.8, 0.1, 0.1, 1) if root.is_weekend else (0, 0, 0, 0.7))

<TakvimEkrani>:
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        
        MDBoxLayout:
            orientation: "vertical"
            pos_hint: {"top": 1}
            
            MDBoxLayout:
                size_hint_y: None
                height: "65dp"
                padding: ["15dp", "5dp"]
                MDIconButton:
                    icon: "account-circle"
                Widget:
                Image:
                    source: "assets/logo_mor.png"
                    size_hint: None, None
                    size: "45dp", "45dp"
                Widget:
                MDIconButton:
                    icon: "cog"
                    on_release: root.manager.current = "ayarlar"

            MDBoxLayout:
                size_hint_y: None
                height: "50dp"
                padding: ["20dp", 0]
                MDIconButton:
                    icon: "chevron-left"
                    on_release: root.ay_degistir(-1)
                MDLabel:
                    id: ay_yil_label
                    halign: "center"
                    bold: True
                    font_style: "H6"
                MDIconButton:
                    icon: "chevron-right"
                    on_release: root.ay_degistir(1)

            MDCard:
                size_hint: 0.92, None
                height: "300dp"
                pos_hint: {"center_x": .5}
                radius: [25]
                md_bg_color: 0.96, 0.96, 0.98, 1
                elevation: 0
                MDGridLayout:
                    id: calendar_grid
                    cols: 7
                    padding: "10dp"
                    spacing: "2dp"

            MDLabel:
                text: "İlaç Takibi"
                bold: True
                padding: ["25dp", "15dp"]
                adaptive_height: True

            ScrollView:
                MDBoxLayout:
                    id: ilac_listesi
                    orientation: "vertical"
                    adaptive_height: True
                    padding: ["20dp", "10dp", "20dp", "120dp"]
                    spacing: "15dp"

        # ALT NAVİGASYON BARI
        MDCard:
            size_hint: 0.95, None
            height: "70dp"
            pos_hint: {"center_x": .5, "center_y": .06}
            radius: [35]
            md_bg_color: 1, 1, 1, 1
            elevation: 3
            MDBoxLayout:
                padding: ["20dp", 0, "130dp", 0]
                MDIconButton:
                    icon: "home-outline"
                    on_release: root.manager.current = "dashboard"
                MDIconButton:
                    icon: "calendar-month"
                    icon_color: 0.5, 0.3, 0.9, 1
                    theme_icon_color: "Custom"
                MDIconButton:
                    icon: "chart-line"
                    on_release: root.manager.current = "grafik"

        # EN ÜST KATMAN: ARTI MENÜ VE BUTON
        MDCard:
            id: menu_card
            size_hint: None, None
            width: "180dp"
            height: "110dp"
            pos_hint: {"right": .85, "y": .12}
            radius: [20, 20, 5, 20]
            opacity: 0
            disabled: True
            md_bg_color: 1, 1, 1, 1
            elevation: 8
            MDBoxLayout:
                orientation: "vertical"
                padding: "10dp"
                MDFlatButton:
                    text: "İlaç Ekle"
                    size_hint_x: 1
                    on_release: root.manager.current = "arti_butonu"
                MDFlatButton:
                    text: "Tahlil Ekle"
                    size_hint_x: 1

        MDIconButton:
            icon: "plus"
            md_bg_color: 0.5, 0.3, 0.9, 1
            theme_icon_color: "Custom"
            icon_color: 1, 1, 1, 1
            pos_hint: {"center_x": .82, "center_y": .09}
            size_hint: None, None
            size: "75dp", "75dp"
            elevation: 10
            on_release: root.toggle_menu()
""")

