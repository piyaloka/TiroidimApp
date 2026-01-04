from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty
from kivymd.uix.card import MDCard
from kivy.config import Config
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.factory import Factory

import datetime as _dt
import calendar as _cal

Config.set('graphics', 'maxfps', '60')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

Window.size = (360, 740)


class WeekCalendar(MDCard):
    # List of 7 dicts: {"dow": "P", "day": "30", "is_weekend": bool}
    days = ListProperty([])
    month_label = StringProperty("")
    selected_idx = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sync_today()

    def _tr_dow(self, weekday: int) -> str:
        # Monday=0 .. Sunday=6
        return ["P", "S", "Ç", "P", "C", "C", "P"][weekday]

    def _month_name_tr(self, month: int) -> str:
        return [
            "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
            "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık",
        ][month - 1]

    def _rebuild(self):
        days = []
        for i in range(7):
            d = self._start_date + _dt.timedelta(days=i)
            days.append({
                "dow": self._tr_dow(d.weekday()),
                "day": f"{d.day:02d}",
                "is_weekend": d.weekday() >= 5,
            })
        self.days = days

        # keep selection inside 0..6
        if self.selected_idx < 0 or self.selected_idx > 6:
            self.selected_idx = 0
        self._update_month_label()

    def _update_month_label(self):
        selected_date = self._start_date + _dt.timedelta(days=self.selected_idx)
        self.month_label = f"{self._month_name_tr(selected_date.month)} {selected_date.year}"

    def sync_today(self):
        today = _dt.date.today()
        self._start_date = today - _dt.timedelta(days=today.weekday())
        self.selected_idx = today.weekday()
        self._rebuild()

    def prev_week(self):
        self._start_date = self._start_date - _dt.timedelta(days=7)
        self._rebuild()

    def next_week(self):
        self._start_date = self._start_date + _dt.timedelta(days=7)
        self._rebuild()

    def select_day(self, idx: int):
        self.selected_idx = idx
        self._update_month_label()

    def get_selected_date(self):
        return self._start_date + _dt.timedelta(days=self.selected_idx)


class SymptomBtn(MDCard):
    text = StringProperty()
    icon = StringProperty()
    group = StringProperty("")
    selected = BooleanProperty(False)

    def toggle_selected(self):
        self.selected = not self.selected


class ActionBtn(MDCard):
    text = StringProperty()
    bg = ListProperty([1, 1, 1, 1])
    text_color = ListProperty([0, 0, 0, 1])
    selected = BooleanProperty(False)
    selected_bg = ListProperty([1, 1, 1, 1])
    selected_text_color = ListProperty([0, 0, 0, 1])


class MedicineCard(MDCard):
    time = StringProperty()
    pill = StringProperty()
    note = StringProperty()
    bg = ListProperty([1, 1, 1, 1])
    btn_color = ListProperty([1, 1, 1, 1])
    medicine_id = StringProperty("")
    selected_action = StringProperty("")

    def select_action(self, action: str):
        self.selected_action = action


