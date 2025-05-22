import sqlite3
import pandas as pd

# Conectare la baza de date
conn = sqlite3.connect("bcr_hackathon.db")

# Citește tot tabelul sursă
df = pd.read_sql("SELECT * FROM hackathon_data", conn)

# Dicționar cu scopuri și coloanele relevante
scoped_columns = {
    "profil_clienti": {
        "ID": "ID_Client",
        "POSTING_DATE": "Luna Raportare",
        "GPI_AGE": "Varsta",
        "GPI_GENDER_CODE": "Gen",
        "GPI_MARITAL_SATUS_CODE": "Stare_Civila",
        "GPI_CLS_CODE_PT_OCCUP": "Ocupatie",
        "GPI_CLS_PT_EDU_DESC": "Educatie",
        "GPI_DOMICILE_TYPE": "Mediu",
        "GPI_REGION_NAME": "Regiune"
    },
    "loialitate_client": {
        "ID": "ID_Client",
        "POSTING_DATE": "Luna Raportare",
        "CLIENT_TENURE": "Vechime_Client",
        "CLIENT_TENURE_ACTIVE_ACC": "Vechime_Cont_Activ",
        "PTS_CLIENT_STATUS_ND": "Zile_Status_Activ",
        "CRT_LST_ACC_CLOSE_ND": "Zile_De_La_Inchidere_Cont"
    },
    "produse_financiare_active": {
        "ID": "ID_Client",
        "POSTING_DATE": "Luna Raportare",
        "CRT_ALL_ACTIVE_CNT": "Conturi_Curente",
        "DEP_ALL_ACTIVE_CNT": "Depozite",
        "LOA_ALL_ACTIVE_CNT": "Credite",
        "ICC_ALL_ACTIVE_CNT": "Carduri_Credit",
        "INV_ALL_ACTIVE_CNT": "Investitii",
        "INS_VIG_ALL_ACTIVE_CNT": "Asigurari"
    },
    "solduri": {
        "ID": "ID_Client",
        "POSTING_DATE": "Luna Raportare",
        "CRT_TOTAL_BALANCE_AMT": "Sold_Cont_Curent",
        "DEP_TOTAL_BALANCE_AMT": "Sold_Depozite",
        "LOA_TOTAL_BALANCE_AMT": "Sold_Credite",
        "CEC_TOTAL_BALANCE_AMT": "Sold_Economii",
        "OVD_TOTAL_BALANCE_AMT": "Sold_Overdraft",
        "OVD_APPROVED_LIMIT_AMT": "Limita_Overdraft",
        "ICC_TOTAL_BALANCE_AMT": "Sold_Card_Credit",
        "SAV_TOTAL_BALANCE_AMT": "Sold_Planuri_Economii"
    },
    "comportament_tranzactii": {
        "ID": "ID_Client",
        "POSTING_DATE": "Luna Raportare",
        "TRX_IN_ALL_CNT": "Nr_Tran_Intrare",
        "TRX_OUT_ALL_CNT": "Nr_Tran_Iesire",
        "TRX_IN_ALL_AMT": "Suma_Tran_Intrare",
        "TRX_OUT_ALL_AMT": "Suma_Tran_Iesire",
        "TRX_OUT_EC_CNT": "Tranzactii_Ecommerce",
        "TRX_OUT_IB_CNT": "Tranzactii_IB",
        "TRX_OUT_POS_CNT": "Tranzactii_POS",
        "TRX_OUT_ATM_CNT": "Retrageri_ATM"
    },
    "cheltuieli": {
        "ID": "ID_Client",
        "POSTING_DATE": "Luna Raportare",
        "MCC_FOOD_AMT": "Cheltuieli_Mancare",
        "MCC_LEISURE_AMT": "Cheltuieli_Timp_Liber",
        "MCC_TRAVEL_AMT": "Cheltuieli_Calatorii",
        "MCC_HOME_AND_CONSTR_AMT": "Cheltuieli_Locuinte",
        "MCC_ELECT_AND_DIG_GOODS_AMT": "Cheltuieli_Electronice"
    },
    "engagement_digital": {
        "ID": "ID_Client",
        "POSTING_DATE": "Luna Raportare",
        "CRT_GEORGE_FLAG": "Are_George",
        "PTS_IB_FLAG": "Are_IB",
        "APPLE_PAY_FLAG": "ApplePay",
        "GOOGLE_PAY_FLAG": "GooglePay",
        "GEORGE_PAY_FLAG": "GeorgePay",
        "CHNL_IB_LOGINS_CNT": "Logari_IB",
        "CHNL_BRANCH_SCANS_CNT": "Scanari_Sucursala",
        "CHNL_INBOUND_CALLS_CNT": "Apeluri_Callcenter"
    },
    "scoring_risc": {
        "ID": "ID_Client",
        "POSTING_DATE": "Luna Raportare",
        "PTS_TOTAL_LOANS_REQ_CNT": "Cereri_Credite",
        "PTS_REJECTED_LOANS_REQ_CNT": "Credite_Refuzate",
        "ICC_UTILIZATION_GRADE": "Grad_Utilizare_CC",
        "OVD_UTILIZATION_GRADE": "Grad_Utilizare_OVD",
        "OVD_REMAINING_LIMIT_AMT": "Limita_OVD_Ramasa",
        "ICC_REMAINING_LIMIT_AMT": "Limita_CC_Ramasa"
    }
}

# Parcurge fiecare scop și creează tabelul asociat
for table_name, column_map in scoped_columns.items():
    selected_cols = [col for col in column_map if col in df.columns]
    renamed_df = df[selected_cols].rename(columns=column_map)
    renamed_df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Tabel creat: {table_name} cu {len(selected_cols)} coloane.")

conn.close()