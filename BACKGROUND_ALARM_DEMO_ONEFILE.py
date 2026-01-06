# BACKGROUND_ALARM_DEMO_ONEFILE.py
# ============================================================
# AMAÇ:
# - Uygulama KAPALIYKEN de çalışan alarm + üst bildirim (Android OS seviyesi)
# - MAIN'E DOKUNMADAN (entegrasyon yok), tek dosyada örnek
#
# GERÇEKLEŞTİRME (Native Android):
#   AlarmManager + BroadcastReceiver + NotificationChannel
#
# Bu dosya tek yerde dokümantasyon amaçlı:
# 1) Kotlin Receiver (bildirimi basar)
# 2) Kotlin Scheduler (AlarmManager ile alarm kurar)
# 3) AndroidManifest ekleri
# 4) Python/Pyjnius çağrı örneği (entegrasyon olursa)
#
# NOT:
# Bu dosya tek başına "çalışan alarm" üretmez; çünkü native dosyaların
# Android projesine eklenmesi gerekir. Buradaki amaç: hazır kodu tek yerde sunmak.
# ============================================================

from __future__ import annotations

import argparse
from pathlib import Path


# ============================================================
# [1] KOTLIN - AlarmReceiver.kt (BroadcastReceiver)
# Entegrasyon yapılırsa örnek dosya yolu:
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
        val message = intent.getStringExtra("message")
            ?: "İlaç saatin geldi. Lütfen ilacını almayı unutma "

        val channelId = "tiroidim_alarm_channel"
        val notificationId = 1001

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

        val notif = NotificationCompat.Builder(context, channelId)
            // Demo için sistem ikonu; projede kendi small icon'unla değiştirilir.
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentTitle(title)
            .setContentText(message)
            .setAutoCancel(true)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .build()

        nm.notify(notificationId, notif)
    }
}
""".strip()


# ============================================================
# [2] KOTLIN - AlarmScheduler.kt (AlarmManager ile alarm kurma)
# Entegrasyon yapılırsa örnek dosya yolu:
# android/app/src/main/java/org/tiroidim/app/AlarmScheduler.kt
# ============================================================

KOTLIN_ALARM_SCHEDULER = r"""
package org.tiroidim.app

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent

object AlarmScheduler {

    private const val REQUEST_CODE = 1001

    fun scheduleExact(
        context: Context,
        triggerAtMillis: Long,
        title: String = "Tiroidim",
        message: String = "İlaç saatin geldi. Lütfen ilacını almayı unutma "
    ) {
        val intent = Intent(context, AlarmReceiver::class.java).apply {
            putExtra("title", title)
            putExtra("message", message)
        }

        val pendingIntent = PendingIntent.getBroadcast(
            context,
            REQUEST_CODE,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val am = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager

        // Uygulama kapalı olsa bile, sistem belirlenen zamanda receiver'ı çağırır.
        // setExactAndAllowWhileIdle: Doze modunda da mümkün olduğunca tetikler.
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
            REQUEST_CODE,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val am = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
        am.cancel(pendingIntent)
    }
}
""".strip()


# ============================================================
# [3] AndroidManifest.xml EKLERİ
# android/app/src/main/AndroidManifest.xml içinde uygun yerlere eklenir
# ============================================================

ANDROID_MANIFEST_SNIPPETS = r"""
<!-- Android 13+ bildirim izni -->
<uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>

<!-- Android 12+ exact alarm (cihaza göre gerekebilir) -->
<uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM"/>

<application ...>
    <receiver
        android:name="org.tiroidim.app.AlarmReceiver"
        android:exported="false" />
</application>
""".strip()


# ============================================================
# [4] PYTHON'DAN ÇAĞIRMA ÖRNEĞİ (ENTEGRASYON OLURSA)
# Pyjnius ile Kotlin AlarmScheduler çağırır.
# ============================================================

PYTHON_CALL_EXAMPLE = r"""
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
    "İlaç saatin geldi. Lütfen ilacını almayı unutma "
)
""".strip()


# ============================================================
# [5] ÇIKTI / DOSYAYA YAZMA
# ============================================================

def print_onefile_demo() -> None:
    print("==== AlarmReceiver.kt ====\n")
    print(KOTLIN_ALARM_RECEIVER)
    print("\n\n==== AlarmScheduler.kt ====\n")
    print(KOTLIN_ALARM_SCHEDULER)
    print("\n\n==== AndroidManifest.xml ekleri ====\n")
    print(ANDROID_MANIFEST_SNIPPETS)
    print("\n\n==== Python çağrı örneği (entegrasyon olursa) ====\n")
    print(PYTHON_CALL_EXAMPLE)
    print()  # final newline


def write_files(out_dir: str) -> None:
    """
    Hocaya 'dosyalar hazır' demek için:
    --write ile bu modül, aşağıdaki çıktıları ayrı dosyalara yazar.
    """
    base = Path(out_dir).resolve()
    base.mkdir(parents=True, exist_ok=True)

    (base / "AlarmReceiver.kt").write_text(KOTLIN_ALARM_RECEIVER + "\n", encoding="utf-8")
    (base / "AlarmScheduler.kt").write_text(KOTLIN_ALARM_SCHEDULER + "\n", encoding="utf-8")
    (base / "AndroidManifest_snippet.xml").write_text(ANDROID_MANIFEST_SNIPPETS + "\n", encoding="utf-8")
    (base / "python_call_example.py").write_text(PYTHON_CALL_EXAMPLE + "\n", encoding="utf-8")

    print(f"[OK] Dosyalar yazıldı: {base}")


def main():
    parser = argparse.ArgumentParser(description="Background Alarm demo (tek dosya) - çıktı üretir.")
    parser.add_argument(
        "--write",
        metavar="DIR",
        help="Kodları ayrı dosyalara yaz (örn: --write out_native)",
    )
    args = parser.parse_args()

    if args.write:
        write_files(args.write)
    else:
        print_onefile_demo()


if __name__ == "__main__":
    main()
