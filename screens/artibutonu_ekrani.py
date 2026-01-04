from kivymd.app import MDApp

from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.floatlayout import FloatLayout

from kivy.factory import Factory

from kivymd.uix.menu import MDDropdownMenu

from kivy.core.window import Window

from kivy.properties import BooleanProperty

from kivy.metrics import dp

from datetime import datetime

from kivy.clock import Clock

import os 

from screens.giris_ekrani import GirisEkrani, HosgeldinEkrani
from screens.onboarding_ekrani import OnboardingEkrani
from screens.hastalik_secme import HastalikSecmeEkrani
from screens.dashboard_ekrani import DashboardEkrani
from screens.takvim_ekrani import TakvimEkrani
from screens.grafik_ekrani import GrafikEkrani
from screens.artibutonu_ekrani import ArtiButonuEkrani
from screens.duzenleme_ekrani import DuzenlemeEkrani
from screens.ayarlar_ekrani import AyarlarEkrani


Window.size = (360, 640)



KV = '''

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


<MyFloatingMenu@MDFloatLayout>:

    size_hint: None, None
    
    size: dp(190), dp(210)
    
    pos_hint: {"right": 0.95, "y": 0.12} 

    opacity: 1 if root.menu_acik else 0
    
    disabled: not root.menu_acik

    canvas.before:
    
        Color:
            rgba: 1, 1, 1, 1
            
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [70, 70, 10, 70]
            
        Triangle:
         
            points: [self.x + self.width - dp(20), self.y, self.x + self.width + dp(5), self.y - dp(15), self.x + self.width - dp(50), self.y]
        Color:
            rgba: 0.5, 0.2, 0.9, .3
            
        Line:
            width: 1.1
            rounded_rectangle: [self.x, self.y, self.width, self.height, 70, 70, 10, 70]


            MDBoxLayout:

                orientation: 'vertical'

                padding: dp(15)

                spacing: dp(10)

                pos_hint: {"center_x": .5, "center_y": .5}

                adaptive_height: True

                MDRaisedButton:

                    text: "İlaç ekle"

                    size_hint_x: 1

                    md_bg_color: 0.5, 0.2, 0.9, 1

                    on_release: app.root.current = "ilac"; root.menu_acik = False

                MDRaisedButton:

                    text: "Alarm ekle"

                    size_hint_x: 1

                    md_bg_color: 0.5, 0.2, 0.9, 1

                    on_release: app.root.current = "alarm"; root.menu_acik = False

                MDRaisedButton:

                    text: "Tahlil ekle"

                    size_hint_x: 1

                    md_bg_color: 0.5, 0.2, 0.9, 1

                    on_release: app.root.current = "tahlil"; root.menu_acik = False



        MDCard:

            size_hint: 1, .1

            pos_hint: {"center_x": .5, "center_y": .05}

            radius: [20, 20, 0, 0]

            elevation: 2

            md_bg_color: 1, 1, 1, 1

            MDBoxLayout:

                orientation: 'horizontal'

                spacing: dp(10)

                padding: dp(10)

                MDBoxLayout:

                    orientation: 'vertical'

                    MDIconButton:

                        icon: "home-outline"

                        pos_hint: {"center_x": .5}

                        theme_text_color: "Custom"

                        text_color: 0.5, 0.2, 0.9, 1

                        on_release: app.root.current = "dashboard"

                    MDLabel:

                        text: "Ana Sayfa"

                        halign: "center"

                        font_style: "Caption"

                        theme_text_color: "Secondary"


                MDBoxLayout:

                    orientation: 'vertical'

                    MDIconButton:

                        icon: "calendar-month-outline"

                        pos_hint: {"center_x": .5}

                        theme_text_color: "Custom"

                        text_color: 0.5, 0.2, 0.9, 1

                        on_release: app.root.current = "takvim"

                    MDLabel:

                        text: "Takvim"

                        halign: "center"

                        font_style: "Caption"

                        theme_text_color: "Secondary"

                MDBoxLayout:

                    orientation: 'vertical'

                    MDIconButton:

                        icon: "chart-bell-curve-cumulative"

                        pos_hint: {"center_x": .5}

                        theme_text_color: "Custom"

                        text_color: 0.5, 0.2, 0.9, 1

                        on_release: app.root.current = "grafik"

                    MDLabel:

                        text: "Grafik"

                        halign: "center"

                        font_style: "Caption"

                        theme_text_color: "Secondary"



<IlacScreen>:

    MDFloatLayout:

        md_bg_color: 1, 1, 1, 1

        MDCard:

            size_hint: .88, .8

            pos_hint: {"center_x": .5, "center_y": .5}

            radius: [60, 60, 10, 80]

            line_color: 0.5, 0.2, 0.9, 1

            padding: dp(25)

            orientation: "vertical"

            spacing: dp(12)

            elevation: 0

            MDLabel:

                text: "İlaç ekle"

                halign: "center"

                font_style: "H5"

                text_color: 0.5, 0.2, 0.9, 1

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

                MDRaisedButton:

                    text: "İptal et"

                    size_hint_x: .5

                    on_release: app.root.current = "menu"

                MDRaisedButton:

                    text: "Kaydet"

                    md_bg_color: 0.5, 0.2, 0.9, 1

                    size_hint_x: .5

                    on_release: app.root.current = "menu"



<AlarmScreen>:

    MDFloatLayout:

        md_bg_color: 1, 1, 1, 1

        MDCard:

            size_hint: .88, .85

            pos_hint: {"center_x": .5, "center_y": .5}

            radius: [60, 60, 10, 80]

            line_color: 0.5, 0.2, 0.9, 1

            padding: dp(20)

            orientation: "vertical"

            spacing: dp(8)

            elevation: 0

            MDLabel:

                text: "Alarm ekle"

                halign: "center"

                font_style: "H5"

                text_color: 0.5, 0.2, 0.9, 1

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

                on_touch_down: if self.collide_point(*args[1].pos): root.open_vakit_dur_menu()

            CustomInput:

                id: a_time_full

                label: "Bildirim"

                text_val: "00:00"

                on_touch_down: if self.collide_point(*args[1].pos): root.start_time_selection()

            MDBoxLayout:

                adaptive_height: True

                spacing: 15

                padding: [0, dp(10), 0, 0]

                MDRaisedButton:

                    text: "İptal et"

                    size_hint_x: .5

                    on_release: app.root.current = "menu"

                MDRaisedButton:

                    text: "Kaydet"

                    md_bg_color: 0.5, 0.2, 0.9, 1

                    size_hint_x: .5

                    on_release: app.root.current = "menu"



<TahlilScreen>:

    MDFloatLayout:

        md_bg_color: 1, 1, 1, 1

        MDCard:

            size_hint: .88, .92

            pos_hint: {"center_x": .5, "center_y": .5}

            radius: [60, 60, 10, 80]

            line_color: 0.5, 0.2, 0.9, 1

            padding: dp(20)

            orientation: "vertical"

            spacing: dp(8)

            elevation: 0

            MDLabel:

                text: "Tahlil ekle"

                halign: "center"

                font_style: "H5"

                text_color: 0.5, 0.2, 0.9, 1

            CustomInput:

                id: t_name

                label: "Tahlil seçiniz"

                text_val: "Seçiniz"

                on_touch_down: if self.collide_point(*args[1].pos): root.open_tahlil_menu()

           

            MDBoxLayout:

                spacing: dp(10)

                adaptive_height: True

                CustomInput:

                    id: t_val

                    label: "Tahlil Değerini giriniz"

                    text_val: "Değer girin"

                    readonly: False

                    input_filter: "int"

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

                        input_filter: "int"

                    CustomInput:

                        id: t_gun

                        label: "Gün"

                        text_val: "0"

                        readonly: False

                        input_filter: "int"

            CustomInput:

                id: t_date

                label: "Tahlili ne zaman yaptırdınız?"

                text_val: "GG/AA/YYYY"

                on_touch_down: if self.collide_point(*args[1].pos): root.start_date_selection()

            MDBoxLayout:

                adaptive_height: True

                spacing: 15

                padding: [0, dp(10), 0, 0]

                MDRaisedButton:

                    text: "İptal et"

                    size_hint_x: .5

                    on_release: app.root.current = "menu"

                MDRaisedButton:

                    text: "Kaydet"

                    md_bg_color: 0.5, 0.2, 0.9, 1

                    size_hint_x: .5

                    on_release: app.root.current = "menu"

'''



