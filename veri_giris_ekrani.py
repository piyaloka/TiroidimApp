from kivymd.uix.snackbar import Snackbar 
from kivy.lang import Builder
from kivy.animation import Animation
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu


Window.size = (350, 600)

KV = '''

MDScreen:
    md_bg_color: 1, 1, 1, 1

    MDCard:
        id: form_page
        pos_hint: {"center_x": 0.5, "center_y": -1} 
        size_hint: 0.95, 0.8
        radius: [30, 30, 30, 30]
        elevation: 12
        padding: "20dp"
        orientation: 'vertical'

        MDLabel:
            id: form_title
            text: "Ekle"
            halign: "center"
            bold: True
            font_style: "H6"
            size_hint_y: None
            height: "40dp"

        MDBoxLayout:
            orientation: 'vertical'
            spacing: "15dp"
            padding: [0, "10dp"]

            MDBoxLayout:
                id: ilac_fields
                orientation: 'vertical'
                size_hint_y: None
                height: 0
                opacity: 0

                MDTextField:
                    id: field_ilac_adi
                    hint_text: "İlaç Adı"

                MDTextField:
                    id: field_dozaj
                    hint_text: "Dozaj (mg/ml)"
                MDTextField:
                    id: field_siklik
                    hint_text: "Kullanım Sıklığı"

            MDBoxLayout:
                id: alarm_fields
                orientation: 'vertical'
                size_hint_y: None
                height: 0
                opacity: 0
                disabled: True
                spacing: "10dp"

                MDLabel:
                    text: "Kullanım Zamanı:"
                    theme_text_color: "Secondary"
                    font_style: "Caption"

                MDDropDownItem:
                    id: drop_item
                    text: "Sabah / Aç (Seçiniz)"
                    on_release: app.show_time_options()
                    pos_hint: {"center_x": .5}

                MDTextField:
                    hint_text: "Kaç gün alınacak?"
                    input_filter: "int"

                MDTextField:
                    hint_text: "Öğündeki kullanım miktarı (Örn: 1 ölçek)"

            MDBoxLayout:
                id: tahlil_fields
                orientation: 'vertical'
                size_hint_y: None
                height: 0
                opacity: 0

                MDRectangleFlatIconButton:
                    icon: "file-upload"
                    text: "Tahlil Dosyası Seç"
                    width: "200dp"
                
        MDBoxLayout:
            spacing: "15dp"
            size_hint_y: None
            height: "60dp"

            MDRoundFlatButton:
                text: "İPTAL ET"
                size_hint_x: .5
                on_release: app.cancel_and_back()

            MDFillRoundFlatButton:
                text: "KAYDET"
                size_hint_x: .5
                md_bg_color: 0.4, 0.1, 0.9, 1
                on_release: app.close_form()

'''

class MedApp(MDApp):
    secilen_zamanlar = []

    def build(self):
        self.theme_cls.primary_palette = "Purple"
        return Builder.load_string(KV)
    
    def open_form(self, mode):        
        self.root.ids.form_title.text = f"{mode.capitalize()} Ekle"

        for f in ['ilac_fields', 'alarm_fields', 'tahlil_fields']:
            self.root.ids[f].opacity = 0
            self.root.ids[f].disabled = True 
            self.root.ids[f].height = 0

        active_id = f"{mode.replace('ç', 'c')}_fields"

        if active_id in self.root.ids:
            active_group = self.root.ids[active_id]
            active_group.opacity = 1
            active_group.disabled = False 
            active_group.height = "250dp" 

        Animation(pos_hint={"center_x": 0.5, "center_y": 0.5}, duration=0.3).start(self.root.ids.form_page)

    def cancel_and_back(self):
        anim = Animation(pos_hint={"center_x": 0.5, "center_y": -1}, duration=0.3)
        anim.start(self.root.ids.form_page)

    def close_form(self):
        ad = self.root.ids.field_ilac_adi.text.strip() 
        doz = self.root.ids.field_dozaj.text.strip()

        if not ad or not doz:
            Snackbar(text="Lütfen ilaç adını ve dozajını boş bırakmayın!", bg_color=(0.8, 0, 0, 1)).open()
            return 

        print(f"BAŞARILI KAYIT: {ad} - {doz} - Zamanlar: {self.secilen_zamanlar}")
    
        Animation(pos_hint={"center_x": 0.5, "center_y": -1}, duration=0.3).start(self.root.ids.form_page)
        self.root.ids.field_ilac_adi.text = ""
        self.root.ids.field_dozaj.text = ""
        self.secilen_zamanlar = []
        self.root.ids.drop_item.text = "Seçiniz (Maksimum 2)"

    def show_time_options(self):
        zamanlar = ["Sabah / Aç", "Sabah / Tok", "Akşam / Aç", "Akşam / Tok"]
        menu_items = [
            {"viewclass": "OneLineListItem", "text": i, "on_release": lambda x=i: self.set_item(x)} 
            for i in zamanlar
        ]

        self.menu = MDDropdownMenu(caller=self.root.ids.drop_item, items=menu_items, width_mult=4)
        self.menu.open()

    def set_item(self, text_item):
        if text_item in self.secilen_zamanlar:
            self.secilen_zamanlar.remove(text_item)

        elif len(self.secilen_zamanlar) < 2:
            self.secilen_zamanlar.append(text_item)

        else:
            Snackbar(text="En fazla 2 zaman seçebilirsiniz!", duration=1).open()
            return

        if not self.secilen_zamanlar:
            self.root.ids.drop_item.text = "Seçiniz (Maks 2)"

        else:
            self.root.ids.drop_item.text = ", ".join(self.secilen_zamanlar)

        if len(self.secilen_zamanlar) == 2:
            self.menu.dismiss()
