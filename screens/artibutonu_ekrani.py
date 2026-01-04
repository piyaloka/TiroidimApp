import sys
import os
#kodunuzda hata çıkmaması için
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDTimePicker
from kivy.lang import Builder
from kivy.metrics import dp
from datetime import datetime
from database import Database

# --- KV TASARIMI ---
# Bu string dosya import edildiğinde SADECE BİR KEZ yüklenecek.
kv_str = """
<CustomInput@MDBoxLayout>:
    orientation: 'vertical'
    adaptive_height: True
    spacing: dp(8)
    label: ""
    text_val: ""
    readonly: True
    input_filter: None
    MDLabel:
        text: root.label
        font_style: "Caption"
        theme_text_color: "Secondary"
        padding: [dp(12), dp(4)]
    MDTextField:
        id: text_field
        text: root.text_val
        mode: "fill"
        fill_color_normal: 0.96, 0.96, 0.98, 1
        radius: [15, 15, 15, 15]
        active_line: False
        readonly: root.readonly
        input_filter: root.input_filter
        hint_text: ""
        on_focus: if self.focus and self.text in ["0", "00:00", "Seçiniz", "GG/AA/YYYY", "Değer girin", "0.00", "Birim"]: self.text = ""

<ArtiButonuEkrani>:
    name: "arti_butonu"
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        MDCard:
            size_hint: .88, .8
            pos_hint: {"center_x": .5, "center_y": .5}
            radius: [60, 60, 10, 80]
            padding: dp(25)
            orientation: "vertical"
            spacing: dp(12)
            elevation: 0
            
            MDLabel:
                text: "İlaç Ekle"
                halign: "center"
                font_style: "H5"
                theme_text_color: "Custom"
                text_color: 0.5, 0.2, 0.9, 1
                adaptive_height: True
            
            CustomInput:
                id: i_name
                label: "İlacınızı seçiniz"
                text_val: "Seçiniz"
                on_touch_down: if self.collide_point(*args[1].pos): root.open_ilac_menu()
            
            CustomInput:
                id: i_doz
                label: "İlaç dozunu seçiniz"
                text_val: "Seçiniz"
                on_touch_down: if self.collide_point(*args[1].pos): root.open_doz_menu()
            
            CustomInput:
                id: i_date
                label: "İlacınızı ne zaman aldınız?"
                text_val: "GG/AA/YYYY"
                on_touch_down: if self.collide_point(*args[1].pos): root.start_date_selection()
            
            MDBoxLayout:
                adaptive_height: True
                spacing: 15
                padding: [0, 20, 0, 0]
                MDRaisedButton:
                    text: "İptal et"
                    size_hint_x: .5
                    md_bg_color: 0.6, 0.4, 0.8, 1
                    on_release: root.manager.current = "dashboard" 
                MDRaisedButton:
                    text: "Kaydet"
                    md_bg_color: 0.5, 0.2, 0.9, 1
                    size_hint_x: .5
                    on_release: root.kaydet()

<AlarmEkrani>:
    name: "alarm_ekle"
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        MDCard:
            size_hint: .88, .85
            pos_hint: {"center_x": .5, "center_y": .5}
            radius: [60, 60, 10, 80]
            padding: dp(20)
            orientation: "vertical"
            spacing: dp(8)
            elevation: 0
            
            MDLabel:
                text: "Alarm Ekle"
                halign: "center"
                font_style: "H5"
                theme_text_color: "Custom"
                text_color: 0.5, 0.2, 0.9, 1
                adaptive_height: True

            CustomInput:
                id: a_name
                label: "İlacınızı seçiniz"
                text_val: "Seçiniz"
                on_touch_down: if self.collide_point(*args[1].pos): root.open_ilac_menu()
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                spacing: dp(12)
                MDLabel:
                    text: "Kaç adet ve kaç gün alacaksınız?"
                    font_style: "Caption"
                    theme_text_color: "Secondary"
                    padding: [dp(12), dp(4)]
                MDBoxLayout:
                    adaptive_height: True
                    spacing: 10
                    CustomInput:
                        id: a_adet
                        label: "Adet"
                        text_val: "0"
                        readonly: False
                        input_filter: "int"
                    CustomInput:
                        id: a_gun
                        label: "Gün"
                        text_val: "0"
                        readonly: False
                        input_filter: "int"
            CustomInput:
                id: a_vakit_durum
                label: "Gün içerisinde?"
                text_val: "Seçiniz"
                on_touch_down: if self.collide_point(*args[1].pos): root.open_time_picker()

            CustomInput:
                id: a_time_full
                label: "Bildirim"
                text_val: "00:00"
                on_touch_down: if self.collide_point(*args[1].pos): root.open_period_menu()

            MDBoxLayout:
                adaptive_height: True
                spacing: 15
                padding: [0, 20, 0, 0]
                MDRaisedButton:
                    text: "İptal et"
                    size_hint_x: .5
                    md_bg_color: 0.6, 0.4, 0.8, 1
                    on_release: root.manager.current = "dashboard" 
                MDRaisedButton:
                    text: "Kaydet"
                    md_bg_color: 0.5, 0.2, 0.9, 1
                    size_hint_x: .5
                    on_release: root.kaydet()

<TahlilEkrani>:
    name: "tahlil_ekle"
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        MDCard:
            size_hint: .88, .92
            pos_hint: {"center_x": .5, "center_y": .5}
            radius: [60, 60, 10, 80]
            padding: dp(20)
            orientation: "vertical"
            spacing: dp(8)
            elevation: 0
            
            MDLabel:
                text: "Tahlil Ekle"
                halign: "center"
                font_style: "H5"
                theme_text_color: "Custom"
                text_color: 0.5, 0.2, 0.9, 1
                adaptive_height: True

            CustomInput:
                id: t_name
                label: "Tahlil Seçiniz"
                text_val: "Seçiniz"
                on_touch_down: if self.collide_point(*args[1].pos): root.open_tahlil_menu()

            MDBoxLayout:
                spacing: dp(10)
                adaptive_height: True
                CustomInput:
                    id: t_val
                    label: "Tahlil Değerini Giriniz"
                    text_val: "Değer girin"
                    readonly: False 
                    input_filter: "float"
                    size_hint_x: .6
                CustomInput:
                    id: t_unit
                    label: "Birim"
                    text_val: "Birim"
                    size_hint_x: .4
                    on_touch_down: if self.collide_point(*args[1].pos): root.open_birim_menu()

            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                spacing: dp(12)
                MDLabel:
                    text: "Kaç adet ve kaç gün alacaksınız?"
                    font_style: "Caption"
                    theme_text_color: "Secondary"
                    padding: [dp(12), dp(4)]
                MDBoxLayout:
                    adaptive_height: True
                    spacing: 10
                    CustomInput:
                        id: t_adet
                        label: "Adet"
                        text_val: "0"
                        readonly: False
                        input_filter: "float"
                    CustomInput:
                        id: t_gun
                        label: "Gün"
                        text_val: "0"
                        readonly: False
                        input_filter: "float"
            CustomInput:
                id: t_date
                label: "Tahlili Ne Zaman Yaptırdınız?"
                text_val: "GG/AA/YYYY"
                on_touch_down: if self.collide_point(*args[1].pos): root.start_date_selection()

            MDBoxLayout:
                adaptive_height: True
                spacing: 15
                padding: [0, dp(10), 0, 0]
                MDRaisedButton:
                    text: "İptal"
                    size_hint_x: .5
                    md_bg_color: 0.6, 0.4, 0.8, 1
                    on_release: root.manager.current = "dashboard" 
                MDRaisedButton:
                    text: "Kaydet"
                    md_bg_color: 0.5, 0.2, 0.9, 1
                    size_hint_x: .5
                    on_release: root.kaydet()
"""