class BaseScreen(Screen):

    ilac_verileri = {

        "Euthyrox": ["25mcg", "50mcg", "75mcg", "100mcg", "125mcg", "150mcg"],

        "Levotiron": ["25mcg", "50mcg", "75mcg", "100mcg"],

        "Tiromel": ["25mcg"], "Tefor": ["100mcg"]

    }

    saatler = [str(i).zfill(2) for i in range(24)]

    dakikalar = [str(i).zfill(2) for i in range(60)]

    gunler = [str(i).zfill(2) for i in range(1, 32)]

    aylar = [str(i).zfill(2) for i in range(1, 13)]

    current_year = datetime.now().year

    yillar = [str(i) for i in range(current_year, 1899, -1)]



    def open_dropdown(self, caller, items, callback):

        self.menu = MDDropdownMenu(

            caller=caller, items=[{"viewclass": "OneLineListItem", "text": i, "on_release": lambda x=i: callback(x, caller)} for i in items],

            width_mult=3, max_height=dp(240), radius=[15, 15, 15, 15]

        )

        self.menu.open()



    def set_val(self, text, caller):

        caller.text = text

        if self.menu: self.menu.dismiss()


class MyFloatingMenu(FloatLayout):
    menu_acik = BooleanProperty(False)


class IlacScreen(BaseScreen):

    temp_day = "01"

    temp_month = "01"

    def open_ilac_menu(self): self.open_dropdown(self.ids.i_name.ids.text_field, list(self.ilac_verileri.keys()), self.set_val)

    def open_doz_menu(self):

        secili = self.ids.i_name.ids.text_field.text

        self.open_dropdown(self.ids.i_doz.ids.text_field, self.ilac_verileri.get(secili, ["İlaç seçin"]), self.set_val)

    def start_date_selection(self): self.open_dropdown(self.ids.i_date.ids.text_field, self.gunler, self.select_day)

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