KV = '''
<WeekCalendar>:
    size_hint_y: None
    height: "112dp"
    radius: [28,]
    elevation: 0
    md_bg_color: [1, 1, 1, 1]
    padding: ["7dp", "12dp", "7dp", "10dp"]

    MDBoxLayout:
        orientation: "vertical"
        spacing: "10dp"

        # HAFTA: günler (harf + sayı tek hap içinde)
        MDGridLayout:
            cols: 7
            adaptive_height: True
            spacing: "8dp"

            # 0
            MDCard:
                size_hint: None, None
                size: "38dp", "70dp"
                radius: [20,]
                elevation: 0
                md_bg_color: ([0.78, 0.72, 0.95, 1] if root.selected_idx == 0 else [1, 1, 1, 1])
                ripple_behavior: True
                ripple_color: [0.5, 0.3, 0.9, 0.18]
                on_release: root.select_day(0)
                MDBoxLayout:
                    orientation: "vertical"
                    padding: [0, "8dp", 0, "8dp"]
                    spacing: "6dp"
                    MDLabel:
                        text: root.days[0]["dow"] if root.days else ""
                        halign: "center"
                        font_size: "10sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: ([0.2, 0.1, 0.35, 1] if root.selected_idx == 0 else [0, 0, 0, 0.55])
                    MDLabel:
                        text: root.days[0]["day"] if root.days else ""
                        halign: "center"
                        font_size: "12sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: ([0.2, 0.1, 0.35, 1] if root.selected_idx == 0 else ([0.85, 0.2, 0.2, 1] if (root.days and root.days[0]["is_weekend"]) else [0, 0, 0, 0.75]))

            # 1
            MDCard:
                size_hint: None, None
                size: "38dp", "70dp"
                radius: [20,]
                elevation: 0
                md_bg_color: ([0.78, 0.72, 0.95, 1] if root.selected_idx == 1 else [1, 1, 1, 1])
                ripple_behavior: True
                ripple_color: [0.5, 0.3, 0.9, 0.18]
                on_release: root.select_day(1)
                MDBoxLayout:
                    orientation: "vertical"
                    padding: [0, "8dp", 0, "8dp"]
                    spacing: "6dp"
                    MDLabel:
                        text: root.days[1]["dow"] if root.days else ""
                        halign: "center"
                        font_size: "10sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: ([0.2, 0.1, 0.35, 1] if root.selected_idx == 1 else [0, 0, 0, 0.55])
                    MDLabel:
                        text: root.days[1]["day"] if root.days else ""
                        halign: "center"
                        font_size: "12sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: ([0.2, 0.1, 0.35, 1] if root.selected_idx == 1 else ([0.85, 0.2, 0.2, 1] if (root.days and root.days[1]["is_weekend"]) else [0, 0, 0, 0.75]))

            # 2
            MDCard:
                size_hint: None, None
                size: "38dp", "70dp"
                radius: [20,]
                elevation: 0
                md_bg_color: ([0.78, 0.72, 0.95, 1] if root.selected_idx == 2 else [1, 1, 1, 1])
                ripple_behavior: True
                ripple_color: [0.5, 0.3, 0.9, 0.18]
                on_release: root.select_day(2)
                MDBoxLayout:
                    orientation: "vertical"
                    padding: [0, "8dp", 0, "8dp"]
                    spacing: "6dp"
                    MDLabel:
                        text: root.days[2]["dow"] if root.days else ""
                        halign: "center"
                        font_size: "10sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: ([0.2, 0.1, 0.35, 1] if root.selected_idx == 2 else [0, 0, 0, 0.55])
                    MDLabel:
                        text: root.days[2]["day"] if root.days else ""
                        halign: "center"
                        font_size: "12sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: ([0.2, 0.1, 0.35, 1] if root.selected_idx == 2 else ([0.85, 0.2, 0.2, 1] if (root.days and root.days[2]["is_weekend"]) else [0, 0, 0, 0.75]))

            # 3
            MDCard:
                size_hint: None, None
                size: "38dp", "70dp"
                radius: [20,]
                elevation: 0
                md_bg_color: ([0.78, 0.72, 0.95, 1] if root.selected_idx == 3 else [1, 1, 1, 1])
                ripple_behavior: True
                ripple_color: [0.5, 0.3, 0.9, 0.18]
                on_release: root.select_day(3)
                MDBoxLayout:
                    orientation: "vertical"
                    padding: [0, "8dp", 0, "8dp"]
                    spacing: "6dp"
                    MDLabel:
                        text: root.days[3]["dow"] if root.days else ""
                        halign: "center"
                        font_size: "10sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: ([0.2, 0.1, 0.35, 1] if root.selected_idx == 3 else [0, 0, 0, 0.55])
                    MDLabel:
                        text: root.days[3]["day"] if root.days else ""
                        halign: "center"
                        font_size: "12sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: ([0.2, 0.1, 0.35, 1] if root.selected_idx == 3 else ([0.85, 0.2, 0.2, 1] if (root.days and root.days[3]["is_weekend"]) else [0, 0, 0, 0.75]))

            # 4
            MDCard:
                size_hint: None, None
                size: "38dp", "70dp"
                radius: [20,]
                elevation: 0
                md_bg_color: ([0.78, 0.72, 0.95, 1] if root.selected_idx == 4 else [1, 1, 1, 1])
                ripple_behavior: True
                ripple_color: [0.5, 0.3, 0.9, 0.18]
                on_release: root.select_day(4)
                MDBoxLayout:
                    orientation: "vertical"
                    padding: [0, "8dp", 0, "8dp"]
                    spacing: "6dp"
                    MDLabel:
                        text: root.days[4]["dow"] if root.days else ""
                        halign: "center"
                        font_size: "10sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: ([0.2, 0.1, 0.35, 1] if root.selected_idx == 4 else [0, 0, 0, 0.55])
                    MDLabel:
                        text: root.days[4]["day"] if root.days else ""
                        halign: "center"
                        font_size: "12sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: ([0.2, 0.1, 0.35, 1] if root.selected_idx == 4 else ([0.85, 0.2, 0.2, 1] if (root.days and root.days[4]["is_weekend"]) else [0, 0, 0, 0.75]))

            # 5
            MDCard:
                size_hint: None, None
                size: "38dp", "70dp"
                radius: [20,]
                elevation: 0
                md_bg_color: ([0.78, 0.72, 0.95, 1] if root.selected_idx == 5 else [1, 1, 1, 1])
                ripple_behavior: True
                ripple_color: [0.5, 0.3, 0.9, 0.18]
                on_release: root.select_day(5)
                MDBoxLayout:
                    orientation: "vertical"
                    padding: [0, "8dp", 0, "8dp"]
                    spacing: "6dp"
                    MDLabel:
                        text: root.days[5]["dow"] if root.days else ""
                        halign: "center"
                        font_size: "10sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: ([0.2, 0.1, 0.35, 1] if root.selected_idx == 5 else [0, 0, 0, 0.55])
                    MDLabel:
                        text: root.days[5]["day"] if root.days else ""
                        halign: "center"
                        font_size: "12sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: ([0.2, 0.1, 0.35, 1] if root.selected_idx == 5 else ([0.85, 0.2, 0.2, 1] if (root.days and root.days[5]["is_weekend"]) else [0, 0, 0, 0.75]))

            # 6
            MDCard:
                size_hint: None, None
                size: "38dp", "70dp"
                radius: [20,]
                elevation: 0
                md_bg_color: ([0.78, 0.72, 0.95, 1] if root.selected_idx == 6 else [1, 1, 1, 1])
                ripple_behavior: True
                ripple_color: [0.5, 0.3, 0.9, 0.18]
                on_release: root.select_day(6)
                MDBoxLayout:
                    orientation: "vertical"
                    padding: [0, "8dp", 0, "8dp"]
                    spacing: "6dp"
                    MDLabel:
                        text: root.days[6]["dow"] if root.days else ""
                        halign: "center"
                        font_size: "10sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: ([0.2, 0.1, 0.35, 1] if root.selected_idx == 6 else [0, 0, 0, 0.55])
                    MDLabel:
                        text: root.days[6]["day"] if root.days else ""
                        halign: "center"
                        font_size: "12sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: ([0.2, 0.1, 0.35, 1] if root.selected_idx == 6 else ([0.85, 0.2, 0.2, 1] if (root.days and root.days[6]["is_weekend"]) else [0, 0, 0, 0.75]))

        # İnce çizgi göstergesi
        MDAnchorLayout:
            size_hint_y: None
            height: "12dp"
            padding: [0, "2dp", 0, 0]
            anchor_x: "center"
            anchor_y: "center"
            MDCard:
                size_hint: None, None
                size: "72dp", "2dp"
                radius: [1,]
                elevation: 0
                md_bg_color: [0.5, 0.3, 0.9, 0.25]
<SymptomBtn>:
    size_hint: None, None
    size: "105dp", "40dp"
    radius: [20,]
    elevation: 0
    md_bg_color: ([0.78, 0.72, 0.95, 1] if root.selected else [0.96, 0.96, 0.98, 1])
    ripple_behavior: True
    ripple_color: [0.5, 0.3, 0.9, 0.18]
    on_release:
        app.toggle_symptom(root)
    MDBoxLayout:
        padding: ["10dp", 0]
        spacing: "5dp"
        MDIcon:
            icon: root.icon
            font_size: "18sp"
            theme_text_color: "Custom"
            text_color: ([0.25, 0.12, 0.5, 1] if root.selected else [0.5, 0.3, 0.9, 1])
            pos_hint: {"center_y": .5}
        MDLabel:
            text: root.text
            font_size: "10sp"
            bold: True
            theme_text_color: "Custom"
            text_color: ([0.25, 0.12, 0.5, 1] if root.selected else [0, 0, 0, 0.8])

<ActionBtn>:
    size_hint: None, None
    size: "65dp", "38dp"
    radius: [18,]
    elevation: 0
    md_bg_color: (root.selected_bg if root.selected else root.bg)
    ripple_behavior: True
    ripple_color: [0.2, 0.2, 0.2, 0.15]
    MDLabel:
        text: root.text
        halign: "center"
        font_size: "10sp"
        bold: True
        theme_text_color: "Custom"
        text_color: (root.selected_text_color if root.selected else root.text_color)

<MedicineCard>:
    orientation: "vertical"
    size_hint_y: None
    height: "140dp"
    size_hint_x: 1
    pos_hint: {"center_x": .5}
    padding: ["16dp", "10dp"]
    radius: [25,]
    elevation: 0
    md_bg_color: root.bg

    MDBoxLayout:
        orientation: "vertical"
        size_hint_y: None
        height: "55dp"
        spacing: "2dp"
        
        MDLabel:
            text: root.time
            bold: True
            font_style: "H6"
            font_size: "18sp"
            size_hint_y: None
            height: "26dp"
            theme_text_color: "Custom"
            text_color: [0, 0, 0, 0.9]

        MDLabel:
            text: root.pill
            font_size: "15sp"
            bold: True
            size_hint_y: None
            height: "22dp"
            theme_text_color: "Custom"
            text_color: [0, 0, 0, 0.7]

    Widget:

    MDBoxLayout:
        spacing: "8dp"
        size_hint_y: None
        height: "38dp"
        
        ActionBtn:
            text: "Aldım"
            bg: [1, 1, 1, 1]
            text_color: [0.6, 0.6, 0.6, 1]
            selected: root.selected_action == "taken"
            selected_bg: [0.55, 0.8, 0.6, 1]
            selected_text_color: [1, 1, 1, 1]
            on_release:
                app.record_medicine_action(root, "taken")

        ActionBtn:
            text: "Atladım"
            bg: [1, 1, 1, 1]
            text_color: [0.6, 0.6, 0.6, 1]
            selected: root.selected_action == "skipped"
            selected_bg: root.btn_color
            selected_text_color: [1, 1, 1, 1]
            on_release:
                app.record_medicine_action(root, "skipped")

        MDCard:
            radius: [18,]
            md_bg_color: [1, 1, 1, 0.5]
            elevation: 0
            padding: ["10dp", 0]
            MDBoxLayout:
                MDLabel:
                    text: root.note
                    font_size: "9sp"
                    bold: True
                MDIcon:
                    icon: "chevron-down"
                    font_size: "16sp"
                    pos_hint: {"center_y": .5}

MDScreen:
    md_bg_color: [1, 1, 1, 1]

    MDBoxLayout:
        orientation: "vertical"
    
        MDBoxLayout:
            size_hint_y: None
            height: "70dp"
            padding: ["18dp", "8dp", "20dp", "8dp"]
            spacing: "6dp"
            MDIconButton:
                icon: "account-circle"
            Widget:
            Image:
                source: "logo_mor.png"
                size_hint: None, None
                size: "45dp", "45dp"
                allow_stretch: True
                keep_ratio: True
            Widget:
            MDIconButton:
                icon: "cog"
                on_release: app.open_settings()

        MDScrollView:
            bar_width: 0
            effect_cls: "ScrollEffect"
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                padding: ["18dp", "18dp", "20dp", "125dp"]
                spacing: "20dp"

                MDLabel:
                    text: root.ids.week_cal.month_label
                    bold: True
                    font_style: "H6"
                
                WeekCalendar:
                    id: week_cal
                    size_hint_x: 1

                MDLabel:
                    text: "Bugün nasıl hissediyorsun?"
                    bold: True
                MDGridLayout:
                    cols: 3
                    adaptive_height: True
                    spacing: "8dp"
                    SymptomBtn:
                        text: "Sakin"
                        icon: "emoticon-happy-outline"
                        group: "mood"
                    SymptomBtn:
                        text: "Mutlu"
                        icon: "emoticon-outline"
                        group: "mood"
                    SymptomBtn:
                        text: "Enerjik"
                        icon: "lightning-bolt-outline"
                        group: "mood"
                    SymptomBtn:
                        text: "Depresif"
                        icon: "emoticon-sad-outline"
                        group: "mood"
                    SymptomBtn:
                        text: "Sinirli"
                        icon: "emoticon-angry-outline"
                        group: "mood"
                    SymptomBtn:
                        text: "Yorgun"
                        icon: "emoticon-confused-outline"
                        group: "mood"

                MDLabel:
                    text: "Bugün hangi semptomları yaşadınız?"
                    bold: True
                MDGridLayout:
                    cols: 3
                    adaptive_height: True
                    spacing: "8dp"
                    SymptomBtn:
                        text: "Kas Ağrısı"
                        icon: "bone"
                        group: "symptom"
                    SymptomBtn:
                        text: "Öksürük"
                        icon: "lungs"
                        group: "symptom"
                    SymptomBtn:
                        text: "Baş Ağrısı"
                        icon: "head-cog-outline"
                        group: "symptom"
                    SymptomBtn:
                        text: "Mide Bulantısı"
                        icon: "stomach"
                        group: "symptom"
                    SymptomBtn:
                        text: "Uykusuzluk"
                        icon: "sleep-off"
                        group: "symptom"
                    SymptomBtn:
                        text: "Eklem Ağrısı"
                        icon: "human-handsup"
                        group: "symptom"

                MDLabel:
                    text: "Hatırlatıcı"
                    bold: True
                
                MDBoxLayout:
                    orientation: "vertical"
                    adaptive_height: True
                    spacing: "12dp"

                    MDAnchorLayout:
                        id: empty_meds
                        size_hint_y: None
                        height: "0dp"
                        opacity: 0
                        padding: ["12dp", "8dp", "12dp", "8dp"]
                        anchor_x: "center"
                        anchor_y: "center"
                        MDLabel:
                            text: "Henüz ilaç eklenmedi"
                            halign: "center"
                            valign: "middle"
                            text_size: self.size
                            theme_text_color: "Custom"
                            text_color: [0, 0, 0, 0.5]

                    MDBoxLayout:
                        id: medicines_list
                        orientation: "vertical"
                        adaptive_height: True
                        spacing: "12dp"

    MDFloatLayout:
        # MENÜ KARTI (ANİMASYONLU)
        MDCard:
            id: menu_card
            size_hint: None, None
            width: "200dp"
            height: "190dp"
            pos_hint: {"right": .84, "y": .12}
            radius: [50, 50, 5, 50]
            md_bg_color: [1, 1, 1, 1]
            elevation: 8
            opacity: 0
            disabled: True
            
            canvas.before:
                Color:
                    rgba: [0.5, 0.3, 0.9, 1]
                Line:
                    width: 2
                    rounded_rectangle: (self.x, self.y, self.width, self.height, 50, 50, 5, 50)
            
            MDBoxLayout:
                orientation: "vertical"
                padding: ["15dp", "8dp", "15dp", "28dp"]
                spacing: "12dp"

                MDFillRoundFlatButton:
                    text: "İlaç ekle"
                    size_hint_x: 1
                    md_bg_color: [0.5, 0.3, 0.9, 1]
                    font_size: "15sp"
                    bold: True
                    on_release: app.button_callback("İlaç Ekle")
                
                MDFillRoundFlatButton:
                    text: "Alarm ekle"
                    size_hint_x: 1
                    md_bg_color: [0.5, 0.3, 0.9, 1]
                    font_size: "15sp"
                    bold: True
                    on_release: app.button_callback("Alarm Ekle")
                
                MDFillRoundFlatButton:
                    text: "Tahlil ekle"
                    size_hint_x: 1
                    md_bg_color: [0.5, 0.3, 0.9, 1]
                    font_size: "15sp"
                    bold: True
                    on_release: app.button_callback("Tahlil Ekle")

        # ALT NAVİGASYON BARI (SABİTLENDİ)
        MDCard:
            size_hint: 0.95, None
            height: "70dp"
            pos_hint: {"center_x": .5, "center_y": .06}
            radius: [35,]
            elevation: 0 
            md_bg_color: [1, 1, 1, 0.98]
            MDBoxLayout:
                padding: ["25dp", 0, "115dp", 0] 
                spacing: "30dp"
                MDIconButton:
                    icon: "home"
                    theme_icon_color: "Custom"
                    icon_color: [0.5, 0.3, 0.9, 1]
                    pos_hint: {"center_y": .5}
                    on_release: app.nav_action("home")
                MDIconButton:
                    icon: "calendar-month-outline"
                    pos_hint: {"center_y": .5}
                    on_release: app.nav_action("calendar")
                MDIconButton:
                    icon: "chart-line"
                    pos_hint: {"center_y": .5}
                    on_release: app.nav_action("chart")

        # ARTI BUTONU
        MDIconButton:
            icon: "plus"
            icon_size: "50sp"
            size_hint: None, None
            size: "100dp", "100dp"
            pos_hint: {"center_x": .82, "center_y": .09}
            md_bg_color: [0.5, 0.3, 0.9, 1]
            theme_icon_color: "Custom"
            icon_color: [1, 1, 1, 1]
            elevation: 10
            on_release: app.toggle_menu()

'''


