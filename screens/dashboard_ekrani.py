from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line
from kivy.core.window import Window

# Daha kompakt oran
Window.size = (390, 720)
Window.clearcolor = (0.95, 0.97, 1, 1)  # çok hafif mavi-beyaz arka plan


class Card(ButtonBehavior, BoxLayout):
    """
    Genel kart komponenti: beyaz arka plan, hafif shadow, radius
    """
    def __init__(self, title="", subtitle="", height=95, **kwargs):
        super().__init__(orientation="horizontal",
                         padding=(22, 14),
                         spacing=4,
                         **kwargs)
        self.size_hint_y = None
        self.height = height

        with self.canvas.before:
            # Gölge
            Color(0, 0, 0, 0.05)
            self.shadow = RoundedRectangle(radius=[18],
                                           pos=(self.x, self.y - 3),
                                           size=(self.width, self.height))
            # Kart arka planı
            Color(1, 1, 1, 1)
            self.bg = RoundedRectangle(radius=[18],
                                       pos=self.pos,
                                       size=self.size)
            # Hafif kontür
            Color(0.8, 0.85, 0.95, 0.8)
            self.border = Line(rounded_rectangle=(self.x, self.y,
                                                  self.width, self.height, 18),
                               width=1)

        self.bind(pos=self._update_bg, size=self._update_bg)

        # Sol tarafta başlık + alt açıklama için dikey içerik alanı
        self.content_box = BoxLayout(orientation="vertical",
                                     spacing=4,
                                     size_hint_x=0.85)
        self.add_widget(self.content_box)

        # Başlık
        self.title_label = Label(
            text=title,
            halign="left",
            valign="middle",
            color=(0.0, 0.0, 0.0, 1),
            font_size=25,
            bold=True,
            font_name="Roboto-Bold",
            size_hint_y=None,
            height=30,
        )
        self.title_label.bind(size=self._update_text_size)
        self.content_box.add_widget(self.title_label)

        # Alt açıklama
        if subtitle:
            self.subtitle_label = Label(
                text=subtitle,
                halign="left",
                valign="top",
                color=(0.38, 0.4, 0.45, 1),
                font_size=19,
                font_name="Roboto-Regular",
            )
            self.subtitle_label.bind(size=self._update_text_size)
            self.content_box.add_widget(self.subtitle_label)

        # Sağ tarafa '>' ikonu (menü olduğunu belirtmek için)
        arrow = Label(
            text=">",
            color=(0, 0, 0, 0.25),   # düşük opaklık
            font_size=32,
            bold=True,
            size_hint=(None, None),
            size=(36, 36),
            halign="right",
            valign="middle",
        )
        arrow.bind(size=self._update_text_size)

        # Sağ tarafa sabitle – kartın ortasında hizalanmış ok
        arrow_layout = AnchorLayout(anchor_x="right", anchor_y="center",
                                    size_hint=(None, 1))
        arrow_layout.width = 40
        arrow_layout.add_widget(arrow)
        self.add_widget(arrow_layout)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.shadow.pos = (self.x, self.y - 3)
        self.shadow.size = self.size
        if hasattr(self, "border"):
            self.border.rounded_rectangle = (
                self.x,
                self.y,
                self.width,
                self.height,
                18,
            )

    def _update_text_size(self, instance, value):
        instance.text_size = value

    def on_press(self):
        # Hafif press efekti
        with self.canvas.before:
            Color(0, 0, 0, 0.07)
            self.shadow = RoundedRectangle(radius=[18],
                                           pos=(self.x, self.y - 2),
                                           size=self.size)
            Color(0.97, 0.98, 1, 1)
            self.bg = RoundedRectangle(radius=[18],
                                       pos=self.pos,
                                       size=self.size)

    def on_release(self):
        with self.canvas.before:
            Color(0, 0, 0, 0.05)
            self.shadow = RoundedRectangle(radius=[18],
                                           pos=(self.x, self.y - 3),
                                           size=self.size)
            Color(1, 1, 1, 1)
            self.bg = RoundedRectangle(radius=[18],
                                       pos=self.pos,
                                       size=self.size)


