from kivymd.uix.screen import MDScreen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from database import Database # Veritabanı sınıfını dahil ediyoruz
from datetime import datetime

class ArtiButonuEkrani(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database() # Veritabanı nesnesi oluşturuluyor
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Örnek bir ilaç ID'si (Normalde bu seçimden gelmeli)
        self.current_ilac_id = 1 

        # ALDIM BUTONU
        self.btn_aldim = Button(
            text="Aldım",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5}
        )
        self.btn_aldim.bind(on_release=self.aldim_islemi)
        
        # ATLADIM BUTONU
        self.btn_atladim = Button(
            text="Atladım",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5},
            background_color=(0.7, 0.7, 0.7, 1) # Gri
        )
        self.btn_atladim.bind(on_release=self.atladim_islemi)

        layout.add_widget(self.btn_aldim)
        layout.add_widget(self.btn_atladim)
        self.add_widget(layout)

    def aldim_islemi(self, instance):
        # 1. Buton Rengini Mor Yap (Görsel Görev)
        instance.background_color = (0.5, 0, 0.5, 1) # Mor renk
        
        # 2. Veritabanına Kaydet (Veri Görevi)
        bugun = datetime.now().strftime('%Y-%m-%d')
        # numaralı satırdaki ilac_logla fonksiyonunu kullanıyoruz
        self.db.ilac_logla(ilac_id=self.current_ilac_id, tarih=bugun, durum="ALINDI")
        
        print(f"{bugun} tarihi için 'ALINDI' kaydı yapıldı ve buton mor oldu.")

    def atladim_islemi(self, instance):
        # Atladım işlemi için kayıt
        bugun = datetime.now().strftime('%Y-%m-%d')
        self.db.ilac_logla(ilac_id=self.current_ilac_id, tarih=bugun, durum="ATLADI")
        
        # Aldım butonunu eski haline getirebilir veya bu butonu kırmızı yapabilirsin
        self.btn_aldim.background_color = (1, 1, 1, 1) # Beyaz/Varsayılan
        print("İlaç atlandı olarak işaretlendi.")
