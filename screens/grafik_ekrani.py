import io
import matplotlib.pyplot as plt
from datetime import datetime

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from database import Database

# --- KV TASARIMI ---
kv_grafik = """
<GrafikEkrani>:
    name: "grafik"
    md_bg_color: 1, 1, 1, 1
    
    MDFloatLayout:
        
        # --- ANA İÇERİK YAPISI (Dikey) ---
        MDBoxLayout:
            orientation: 'vertical'
            
            # --- 1. ÜST BAR (Dashboard ile Aynı) ---
            MDBoxLayout:
                size_hint_y: None
                height: "70dp"
                padding: ["18dp", "8dp", "20dp", "8dp"]
                spacing: "6dp"
                md_bg_color: 1, 1, 1, 1
                
                # SOL ÜST: Profil Butonu
                MDIconButton:
                    icon: "account-circle"
                    theme_text_color: "Custom"
                    text_color: 0.2, 0.2, 0.2, 1
                    on_release: root.open_profile() # Düzenleme sayfasına gider
                
                Widget: # Boşluk
                
                # ORTA: Logo
                Image:
                    source: "assets/logo_mor.png"
                    size_hint: None, None
                    size: "45dp", "45dp"
                    allow_stretch: True
                    keep_ratio: True
                
                Widget: # Boşluk

                # SAĞ ÜST: Ayarlar Butonu
                MDIconButton:
                    icon: "cog"
                    theme_text_color: "Custom"
                    text_color: 0.2, 0.2, 0.2, 1
                    on_release: root.open_settings() # Ayarlar sayfasına gider

            # --- 2. GRAFİK BAŞLIĞI ---
            MDLabel:
                text: "Analiz ve Grafikler"
                font_style: "H5"
                bold: True
                theme_text_color: "Custom"
                text_color: 0.2, 0.1, 0.35, 1
                halign: "center"
                size_hint_y: None
                height: "40dp"

            # --- 3. SCROLL EDİLEBİLİR İÇERİK ---
            MDScrollView:
                bar_width: 0
                MDBoxLayout:
                    orientation: 'vertical'
                    adaptive_height: True
                    # Alt tarafa (130dp) boşluk bırakıyoruz ki menü butonları içeriği kapatmasın
                    padding: ["20dp", "10dp", "20dp", "130dp"] 
                    spacing: "20dp"

                    # GRAFİK KARTI
                    MDCard:
                        size_hint_y: None
                        height: "320dp"
                        radius: [25,]
                        elevation: 0
                        padding: "10dp"
                        orientation: 'vertical'
                        md_bg_color: [0.96, 0.96, 0.98, 1]
                        
                        MDLabel:
                            text: "TSH - T3 - T4 Değişimi"
                            font_style: "Caption"
                            bold: True
                            size_hint_y: None
                            height: "20dp"
                            theme_text_color: "Secondary"
                            halign: "center"

                        # Grafik Resmi Buraya Gelecek
                        MDBoxLayout:
                            id: chart_box
                            orientation: 'vertical'
                            size_hint: 1, 1

                    # LİSTE BAŞLIĞI
                    MDLabel:
                        text: "Laboratuvar Geçmişi"
                        font_style: "H6"
                        bold: True
                        adaptive_height: True
                        theme_text_color: "Custom"
                        text_color: 0.2, 0.1, 0.35, 1
                        padding: [0, "10dp", 0, 0]

                    # SONUÇLAR LİSTESİ
                    MDBoxLayout:
                        id: results_list
                        orientation: 'vertical'
                        adaptive_height: True
                        spacing: "15dp"

        # --- ALT NAVİGASYON (YÜZEN KART) ---
        MDCard:
            size_hint: 0.95, None
            height: "70dp"
            pos_hint: {"center_x": .5, "center_y": .06}
            radius: [35,]
            elevation: 2 
            md_bg_color: [1, 1, 1, 0.98]
            
            MDBoxLayout:
                # AYAR: Sağ taraftaki boşluğu 135dp yaptık (Simgeler sola kaydı)
                padding: ["25dp", 0, "135dp", 0] 
                spacing: "30dp"
                
                # --- ANASAYFA (PASİF - SİYAH) ---
                MDIconButton:
                    icon: "home-outline"
                    theme_icon_color: "Custom"
                    icon_color: [0.2, 0.2, 0.2, 1] 
                    pos_hint: {"center_y": .5}
                    on_release: root.manager.current = "dashboard"
                    size_hint_x: 0.5
                
                # --- TAKVİM (PASİF - SİYAH) ---
                MDIconButton:
                    icon: "calendar-month-outline"
                    theme_icon_color: "Custom"
                    icon_color: [0.2, 0.2, 0.2, 1] 
                    pos_hint: {"center_y": .5}
                    on_release: root.manager.current = "takvim"
                    size_hint_x: 0.5

                # --- GRAFİK (AKTİF - MOR) ---
                MDIconButton:
                    icon: "chart-line"
                    theme_icon_color: "Custom"
                    icon_color: [0.4, 0.1, 0.8, 1] 
                    md_bg_color: [0.9, 0.85, 1, 0.5] 
                    pos_hint: {"center_y": .5}
                    size_hint_x: 0.5
                    # Zaten buradayız, tekrar tıklarsa sayfa yenilenebilir
                    on_release: root.on_enter()

        # --- ARTI BUTONU (BÜYÜK & SAĞ ALTA) ---
        MDIconButton:
            icon: "plus"
            icon_size: "60sp"
            size_hint: None, None
            size: "110dp", "110dp"
            pos_hint: {"center_x": .82, "center_y": .09}
            md_bg_color: [0.5, 0.3, 0.9, 1]
            theme_icon_color: "Custom"
            icon_color: [1, 1, 1, 1]
            elevation: 10
            # Direkt olarak İlaç/Tahlil ekleme ekranına yönlendirir
            on_release: root.manager.current = "arti_butonu"
"""