class BriefReviewCard(Card):
    """
    Üstteki “Tiroid Özeti” kartı – 3 satırlı özet
    """
    def __init__(self, **kwargs):
        super().__init__(title="", subtitle="", height=170, **kwargs)

        self.clear_widgets()

        # İçerik: üstte hizalanmış dikey layout
        inner = BoxLayout(orientation="vertical",
                          padding=(0, 0, 0, 0),
                          spacing=2,
                          size_hint_y=None)
        inner.bind(minimum_height=inner.setter("height"))

        title = Label(
            text="Tiroid Özeti",
            halign="left",
            valign="middle",
            color=(0, 0, 0, 1),
            font_size=28,
            bold=True,
            font_name="Roboto-Bold",
            size_hint_y=None,
            height=32,
        )
        title.bind(size=self._update_text_size)
        inner.add_widget(title)

        info_layout = GridLayout(cols=1,
                                 spacing=2,
                                 size_hint_y=None,
                                 padding=(0, 2, 0, 0))
        info_layout.bind(minimum_height=info_layout.setter("height"))

        def row(label, value):
            box = BoxLayout(orientation="horizontal",
                            size_hint_y=None,
                            height=28)
            l1 = Label(
                text=label,
                halign="left",
                valign="middle",
                color=(0.4, 0.42, 0.48, 1),
                font_size=20,
                font_name="Roboto-Regular",
            )
            l1.size_hint_x = 0.6
            l1.bind(size=self._update_text_size)

            l2 = Label(
                text=value,
                halign="right",
                valign="middle",
                color=(0.0, 0.0, 0.0, 1),
                font_size=23,
                bold=True,
                font_name="Roboto-Bold",
            )
            l2.size_hint_x = 0.4
            l2.bind(size=self._update_text_size)
            box.add_widget(l1)
            box.add_widget(l2)
            return box

        info_layout.add_widget(row("Son ilaç dozu", "75 mcg"))
        info_layout.add_widget(row("Son TSH sonucu", "2.8 mIU/L"))
        info_layout.add_widget(row("Uyum yüzdesi", "%82"))
        inner.add_widget(info_layout)

        # Sol kısım: içeriği kartın üstüne sabitle
        left_anchor = AnchorLayout(anchor_x="left", anchor_y="top")
        left_anchor.add_widget(inner)

        # Sağ tarafa '>' ikonu (menü olduğunu belirtmek için)
        arrow = Label(
            text=">",
            color=(0, 0, 0, 0.25),   # düşük opaklık
            font_size=32,
            bold=True,
            size_hint=(None, None),
            size=(36, 36),
            halign="right",
            valign="middle",
        )
        arrow.bind(size=self._update_text_size)

        arrow_layout = AnchorLayout(anchor_x="right", anchor_y="center",
                                    size_hint=(None, 1))
        arrow_layout.add_widget(arrow)

        # Tümünü yatay bir layout içinde topla
        root = BoxLayout(orientation="horizontal",
                         padding=(0, 0, 0, 0),
                         spacing=0)
        root.add_widget(left_anchor)
        root.add_widget(arrow_layout)

        self.add_widget(root)


