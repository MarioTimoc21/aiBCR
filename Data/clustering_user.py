import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os
import sqlite3


def load_data_user_style(db_path=None):
    
    if db_path is None:
        base_dir = os.path.dirname(__file__)
        db_path = os.path.join(base_dir, "bcr_hackathon.db")

    conn = sqlite3.connect(db_path)
    query = """
        SELECT ID,
               CEC_TOTAL_BALANCE_AMT,
               DEP_TOTAL_BALANCE_AMT,
               SAV_TOTAL_BALANCE_AMT,
               LOA_TOTAL_BALANCE_AMT,
               ICC_TOTAL_BALANCE_AMT,
               OVD_TOTAL_BALANCE_AMT,
               TRX_OUT_ALL_AMT,
               TRX_IN_ALL_AMT,
               GPI_AGE,
               CEC_AVG_BALANCE_AMT,
               CEC_TOTAL_BALANCE_AMT,
               LOA_AVG_BALANCE_AMT,
               ICC_UTILIZATION_GRADE,
               TRX_OUT_IB_CNT,
               TRX_OUT_POS_CNT
        FROM hackathon_data
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df.dropna()


def load_data_user_goals(db_path=None):
    if db_path is None:
        base_dir = os.path.dirname(__file__)
        db_path = os.path.join(base_dir, "bcr_hackathon.db")

    conn = sqlite3.connect(db_path)
    query = """
        SELECT ID,
               CLIENT_TENURE,
               SAV_TOTAL_BALANCE_AMT,
               TER_ALL_ACTIVE_CNT,
               DEP_ALL_ACTIVE_CNT,
               PPI_ALL_ACTIVE_CNT,
               INS_VIG_ALL_ACTIVE_CNT,
               GPI_AGE
        FROM hackathon_data
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    df = df.dropna()

    return df


def load_data_user_spending(db_path=None):
    if db_path is None:
        base_dir = os.path.dirname(__file__)
        db_path = os.path.join(base_dir, "bcr_hackathon.db")

    conn = sqlite3.connect(db_path)
    query = """
        SELECT ID,
               MCC_FOOD_AMT,
               MCC_LEISURE_AMT,
               MCC_TRAVEL_AMT,
               MCC_TRANSPORTATION_AMT,
               MCC_ELECT_AND_DIG_GOODS_AMT,
               GPI_AGE,
               GPI_GENDER_CODE,
               GPI_DOMICILE_TYPE
        FROM hackathon_data
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    df = pd.get_dummies(df, columns=['GPI_GENDER_CODE', 'GPI_DOMICILE_TYPE'], drop_first=True)
    return df.dropna()


def load_data_user_digital_pref(db_path=None):
    if db_path is None:
        base_dir = os.path.dirname(__file__)
        db_path = os.path.join(base_dir, "bcr_hackathon.db")

    conn = sqlite3.connect(db_path)
    query = """
        SELECT ID,
               PTS_IB_FLAG,
               CHNL_IB_LOGINS_CNT,
               CHNL_BRANCH_SCANS_CNT,
               CHNL_INBOUND_CALLS_CNT,
               CRT_GEORGE_FLAG,
               GEORGE_INFO_FLAG,
               APPLE_PAY_FLAG,
               GOOGLE_PAY_FLAG
        FROM hackathon_data
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    for col in ['PTS_IB_FLAG', 'CRT_GEORGE_FLAG', 'GEORGE_INFO_FLAG', 'APPLE_PAY_FLAG', 'GOOGLE_PAY_FLAG']:
        if df[col].dtype == object:
            df[col] = df[col].map({'Y': 1, 'N': 0})

    return df.dropna()


def label_user_style(cluster_number):
    labels = {
        0: "Balanced Financial Managers",
        1: "Growth & Risk Oriented",
        2: "Conservative Savers",
        3: "Active Spenders"
    }
    return labels.get(cluster_number, "Unknown")


def label_user_goals(cluster_number):
    labels = {
        0: "Emergency Fund & Safety",
        1: "Mortgage & Housing",
        2: "Retirement & Long-Term Planning",
        3: "Education & Family Savings"
    }
    return labels.get(cluster_number, "Unknown")


def label_user_spending(cluster_number):
    labels = {
        0: "Lifestyle & Luxury",
        1: "Essential Expenses & Utilities",
        2: "Travel & Experiences",
        3: "Tech & Online Shopping"
    }
    return labels.get(cluster_number, "Unknown")


def label_user_digital(cluster_number):
    labels = {
        0: "Digital-First & Mobile",
        1: "Physical Interaction Preference",
        2: "Self-Banking & Autonomy",
        3: "Assistance & Support Needed"
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
        clustering_type (str): Tipul de clustering ('style', 'goals', 'spending', 'digital')
    
    Returns:
        pandas.DataFrame: DataFrame cu datele de clustering
    """
    
    # Definire configuratii pentru fiecare tip de clustering
    clustering_config = {
        'style': {
            'csv_file': 'clustered_user_style.csv',
            'load_func': load_data_user_style,
            'label_func': label_user_style,
            'prefix': 'style'
        },
        'goals': {
            'csv_file': 'clustered_user_goals.csv',
            'load_func': load_data_user_goals,
            'label_func': label_user_goals,
            'prefix': 'goals'
        },
        'spending': {
            'csv_file': 'clustered_user_spending.csv',
            'load_func': load_data_user_spending,
            'label_func': label_user_spending,
            'prefix': 'spending'
        },
        'digital': {
            'csv_file': 'clustered_user_digital.csv',
            'load_func': load_data_user_digital_pref,
            'label_func': label_user_digital,
            'prefix': 'digital'
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
    rezultat = df[df["ID"] == client_id]

    if rezultat.empty:
        print(f"Clientul cu ID-ul '{client_id}' nu a fost gasit.")
        return

    print(f"\nInformatii pentru clientul {client_id}:")
    print(rezultat[[f"{prefix}_cluster_id", f"{prefix}_cluster_label"]].drop_duplicates())


def main():
    print("=== Clustering Utilizatori BCR ===")
    print("1. Stiluri de Management Financiar")
    print("2. Obiective Financiare")
    print("3. Patterns de Cheltuieli")
    print("4. Preferinte Digitale")
    opt = input("Alege optiunea [1/2/3/4]: ").strip()

    clustering_map = {
        "1": "style",
        "2": "goals", 
        "3": "spending",
        "4": "digital"
    }
    
    if opt not in clustering_map:
        print("Optiune invalida.")
        return
    
    clustering_type = clustering_map[opt]
    
    # Incarca sau creeaza clustering-ul
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