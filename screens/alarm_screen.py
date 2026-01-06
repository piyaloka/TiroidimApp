# screens/alarm_screen.py
# ======================================================
# Alarm & Bildirim Screen Modülü
# - main.py'ye dokunulmadan kullanılmak üzere yazıldı
# - Uygulama AÇIKKEN alarm saatini kontrol eder
# - Saat gelince Android üst bildirim gönderir
#
# NOT:
# Bu modül "screen bazlı"dır.
# Android'de uygulama tamamen kapalıyken çalışması
# native (AlarmManager) gerektirir.
# ======================================================

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from datetime import datetime
from plyer import notification


class AlarmScreen(Screen):
    """
    Screen tabanlı alarm ve bildirim örneği.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ÖRNEK alarm saati (HH:MM)
        # Normalde bu saat ayarlardan / DB'den gelir
        self.alarm_hour = 9
        self.alarm_minute = 0

        self._alarm_triggered_today = False

    def on_enter(self):
        """
        Screen açıldığında alarm kontrolünü başlatır.
        """
        Clock.schedule_interval(self.check_alarm, 1)

    def on_leave(self):
        """
        Screen kapatıldığında kontrolü durdurur.
        """
        Clock.unschedule(self.check_alarm)

    def check_alarm(self, dt):
        now = datetime.now()

        # Gün değiştiyse alarm tekrar aktif olsun
        if now.hour == 0 and now.minute == 0:
            self._alarm_triggered_today = False

        if self._alarm_triggered_today:
            return

        # Saat ve dakika eşleşirse alarm çalar
        if now.hour == self.alarm_hour and now.minute == self.alarm_minute:
            self.send_notification()
            self._alarm_triggered_today = True

    def send_notification(self):
        """
        Android / Desktop üst bildirim gönderir.
        """
        try:
            notification.notify(
                title="Tiroidim",
                message="İlaç saatin geldi. Lütfen ilacını almayı unutma 💊",
                timeout=10
            )
        except Exception as e:
            print("Bildirim gönderilemedi:", e)
