import sqlite3

def veritabani_baslat():
    conn = sqlite3.connect("tiroid.db")
    cursor = conn.cursor()
    
    # Kullanıcı Tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kullanici (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad_soyad TEXT,
        tiroid_tipi TEXT
    )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    veritabani_baslat()
    print("Veritabani dosyasi olusturuldu!")