class ThyroidApp(MDApp):
    menu_open = BooleanProperty(False)
    medicines = ListProperty([])

    def build(self):
        self.theme_cls.material_style = "M3"
        self.title = "Tiroidim"
        root = Builder.load_string(KV)
        self.week_cal = root.ids.week_cal
        self.medicines_list = root.ids.medicines_list
        self.empty_meds = root.ids.empty_meds
        self.week_cal.sync_today()
        self.symptom_buttons = [w for w in root.walk() if isinstance(w, SymptomBtn)]
        self.medicine_cards = []
        self.day_moods = {}
        self.day_symptoms = {}
        self.day_medicine_actions = {}
        self.week_cal.bind(selected_idx=self.apply_day_state, days=self.apply_day_state)

        # Menü animasyon hedefi
        self.menu_card = root.ids.menu_card
        self.menu_target_h = dp(190)

        # Başlangıçta kapalı
        self.menu_card.height = 0
        self.menu_card.opacity = 0
        self.menu_card.disabled = True
        self._schedule_midnight_refresh()
        self.refresh_medicines()
        self.apply_day_state()

        return root

    def toggle_menu(self):
        self.menu_open = not self.menu_open

        if self.menu_open:
            self.menu_card.disabled = False
            Animation.cancel_all(self.menu_card)
            Animation(opacity=1, height=self.menu_target_h, d=0.18, t="out_quad").start(self.menu_card)
        else:
            Animation.cancel_all(self.menu_card)
            anim = Animation(opacity=0, height=0, d=0.12, t="in_quad")
            anim.bind(on_complete=lambda *_: setattr(self.menu_card, "disabled", True))
            anim.start(self.menu_card)

    def nav_action(self, screen_name: str):
        if self.menu_open:
            self.toggle_menu()
        print(f"Aksiyon: {screen_name}")

    def open_settings(self):
        # Şimdilik sadece buton callback'i: gerçek ayarlar ekranı arkadaşındaki projede.
        # Burada bir pencere açmıyoruz ki sende kırılmasın.
        if self.menu_open:
            self.toggle_menu()

        print("Aksiyon: Ayarlar")

    def button_callback(self, text):
        print(f"Aksiyon: {text}")
        # Menü açıksa animasyonla kapat
        if self.menu_open:
            self.toggle_menu()

    def _selected_date_key(self):
        return self.week_cal.get_selected_date().isoformat()

    def toggle_symptom(self, btn):
        btn.toggle_selected()
        date_key = self._selected_date_key()
        if btn.group == "mood":
            selected_set = self.day_moods.setdefault(date_key, set())
        else:
            selected_set = self.day_symptoms.setdefault(date_key, set())
        if btn.selected:
            selected_set.add(btn.text)
        else:
            selected_set.discard(btn.text)
        self.button_callback(btn.text)

    def record_medicine_action(self, card, action: str):
        if not card.medicine_id:
            card.medicine_id = f"{card.pill}|{card.time}|{card.note}"
        date_key = self._selected_date_key()
        actions = self.day_medicine_actions.setdefault(date_key, {})
        actions[card.medicine_id] = action
        card.select_action(action)
        label = "Aldındı" if action == "taken" else "Atlandı"
        self.button_callback(f"{card.pill} {label}")

    def apply_day_state(self, *_):
        date_key = self._selected_date_key()
        moods = self.day_moods.get(date_key, set())
        symptoms = self.day_symptoms.get(date_key, set())
        for btn in self.symptom_buttons:
            if btn.group == "mood":
                btn.selected = btn.text in moods
            elif btn.group == "symptom":
                btn.selected = btn.text in symptoms
        actions = self.day_medicine_actions.get(date_key, {})
        for card in self.medicine_cards:
            card.selected_action = actions.get(card.medicine_id, "")

    def set_medicines(self, medicines):
        self.medicines = medicines
        self.refresh_medicines()

    def refresh_medicines(self):
        self.medicines_list.clear_widgets()
        self.medicine_cards = []
        if not self.medicines:
            self.empty_meds.opacity = 1
            self.empty_meds.height = dp(40)
            return

        self.empty_meds.opacity = 0
        self.empty_meds.height = 0
        for item in self.medicines:
            card = Factory.MedicineCard(
                time=item.get("time", ""),
                pill=item.get("pill", ""),
                note=item.get("note", ""),
                bg=item.get("bg", [1, 1, 1, 1]),
                btn_color=item.get("btn_color", [0.6, 0.6, 0.6, 1]),
                medicine_id=item.get("id", ""),
            )
            if not card.medicine_id:
                card.medicine_id = f"{card.pill}|{card.time}|{card.note}"
            self.medicines_list.add_widget(card)
            self.medicine_cards.append(card)
        self.apply_day_state()

    def _schedule_midnight_refresh(self):
        now = _dt.datetime.now()
        tomorrow = (now + _dt.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        delay = (tomorrow - now).total_seconds()
        Clock.schedule_once(self._midnight_refresh, delay)

    def _midnight_refresh(self, *_):
        self.week_cal.sync_today()
        self._schedule_midnight_refresh()


if __name__ == '__main__':
    ThyroidApp().run()
