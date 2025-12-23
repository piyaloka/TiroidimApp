from kivy.uix.screenmanager import Screen #ekran olusturur ve ekranlar arasi gecis yapar
from kivymd.uix.textfield import MDTextField #kullanicinin yazi yazabilecegi kutuyu olusturur
from kivymd.uix.button import MDRaisedButton #basilabilir kutu (buton) olusturur
from kivymd.uix.boxlayout import MDBoxLayout #kutuların düzenini belirler
from kivymd.uix.label import MDLabel #ekranda yazi olmasini saglar baslik gibi

# Kullanıcı profil bilgileri
user_profile = {
    "name_surname": "",
    "thyroid_type": ""
}

class OnboardingScreen(Screen): #Screen sınıfından turetilmis yeni sinif tanimi
    def __init__(screenobject1, **kwargs): #yeni sınıfın başlatıcı fonksiyonu
        super().__init__(**kwargs) #kwargs Screen sınıfındaki ekran ozelliklerini aktariyor
        #super(): üst sinif (Screen) init fonksiyonunu calistirarak ust sinif fonksiyonlarini ve ozelliklerini yeni sınif nesnesine verir [name, on_enter, on_leave]

        # ANA DIKEY LAYOUT
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=40,
            spacing=40
        )

        # ---- SAG UST PROFIL BUTONU ICIN UST BAR ----
        top_bar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=50
        )

        top_bar.add_widget(MDLabel())  # sol tarafi bos birakir

        profile_btn = MDRaisedButton(
            text="Profil",
            on_release=screenobject1.open_profile_edit
        )

        top_bar.add_widget(profile_btn)

        # ust bar layouta eklenir
        main_layout.add_widget(top_bar)

        #giriste cikacak hazir yazi ortada ve h3 yazi tipinde 
        title = MDLabel(
            text="Merhaba, \n Tiroidim uygulamasına hoşgeldiniz",
            halign="center",
            font_style="H4"
        )

        # İsim inputu
        screenobject1.name_surname_input = MDTextField(
            hint_text="Ad ve soyad bilginizi giriniz"
        )

        # Tiroid tipi (basit butonlar)
        screenobject1.type_label = MDLabel(
            text="Tiroid Tipi Seçin",
            halign="center"
        )

        screenobject1.btn_hypo = MDRaisedButton(
            text="Hipotiroid",
            on_release=screenobject1.select_hypo #butona basinca select_hypo fonksiyonu calisir
        )

        screenobject1.btn_hyper = MDRaisedButton(
            text="Hipertiroid",
            on_release=screenobject1.select_hyper #butona basinca select_hyper fonksiyonu calisir
        )

        # Kaydet butonu
        screenobject1.save_btn = MDRaisedButton(
            text="Kaydet",
            on_release=screenobject1.save_data #butona basinca save_data fonksiyonu calisir
        )

        # add_widget layout nesnesine widget eklemek için MDBoxLayout’un hazır fonksiyonu
        main_layout.add_widget(title)
        main_layout.add_widget(screenobject1.name_surname_input)
        main_layout.add_widget(screenobject1.type_label)
        main_layout.add_widget(screenobject1.btn_hypo)
        main_layout.add_widget(screenobject1.btn_hyper)
        main_layout.add_widget(screenobject1.save_btn)

        #layout nesnesini ekle screenobject1 nesnesine - ana ekranda butonlar düzenli hale gelir-
        screenobject1.add_widget(main_layout)

        # Seçilen tip
        screenobject1.selected_type = "" #save_data da kayıt yapilirken lazim

    def select_hypo(screenobject1, button):
        screenobject1.selected_type = "Hipotiroid"
        screenobject1.type_label.text = "Seçilen: Hipotiroid"

    def select_hyper(screenobject1, button):
        screenobject1.selected_type = "Hipertiroid"
        screenobject1.type_label.text = "Seçilen: Hipertiroid"

    def save_data(screenobject1, button):
        # sadece ilk kayit yapilir, ekran DEGISTIRILMEZ
        user_profile["name_surname"] = screenobject1.name_surname_input.text
        user_profile["thyroid_type"] = screenobject1.selected_type

        print("Kaydedildi:", user_profile)

    def open_profile_edit(screenobject1, button):
        # profil guncelleme ekrani SADECE buradan acilir
        screenobject1.manager.current = "profile_edit"
