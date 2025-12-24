from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import ScreenManager, Screen


# =========================
# YENİ SAYFA: İLAÇ EKLE
# =========================
class AddDrugScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (1, 1, 1, 1)  # Beyaz arka plan

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        self.drug_name = MDTextField(
            hint_text="İlaç Adı",
            mode="rectangle"
        )

        self.dosage = MDTextField(
            hint_text="Dozaj (örn: 500 mg)",
            mode="rectangle"
        )

        self.frequency = MDTextField(
            hint_text="Kullanım Sıklığı (örn: Günde 2 kez)",
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


# =========================
# ANA UYGULAMA
# =========================
class MainApp(MDApp):

    def build(self):
        # ScreenManager ekleniyor (çok ekran için)
        self.sm = ScreenManager()

        # ===== SENİN ANA EKRANIN =====
        screen = MDScreen(name="main")
        layout = BoxLayout(orientation='vertical')

        button = MDFloatingActionButton(
            icon="plus",
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            md_bg_color=(128, 0, 128, 1),
            icon_size="50dp",
        )

        button.bind(on_press=self.open_dialog)

        layout.add_widget(button)
        screen.add_widget(layout)

        # ScreenManager'a ana ekran ekleniyor
        self.sm.add_widget(screen)

        # Yeni sayfa ekleniyor
        self.sm.add_widget(AddDrugScreen(name="add_drug"))

        return self.sm

    # =========================
    # DIALOG
    # =========================
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

        # 👉 dialog içinden yeni sayfaya geçiş
        new_button.bind(on_press=self.go_to_add_drug)

        content.add_widget(new_button)

        self.dialog = MDDialog(
            type="custom",
            content_cls=content,
            size_hint=(None, None),
            size=(700, 500),
            auto_dismiss=True,
            background="white"
        )

        self.dialog.open()

    # =========================
    # SAYFA GEÇİŞİ
    # =========================
    def go_to_add_drug(self, instance):
        self.dialog.dismiss()
        self.sm.current = "add_drug"


# =========================
# APP BAŞLAT
# =========================
MainApp().run()