class Header(RelativeLayout):
    """
    Apple Health tarzı üst header: gradient hissi + “Merhaba, Kullanıcı”
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 194

        with self.canvas.before:
            # Üstte pastel pembe, alta doğru açık mavi hissi
            Color(1.0, 0.82, 0.9, 1)
            self.bg_top = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[0, 0, 26, 26],
            )

        self.bind(pos=self._update_bg, size=self._update_bg)

        content = BoxLayout(orientation="horizontal",
                            padding=(22, 24, 12, 18),
                            spacing=16)
        left = BoxLayout(orientation="vertical", spacing=4)

        # Küçük uygulama adı
        app_label = Label(
            text="TiroidApp",
            halign="left",
            valign="middle",
            color=(0.35, 0.35, 0.55, 1),
            font_size=18,
            bold=True,
            font_name="Roboto-Bold",
            size_hint_y=None,
            height=24,
        )
        app_label.bind(size=self._update_text_size)

        # Büyük karşılama yazısı
        hello = Label(
            text="Merhaba, Kullanıcı",
            halign="left",
            valign="middle",
            color=(0, 0, 0, 0.95),
            font_size=38,
            bold=True,
            font_name="Roboto-Bold",
            size_hint_y=None,
            height=42,
        )
        hello.bind(size=self._update_text_size)

        # Alt satır: tarih benzeri ikincil bilgi (şimdilik sabit metin)
        subline = Label(
            text="Çarşamba, 29 Aralık",
            halign="left",
            valign="top",
            color=(0.35, 0.35, 0.65, 1),
            font_size=20,
            font_name="Roboto-Regular",
            size_hint_y=None,
            height=28,
        )
        subline.bind(size=self._update_text_size)

        left.add_widget(app_label)
        left.add_widget(hello)
        left.add_widget(subline)

        # Sağ taraf: Ayarlar ikonu + profil foto yuvarlak
        right_box = BoxLayout(orientation="horizontal",
                              spacing=6,
                              size_hint=(None, 1))
        right_box.bind(minimum_width=right_box.setter("width"))

        # Ayarlar ikonu: mor yuvarlak arka plan + gear resmi
        settings_container = RelativeLayout(size_hint=(None, None),
                                            size=(90, 90))
        with settings_container.canvas.before:
            Color(0.70, 0.55, 0.98, 1)  # açık mor (FAB ile arka plan arası)
            settings_container.bg = Ellipse(pos=settings_container.pos,
                                           size=settings_container.size)

        def update_settings_bg(instance, value):
            settings_container.bg.pos = settings_container.pos
            settings_container.bg.size = settings_container.size

        settings_container.bind(pos=update_settings_bg, size=update_settings_bg)

        settings_icon = Image(
            source="settings Background Removed.png",
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(0.58, 0.58),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        settings_container.add_widget(settings_icon)

        # Profil avatar: beyaz yuvarlak arka plan + kullanıcı resmi
        profile = RelativeLayout(size_hint=(None, None),
                                 size=(110, 110))
        with profile.canvas.before:
            Color(1, 1, 1, 1)
            profile.bg = Ellipse(pos=profile.pos, size=profile.size)
        profile.bind(pos=lambda inst, val: setattr(profile.bg, "pos", val),
                     size=lambda inst, val: setattr(profile.bg, "size", val))

        profile_image = Image(
            source="account-icon-user-icon-vector-graphics_292645-552 Background Removed.png",
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(0.86, 0.86),
            pos_hint={"center_x": 0.5, "center_y": 0.428},
        )
        profile.add_widget(profile_image)

        right_box.add_widget(settings_container)
        right_box.add_widget(profile)

        content.add_widget(left)
        content.add_widget(right_box)
        self.add_widget(content)

    def _update_bg(self, *args):
        self.bg_top.pos = self.pos
        self.bg_top.size = self.size

    def _update_text_size(self, instance, value):
        instance.text_size = value


class DashboardScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        # HEADER
        self.header = Header()
        self.add_widget(self.header)

        # Orta alan: Scrollable içerik + fab
        body = FloatLayout()
        self.add_widget(body)

        scroll = ScrollView(size_hint=(1, 1))
        body.add_widget(scroll)

        content = BoxLayout(orientation="vertical",
                            padding=(14, 2, 14, 10),  # üst boşluk azaltıldı
                            spacing=10,
                            size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))
        scroll.add_widget(content)

        # 1) Tiroid Özeti
        self.brief_card = BriefReviewCard()
        content.add_widget(self.brief_card)

        # 2-5) Alt kartlar: Takvim, İlaçlar, Lab, Semptomlar
        self.section_cards = []

        takvim_card = Card(
            title="Takvim & Hatırlatıcılar",
            subtitle="Yaklaşan ilaç saatleri ve randevular burada listelenecek.",
            height=95,
        )
        self.section_cards.append(takvim_card)
        content.add_widget(takvim_card)

        ilac_card = Card(
            title="İlaçlar",
            subtitle="Günlük dozlar ve kullanım geçmişi burada özetlenecek.",
            height=95,
        )
        self.section_cards.append(ilac_card)
        content.add_widget(ilac_card)

        lab_card = Card(
            title="Laboratuvar Sonuçları",
            subtitle="TSH / T3 / T4 değerleri ve trendler burada gösterilecek.",
            height=95,
        )
        self.section_cards.append(lab_card)
        content.add_widget(lab_card)

        semptom_card = Card(
            title="Son Semptomlar",
            subtitle="Son girilen semptomlar ve şiddet puanları listelenecek.",
            height=95,
        )
        self.section_cards.append(semptom_card)
        content.add_widget(semptom_card)

        # Pencere boyutu değiştiğinde kart yüksekliklerini yeniden hesapla
        from kivy.core.window import Window as CoreWindow
        CoreWindow.bind(size=self.on_window_resize)
        # Başlangıçta da bir kez çağır
        self.on_window_resize(CoreWindow, CoreWindow.size)

        # Floating Quick Add butonu – TAM YUVARLAK
        fab = Button(
            text="+",
            font_size=42,
            size_hint=(None, None),
            size=(90, 90),
            pos_hint={"right": 0.94, "y": 0.05},
            background_normal="",
            background_color=(0, 0, 0, 0),  # arka planı transparan yap
            color=(1, 1, 1, 1),
        )
        with fab.canvas.before:
            Color(0.55, 0.35, 0.95, 1)
            fab.bg = Ellipse(pos=fab.pos, size=fab.size)

        def update_fab_bg(instance, value):
            fab.bg.pos = fab.pos
            fab.bg.size = fab.size

        fab.bind(pos=update_fab_bg, size=update_fab_bg)
        body.add_widget(fab)

    def on_window_resize(self, instance, size):
        # Yükseklik bazlı oranla kartları yeniden boyutlandır
        width, height = size
        # Üst özet kartı pencerenin yaklaşık %26'sı kadar olsun
        if hasattr(self, "brief_card"):
            self.brief_card.height = height * 0.26
        # Alt kartlar pencerenin yaklaşık %18'i kadar olsun
        if hasattr(self, "section_cards"):
            for card in self.section_cards:
                card.height = height * 0.18


class TiroidDashboardApp(App):
    def build(self):
        self.title = "TiroidApp"
        return DashboardScreen()


if __name__ == "__main__":
    TiroidDashboardApp().run()
        
