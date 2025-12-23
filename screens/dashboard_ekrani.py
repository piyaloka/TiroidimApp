from datetime import datetime

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from database import Database


class DashboardEkrani(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

    def on_pre_enter(self, *args):
        self.refresh()

    def refresh(self):
        bugun = datetime.now().strftime("%Y-%m-%d")

        # ÜSTTEKİ GÜN DURUMU (✅⚠️❌)
        try:
            durum = self.db.gun_ikonunu_hesapla(bugun)
            self.ids.lbl_gun_durumu.text = f'Bugün: {durum["icon"]}  {durum["text"]}'
        except Exception as e:
            self.ids.lbl_gun_durumu.text = f"Hata: {e}"

        # İLAÇ KARTLARI
        self.ids.ilac_listesi.clear_widgets()

        kartlar = self.db.dashboard_kartlarini_getir(bugun)

        if not kartlar:
            self.ids.ilac_listesi.add_widget(
                Label(text="Henüz ilaç eklenmemiş.")
            )
            return

        for k in kartlar:
            satir = BoxLayout(size_hint_y=None, height=50, spacing=10)

            if k["taken"] is True:
                durum_txt = "✅ Alındı"
            elif k["taken"] is False:
                durum_txt = "❌ Atlandı"
            else:
                durum_txt = "⏳ Bekliyor"

            lbl = Label(
                text=f'{k["saat"]} | {k["ilac_adi"]} {k["doz"]} | {durum_txt}',
                halign="left",
                valign="middle"
            )
            lbl.bind(size=lambda x, y: setattr(x, "text_size", y))
            satir.add_widget(lbl)

            btn_aldim = Button(text="Aldım", size_hint_x=None, width=80)
            btn_aldim.bind(
                on_press=lambda _, ilac_id=k["ilac_id"]: self.logla(ilac_id, "ALINDI")
            )
            satir.add_widget(btn_aldim)

            btn_atladim = Button(text="Atladım", size_hint_x=None, width=80)
            btn_atladim.bind(
                on_press=lambda _, ilac_id=k["ilac_id"]: self.logla(ilac_id, "ATLADI")
            )
            satir.add_widget(btn_atladim)

            self.ids.ilac_listesi.add_widget(satir)

    def logla(self, ilac_id, durum):
        bugun = datetime.now().strftime("%Y-%m-%d")
        self.db.ilac_logla(ilac_id, bugun, durum)
        self.refresh()
