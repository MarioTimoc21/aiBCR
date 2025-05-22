import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os
import sqlite3


def load_data_profit_risk(db_path=None):
    if db_path is None:
        base_dir = os.path.dirname(__file__)
        db_path = os.path.join(base_dir, "bcr_hackathon.db")

    conn = sqlite3.connect(db_path)
    query = """
        SELECT ID,
               CEC_TOTAL_BALANCE_AMT,
               DEP_TOTAL_BALANCE_AMT,
               LOA_TOTAL_BALANCE_AMT,
               ICC_TOTAL_BALANCE_AMT,
               OVD_TOTAL_BALANCE_AMT,
               OVD_UTILIZATION_GRADE,
               ICC_UTILIZATION_GRADE,
               PTS_REJECTED_LOANS_REQ_CNT,
               CEC_ALL_ACTIVE_CNT,
               CLO_ALL_ACTIVE_CNT,
               CRT_ALL_ACTIVE_CNT,
               DEP_ALL_ACTIVE_CNT,
               ICC_ALL_ACTIVE_CNT,
               LOA_ALL_ACTIVE_CNT
        FROM hackathon_data
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df.dropna()


def load_data_lifecycle(db_path=None):
    if db_path is None:
        base_dir = os.path.dirname(__file__)
        db_path = os.path.join(base_dir, "bcr_hackathon.db")

    conn = sqlite3.connect(db_path)
    query = """
        SELECT ID,
               CLIENT_TENURE,
               CRT_ALL_ACTIVE_CNT,
               DEP_ALL_ACTIVE_CNT,
               ICC_ALL_ACTIVE_CNT,
               LOA_ALL_ACTIVE_CNT,
               CRT_TOTAL_BALANCE_AMT,
               PTS_REJECTED_LOANS_REQ_CNT
        FROM hackathon_data
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df.dropna()


def load_data_transactional(db_path=None):
    if db_path is None:
        base_dir = os.path.dirname(__file__)
        db_path = os.path.join(base_dir, "bcr_hackathon.db")

    conn = sqlite3.connect(db_path)
    query = """
        SELECT ID,
               TRX_IN_ALL_CNT,
               TRX_OUT_ALL_CNT,
               TRX_IN_ALL_AMT,
               TRX_OUT_ALL_AMT,
               TRX_OUT_POS_CNT,
               TRX_OUT_IB_CNT
        FROM hackathon_data
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df.dropna()


def load_data_cross_selling(db_path=None):
    if db_path is None:
        base_dir = os.path.dirname(__file__)
        db_path = os.path.join(base_dir, "bcr_hackathon.db")

    conn = sqlite3.connect(db_path)
    query = """
        SELECT ID,
               CEC_ALL_ACTIVE_CNT,
               CLO_ALL_ACTIVE_CNT,
               CRT_ALL_ACTIVE_CNT,
               DEP_ALL_ACTIVE_CNT,
               ICC_ALL_ACTIVE_CNT,
               INS_VIG_ALL_ACTIVE_CNT,
               INV_ALL_ACTIVE_CNT,
               PPI_ALL_ACTIVE_CNT,
               MONEYBACK_FLAG,
               WALLET_FLAG,
               GEORGE_INFO_FLAG,
               PTS_IB_FLAG,
               TRX_OUT_IB_CNT,
               TRX_OUT_POS_CNT,
               GPI_CUSTOMER_TYPE_DESC,
               CLIENT_TENURE,
               PTS_TOTAL_LOANS_REQ_CNT,
               PTS_REJECTED_LOANS_REQ_CNT,
               ICC_APPROVED_LIMIT,
               CLO_APPROVED_LIMIT,
               ICC_UTILIZATION_GRADE
        FROM hackathon_data
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    df = df.dropna()

    for col in ['MONEYBACK_FLAG', 'WALLET_FLAG', 'GEORGE_INFO_FLAG', 'PTS_IB_FLAG']:
        if df[col].dtype == object:
            df[col] = df[col].map({'Y': 1, 'N': 0})

    df = pd.get_dummies(df, columns=['GPI_CUSTOMER_TYPE_DESC'], drop_first=True)

    return df


