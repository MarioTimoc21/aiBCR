import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os
import sqlite3

def load_credit_risk_data(db_path=None):
    if db_path is None:
        base_dir = os.path.dirname(__file__)
        db_path = os.path.join(base_dir, "bcr_hackathon.db")

    try:
        conn = sqlite3.connect(db_path)
        print(f"Conectat cu succes la baza de date: {db_path}")

        query = """
        SELECT ID, 
               OVD_UTILIZATION_GRADE, 
               ICC_UTILIZATION_GRADE, 
               PTS_REJECTED_LOANS_REQ_CNT
        FROM hackathon_data
        """
        df = pd.read_sql_query(query, conn)
        conn.close()

        print(f"Date încărcate: {len(df)} rânduri")
        return df.dropna()
    except Exception as e:
        print(f"Eroare la încărcarea datelor: {e}")
        return pd.DataFrame()

def label_credit_risk(cluster_number):
    labels = {
        0: "Utilizatori prudenți",
        1: "Utilizatori activi de credit",
        2: "Dependenți de credit",
        3: "Clienți cu risc"
    }
    return labels.get(cluster_number, "Necunoscut")

def cluster_credit_risk(df, n_clusters=4):
    if df.empty:
        print("Nu există date pentru segmentarea riscului.")
        return df

    features = df.drop(columns=["ID"])
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["credit_risk_cluster"] = kmeans.fit_predict(scaled)
    df["credit_risk_label"] = df["credit_risk_cluster"].apply(label_credit_risk)

    print("✅ Segmentarea riscului de credit a fost realizată cu succes.")
    return df

if __name__ == "__main__":
    data = load_credit_risk_data()

    if not data.empty:
        segmented = cluster_credit_risk(data)
        print(segmented.head())

        out_path = os.path.join(os.path.dirname(__file__), "credit_risk_segments.csv")
        segmented.to_csv(out_path, index=False)
        print(f"Rezultatele au fost salvate în: {out_path}")

        print("\n📊 Statistici pe segmente:")
        print(segmented.groupby("credit_risk_label").mean(numeric_only=True))
    else:
        print("⚠️ Date insuficiente pentru analiza riscului de credit.")
