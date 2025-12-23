project/
│
├── main.py
├── database.py
├── profil_ekrani.py        # Onboarding
├── disease_ekrani.py       # Hastalık seçimi
├── screens/
│   └── dashboard_ekrani.py
  from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from database import Database


class AyarlarEkrani(Screen):
    secili_ilac_id = None
    secili_ilac_adi = StringProperty("")
    mevcut_saat = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

    def on_pre_enter(self):
        self.ilaclari_yukle()

    def ilaclari_yukle(self):
        """
        Veritabanındaki kullanıcının ilaçlarını dropdown'a yükler
        """
        self.ids.ilac_menu.clear_widgets()
        ilaclar = self.db.kullanici_ilaclarini_getir()

        for ilac in ilaclar:
            ilac_id, ad, doz, saat, _ = ilac
            self.ids.ilac_menu.add_widget(
                self.ids.create_button(
                    f"{ad} {doz}",
                    ilac_id,
                    saat
                )
            )

    def ilac_sec(self, ilac_id, ad, saat):
        """
        Kullanıcı bir ilaç seçtiğinde çalışır
        """
        self.secili_ilac_id = ilac_id
        self.secili_ilac_adi = ad
        self.mevcut_saat = saat

    def saat_guncelle(self):
        """
        Yeni saat bilgisini veritabanına yazar
        """
        if not self.secili_ilac_id:
            return

        yeni_saat = self.ids.saat_input.text

        conn = self.db.baglanti_ac()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE kullanici_ilaclari SET saat = ? WHERE id = ?",
            (yeni_saat, self.secili_ilac_id)
        )
        conn.commit()
        conn.close()

        self.mevcut_saat = yeni_saat
        self.ilaclari_yukle()


<AyarlarEkrani>:
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 15

        Label:
            text: "İlaç Saati Ayarları"
            font_size: 22
            size_hint_y: None
            height: 40

        Label:
            text: "İlaç Seç"
            size_hint_y: None
            height: 30

        ScrollView:
            size_hint_y: 0.4

            BoxLayout:
                id: ilac_menu
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: 5

        Label:
            text: "Seçilen İlaç: " + root.secili_ilac_adi

        Label:
            text: "Mevcut Saat: " + root.mevcut_saat

        TextInput:
            id: saat_input
            hint_text: "Yeni Saat (örn: 08:30)"
            multiline: False

        Button:
            text: "Saati Güncelle"
            size_hint_y: None
            height: 45
            on_release: root.saat_guncelle()

<Widget>:
    def create_button(self, text, ilac_id, saat):
        from kivy.uix.button import Button
        return Button(
            text=text,
            size_hint_y=None,
            height=40,
            on_release=lambda x: app.root.get_screen("ayarlar").ilac_sec(
                ilac_id, text, saat
            )
        )
