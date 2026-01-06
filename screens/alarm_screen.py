# alarm_demo.py
# ============================================================
# TEK BAŞINA ÇALIŞAN DEMO (Kivy)
# - Ekran açar (beyaz)
# - Üstten "Android bildirimi gibi" banner düşürür (GARANTİ görünür)
# - Alarmı 10 saniye sonrasına kurar
# - İstersen butonla da tetiklersin
# - plyer varsa aynı anda sistem bildirimi de dener (yoksa çökmez)
#
# Çalıştır:
#   python alarm_demo.py
# ============================================================

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.animation import Animation

# plyer opsiyonel: yoksa crash olmasın
try:
    from plyer import notification
except Exception:
    notification = None


class TopBanner(FloatLayout):
    """Üstten kayan bildirim bannerı (uygulama içi)."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (1, None)
        self.height = dp(92)
        self.x = 0
        self.y = Window.height + dp(20)  # başlangıç: ekran dışı

        # Arka plan (pastel kart)
        from kivy.graphics import Color, RoundedRectangle
        with self.canvas.before:
            Color(0.96, 0.95, 1.00, 1)  # çok açık mor/pastel
            self.bg = RoundedRectangle(pos=self.pos, size=(Window.width, self.height), radius=[dp(18)])

        # Başlık
        self.title = Label(
            text="Tiroidim",
            size_hint=(1, None),
            height=dp(32),
            pos_hint={"top": 1},
            halign="left",
            valign="middle",
            padding=(dp(16), 0),
            color=(0.1, 0.1, 0.1, 1),  # siyah
            bold=True
        )
        self.title.bind(size=lambda inst, val: setattr(inst, "text_size", val))

        # Mesaj
        self.msg = Label(
            text="",
            size_hint=(1, None),
            height=dp(46),
            pos_hint={"y": 0},
            halign="left",
            valign="middle",
            padding=(dp(16), 0),
            color=(0.2, 0.2, 0.2, 1)
        )
        self.msg.bind(size=lambda inst, val: setattr(inst, "text_size", val))

        self.add_widget(self.title)
        self.add_widget(self.msg)

        Window.bind(size=self._on_resize)

    def _on_resize(self, *_):
        self.bg.size = (Window.width, self.height)
        self.bg.pos = self.pos

    def _sync_bg(self, *_):
        self.bg.pos = self.pos

    def show(self, title: str, message: str, duration_sec: float = 12.0):
        self.title.text = title
        self.msg.text = message

        # Görünsün diye üstten biraz aşağı indiriyoruz
        target_y = Window.height - self.height - dp(24)

        anim_in = Animation(y=target_y, duration=0.25, t="out_quad")
        anim_in.bind(on_progress=self._sync_bg)
        anim_in.start(self)

        # Uzun kalsın
        Clock.schedule_once(lambda *_: self.hide(), duration_sec)

    def hide(self):
        anim_out = Animation(y=Window.height + dp(20), duration=0.25, t="in_quad")
        anim_out.bind(on_progress=self._sync_bg)
        anim_out.start(self)


class Root(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Window.clearcolor = (1, 1, 1, 1)  # beyaz ekran

        self.banner = TopBanner()
        self.add_widget(self.banner)

        # Buton: elle tetikle
        btn = Button(
            text="Alarmı Test Et (Banner Göster)",
            size_hint=(None, None),
            size=(dp(280), dp(54)),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_normal="",
            background_color=(0.42, 0.17, 1.0, 1),  # mor buton
            color=(1, 1, 1, 1),
        )
        btn.bind(on_release=lambda *_: self.fire_alarm(med="Levotiron", time_text="09:00"))
        self.add_widget(btn)

        # Otomatik: 2 saniye sonra “alarm 10 sn sonra çalacak” diye banner
        Clock.schedule_once(lambda *_: self.banner.show(
            "Tiroidim", "Demo kuruldu: 10 saniye sonra alarm bannerı gelecek ✅", 4.0
        ), 1.0)

        # Alarmı 10 saniye sonraya kur
        Clock.schedule_once(lambda *_: self.fire_alarm(med="Levotiron", time_text="09:00"), 10.0)

    def fire_alarm(self, med: str, time_text: str):
        title = f"Tiroidim • {med}"
        message = f"Saat: {time_text} — Lütfen ilacını almayı unutma 💊"

        # 1) Uygulama içi banner (GARANTİ görünür)
        self.banner.show(title, message, duration_sec=15.0)

        # 2) Sistem bildirimi (plyer varsa dener; yoksa çökmez)
        if notification is not None:
            try:
                notification.notify(title=title, message=message, timeout=10)
            except Exception as e:
                print("Sistem bildirimi gönderilemedi:", e)
        else:
            print("[INFO] plyer yok -> sadece banner gösterildi.")


class AlarmDemoApp(App):
    def build(self):
        return Root()


if __name__ == "__main__":
    AlarmDemoApp().run()
