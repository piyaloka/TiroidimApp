from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import ScreenManager


class AddDrugScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (1, 1, 1, 1)  # Beyaz arka plan

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        # İlaç adı
        self.drug_name = MDTextField(
            hint_text="İlaç Adı",
            mode="rectangle"
        )

        # Dozaj
        self.dosage = MDTextField(
            hint_text="Dozaj (ör: 500 mg)",
            mode="rectangle"
        )

        # Kullanım sıklığı
        self.frequency = MDTextField(
            hint_text="Kullanım Sıklığı (ör: Günde 2 kez)",
            mode="rectangle"
        )

        back_button = MDRaisedButton(
            text="Geri Dön",
            on_press=self.go_back
        )

        layout.add_widget(self.drug_name)
        layout.add_widget(self.dosage)
        layout.add_widget(self.frequency)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = "main"


class MainApp(MDApp):

    def build(self):
        self.sm = ScreenManager()

        main_screen = MDScreen(name="main")
        layout = BoxLayout(orientation='vertical')

        button = MDFloatingActionButton(
            icon="plus",
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            md_bg_color=(128, 0, 128, 1),
            icon_size="50dp",
        )

        button.bind(on_press=self.open_dialog)

        layout.add_widget(button)
        main_screen.add_widget(layout)

        self.sm.add_widget(main_screen)
        self.sm.add_widget(AddDrugScreen(name="add_drug"))

        return self.sm

    def open_dialog(self, instance):
        content = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=20
        )

        new_button = MDRaisedButton(
            text="İlaç Ekle",
            size_hint=(None, None),
            width=200,
            height=42,
            md_bg_color=(128, 0, 128, 1),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5}
        )

        new_button.bind(on_press=self.go_to_add_drug)

        content.add_widget(new_button)

        self.dialog = MDDialog(
            type="custom",
            content_cls=content,
            size_hint=(None, None),
            size=(700, 500),
            auto_dismiss=True
        )

        self.dialog.open()

    def go_to_add_drug(self, instance):
        self.dialog.dismiss()
        self.sm.current = "add_drug"

MainApp().run()

