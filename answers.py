def answer_raport_financiar(data):
    trx_in = data.get("TRX_IN_ALL_AMT", 0)
    trx_out = data.get("TRX_OUT_ALL_AMT", 0)
    dep_balance = data.get("DEP_TOTAL_BALANCE_AMT", 0)
    crt_balance = data.get("CRT_TOTAL_BALANCE_AMT", 0)
    venit = data.get("GPI_LST_SALARY_ND", 0)
    
    return f"Raportul financiar pentru ultimele 6 luni: Venit {venit:.2f} lei, Tranzacții primite {trx_in:.2f} lei, Tranzacții ieșite {trx_out:.2f} lei, Sold depozit {dep_balance:.2f} lei, Sold credit {crt_balance:.2f} lei."

def answer_cheltuieli_mâncare(data):

    cheltuieli = data.get("MCC_FOOD_AMT", 0)
    return f"Cheltuielile tale pe mâncare luna trecută au fost {cheltuieli:.2f} lei."

def answer_cheltuieli_utilități(data):
    cheltuieli = data.get("MCC_UTILITY_SERV_AMT", 0)
    return f"Cheltuielile tale pe utilități au fost {cheltuieli:.2f} lei."

def answer_cheltuieli_transport(data):
    cheltuieli = data.get("MCC_TRANSPORTATION_AMT", 0)
    return f"Cheltuielile tale pe transport au fost {cheltuieli:.2f} lei."

def answer_sold_total_conturi(data):
    sold_dep = data.get("DEP_TOTAL_BALANCE_AMT", 0)
    sold_cec = data.get("CEC_TOTAL_BALANCE_AMT", 0)
    sold_crt = data.get("CRT_TOTAL_BALANCE_AMT", 0)
    total_sold = sold_dep + sold_cec + sold_crt
    return f"Soldul total în toate conturile tale este {total_sold:.2f} lei."

def answer_sold_cont_curent(data):
    sold = data.get("CRT_TOTAL_BALANCE_AMT", 0)
    return f"Soldul contului curent este {sold:.2f} lei."

def answer_sold_cont_depozit(data):
    sold = data.get("DEP_TOTAL_BALANCE_AMT", 0)
    return f"Soldul contului de depozit este {sold:.2f} lei."

def answer_sold_credit(data):
    sold = data.get("CRT_TOTAL_BALANCE_AMT", 0)
    return f"Soldul creditului tău este {sold:.2f} lei."

def answer_limita_card_credit(data):
    approved_limit = data.get("ICC_APPROVED_LIMIT", 0)
    remaining_limit = data.get("ICC_REMAINING_LIMIT_AMT", 0)
    return f"Limita ta aprobată la cardul de credit este {approved_limit:.2f} lei, iar limita rămasă este {remaining_limit:.2f} lei."

def answer_cheltuieli_digital_payments(data):
    cheltuieli = data.get("MCC_DIGITAL_PAYMENTS_AMT", 0)
    return f"Cheltuielile tale folosind portofele digitale au fost {cheltuieli:.2f} lei."

def answer_tranzacții_atm(data):
    tranzacții_in = data.get("TRX_IN_ATM_CNT", 0)
    tranzacții_out = data.get("TRX_OUT_ATM_CNT", 0)
    return f"Ai avut {tranzacții_in} tranzacții intrare și {tranzacții_out} tranzacții ieșire la ATM."

def answer_cheltuieli_retail(data):
    cheltuieli = data.get("MCC_RETAIL_AMT", 0)
    return f"Cheltuielile tale în retail au fost {cheltuieli:.2f} lei."

def answer_limita_credit_utilizata(data):
    utilizare = data.get("CRT_UTILIZATION_GRADE", 0)
    return f"Gradul de utilizare a creditului tău este {utilizare:.2f}%."

def answer_venit_luna_trecuta(data):
    venit = data.get("GPI_LST_SALARY_ND", 0)
    return f"Venitul tău din luna trecută a fost {venit:.2f} lei."

def answer_economisire_10_percent(data):
    economii = data.get("SAV_TOTAL_BALANCE_AMT", 0)
    return f"Economiile tale sunt de {economii:.2f} lei, reprezentând {economii / 100:.2f}% din venitul tău."

def answer_produse_active_banca(data):
    produse = data.get("PRODUSE_ACTIVE_BANCA", 0)
    return f"Ai {produse} produse active la bancă."

def answer_durata_relatie_banca(data):
    durata = data.get("DURATA_RELATIE_BANCA", 0)
    return f"Durata relației tale cu banca este de {durata} ani."

def answer_stare_cererilor_imprumut(data):
    cereri = data.get("CERERI_IMPRUMUT", 0)
    return f"Numărul cererilor tale de împrumut este {cereri}."

def answer_cheltuieli_calatorii(data):
    cheltuieli = data.get("MCC_TRAVEL_AMT", 0)
    return f"Cheltuielile tale pentru călătorii au fost {cheltuieli:.2f} lei."

