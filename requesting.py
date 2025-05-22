import sqlite3
import pandas as pd
import os

def load_db_connection(db_name="bcr_hackathon.db"):
    base_dir = os.path.dirname(__file__)
    db_path = os.path.join(base_dir, "Data", db_name)
    return sqlite3.connect(db_path)

def get_sold_data(user_id, ultima_luna = True):
    conn = load_db_connection()
    query = "SELECT * FROM solduri WHERE ID_Client = ?"
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()

    if df.empty:
        return None
    
    df = df.sort_values(by="Luna Raportare", ascending=True)
    
    if ultima_luna:
        row = df.iloc[-1]
        solduri = {
            "luna_raport": row["Luna Raportare"],
            "cont_curent": row["Sold_Cont_Curent"],
            "depozite": row["Sold_Depozite"],
            "credite": row["Sold_Credite"],
            "economii": row["Sold_Economii"],
            "overdraft": row["Sold_Overdraft"],
            "limita_overdraft": row["Limita_Overdraft"],
            "card_credit": row["Sold_Card_Credit"],
            "planuri_economii": row["Sold_Planuri_Economii"]
        }

        activ = solduri["cont_curent"] + solduri["depozite"] + solduri["economii"] + solduri["planuri_economii"]
        datorii = solduri["credite"] + solduri["overdraft"] + solduri["card_credit"]
        net = activ + datorii

        insights = {
            "total_activ": round(activ, 2),
            "total_datorii": round(datorii, 2),
            "net_worth": round(net, 2),
            "rata_economisire_vs_datorii": round(activ / abs(datorii), 2) if datorii != 0 else None
        }

        return {
            "user_id": user_id,
            "solduri": solduri,
            "insights": insights
        }
    else:
        df["Activ"] = df["Sold_Cont_Curent"] + df["Sold_Depozite"] + df["Sold_Economii"] + df["Sold_Planuri_Economii"]
        df["Datorii"] = df["Sold_Credite"] + df["Sold_Overdraft"] + df["Sold_Card_Credit"]
        df["Net"] = df["Activ"] + df["Datorii"]
        df["Rata_Economisire_vs_Datorii"] = df.apply(lambda x: round(x["Activ"] / abs(x["Datorii"]), 2) if x["Datorii"] != 0 else None, axis=1)

        evolution = df[["Luna Raportare", "Activ", "Datorii", "Net", "Rata_Economisire_vs_Datorii"]].to_dict(orient="records")

        return {
            "user_id": user_id,
            "evolutie_lunara": evolution
        }
    
def get_cheltuieli_data(user_id, ultima_luna=True):
    conn = load_db_connection()
    query = "SELECT * FROM cheltuieli WHERE ID_Client = ?"
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()

    if df.empty:
        return None

    df = df.sort_values("Luna Raportare")

    categories = [
        "Cheltuieli_Mancare",
        "Cheltuieli_Timp_Liber",
        "Cheltuieli_Calatorii",
        "Cheltuieli_Locuinte",
        "Cheltuieli_Electronice"
    ]

    if ultima_luna:
        row = df.iloc[-1]
        detaliu = {cat: row[cat] for cat in categories}
        total = sum(detaliu.values())
        top_cat = max(detaliu, key=detaliu.get)

        return {
            "user_id": user_id,
            "luna_raport": row["Luna Raportare"],
            "cheltuieli": detaliu,
            "total_cheltuieli": round(total, 2),
            "categorie_dominanta": top_cat
        }

    else:
        df["Total"] = df[categories].sum(axis=1)
        df["Categorie_Max"] = df[categories].idxmax(axis=1)

        evolutie = df[["Luna Raportare", *categories, "Total", "Categorie_Max"]].to_dict(orient="records")

        return {
            "user_id": user_id,
            "evolutie_cheltuieli": evolutie
        }




