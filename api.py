from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import Data.clustering_user as user_clustering
import Data.clustering_banker as banker_clustering
from requesting import *

app = Flask(__name__)

# Mapare dinamica functii cluster
user_functions = {
    "style": (user_clustering.load_data_user_style, user_clustering.label_user_style),
    "goals": (user_clustering.load_data_user_goals, user_clustering.label_user_goals),
    "spending": (user_clustering.load_data_user_spending, user_clustering.label_user_spending),
    "digital": (user_clustering.load_data_user_digital_pref, user_clustering.label_user_digital),
}

banker_functions = {
    "profit_risk": (banker_clustering.load_data_profit_risk, banker_clustering.label_profit_risk),
    "lifecycle": (banker_clustering.load_data_lifecycle, banker_clustering.label_lifecycle),
    "transactional": (banker_clustering.load_data_transactional, banker_clustering.label_transactional),
    "cross_selling": (banker_clustering.load_data_cross_selling, banker_clustering.label_cross_selling),
    "retention": (banker_clustering.load_data_retention_loyalty, banker_clustering.label_retention_loyalty)
}

# Cluster client
@app.route('/api/user/<cluster_type>/<user_id>', methods=['GET'])
def get_user_cluster(cluster_type, user_id):
    if cluster_type not in user_functions:
        return jsonify({"error": "Invalid user cluster type"}), 400

    try:
        # Folosim explicit functia din modulul user_clustering
        df = user_clustering.load_or_create_clustering(cluster_type)
        
        # Convertim ID-urile la string pentru comparatie sigura
        df["ID"] = df["ID"].astype(str)
        user_id = str(user_id)
        
        row = df[df["ID"] == user_id]
        if row.empty:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "user_id": user_id,
            "cluster_type": cluster_type,
            "cluster_id": int(row[f"{cluster_type}_cluster_id"].iloc[0]),
            "cluster_label": row[f"{cluster_type}_cluster_label"].iloc[0]
        })
    except Exception as e:
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500

# Cluster banker
@app.route('/api/banker/<cluster_type>/<user_id>', methods=['GET'])
def get_banker_cluster(cluster_type, user_id):
    if cluster_type not in banker_functions:
        return jsonify({"error": "Invalid banker cluster type"}), 400

    try:
        # Folosim explicit functia din modulul banker_clustering
        df = banker_clustering.load_or_create_clustering(cluster_type)
        
        # Convertim ID-urile la string pentru comparatie sigura
        df["ID"] = df["ID"].astype(str)
        user_id = str(user_id)
        
        row = df[df["ID"] == user_id]
        if row.empty:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "user_id": user_id,
            "cluster_type": cluster_type,
            "cluster_id": int(row[f"{cluster_type}_cluster_id"].iloc[0]),
            "cluster_label": row[f"{cluster_type}_cluster_label"].iloc[0]
        })
    except Exception as e:
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500

# Afisare solduri
@app.route('/api/solduri/<user_id>', methods=['GET'])
def solduri_info(user_id):
    all_luni = request.args.get('all', 'false').lower() == 'true'

    result = get_sold_data(user_id, ultima_luna=False)
    if result is None:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(result)

# Afisare cheltuieli
@app.route('/api/cheltuieli/<user_id>', methods=['GET'])
def cheltuieli_info(user_id):
    all_luni = request.args.get('all', 'false')
    result = get_cheltuieli_data(user_id, ultima_luna=(all_luni.lower() != 'true'))
    if result is None:
        return jsonify({"error": "Clientul nu are cheltuieli disponibile"}), 404
    return jsonify(result)

# Functie robusta de citire in bucati
def fetch_cheltuieli_for_ids(ids, chunk_size=900):
    conn = load_db_connection()
    all_chunks = []
    
    for i in range(0, len(ids), chunk_size):
        chunk = ids[i:i + chunk_size]
        query = f"""
            SELECT * FROM cheltuieli
            WHERE ID_Client IN ({','.join(['?'] * len(chunk))})
        """
        chunk_df = pd.read_sql_query(query, conn, params=chunk)
        all_chunks.append(chunk_df)
    
    conn.close()
    return pd.concat(all_chunks, ignore_index=True)