# --- ÖNEMLİ DÜZELTME: Builder burada çalışmalı ---
Builder.load_string(kv_str)

# --- ORTAK FONKSİYONLAR İÇİN BASE CLASS ---
class BaseMenuScreen(MDScreen):
    db = None
    menu = None
    
    # Tarih seçimi için ortak listeler
    saatler = [str(i).zfill(2) for i in range(24)]
    dakikalar = [str(i).zfill(2) for i in range(60)]
    gunler = [str(i).zfill(2) for i in range(1, 32)]
    aylar = [str(i).zfill(2) for i in range(1, 13)]
    current_year = datetime.now().year
    yillar = [str(i) for i in range(current_year, 2000, -1)]
    temp_day = "01"
    temp_month = "01"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

    def open_dropdown(self, caller, items, callback):
        self.menu = MDDropdownMenu(
            caller=caller,
            items=[{"viewclass": "OneLineListItem", "text": i, "on_release": lambda x=i: callback(x, caller)} for i in items],
            width_mult=3,
            max_height=dp(240),
            radius=[15, 15, 15, 15],
        )
        self.menu.open()

    def set_val(self, text, caller):
        caller.text = text
        if self.menu: self.menu.dismiss()

    # Ortak Tarih Seçimi
    def start_date_selection(self):
        # Eğer bu sınıfın bir t_date veya i_date id'si varsa onu kullanır
        caller = self.ids.get("t_date") or self.ids.get("i_date")
        if caller:
            self.open_dropdown(caller.ids.text_field, self.gunler, self.select_day)

    def select_day(self, day, caller):
        self.temp_day = day
        self.menu.dismiss()
        self.open_dropdown(caller, self.aylar, self.select_month)

    def select_month(self, month, caller):
        self.temp_month = month
        self.menu.dismiss()
        self.open_dropdown(caller, self.yillar, self.complete_date_selection)

    def complete_date_selection(self, year, caller):
        caller.text = f"{self.temp_day}/{self.temp_month}/{year}"
        self.menu.dismiss()


