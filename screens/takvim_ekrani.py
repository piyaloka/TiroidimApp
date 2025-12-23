from kivymd.uix.screen import MDScreen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from database import Database
from datetime import datetime

class TakvimEkrani(MDScreen):
    def on_enter(self):
        """Ekran her açıldığında veritabanından güncel verileri çeker."""
        self.clear_widgets() # Ekranı temizle (üst üste binmemesi için)
        self.db = Database()
        self.layout = BoxLayout(orientation='vertical', padding=10)
        
        # Başlık
        self.layout.add_widget(Label(text="İlaç Takip Takvimi", size_hint_y=0.1, color=(0,0,0,1)))
        
        # Takvim Izgarası (7 sütun - haftanın günleri için)
        self.grid = GridLayout(cols=7, spacing=5)
        self.takvimi_olustur()
        
        self.layout.add_widget(self.grid)
        self.add_widget(self.layout)

    def takvimi_olustur(self):
        bugun = datetime.now().strftime('%Y-%m-%d')
        
        # Veritabanından bugünün durumunu al
        # gun_ikonunu_hesapla fonksiyonu ✅, ❌ veya ⚠️ döner
        durum_verisi = self.db.gun_ikonunu_hesapla(bugun)
        
        # Örnek olarak 1'den 30'a kadar günleri çiziyoruz
        for gun in range(1, 31):
            gun_box = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
            
            # Gün Numarası
            gun_box.add_widget(Label(text=str(gun), color=(0,0,0,1)))
            
            # Eğer döngüdeki gün "Bugün" ise ve veritabanında "ALINDI" kaydı varsa
            # (Basitlik olması için sadece bugüne odaklanıyoruz)
            if gun == datetime.now().day:
                if durum_verisi["status"] == "ALL_TAKEN":
                    # YEŞİL TİK EKLEME
                    # Not: assets klasöründe 'check.png' olduğunu varsayıyoruz
                    tik_ikonu = Image(source='assets/check.png') 
                    gun_box.add_widget(tik_ikonu)
                else:
                    # Alınmadıysa veya eksikse durum ikonunu metin olarak bas
                    gun_box.add_widget(Label(text=durum_verisi["icon"], font_name="Arial"))
            
            self.grid.add_widget(gun_box)
