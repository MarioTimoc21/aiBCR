import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os
import sqlite3

# === INCARCARE DATE ===

def load_data_basic(db_path=None):
    if db_path is None:
        base_dir = os.path.dirname(__file__)
        db_path = os.path.join(base_dir, "bcr_hackathon.db")
    conn = sqlite3.connect(db_path)
    query = """
        SELECT ID, TRX_IN_ALL_AMT, CEC_TOTAL_BALANCE_AMT, DEP_TOTAL_BALANCE_AMT, 
               LOA_TOTAL_BALANCE_AMT, ICC_TOTAL_BALANCE_AMT, OVD_TOTAL_BALANCE_AMT 
        FROM hackathon_data
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.dropna()

def load_data_credit_risk(db_path=None):
    if db_path is None:
        base_dir = os.path.dirname(__file__)
        db_path = os.path.join(base_dir, "bcr_hackathon.db")
    conn = sqlite3.connect(db_path)
    query = """
        SELECT ID, 
               OVD_UTILIZATION_GRADE, 
               ICC_UTILIZATION_GRADE, 
               PTS_REJECTED_LOANS_REQ_CNT
        FROM hackathon_data
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.dropna()

# === FUNCTII DE ETICHETARE ===

def label_credit_risk(cluster_number):
    labels = {
        0: "Utilizatori prudenti",
        1: "Utilizatori activi de credit",
        2: "Dependenti de credit",
        3: "Clienti cu risc"
    }
    return labels.get(cluster_number, "Necunoscut")

def label_profitability(cluster_number):
    labels = {
        0: "Debitori risc",
        1: "Utilizatori moderati",
        2: "Clienti low-income",
        3: "Clienti premium"
    }
    return labels.get(cluster_number, "Necunoscut")

# === CLUSTERING GENERAL ===

def perform_clustering(df, n_clusters=4, label_func=None, prefix="cluster"):
    if df.empty:
        print("[!] DataFrame-ul este gol.")
        return df
    features = df.drop(columns=["ID"])
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df[f"{prefix}_id"] = kmeans.fit_predict(scaled)
    if label_func:
        df[f"{prefix}_label"] = df[f"{prefix}_id"].apply(label_func)
    return df

# === IDENTIFICARE CLIENT ===

def identify_client(df, id_col="ID"):
    client_id = input("\n[?] Introdu ID-ul clientului: ").strip()
    df[id_col] = df[id_col].astype(str)
    client_id = str(client_id)
    rezultat = df[df[id_col] == client_id]

    if rezultat.empty:
        print(f"[!] Clientul cu ID-ul '{client_id}' nu a fost gasit in acest set.")
        print("\n[*] Exemple de ID-uri disponibile:")
        print(df[id_col].unique()[:10])
        return

    print(f"\n[OK] Informatii pentru clientul {client_id} (gasit in {len(rezultat)} randuri):")

    cluster_cols = [col for col in df.columns if ('cluster' in col or 'profit' in col or 'credit' in col) and ('label' in col or 'id' in col)]
    for col in cluster_cols:
        valori_unice = rezultat[col].unique()
        print(f"-> {col}: {', '.join(map(str, valori_unice))}")

# === INTERFATA PRINCIPALA ===

def main():
    print("=== Segmentare clienti BCR ===")
    print("1. Segmentare dupa profitabilitate")
    print("2. Segmentare dupa risc si apetit de credit")
    opt = input("Alege optiunea [1/2]: ").strip()

    if opt == "1":
        df = load_data_basic()
        df = perform_clustering(df, n_clusters=4, label_func=label_profitability, prefix="profit")
        output = "clustered_profitability.csv"
    elif opt == "2":
        df = load_data_credit_risk()
        df = perform_clustering(df, n_clusters=4, label_func=label_credit_risk, prefix="credit")
        output = "clustered_credit_risk.csv"
    else:
        print("Optiune invalida.")
        return

    print("\n[INFO] Primele 5 randuri:")
    print(df.head())

    df.to_csv(output, index=False)
    print(f"\n[OK] Rezultatele au fost salvate in: {output}")

    # Reciteste CSV pentru a include toate coloanele
    df_csv = pd.read_csv(output)
    identify_client(df_csv)

if __name__ == "__main__":
    main()
