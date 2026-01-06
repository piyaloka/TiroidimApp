# screens/alarm_screen.py
# ======================================================
# Alarm & Bildirim Screen Modülü (Uygulama AÇIKKEN)
# - main.py'ye dokunmadan modül olarak eklenebilir
# - Screen açılınca alarm saatini kontrol eder
# - Saat gelince bildirim gönderir
#
# NOT:
# Uygulama tamamen kapalıyken çalışması için native (AlarmManager) gerekir.
# ======================================================

from datetime import datetime, date, timedelta

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

# plyer bazı ortamlarda (özellikle desktop test) import edilemeyebilir.
# Bu yüzden crash ettirmiyoruz.
try:
    from plyer import notification
except Exception:
    notification = None


class AlarmScreen(Screen):
    """
    Screen tabanlı alarm ve bildirim örneği (app açıkken çalışır).
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ÖRNEK alarm saati (HH:MM)
        # Normalde bu saat ayarlardan / DB’den gelir
        self.alarm_hour = 9
        self.alarm_minute = 0

        # Clock event referansı: schedule/unschedule hatalarını önler
        self._event = None

        # Spam önlemek için:
        self._last_fired_date = None  # type: date | None
        self._last_fired_at = None    # type: datetime | None
        self._cooldown = timedelta(seconds=60)

    def on_enter(self, *args):
        """
        Screen açıldığında alarm kontrolünü başlatır.
        """
        if self._event is None:
            self._event = Clock.schedule_interval(self.check_alarm, 1.0)

    def on_leave(self, *args):
        """
        Screen kapatıldığında kontrolü durdurur.
        """
        if self._event is not None:
            self._event.cancel()
            self._event = None

    def check_alarm(self, dt):
        now = datetime.now()

        # Saat ve dakika eşleşirse alarm çalar
        if now.hour == self.alarm_hour and now.minute == self.alarm_minute:

            # Aynı gün içinde 1 kez çalsın
            if self._last_fired_date == now.date():
                return

            # Cooldown: aynı dakikada art arda tetiklenmesin
            if self._last_fired_at is not None and (now - self._last_fired_at) < self._cooldown:
                return

            self.send_notification()
            self._last_fired_at = now
            self._last_fired_date = now.date()

    def send_notification(self):
        """
        Android / Desktop üst bildirim gönderir.
        """
        title = "Tiroidim"
        message = "İlaç saatin geldi. Lütfen ilacını almayı unutma "

        # plyer yoksa crash etmeden mock bas
        if notification is None:
            print(f"[BILDIRIM MOCK] {title} - {message}")
            return

        try:
            notification.notify(
                title=title,
                message=message,
                timeout=10
            )
        except Exception as e:
            print("Bildirim gönderilemedi:", e)