def answer_cheltuieli_divertisment(data):
    cheltuieli = data.get("MCC_LEISURE_AMT", 0)
    return f"Cheltuielile tale pentru divertisment au fost {cheltuieli:.2f} lei."

def answer_sold_cont_economii(data):
    sold = data.get("SAV_TOTAL_BALANCE_AMT", 0)
    return f"Soldul tău în contul de economii este {sold:.2f} lei."

def answer_intretinere_locuinta(data):
    cheltuieli = data.get("MCC_HOME_AND_CONSTR_AMT", 0)
    return f"Cheltuielile tale pentru întreținerea locuinței au fost {cheltuieli:.2f} lei."

def answer_cheltuieli_îmbrăcăminte(data):
    cheltuieli = data.get("MCC_CLOTHING_AMT", 0)
    return f"Cheltuielile tale pentru îmbrăcăminte au fost {cheltuieli:.2f} lei."

def answer_servicii_profesionale(data):
    cheltuieli = data.get("MCC_PROFESSIONAL_SERV_AMT", 0)
    return f"Cheltuielile tale pentru servicii profesionale au fost {cheltuieli:.2f} lei."

def answer_cheltuieli_restaurante(data):
    cheltuieli = data.get("MCC_FOOD_AMT", 0)
    return f"Cheltuielile tale la restaurante au fost {cheltuieli:.2f} lei."

def answer_utilizare_overdraft(data):
    utilizare = data.get("OVD_UTILIZATION_GRADE", 0)
    return f"Gradul de utilizare a overdraft-ului este {utilizare:.2f}%."

def answer_sold_refinanțare(data):
    sold = data.get("REFIN_ALL_ACTIVE_CNT", 0)
    return f"Soldul contului de refinanțare este {sold:.2f} lei."

def answer_tranzacții_international(data):
    tranzacții_in = data.get("TRX_IN_OTH_COUNTRY_CNT", 0)
    tranzacții_out = data.get("TRX_OUT_OTH_COUNTRY_CNT", 0)
    return f"Ai avut {tranzacții_in} tranzacții intrare și {tranzacții_out} tranzacții ieșire în afacerea țării."

def answer_venituri_cheltuieli_anul(data):
    venit = data.get("TRX_IN_ALL_AMT", 0)
    cheltuieli = data.get("TRX_OUT_ALL_AMT", 0)
    return f"Veniturile tale pe anul trecut au fost {venit:.2f} lei și cheltuielile tale au fost {cheltuieli:.2f} lei."

def answer_istoric_imprumuturi(data):
    cereri_total = data.get("PTS_TOTAL_LOANS_REQ_CNT", 0)
    cereri_resp = data.get("PTS_REJECTED_LOANS_REQ_CNT", 0)
    return f"Ai avut {cereri_total} cereri de împrumut, din care {cereri_resp} au fost respinse."

def answer_produse_asigurare(data):
    asigurari = data.get("INS_VIG_ALL_ACTIVE_CNT", 0)
    return f"Ai {asigurari} produse de asigurare active."

def answer_plăți_portofele_digitale(data):
    plăți = data.get("WALLET_FLAG", 0)
    return f"Ai realizat {plăți} plăți folosind portofele digitale."

def answer_servicii_afaceri(data):
    cheltuieli = data.get("MCC_BUSINESS_SERV_AMT", 0)
    return f"Cheltuielile tale pentru servicii de afaceri au fost {cheltuieli:.2f} lei."

def answer_comisioane_bancare(data):
    comisioane = data.get("MCC_BANKING_ALTER_AMT", 0)
    return f"Comisioanele tale bancare au fost {comisioane:.2f} lei."

def answer_sold_economii(data):
    sold = data.get("SAV_TOTAL_BALANCE_AMT", 0)
    return f"Soldul tău pe contul de economii este {sold:.2f} lei."

def answer_tranzacții_internet_banking(data):
    tranzacții = data.get("TRX_OUT_IB_CNT", 0)
    return f"Ai realizat {tranzacții} tranzacții prin Internet Banking."

def answer_scor_credit(data):
    scor = data.get("PTS_CLIENT_STATUS_ND", 0)
    return f"Scorul tău de credit este {scor}."

def answer_utilizare_credit_ipotecar(data):
    utilizare = data.get("LOA_UTILIZATION_GRADE", 0)
    return f"Gradul tău de utilizare a creditului ipotecar este {utilizare:.2f}%."

def answer_sold_conturi_ultimele_3_luni(data):
    sold_avg = data.get("SAV_AVG_BALANCE_AMT", 0)
    return f"Soldul mediu pe conturi în ultimele 3 luni este {sold_avg:.2f} lei."

def answer_evolutie_cheltuieli_ultimele_12_luni(data):
    cheltuieli = data.get("TRX_OUT_ALL_AMT", 0)
    return f"Evoluția cheltuielilor tale pe ultimele 12 luni este {cheltuieli:.2f} lei."