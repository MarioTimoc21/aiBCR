import sqlite3

# Conectare la baza de date
conn = sqlite3.connect("bcr_hackathon.db")
cursor = conn.cursor()

# Lista tabelelor create anterior
tabele_de_sters = [
    "scoring_risc",
    "engagement_digital",
    "cheltuieli",
    "comportament_tranzactii",
    "solduri",
    "produse_financiare_active",
    "loialitate_client",
    "profil_clienti"
]

# Șterge fiecare tabel
for tabel in tabele_de_sters:
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {tabel}")
        print(f"Tabelul '{tabel}' a fost șters.")
    except Exception as e:
        print(f"Eroare la ștergerea tabelului '{tabel}': {e}")

# Commit și închide conexiunea
conn.commit()
conn.close()