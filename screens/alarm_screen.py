# alarm_visual_demo.py
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.animation import Animation

# İstersen gerçek sistem bildirimi de denensin:
try:
    from plyer import notification
except Exception:
    notification = None


class NotificationBanner(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (1, None)
        self.height = dp(90)

        # Başlangıçta ekranın üstünün dışında
        self.pos = (0, Window.height + dp(10))

        # Yazılar
        self.title_label = Label(
            text="Tiroidim",
            size_hint=(1, None),
            height=dp(30),
            pos_hint={"top": 1},
            halign="left",
            valign="middle",
            padding=(dp(16), 0),
            color=(0, 0, 0, 1),  # siyah
            bold=True,
        )
        self.title_label.bind(size=lambda inst, val: setattr(inst, "text_size", val))

        self.msg_label = Label(
            text="İlaç saatin geldi 💊",
            size_hint=(1, None),
            height=dp(45),
            pos_hint={"y": 0.05},
            halign="left",
            valign="middle",
            padding=(dp(16), 0),
            color=(0, 0, 0, 1),  # siyah
        )
        self.msg_label.bind(size=lambda inst, val: setattr(inst, "text_size", val))

        # Arka plan: açık gri kart
        from kivy.graphics import Color, RoundedRectangle
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self._bg = RoundedRectangle(pos=self.pos, size=(Window.width, self.height), radius=[dp(16)])

        self.add_widget(self.title_label)
        self.add_widget(self.msg_label)

        Window.bind(size=self._on_window_resize)

    def _on_window_resize(self, *_):
        self._bg.size = (Window.width, self.height)
        self.x = 0
        self._bg.pos = self.pos

    def _sync_bg(self, *_):
        self._bg.pos = self.pos

    def show(self, title: str, message: str, duration_sec: float = 15):
        self.title_label.text = title
        self.msg_label.text = message

        # Üstten biraz aşağı indir (garanti görünür)
        target_y = Window.height - self.height - dp(40)

        anim_in = Animation(y=target_y, duration=0.25, t="out_quad")
        anim_in.bind(on_progress=self._sync_bg)
        anim_in.start(self)

        # duration sonra kapat
        Clock.schedule_once(lambda *_: self.hide(), duration_sec)

    def hide(self):
        anim_out = Animation(y=Window.height + dp(10), duration=0.25, t="in_quad")
        anim_out.bind(on_progress=self._sync_bg)
        anim_out.start(self)


class Root(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Window.clearcolor = (1, 1, 1, 1)  # beyaz arka plan

        self.banner = NotificationBanner()
        self.add_widget(self.banner)

        # Ekranda manuel test butonu (garanti)
        btn = Button(
            text="Bildirimi Göster",
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        btn.bind(on_release=lambda *_: self.fire())
        self.add_widget(btn)

        # Otomatik olarak 2 sn sonra da göster
        Clock.schedule_once(lambda *_: self.fire(), 2)

    def fire(self):
        title = "Tiroidim"
        message = "İlaç saatin geldi. Lütfen ilacını almayı unutma 💊"

        # Uygulama içi mock banner (ekran görüntüsü için en garantisi)
        self.banner.show(title, message, duration_sec=15)

        # Gerçek sistem bildirimi (varsa)
        if notification is not None:
            try:
                notification.notify(title=title, message=message, timeout=10)
            except Exception as e:
                print("Sistem bildirimi gönderilemedi:", e)
        else:
            print("[INFO] plyer yok, sistem bildirimi atlanıyor.")


class DemoApp(App):
    def build(self):
        return Root()


if __name__ == "__main__":
    DemoApp().run()