# Analiza spending in cadrul clusterului
@app.route('/api/analiza/spending/<user_id>', methods=['GET'])
def analiza_spending(user_id):
    try:
        user_id = str(user_id)
        df_cluster = user_clustering.load_or_create_clustering("spending")
        df_cluster["ID"] = df_cluster["ID"].astype(str)

        row = df_cluster[df_cluster["ID"] == user_id]
        if row.empty:
            return jsonify({"error": "Utilizatorul nu a fost gasit"}), 404

        cluster_label = row["spending_cluster_label"].iloc[0]
        users_in_cluster = df_cluster[df_cluster["spending_cluster_label"] == cluster_label]["ID"].tolist()

        df_chelt = fetch_cheltuieli_for_ids(users_in_cluster)
        if df_chelt.empty or user_id not in df_chelt["ID_Client"].astype(str).values:
            return jsonify({"error": "Nu exista date despre cheltuieli"}), 404

        # Normalizeaza coloanele pentru a evita probleme cu spatii
        df_chelt.rename(columns=lambda x: x.strip().replace(" ", "_"), inplace=True)
        df_chelt["ID_Client"] = df_chelt["ID_Client"].astype(str)

        df_user = df_chelt[df_chelt["ID_Client"] == user_id]
        df_user.sort_values("Luna_Raportare", inplace=True)

        categorii = ["Cheltuieli_Mancare", "Cheltuieli_Timp_Liber", "Cheltuieli_Locuinte", "Cheltuieli_Calatorii", "Cheltuieli_Electronice"]
        df_user["Total"] = df_user[categorii].sum(axis=1)

        # 1. STRUCTURA PE CATEGORII (ultima luna)
        ultima_luna = df_user["Luna_Raportare"].max()
        row_ultima = df_user[df_user["Luna_Raportare"] == ultima_luna]
        total_luna = row_ultima[categorii].sum(axis=1).values[0]
        structura = {
            cat.replace("Cheltuieli_", ""): round(row_ultima[cat].values[0] / total_luna * 100, 2)
            for cat in categorii
        }

        # 3. COMPARATIE CU CLUSTER
        df_chelt["cheltuieli_totale"] = df_chelt[categorii].sum(axis=1)
        media_user = df_user["Total"].mean()
        media_cluster = df_chelt.groupby("ID_Client")["cheltuieli_totale"].mean()
        percentila = round((media_cluster < media_user).mean() * 100, 2)
        comparatie = f"Cheltuiesti mai mult decat {percentila}% dintre utilizatorii din acelasi grup."

        # 4. RATA CHELTUIELI / VENIT
        conn = load_db_connection()
        df_tranz = pd.read_sql("SELECT * FROM comportament_tranzactii WHERE ID_Client = ?", conn, params=[user_id])
        conn.close()
        venit_mediu = df_tranz["Suma_Tran_Intrare"].mean()
        rata = round(media_user / venit_mediu * 100, 2) if venit_mediu else None

        # 5. ALERTE
        alerte = []
        for cat in categorii:
            pondere = row_ultima[cat].values[0] / total_luna
            if pondere > 0.5:
                alerte.append(f"Cheltuielile cu {cat.replace('Cheltuieli_', '').lower()} au depasit 50% din total - posibil dezechilibru.")

        # 6. VARIATII IN TIMP (versiune imbunatatita)
        variatii = []
        df_user_diff = df_user[["Luna_Raportare", "Total"]].copy()
        df_user_diff["delta"] = df_user_diff["Total"].pct_change()

        prev_total = None
        for _, row in df_user_diff.iterrows():
            luna = row["Luna_Raportare"]
            total = row["Total"]
            delta = row["delta"]

            if pd.isna(delta):
                prev_total = total
                continue

            if prev_total == 0 and total > 0:
                variatii.append(f"In luna {luna}, ai avut cheltuieli dupa o luna cu zero activitate.")
            elif prev_total == 0 and total == 0:
                # Ignoram lunile consecutive cu zero
                pass
            elif abs(delta) > 0.3:
                semn = "scadere" if delta < 0 else "crestere"
                variatii.append(f"In luna {luna}, a fost o {semn} de {round(abs(delta) * 100, 1)}% fata de luna precedenta.")
            prev_total = total

        return jsonify({
            "user_id": user_id,
            "cluster": cluster_label,
            "structura_cheltuieli_%": structura,
            "cheltuieli_medie_lunara": round(media_user, 2),
            "rata_cheltuieli_venit_%": rata,
            "comparatie_cu_cluster": comparatie,
            "alerte dezechilibru": alerte,
            "variatii_timp": variatii
        })

    except Exception as e:
        return jsonify({"error": f"Eroare interna: {str(e)}"}), 500

@app.route('/api/analiza/')
@app.route('/')
def index():
    return jsonify({
        "message": "API BCR activ",
        "user_clusters": list(user_functions.keys()),
        "banker_clusters": list(banker_functions.keys())
    })

if __name__ == '__main__':
    app.run(debug=True)