# --- 1. SINIF: İLAÇ EKLEME ---
class ArtiButonuEkrani(BaseMenuScreen):
    def open_ilac_menu(self):
        ilac_listesi = self.db.master_ilac_listesi_getir() or ["İlaç Bulunamadı"]
        self.open_dropdown(self.ids.i_name.ids.text_field, ilac_listesi, self.set_val)

    def open_doz_menu(self):
        dozlar = ["25mcg", "50mcg", "75mcg", "100mcg", "125mcg", "150mcg", "200mcg"]
        self.open_dropdown(self.ids.i_doz.ids.text_field, dozlar, self.set_val)

    def kaydet(self):
        ad = self.ids.i_name.ids.text_field.text.split(' - ')[0]
        doz = self.ids.i_doz.ids.text_field.text
        if ad != "Seçiniz" and doz != "Seçiniz":
            self.db.kullanici_ilaci_ekle(ad, doz, "09:00", "Her Gün")
            print(f"İlaç Kaydedildi: {ad}")
            self.manager.current = "dashboard"

# --- 2. SINIF: ALARM EKLEME ---
class AlarmEkrani(BaseMenuScreen):
    def open_ilac_menu(self):
        # Kullanıcının eklediği ilaçları listele
        ilaclar = self.db.kullanici_ilaclarini_getir() # [(id, ad, doz...), ...]
        if not ilaclar:
            liste = ["Önce İlaç Ekleyin"]
        else:
            liste = [f"{i[1]} ({i[2]})" for i in ilaclar]
        
        self.open_dropdown(self.ids.a_name.ids.text_field, liste, self.set_val)

    def open_time_picker(self):
        options = ["Sabah / Aç", "Sabah / Tok", "Öğle / Aç", "Öğle / Tok", "Akşam / Aç", "Akşam / Tok"]
        self.open_dropdown(self.ids.a_vakit_durum.ids.text_field, options, self.set_val)
    
    def open_period_menu(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.on_time_save)
        time_dialog.open()
    
    def on_time_save(self, instance, time):
        # Saati string formatına çevir (09:05 gibi)
        saat_str = time.strftime("%H:%M")
        self.ids.a_time_full.ids.text_field.text = saat_str

    def kaydet(self):
        ilac = self.ids.a_name.ids.text_field.text
        adet = self.ids.a_adet.ids.text_field.text
        gun = self.ids.a_gun.ids.text_field.text
        vakit = self.ids.a_vakit_durum.ids.text_field.text
        saat = self.ids.a_time_full.ids.text_field.text
        
        if ilac in ["Seçiniz", "Önce İlaç Ekleyin"]:
            print("Hata: İlaç seçilmedi")
            return
            
        print(f"Kaydediliyor: {ilac}, {adet} Adet, {gun} Gün, Vakit: {vakit}, Saat: {saat}")
        self.manager.current = "dashboard" 


# --- 3. SINIF: TAHLİL EKLEME ---
class TahlilEkrani(BaseMenuScreen):
    _last_len = 0  

    def on_enter(self, *args):
        self.ids.t_val.ids.text_field.bind(text=self.auto_dot)

    def auto_dot(self, instance, value):
        curr_len = len(value)
        if curr_len < self._last_len:
            self._last_len = curr_len
            return

        raw_val = value.replace('.', '')
        if len(raw_val) >= 2 and '.' not in value:
            new_text = f"{raw_val[0]}.{raw_val[1:]}"
            instance.text = new_text
            # İmleci sona taşı
            instance.cursor = (len(new_text), 0)

        self._last_len = len(instance.text)

    def open_tahlil_menu(self):
        tahliller = ["TSH", "Serbest T3", "Serbest T4", "Anti-TPO"]
        self.open_dropdown(self.ids.t_name.ids.text_field, tahliller, self.select_tahlil_and_unit)
    
    def select_tahlil_and_unit(self, tahlil_ad, caller):
        caller.text = tahlil_ad
        if tahlil_ad == "TSH":
            self.ids.t_unit.ids.text_field.text = "mIU/L"
        elif "T3" in tahlil_ad or "T4" in tahlil_ad:
            self.ids.t_unit.ids.text_field.text = "ng/dL"
        else:
            self.ids.t_unit.ids.text_field.text = "IU/mL"
        
        if self.menu:
            self.menu.dismiss()

    def open_birim_menu(self):
        birimler = ["mIU/L", "ng/dL", "pg/mL", "pmol/L", "IU/mL"]
        self.open_dropdown(self.ids.t_unit.ids.text_field, birimler, self.set_val)

    def kaydet(self):
        ad = self.ids.t_name.ids.text_field.text
        deger = self.ids.t_val.ids.text_field.text
        birim = self.ids.t_unit.ids.text_field.text
        tarih = self.ids.t_date.ids.text_field.text
    
        if ad == "Seçiniz" or deger in ["", "Değer girin"]:
            print("Lütfen tahlil adı ve değerini kontrol edin!")
            return
        
        print(f"Tahlil Kaydedildi: {ad} - {deger} {birim} - Tarih: {tarih}")
        self.manager.current = "dashboard"