def load_data_retention_loyalty(db_path=None):
    if db_path is None:
        base_dir = os.path.dirname(__file__)
        db_path = os.path.join(base_dir, "bcr_hackathon.db")

    conn = sqlite3.connect(db_path)
    query = """
        SELECT ID,
               CLIENT_TENURE,
               PTS_IB_FLAG,
               GEORGE_INFO_FLAG,
               WALLET_FLAG,
               APPLE_PAY_FLAG,
               GOOGLE_PAY_FLAG,
               MONEYBACK_FLAG,
               PBS_FLAG,
               CHNL_IB_LOGINS_CNT,
               CHNL_BRANCH_SCANS_CNT,
               CHNL_INBOUND_CALLS_CNT,
               TRX_OUT_POS_CNT,
               TRX_OUT_IB_CNT,
               TRX_OUT_ALL_CNT,
               LOA_REFUND_FLAG,
               LOA_TOTAL_REFUND_FLAG
        FROM hackathon_data
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    df = df.dropna()

    for col in ['PTS_IB_FLAG', 'GEORGE_INFO_FLAG', 'WALLET_FLAG', 'APPLE_PAY_FLAG', 'GOOGLE_PAY_FLAG', 'MONEYBACK_FLAG', 'PBS_FLAG', 'LOA_REFUND_FLAG', 'LOA_TOTAL_REFUND_FLAG']:
        if df[col].dtype == object:
            df[col] = df[col].map({'Y': 1, 'N': 0})

    return df


def label_retention_loyalty(cluster_number):
    labels = {
        0: "Loyal Digital Users",
        1: "Occasional Clients",
        2: "Migration Risk",
        3: "Recoverable Inactive Clients"
    }
    return labels.get(cluster_number, "Unknown")


def label_profit_risk(cluster_number):
    labels = {
        0: "Premium & Stability",
        1: "Profitable with Credit Risk",
        2: "Cost > Revenue",
        3: "Untapped Potential"
    }
    return labels.get(cluster_number, "Unknown")


def label_lifecycle(cluster_number):
    labels = {
        0: "New Clients < 1 year",
        1: "Developing Users",
        2: "Loyal Mature Clients",
        3: "Declining Trend"
    }
    return labels.get(cluster_number, "Unknown")


def label_transactional(cluster_number):
    labels = {
        0: "Frequent Small Transactions",
        1: "High Volume & High Value",
        2: "Inconsistent Usage",
        3: "Minimal Activity Accounts"
    }
    return labels.get(cluster_number, "Unknown")


def label_cross_selling(cluster_number):
    labels = {
        0: "Multi-Product",
        1: "Credit Focused",
        2: "Investment & Savings Potential",
        3: "Basic Users (1-2 products)"
    }
    return labels.get(cluster_number, "Unknown")


def perform_clustering(df, n_clusters=4, prefix="cluster", label_func=None):
    if df.empty:
        print("DataFrame-ul este gol.")
        return df

    features = df.drop(columns=["ID"])
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df[f"{prefix}_cluster_id"] = kmeans.fit_predict(scaled)
    if label_func:
        df[f"{prefix}_cluster_label"] = df[f"{prefix}_cluster_id"].apply(label_func)
    return df


def load_or_create_clustering(clustering_type):
    """
    Incarca datele de clustering din CSV daca exista, altfel creeaza clustering-ul.
    
    Args:
        clustering_type (str): Tipul de clustering ('profit_risk', 'lifecycle', 
                              'transactional', 'cross_selling', 'retention')
    
    Returns:
        pandas.DataFrame: DataFrame cu datele de clustering
    """
    
    # Definire configuratii pentru fiecare tip de clustering
    clustering_config = {
        'profit_risk': {
            'csv_file': 'clustered_banker_profit_risk.csv',
            'load_func': load_data_profit_risk,
            'label_func': label_profit_risk,
            'prefix': 'profit_risk'
        },
        'lifecycle': {
            'csv_file': 'clustered_banker_lifecycle.csv',
            'load_func': load_data_lifecycle,
            'label_func': label_lifecycle,
            'prefix': 'lifecycle'
        },
        'transactional': {
            'csv_file': 'clustered_banker_transactional.csv',
            'load_func': load_data_transactional,
            'label_func': label_transactional,
            'prefix': 'transactional'
        },
        'cross_selling': {
            'csv_file': 'clustered_banker_cross_selling.csv',
            'load_func': load_data_cross_selling,
            'label_func': label_cross_selling,
            'prefix': 'cross_selling'
        },
        'retention': {
            'csv_file': 'clustered_banker_retention.csv',
            'load_func': load_data_retention_loyalty,
            'label_func': label_retention_loyalty,
            'prefix': 'retention'
        }
    }
    
    if clustering_type not in clustering_config:
        raise ValueError(f"Tip de clustering invalid: {clustering_type}")
    
    config = clustering_config[clustering_type]
    
    # Determinam calea catre directorul Data
    # Aceasta va merge corect chiar daca functia e apelata din alt director
    data_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construim calea completa catre fisierul CSV
    csv_file = os.path.join(data_dir, config['csv_file'])
    
    # Verifica daca fisierul CSV exista
    if os.path.exists(csv_file):
        print(f"Se incarca datele existente din: {csv_file}")
        try:
            df = pd.read_csv(csv_file)
            print(f"Datele au fost incarcate cu succes ({len(df)} inregistrari)")
            return df
        except Exception as e:
            print(f"Eroare la incarcarea fisierului CSV: {e}")
            print("Se va realiza clustering-ul din nou...")
    
    # Daca fisierul nu exista sau nu poate fi incarcat, face clustering-ul
    print(f"Se realizeaza clustering-ul pentru {clustering_type}...")
    
    # Incarca datele din baza de date
    df = config['load_func']()
    
    # Realizeaza clustering-ul
    df = perform_clustering(
        df, 
        prefix=config['prefix'], 
        label_func=config['label_func']
    )
    
    # Salveaza rezultatele in CSV
    df.to_csv(csv_file, index=False)
    print(f"Rezultatele au fost salvate in: {csv_file}")
    
    return df


def identify_client(df, prefix):
    client_id = input("\nIntrodu ID-ul clientului: ").strip()
    df["ID"] = df["ID"].astype(str)
    client_id = str(client_id)
    rezultat = df[df["ID"] == client_id]

    if rezultat.empty:
        print(f"Clientul cu ID-ul '{client_id}' nu a fost gasit.")
        return

    print(f"\nInformatii pentru clientul {client_id}:")
    print(rezultat[[f"{prefix}_cluster_id", f"{prefix}_cluster_label"]].drop_duplicates())


def main():
    print("=== Clustering Clienti BCR ===")
    print("1. Clustering Profitabilitate si Risc")
    print("2. Clustering Ciclu de Viata")
    print("3. Clustering Comportament Tranzactional")
    print("4. Clustering Cross-Selling Potential")
    print("5. Clustering Retentie si Loialitate")
    opt = input("Alege optiunea [1/2/3/4/5]: ").strip()

    clustering_map = {
        "1": "profit_risk",
        "2": "lifecycle", 
        "3": "transactional",
        "4": "cross_selling",
        "5": "retention"
    }
    
    if opt not in clustering_map:
        print("Optiune invalida.")
        return
    
    clustering_type = clustering_map[opt]
    
    # Incarca sau creeaza clustering-ul folosind noua functie
    df = load_or_create_clustering(clustering_type)
    
    # Afiseaza statistici
    cluster_col = [col for col in df.columns if "cluster_label" in col][0]
    print("\nStatistici pe clustere:")
    print(df.groupby(cluster_col).mean(numeric_only=True))
    
    # Identifica clientul
    prefix = cluster_col.replace("_cluster_label", "")
    identify_client(df, prefix)


if __name__ == "__main__":
    main()
