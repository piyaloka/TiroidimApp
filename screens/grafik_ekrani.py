# rapor_ekrani.py
from kivymd.uix.screen import MDScreen
from kivy.uix.boxlayout import BoxLayout

# Grafik kütüphaneleri
from graph_lib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

# Üye 2'nin  yazdığın veritabanı sınıfını içe aktarıyoruz
from database import Database

class GrafikEkrani(MDScreen):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        # Veritabanı nesnesini başlatıyoruz. Böylece her seferinde sqlite3.connect 
        self.db = Database()

    def on_enter(self):
        """Ekran her açıldığında grafiği tazelemek için bu fonksiyon tetiklenir."""
        # Eski grafikleri temizleyip yenisini çizmek için içeriği temizliyoruz
        self.clear_widgets() 
        self.ciz_grafik()

    def ciz_grafik(self):
        # Üye 2'nin hazırladığı fonksiyonu çağırıyoruz.
        # Bu fonksiyon verileri (id, tsh, t3, t4, tarih) sırasıyla ve tarihe göre sıralı döner.
        veriler = self.db.get_lab_history()

        # Veritabanında henüz hiç tahlil kaydı yoksa hata vermemesi için kontrol
        if not veriler:
            print("Grafik çizilecek veri bulunamadı!")
            return

        # Veritabanından gelen verileri grafik için listelere ayırıyoruz.
        # Sıralama: v[2] -> T3, v[3] -> T4, v[4] -> Tarih
        tarih_listesi = [v[4] for v in veriler] 
        t3_listesi = [v[2] for v in veriler]    
        t4_listesi = [v[3] for v in veriler]    

        # Grafik çizim alanını temizleyip yeni değerleri giriyoruz
        plt.clf()
        fig, ax = plt.subplots()

        # T3 ve T4 çizgilerini çiziyoruz
        ax.plot(tarih_listesi, t3_listesi, label="T3 Değeri", color="purple", marker='o')
        ax.plot(tarih_listesi, t4_listesi, label="T4 Değeri", color="blue", marker='s')

        # Grafik başlıkları ve isimlendirmeleri
        ax.set_title("Tiroid Hormon Takip Grafiği")
        ax.set_xlabel("Tahlil Tarihi")
        ax.set_ylabel("Değerler")
        ax.legend()
        
        # Tarihlerin birbirine girmemesi için 45 derece döndürüyoruz
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Grafiği Kivy içinde görüntülenebilir bir kutuya ekliyoruz
        kutu = BoxLayout()
        kutu.add_widget(FigureCanvasKivyAgg(fig))

        # Oluşturduğumuz bu grafik kutusunu ana ekrana ekliyoruz
        self.add_widget(kutu)

