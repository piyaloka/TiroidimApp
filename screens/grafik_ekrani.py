import sys
import os
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
# --- EKSİK OLAN SATIR BUYDU: ---
from kivymd.uix.label import MDLabel 
# -------------------------------
import matplotlib.pyplot as plt

# --- 1. DOSYA YOLLARI ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.append(project_root)

# --- 2. KÜTÜPHANELER ---
# Graph Lib
try:
    from graph_lib.backend_kivyagg import FigureCanvasKivyAgg
except ImportError:
    # Bulamazsa sistem kütüphanesini dene
    try:
        from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
    except:
        FigureCanvasKivyAgg = None

# Database
try:
    from database import Database
except ImportError:
    class Database:
        def tahlil_sonuclarini_getir(self):
            return {"tarihler": ["Pzt", "Sal"], "t4": [1.0, 1.2], "t3": [3.0, 3.1]}

# KV Dosyasını Yükle
kv_path = os.path.join(project_root, 'assets', 'grafik.kv')
Builder.load_file(kv_path)

# --- 3. EKRAN KODU ---
class GrafikEkrani(MDScreen):
    def on_enter(self):
        self.grafigi_olustur()

    def grafigi_olustur(self):
        # Kutu kontrolü
        if 'grafik_kutusu' not in self.ids:
            return
            
        box = self.ids.grafik_kutusu
        box.clear_widgets()

        # Verileri Al
        db = Database()
        if hasattr(db, 'tahlil_sonuclarini_getir'):
            veriler = db.tahlil_sonuclarini_getir()
        else:
            veriler = {}

        # Grafik Çiz
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#ffffff')
        ax.set_facecolor('#f9f9f9')
        
        if veriler and "tarihler" in veriler:
            ax.plot(veriler["tarihler"], veriler["t4"], label='T4', color='#6200EE', marker='o')
            ax.plot(veriler["tarihler"], veriler["t3"], label='T3', color='#03DAC6', marker='s')
            ax.legend()

        ax.grid(True, linestyle='--', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Ekrana Ekle
        if FigureCanvasKivyAgg:
            grafik_widget = FigureCanvasKivyAgg(fig)
            box.add_widget(grafik_widget)
        else:
            # İşte hata veren satır burasıydı, artık çalışacak:
            box.add_widget(MDLabel(text="Grafik Kütüphanesi Yüklenemedi!", halign="center"))
            