Builder.load_string(kv_grafik)

class GrafikEkrani(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

    def on_enter(self):
        """Ekran her açıldığında verileri tazeleyip grafiği yeniden çizer"""
        self.update_content()

    def open_profile(self):
        """Profil (Düzenleme) ekranına git"""
        self.manager.current = "duzenleme"

    def open_settings(self):
        """Ayarlar ekranına git"""
        self.manager.current = "ayarlar"

    def update_content(self):
        # 1. Temizlik
        self.ids.chart_box.clear_widgets()
        self.ids.results_list.clear_widgets()

        # 2. Veri Çekme
        sonuclar = self.db.get_lab_history() 

        if not sonuclar:
            self.show_no_data()
            return

        # 3. Veri Ayrıştırma
        dates = []
        tsh_vals = []
        t3_vals = []
        t4_vals = []

        for veri in sonuclar:
            date_str = veri[4]
            try:
                dt_obj = datetime.strptime(date_str, "%d/%m/%Y")
                dates.append(dt_obj.strftime("%d/%m"))
            except ValueError:
                dates.append(date_str[:5]) 
            
            tsh_vals.append(float(veri[1]) if veri[1] is not None else None)
            t3_vals.append(float(veri[2]) if veri[2] is not None else None)
            t4_vals.append(float(veri[3]) if veri[3] is not None else None)

        # 4. Grafik Çizme
        self.create_chart_image(dates, tsh_vals, t3_vals, t4_vals)

        # 5. Liste Doldurma (En yeniden eskiye)
        for veri in reversed(sonuclar):
            self.create_result_card(veri)

    def show_no_data(self):
        box = MDBoxLayout(orientation='vertical', spacing="10dp", pos_hint={"center_x": .5, "center_y": .5})
        
        icon = MDIconButton(
            icon="chart-bar",
            icon_size="40sp",
            theme_icon_color="Custom",
            icon_color=[0.8, 0.8, 0.8, 1],
            pos_hint={"center_x": .5}
        )
        
        lbl = MDLabel(
            text="Henüz tahlil verisi bulunamadı.\nSağ alttaki '+' butonuna basıp\nsonuçlarınızı girebilirsiniz.",
            halign="center",
            theme_text_color="Hint",
            font_size="14sp"
        )
        box.add_widget(icon)
        box.add_widget(lbl)
        self.ids.chart_box.add_widget(box)

    def create_chart_image(self, dates, tsh, t3, t4):
        plt.clf()
        fig, ax = plt.subplots(figsize=(5, 3.2), dpi=100)
        
        # Çizgiler
        ax.plot(dates, tsh, marker='o', linestyle='-', color='#6200EA', label='TSH', linewidth=2)
        ax.plot(dates, t3, marker='s', linestyle='--', color='#FF9800', label='T3', linewidth=2)
        ax.plot(dates, t4, marker='^', linestyle=':', color='#009688', label='T4', linewidth=2)

        # Tasarım
        ax.set_facecolor('#F8F8FA')
        fig.patch.set_facecolor('#F8F8FA')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#DDDDDD')
        ax.spines['bottom'].set_color('#DDDDDD')
        
        ax.grid(True, linestyle='--', alpha=0.3, color='gray')
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3, frameon=False, fontsize=9)
        
        ax.tick_params(axis='x', labelsize=8, rotation=15, colors="#555555") 
        ax.tick_params(axis='y', labelsize=8, colors="#555555")
        
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)

        im_data = CoreImage(buf, ext='png')
        
        img_widget = Image(
            texture=im_data.texture,
            allow_stretch=True, 
            keep_ratio=False
        )
        
        self.ids.chart_box.add_widget(img_widget)

    def create_result_card(self, veri):
        card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height="90dp",
            radius=[20,],
            padding="12dp",
            elevation=0,
            md_bg_color=[0.98, 0.98, 1, 1],
            line_color=[0, 0, 0, 0.05],
            line_width=1
        )

        lbl_date = MDLabel(
            text=f"Tarih: {veri[4]}", 
            font_style="Subtitle2", 
            theme_text_color="Primary", 
            bold=True, 
            adaptive_height=True
        )
        card.add_widget(lbl_date)

        values_box = MDBoxLayout(orientation='horizontal', spacing="10dp", padding=[0, "5dp", 0, 0])
        
        val_tsh = veri[1] if veri[1] is not None else "-"
        val_t3 = veri[2] if veri[2] is not None else "-"
        val_t4 = veri[3] if veri[3] is not None else "-"

        values_box.add_widget(self.make_val_box("TSH", val_tsh, "mIU/L", "#6200EA"))
        values_box.add_widget(self.make_val_box("T3", val_t3, "pg/mL", "#FF9800"))
        values_box.add_widget(self.make_val_box("T4", val_t4, "ng/dL", "#009688"))

        card.add_widget(values_box)
        self.ids.results_list.add_widget(card)

    def make_val_box(self, label, value, unit, color_hex):
        box = MDBoxLayout(orientation='vertical', size_hint_x=1)
        
        lbl_title = MDLabel(
            text=label, 
            font_style="Caption", 
            halign="center", 
            theme_text_color="Custom", 
            text_color=get_color_from_hex(color_hex),
            bold=True
        )
        
        lbl_val = MDLabel(
            text=str(value), 
            font_style="Body1", 
            halign="center", 
            bold=True
        )
        
        lbl_unit = MDLabel(
            text=unit, 
            font_style="Overline", 
            halign="center", 
            theme_text_color="Secondary"
        )
        
        box.add_widget(lbl_title)
        box.add_widget(lbl_val)
        box.add_widget(lbl_unit)
        return box