class AlarmScreen(BaseScreen):

    temp_hour = "00"

    def open_ilac_menu(self): self.open_dropdown(self.ids.a_name.ids.text_field, list(self.ilac_verileri.keys()), self.set_val)

    def open_vakit_dur_menu(self):

        options = ["Sabah / Aç", "Sabah / Tok", "Akşam / Aç", "Akşam / Tok"]

        self.open_dropdown(self.ids.a_vakit_durum.ids.text_field, options, self.set_multi_val)

    def start_time_selection(self): self.open_dropdown(self.ids.a_time_full.ids.text_field, self.saatler, self.select_hour_then_min)

    def select_hour_then_min(self, hour, caller):

        self.temp_hour = hour

        self.menu.dismiss()

        self.open_dropdown(self.ids.a_time_full.ids.text_field, self.dakikalar, self.complete_time_selection)

    def complete_time_selection(self, minute, caller):

        caller.text = f"{self.temp_hour}:{minute}"

        self.menu.dismiss()

    def set_multi_val(self, text, caller):

        current_text = caller.text

        if not current_text or current_text == "Seçiniz": caller.text = text

        else:

            selections = [s.strip() for s in current_text.split(",")]

            if text not in selections:

                if len(selections) < 2: caller.text = f"{current_text}, {text}"

        self.menu.dismiss()



