from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
from onboardingscreen import user_profile

class ProfileEditScreen(Screen):  # Profil düzenleme ekranı
    def __init__(screenobject2, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(
            orientation='vertical',
            padding=80,
            spacing=80
        )

        title = MDLabel(
            text="Profil Bilgilerini Düzenle",
            halign="center",
            font_style="H4"
        )

        # Önceden girilen isim otomatik gelir
        screenobject2.name_surname_input = MDTextField(
            hint_text="Ad ve soyad bilginizi giriniz",
            text=user_profile["name_surname"]
        )

        screenobject2.type_label = MDLabel(
            text=f"Seçilen: {user_profile['thyroid_type']}",
            halign="center"
        )

        screenobject2.btn_hypo = MDRaisedButton(
            text="Hipotiroid",
            on_release=screenobject2.select_hypo
        )

        screenobject2.btn_hyper = MDRaisedButton(
            text="Hipertiroid",
            on_release=screenobject2.select_hyper
        )

        screenobject2.save_btn = MDRaisedButton(
            text="Güncelle",
            on_release=screenobject2.update_data
        )

        layout.add_widget(title)
        layout.add_widget(screenobject2.name_surname_input)
        layout.add_widget(screenobject2.type_label)
        layout.add_widget(screenobject2.btn_hypo)
        layout.add_widget(screenobject2.btn_hyper)
        layout.add_widget(screenobject2.save_btn)

        screenobject2.add_widget(layout)

        screenobject2.selected_type = user_profile["thyroid_type"]

    def select_hypo(screenobject2, button):
        screenobject2.selected_type = "Hipotiroid"
        screenobject2.type_label.text = "Seçilen: Hipotiroid"

    def select_hyper(screenobject2, button):
        screenobject2.selected_type = "Hipertiroid"
        screenobject2.type_label.text = "Seçilen: Hipertiroid"

    def update_data(screenobject2, button):
        user_profile["name_surname"] = screenobject2.name_surname_input.text
        user_profile["thyroid_type"] = screenobject2.selected_type

        print("Profil güncellendi:", user_profile)

        # guncelleme yapildi mesaji
        toast("Profil bilgileri güncellendi")

    def on_enter(screenobject2):
        # ekrana her girildiginde guncel bilgiler otomatik dolar
        screenobject2.name_surname_input.text = user_profile["name_surname"]
        screenobject2.selected_type = user_profile["thyroid_type"]
        screenobject2.type_label.text = f"Seçilen: {screenobject2.selected_type}"
