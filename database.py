import sqlite3
from datetime import datetime


class Database:
    def __init__(self):
        # Yerel SQLite veritabanı dosyasının adını belirliyoruz. [cite: 4]
        self.db_name = "tiroid_takip.db"
        # Uygulama her açıldığında tabloların ve varsayılan verilerin hazır olduğundan emin oluyoruz.
        self.tablolari_olustur()
        self.varsayilan_semptomlari_yukle()
        self.varsayilan_duygulari_yukle()
        self.master_ilaclari_yukle()

    def baglanti_ac(self):
        """Veritabanına güvenli bir bağlantı açar ve ilişkileri aktif eder."""
        conn = sqlite3.connect(self.db_name)
        # PRAGMA: Tablolar arası bağlantıları (ilişkileri) aktif eder.
        # Bir ilaç silindiğinde ona ait eski kayıtların da otomatik silinmesini (CASCADE) sağlar.
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def tablolari_olustur(self):
        """Teknik şartnamede belirtilen tüm tabloları oluşturur. """
        conn = self.baglanti_ac()
        cursor = conn.cursor()

        # 1. KULLANICI PROFİLİ: Onboarding ekranındaki bilgileri tutar. [cite: 33]
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kullanici (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad_soyad TEXT,
                yas INTEGER,
                boy INTEGER,
                kilo INTEGER,
                tiroid_tipi TEXT
            )
        """)

        # 2. MASTER İLAÇ LİSTESİ: Piyasada hazır bulunan ilaçlar (Seçenek Havuzu). [cite: 20]
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS master_ilaclar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ilac_adi TEXT,
                varsayilan_doz TEXT
            )
        """)

        # 3. KULLANICI İLAÇLARI: Kullanıcının kendi listesine eklediği özel saatli ilaçlar. [cite: 19, 41]
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kullanici_ilaclari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ilac_adi TEXT, 
                doz TEXT, 
                saat TEXT, 
                periyot TEXT
            )
        """)

        # 4. GÜNLÜK İLAÇ LOGLARI: Takvimin ✅, ❌ veya ⚠️ ikonlarını belirleyen kayıtlar. [cite: 19, 26, 27]
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS gunluk_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ilac_id INTEGER NOT NULL,
        tarih TEXT NOT NULL,
        durum TEXT NOT NULL, -- 'ALINDI' veya 'ATLADI'
        FOREIGN KEY(ilac_id) REFERENCES kullanici_ilaclari(id) ON DELETE CASCADE,
        UNIQUE(ilac_id, tarih)
    )
""")

        # 5. TAHLİL SONUÇLARI: Kullanıcının girdiği TSH, T3, T4 değerleri (Silinemez!). [cite: 19, 56, 66]
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tahlil_sonuclari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tsh REAL,
                t3 REAL,
                t4 REAL,
                tarih TEXT
            )
        """)

        # 6. GÜNLÜK DURUM: Dashboard'daki duygu durumu ve semptom seçimleri. [cite: 40]
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gunluk_durum (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarih TEXT UNIQUE,
                duygu_durum TEXT,
                semptomlar TEXT 
            )
        """)

        # 7. MASTER SEMPTOM VE DUYGU TÜRLERİ: Seçmeli listelerin kaynak tabloları.
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS semptom_turleri (id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT UNIQUE)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS duygu_turleri (id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT UNIQUE)")

        conn.commit()
        conn.close()

    # --- VARSAYILAN VERİLERİN YÜKLENMESİ (MASTER DATA) ---

    def master_ilaclari_yukle(self):
        """Piyasadaki ilaçları otomatik yükleyerek kullanıcı hatasını önler. [cite: 20]"""
        ilaclar = [
            ("Euthyrox", "25mcg"), ("Euthyrox", "50mcg"), ("Euthyrox", "100mcg"),
            ("Levotiron", "25mcg"), ("Levotiron",
                                     "75mcg"), ("Levotiron", "100mcg"),
            ("Tiromel", "25mcg"), ("Tefor", "100mcg")
        ]
        conn = self.baglanti_ac()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM master_ilaclar")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO master_ilaclar (ilac_adi, varsayilan_doz) VALUES (?, ?)", ilaclar)
        conn.commit()
        conn.close()

    def varsayilan_semptomlari_yukle(self):
        """Dashboard'daki semptom seçeneklerini hazırlar."""
        semptomlar = ["Yorgunluk", "Kilo Değişimi",
                      "Saç Dökülmesi", "Çarpıntı", "Unutkanlık", "Sinirlilik"]
        conn = self.baglanti_ac()
        cursor = conn.cursor()
        for s in semptomlar:
            cursor.execute(
                "INSERT OR IGNORE INTO semptom_turleri (ad) VALUES (?)", (s,))
        conn.commit()
        conn.close()

    def varsayilan_duygulari_yukle(self):
        """Dashboard'daki duygu durum seçeneklerini hazırlar."""
        duygular = ["Mutlu", "Yorgun", "Sinirli",
                    "Sakin", "Enerjik", "Depresif"]
        conn = self.baglanti_ac()
        cursor = conn.cursor()
        for d in duygular:
            cursor.execute(
                "INSERT OR IGNORE INTO duygu_turleri (ad) VALUES (?)", (d,))
        conn.commit()
        conn.close()

    # --- EKİP ÜYELERİ İÇİN API FONKSİYONLARI ---

    def kullanici_kayitli_mi(self):
        """Üye 1 (Kaptan) için: Navigasyon (Kayıtlı mı?) kontrolü yapar. [cite: 13]"""
        conn = self.baglanti_ac()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM kullanici")
        sonuc = cursor.fetchone()[0] > 0
        conn.close()
        return sonuc

    def master_ilac_listesi_getir(self):
        """Üye 7 için: İlaç ekleme dropdown menüsünü doldurur. [cite: 55]"""
        conn = self.baglanti_ac()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ilac_adi || ' - ' || varsayilan_doz FROM master_ilaclar")
        liste = [r[0] for r in cursor.fetchall()]
        conn.close()
        return liste

    def kullanici_ilaci_ekle(self, ad, doz, saat, periyot):
        """Üye 7 için: Seçilen ilacı kullanıcının listesine kaydeder. [cite: 50, 54]"""
        conn = self.baglanti_ac()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO kullanici_ilaclari (ilac_adi, doz, saat, periyot) VALUES (?, ?, ?, ?)", (ad, doz, saat, periyot))
        conn.commit()
        conn.close()

    def ilac_logla(self, ilac_id, tarih, durum):
        """Üye 9 için: Dashboard'daki 'Aldım/Atladım' butonlarını kaydeder. [cite: 68]"""
        conn = self.baglanti_ac()
        cursor = conn.cursor()
        # INSERT OR REPLACE: Aynı gün için birden fazla kayıt oluşmasını önler.
        cursor.execute(
            "INSERT OR REPLACE INTO gunluk_log (ilac_id, tarih, durum) VALUES (?, ?, ?)", (ilac_id, tarih, durum))
        conn.commit()
        conn.close()

    def tahlil_ekle(self, tsh, t3, t4, tarih):
        """Üye 7 için: Tahlil verilerini sisteme işler. [cite: 56]"""
        conn = self.baglanti_ac()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tahlil_sonuclari (tsh, t3, t4, tarih) VALUES (?, ?, ?, ?)", (tsh, t3, t4, tarih))
        conn.commit()
        conn.close()

    def ilac_sil(self, ilac_id):
        """Üye 8 için: İlacı ayarlar sayfasından siler. [cite: 62]"""
        conn = self.baglanti_ac()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM kullanici_ilaclari WHERE id = ?", (ilac_id,))
        conn.commit()
        conn.close()

    def get_lab_history(self):
        """Üye 9 için: Grafik verilerini tarihe göre sıralı döner. [cite: 66, 67]"""
        conn = self.baglanti_ac()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tahlil_sonuclari ORDER BY tarih ASC")
        sonuclar = cursor.fetchall()
        conn.close()
        return sonuclar

    def durum_kaydet(self, tarih, duygu, semptom_listesi):
        """Üye 5 için: Günlük ruh hali ve semptomları saklar. [cite: 40]"""
        semptomlar_str = ",".join(semptom_listesi)
        conn = self.baglanti_ac()
        cursor = conn.cursor()
        # Tarih UNIQUE olduğu için kullanıcının aynı gün yaptığı güncellemeyi kaydeder.
        cursor.execute("INSERT OR REPLACE INTO gunluk_durum (tarih, duygu_durum, semptomlar) VALUES (?, ?, ?)",
                       (tarih, duygu, semptomlar_str))
        conn.commit()
        conn.close()

    def kullanici_ilaclarini_getir(self):
        """Dashboard ve Takvim için: Kullanıcının ilaç listesini saat sırasıyla getirir."""
        conn = self.baglanti_ac()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, ilac_adi, doz, saat, periyot FROM kullanici_ilaclari ORDER BY saat ASC")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def gunluk_loglari_getir(self, tarih):
        """Takvim ikonu ve kartlar için: O günün ALINDI/ATLADI kayıtlarını getirir."""
        conn = self.baglanti_ac()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ilac_id, durum FROM gunluk_log WHERE tarih = ?", (tarih,))
        rows = cursor.fetchall()
        conn.close()

    # kolay erişim için dict: {ilac_id: "ALINDI" / "ATLADI"}
        return {r[0]: r[1] for r in rows}

    def gun_ikonunu_hesapla(self, tarih):
        """
        ✅ Hepsi ALINDI
        ❌ Hepsi ATLADI (ya da hiç ALINDI yok)
        ⚠️ Karışık (bazısı alındı bazısı atlandı / eksik)
        ➖ O gün için ilaç yok
        """
        ilaclar = self.kullanici_ilaclarini_getir()
        if not ilaclar:
            return {"status": "NO_PLAN", "icon": "➖", "text": "İlaç planı yok"}

        log_map = self.gunluk_loglari_getir(tarih)

        toplam = len(ilaclar)
        alindi = 0
        atlandi = 0
        kayitsiz = 0

        for ilac in ilaclar:
            ilac_id = ilac[0]
            durum = log_map.get(ilac_id)

            if durum == "ALINDI":
                alindi += 1
            elif durum == "ATLADI":
                atlandi += 1
            else:
                kayitsiz += 1  # o ilaç için o gün hiç seçim yapılmamış

        # Karar:
        if alindi == toplam:
            return {"status": "ALL_TAKEN", "icon": "✅", "text": "Tüm ilaçlar alındı"}
        if alindi == 0 and (atlandi > 0 or kayitsiz > 0):
            return {"status": "NONE_TAKEN", "icon": "❌", "text": "İlaçlar alınmadı"}
        return {"status": "PARTIAL", "icon": "⚠️", "text": f"{alindi}/{toplam} alındı"}

    def dashboard_kartlarini_getir(self, tarih):
        """
        Dashboard ekranı kartları:
        - saat, ilaç adı, doz
        - taken: True/False/None (None: daha seçilmemiş)
        """
        ilaclar = self.kullanici_ilaclarini_getir()
        log_map = self.gunluk_loglari_getir(tarih)

        kartlar = []
        for ilac in ilaclar:
            ilac_id, ad, doz, saat, periyot = ilac
            durum = log_map.get(ilac_id)

            if durum == "ALINDI":
                taken = True
            elif durum == "ATLADI":
                taken = False
            else:
                taken = None  # hiç seçim yapılmamış

            kartlar.append({
                "ilac_id": ilac_id,
                "ilac_adi": ad,
                "doz": doz,
                "saat": saat,
                "periyot": periyot,
                "taken": taken
            })

        return kartlar
    
# Test kodu
if __name__ == "__main__":
    print("Veritabanı sistemi başlatılıyor...")

    # Bu satır Database sınıfından bir 'nesne' oluşturur.
    # Bu yapıldığı anda __init__ fonksiyonu çalışır ve db dosyası klasöründe belirir.
    db = Database()

    print(" Basarili! 'tiroid_takip.db' dosyasi olusturuldu.")
    print(" Tablolar kuruldu ve Master Data yuklendi.")