class TahlilScreen(BaseScreen):

    temp_day = "01"

    temp_month = "01"

    _last_len = 0 # Silme kontrolü için



    def on_enter(self, *args):

        # Bind işlemini sadece bir kez yapıyoruz

        self.ids.t_val.ids.text_field.bind(text=self.auto_dot)



    def auto_dot(self, instance, value):

        curr_len = len(value)

        # Eğer silme işlemi yapılıyorsa hiçbir şey yapma

        if curr_len < self._last_len:

            self._last_len = curr_len

            return



        # Sadece rakamları al

        raw_val = value.replace('.', '')

       

        # Eğer 2. karakter girildiyse ve henüz nokta yoksa araya nokta koy

        if len(raw_val) >= 2 and '.' not in value:

            new_text = f"{raw_val[0]}.{raw_val[1:]}"

            # Sonsuz döngüyü engellemek için geçici olarak unbind

            instance.unbind(text=self.auto_dot)

            instance.text = new_text

            instance.bind(text=self.auto_dot)

            # İmleci en sona at (Clock kullanımı mobilde daha stabildir)

            Clock.schedule_once(lambda dt: setattr(instance, 'cursor', (len(new_text), 0)))



        self._last_len = len(instance.text)



    def open_tahlil_menu(self):

        self.open_dropdown(self.ids.t_name.ids.text_field, ["TSH", "fT3", "fT4"], self.select_tahlil_and_unit)

   

    def select_tahlil_and_unit(self, tahlil_ad, caller):

        caller.text = tahlil_ad

        if tahlil_ad == "TSH":

            self.ids.t_unit.ids.text_field.text = "mIU/L"

        else:

            self.ids.t_unit.ids.text_field.text = "ng/dL"

        self.menu.dismiss()



    def open_birim_menu(self):

        self.open_dropdown(self.ids.t_unit.ids.text_field, ["mIU/L", "ng/dL", "pg/mL", "pmol/L"], self.set_val)

   

    def start_date_selection(self): self.open_dropdown(self.ids.t_date.ids.text_field, self.gunler, self.select_day)

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



class ThyroidApp(MDApp):

    def build(self):

        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Green"
        self.theme_cls.material_style = "M3"
        self.title = "Tiroidim"

        Builder.load_string(KV)

        sm = ScreenManager()

        dashboard = DashboardEkrani(name="dashboard")

        self.floating_menu = Factory.MyFloatingMenu()
        self.floating_menu.menu_acik = False  
        dashboard.add_widget(self.floating_menu)

        sm.add_widget(dashboard)

        sm.add_widget(IlacScreen(name="ilac"))

        sm.add_widget(AlarmScreen(name="alarm"))

        sm.add_widget(TahlilScreen(name="tahlil"))

        sm.add_widget(GirisEkrani(name="giris"))
        sm.add_widget(HosgeldinEkrani(name="hosgeldin"))
        sm.add_widget(OnboardingEkrani(name="onboarding"))
        sm.add_widget(HastalikSecmeEkrani(name="hastalik_secme"))
        sm.add_widget(DashboardEkrani(name="dashboard"))
        sm.add_widget(TakvimEkrani(name="takvim"))
        sm.add_widget(GrafikEkrani(name="grafik"))
        sm.add_widget(ArtiButonuEkrani(name="arti_butonu"))
        sm.add_widget(DuzenlemeEkrani(name="duzenleme"))
        sm.add_widget(AyarlarEkrani(name="ayarlar"))

        sm.current = "giris"

        return sm 

    def toggle_my_menu(self):
        if hasattr(self, 'floating_menu'):
            self.floating_menu.menu_acik = not self.floating_menu.menu_acik

if __name__ == "__main__":

    ThyroidApp().run()
