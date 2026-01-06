# BACKGROUND_ALARM_DEMO_ONEFILE.py
# ============================================================
# AMAÇ:
# - Uygulama KAPALIYKEN de çalışan alarm + üst bildirim
# - MAIN'E DOKUNMADAN (entegrasyon yok), tek dosyada örnek olarak 
#
# GERÇEKLEŞTİRME:
# Android’de arka planda tetikleme için OS seviyesinde:
#   AlarmManager + BroadcastReceiver + NotificationChannel gerekir.
# Bu yüzden native Android tarafında Kotlin/Java kodu şarttır.
#
# Bu dosya "tek yerde her şey" dokümantasyon amaçlıdır:
# 1) Kotlin Receiver (bildirimi basan)
# 2) Kotlin Scheduler (AlarmManager ile alarmı kuran)
# 3) AndroidManifest ekleri
# 4) (Opsiyonel) Python/Kivy içinden Pyjnius ile çağırma örneği
# ============================================================


# ============================================================
# [1] KOTLIN - AlarmReceiver.kt (BroadcastReceiver)
# Dosya yolu (entegrasyon yapılırsa):
# android/app/src/main/java/org/tiroidim/app/AlarmReceiver.kt
# ============================================================

KOTLIN_ALARM_RECEIVER = r"""
package org.tiroidim.app

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat

class AlarmReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        val title = intent.getStringExtra("title") ?: "Tiroidim"
        val message = intent.getStringExtra("message") ?: "İlaç saatin geldi. Lütfen ilacını almayı unutma 💊"

        val channelId = "tiroidim_alarm_channel"
        val nm = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        // Android 8+ Notification Channel zorunlu
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                channelId,
                "İlaç Hatırlatıcıları",
                NotificationManager.IMPORTANCE_HIGH
            )
            nm.createNotificationChannel(channel)
        }

        val notification = NotificationCompat.Builder(context, channelId)
            // demo için sistem ikonu; projede kendi small icon'la değiştirilir
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentTitle(title)
            .setContentText(message)
            .setAutoCancel(true)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .build()

        nm.notify(1001, notification)
    }
}
"""


# ============================================================
# [2] KOTLIN - AlarmScheduler.kt (AlarmManager ile alarm kurma)
# Dosya yolu (entegrasyon yapılırsa):
# android/app/src/main/java/org/tiroidim/app/AlarmScheduler.kt
# ============================================================

KOTLIN_ALARM_SCHEDULER = r"""
package org.tiroidim.app

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent

object AlarmScheduler {

    fun scheduleExact(
        context: Context,
        triggerAtMillis: Long,
        title: String = "Tiroidim",
        message: String = "İlaç saatin geldi. Lütfen ilacını almayı unutma 💊"
    ) {
        val intent = Intent(context, AlarmReceiver::class.java).apply {
            putExtra("title", title)
            putExtra("message", message)
        }

        val pendingIntent = PendingIntent.getBroadcast(
            context,
            1001,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val am = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager

        // Uygulama kapalı olsa bile, sistem belirlenen zamanda receiver'ı çağırır.
        // setExactAndAllowWhileIdle: Doze'da bile mümkün olduğunca çalıştırmaya çalışır.
        am.setExactAndAllowWhileIdle(
            AlarmManager.RTC_WAKEUP,
            triggerAtMillis,
            pendingIntent
        )
    }

    fun cancel(context: Context) {
        val intent = Intent(context, AlarmReceiver::class.java)
        val pendingIntent = PendingIntent.getBroadcast(
            context,
            1001,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        val am = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
        am.cancel(pendingIntent)
    }
}
"""


# ============================================================
# [3] AndroidManifest.xml EKLERİ
# Entegrasyon yapılırsa:
# android/app/src/main/AndroidManifest.xml içinde uygun yerlere eklenir
# ============================================================

ANDROID_MANIFEST_SNIPPETS = r"""
<!-- Permissions (Android 13+ bildirim izni) -->
<uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>

<!-- Exact alarm izni (Android 12+ bazı cihazlarda gerekli olabilir) -->
<uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM"/>

<application ...>

    <!-- Receiver kaydı -->
    <receiver
        android:name="org.tiroidim.app.AlarmReceiver"
        android:exported="false" />

</application>
"""


# ============================================================
# [4] PYTHON'DAN ÇAĞIRMA ÖRNEĞİ (ENTEGRASYON YAPILIRSA)
# Bu kod, main'e eklenmeden gösterim amaçlıdır.
# Pyjnius ile Kotlin AlarmScheduler çağırır.
# ============================================================

PYTHON_CALL_EXAMPLE = r"""
# Bu çağrı örneği, Kivy tarafında herhangi bir yerde kullanılabilir.
# (Örn: ayarlardan alarm kur butonuna basınca)
from jnius import autoclass
import time

PythonActivity = autoclass("org.kivy.android.PythonActivity")
AlarmScheduler = autoclass("org.tiroidim.app.AlarmScheduler")

ctx = PythonActivity.mActivity

# Örnek: 60 saniye sonra çalsın
trigger_ms = int((time.time() + 60) * 1000)

AlarmScheduler.scheduleExact(
    ctx,
    trigger_ms,
    "Tiroidim",
    "İlaç saatin geldi. Lütfen ilacını almayı unutma 💊"
)
"""


# ============================================================
# [5] TEK DOSYADA HOCAYA GÖSTERİM ÇIKTISI
# Terminalde/raporda "tek dosyada kodlar burada" demek için:
# Bu dosyayı açıp aşağıdaki çıktıyı göstermen yeterli.
# ============================================================

def print_onefile_demo():
    print("==== AlarmReceiver.kt ====\n")
    print(KOTLIN_ALARM_RECEIVER)
    print("\n==== AlarmScheduler.kt ====\n")
    print(KOTLIN_ALARM_SCHEDULER)
    print("\n==== AndroidManifest.xml ekleri ====\n")
    print(ANDROID_MANIFEST_SNIPPETS)
    print("\n==== Python çağrı örneği (entegrasyon olursa) ====\n")
    print(PYTHON_CALL_EXAMPLE)


if __name__ == "__main__":
    # Bu dosya çalıştırılırsa sadece kod metinlerini yazdırır.
    # Entegrasyon yapılmadığı için "çalışan alarm" olmaz; amaç: örnek teslim.
    print_onefile_demo()
