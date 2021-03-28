import matplotlib.pyplot as plt
import pandas as pd
import os

# URL da cui scaricare i dati necessari
URLS = {
    "nazionale": "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv",
    "regioni": "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",
    "vaccini_summary": "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.csv",
    "anagrafica_vaccini_summary": "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/anagrafica-vaccini-summary-latest.csv",
    "somministrazioni_vaccini_summary": "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-summary-latest.csv",
    "consegne_vaccini": "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/consegne-vaccini-latest.csv",
    "somministrazioni_vaccini": "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv"
}

# Colonne che necessitano la conversione in formato datetime (tutti i csv)
DATETIME_COLUMNS = ["data", "data_somministrazione", "data_consegna"]

TOTALE_TERAPIA_INTENSIVA = {
    "nazionale": 9059,
    "Abruzzo": 215,
    "Basilicata": 88,
    "Calabria": 152,
    "Campania": 620,
    "Emilia-Romagna": 760,
    "Friuli Venezia Giulia": 175,
    "Lazio": 943,
    "Liguria": 222,
    "Lombardia": 1416,
    "Marche": 240,
    "Molise": 17,
    "P.A. Bolzano": 100,
    "P.A. Trento": 90,
    "Piemonte": 628,
    "Puglia": 659,
    "Sardegna": 208,
    "Sicilia": 834,
    "Toscana": 601,
    "Umbria": 139,
    "Valle d'Aosta": 20,
    "Veneto": 1000
}

FASCE_POPOLAZIONE = {
    "16-19": {
        "nazionale": 2298846,
        "Abruzzo": 46751,
        "Basilicata": 22032,
        "Calabria": 76743,
        "Campania": 261694,
        "Emilia-Romagna": 160045,
        "Friuli Venezia Giulia": 42431,
        "Lazio": 211964,
        "Liguria": 51388,
        "Lombardia": 377933,
        "Marche": 55166,
        "Molise": 10882,
        "P.A. Bolzano": 23269,
        "P.A. Trento": 22424,
        "Piemonte": 153619,
        "Puglia": 166541,
        "Sardegna": 55615,
        "Sicilia": 207885,
        "Toscana": 130759,
        "Umbria": 30749,
        "Valle d'Aosta": 4706,
        "Veneto": 186250        
        },
    "20-29": {
        "nazionale": 6084382,
        "Abruzzo": 130083,
        "Basilicata": 61183,
        "Calabria": 213889,
        "Campania": 693479,
        "Emilia-Romagna": 420660,
        "Friuli Venezia Giulia": 109351,
        "Lazio": 564461,
        "Liguria": 136323,
        "Lombardia": 986159,
        "Marche": 146739,
        "Molise": 32122,
        "P.A. Bolzano": 61094,
        "P.A. Trento": 57755,
        "Piemonte": 406190,
        "Puglia": 439275,
        "Sardegna": 152275,
        "Sicilia": 559157,
        "Toscana": 339743,
        "Umbria": 339743,
        "Valle d'Aosta": 11870,
        "Veneto": 481226        
        },
    "30-39": {
        "nazionale": 7552646,
        "Abruzzo": 150713,
        "Basilicata": 65204,
        "Calabria": 236668,
        "Campania": 715258,
        "Emilia-Romagna": 501241,
        "Friuli Venezia Giulia": 125629,
        "Lazio": 682708,
        "Liguria": 147602,
        "Lombardia": 1164199,
        "Marche": 166387,
        "Molise": 34661,
        "P.A. Bolzano": 63127,
        "P.A. Trento": 61062,
        "Piemonte": 459367,
        "Puglia": 460961,
        "Sardegna": 185432,
        "Sicilia": 589747,
        "Toscana": 401488,
        "Umbria": 97163,
        "Valle d'Aosta": 13174,
        "Veneto": 532841        
        },
    "40-49": {
        "nazionale": 8937229,
        "Abruzzo": 190060,
        "Basilicata": 78467,
        "Calabria": 266417,
        "Campania": 835597,
        "Emilia-Romagna": 693312,
        "Friuli Venezia Giulia": 178677,
        "Lazio": 906328,
        "Liguria": 212370,
        "Lombardia": 1545073,
        "Marche": 224450,
        "Molise": 42214,
        "P.A. Bolzano": 75664,
        "P.A. Trento": 78088,
        "Piemonte": 632745,
        "Puglia": 583292,
        "Sardegna": 250930,
        "Sicilia": 698439,
        "Toscana": 556667,
        "Umbria": 127832,
        "Valle d'Aosta": 18555,
        "Veneto": 742052        
        },
    "50-59": {
        "nazionale": 9414195,
        "Abruzzo": 204157,
        "Basilicata": 605586,
        "Calabria": 286804,
        "Campania": 868684,
        "Emilia-Romagna": 704097,
        "Friuli Venezia Giulia": 196083,
        "Lazio": 932830,
        "Liguria": 252685,
        "Lombardia": 1592109,
        "Marche": 236194,
        "Molise": 47443,
        "P.A. Bolzano": 83539,
        "P.A. Trento": 85805,
        "Piemonte": 688698,
        "Puglia": 605586,
        "Sardegna": 266068,
        "Sicilia": 732965,
        "Toscana": 587110,
        "Umbria": 135299,
        "Valle d'Aosta": 20757,
        "Veneto": 799460        
        },
    "60-69": {
        "nazionale": 7364364,
        "Abruzzo": 167705,
        "Basilicata": 72817,
        "Calabria": 241215,
        "Campania": 670867,
        "Emilia-Romagna": 542211,
        "Friuli Venezia Giulia": 155789,
        "Lazio": 697089,
        "Liguria": 202775,
        "Lombardia": 1189118,
        "Marche": 193166,
        "Molise": 40509,
        "P.A. Bolzano": 57041,
        "P.A. Trento": 67027,
        "Piemonte": 558231,
        "Puglia": 490900,
        "Sardegna": 223641,
        "Sicilia": 601201,
        "Toscana": 463253,
        "Umbria": 110539,
        "Valle d'Aosta": 16060,
        "Veneto": 603210        
        },
    "70-79": {
        "nazionale": 5968373,
        "Abruzzo": 130572,
        "Basilicata": 51805,
        "Calabria": 175208,
        "Campania": 484380,
        "Emilia-Romagna": 457129,
        "Friuli Venezia Giulia": 141409,
        "Lazio": 552007,
        "Liguria": 186034,
        "Lombardia": 996209,
        "Marche": 155941,
        "Molise": 30291,
        "P.A. Bolzano": 46613,
        "P.A. Trento": 52316,
        "Piemonte": 477416,
        "Puglia": 390534,
        "Sardegna": 170857,
        "Sicilia": 456965,
        "Toscana": 410151,
        "Umbria": 95004,
        "Valle d'Aosta": 13089,
        "Veneto": 494443        
        },
    "80-89": {
        "nazionale": 3628160,
        "Abruzzo": 84488,
        "Basilicata": 36107,
        "Calabria": 107720,
        "Campania": 255273,
        "Emilia-Romagna": 297666,
        "Friuli Venezia Giulia": 83307,
        "Lazio": 331378,
        "Liguria": 125810,
        "Lombardia": 609477,
        "Marche": 107825,
        "Molise": 21038,
        "P.A. Bolzano": 27108,
        "P.A. Trento": 30464,
        "Piemonte": 306712,
        "Puglia": 222224,
        "Sardegna": 95172,
        "Sicilia": 263130,
        "Toscana": 259653,
        "Umbria": 62778,
        "Valle d'Aosta": 7800,
        "Veneto": 293030        
        },
    "90+": {
        "nazionale": 791543,
        "Abruzzo": 19515,
        "Basilicata": 7823,
        "Calabria": 23058,
        "Campania": 49044,
        "Emilia-Romagna": 71687,
        "Friuli Venezia Giulia": 20186,
        "Lazio": 69227,
        "Liguria": 30159,
        "Lombardia": 128163,
        "Marche": 25540,
        "Molise": 5219,
        "P.A. Bolzano": 6165,
        "P.A. Trento": 7922,
        "Piemonte": 64688,
        "Puglia": 45902,
        "Sardegna": 21111,
        "Sicilia": 52785,
        "Toscana": 60936,
        "Umbria": 15139,
        "Valle d'Aosta": 1764,
        "Veneto": 65510        
        },
    "totale": {
        "nazionale": 59641488,
        "Abruzzo": 1293941,
        "Basilicata": 553254,
        "Calabria": 1894110,
        "Campania": 5712143,
        "Emilia-Romagna": 4464119,
        "Friuli Venezia Giulia": 1206216,
        "Lazio": 5755700,
        "Liguria": 1524826,
        "Lombardia": 10027602,
        "Marche": 1512672,
        "Molise": 300516,
        "P.A. Bolzano": 532644,
        "P.A. Trento": 545425,
        "Piemonte": 4311217,
        "Puglia": 3953305,
        "Sardegna": 1611621,
        "Sicilia": 4875290,
        "Toscana": 3692555,
        "Umbria": 870165,
        "Valle d'Aosta": 125034,
        "Veneto": 4879133
    }
    }

# Contiene tutti i dati elaborati
data = {}

def download_csv(name, url):
    dataframe = pd.read_csv(url)

    for col in DATETIME_COLUMNS:
        if col in dataframe:
            dataframe[col] = pd.to_datetime(dataframe[col], format="%Y-%m-%dT%H:%M:%S")
    
    # Codici ISTAT delle regioni
    # 01 PIEMONTE 02 VALLE D’AOSTA 03 LOMBARDIA 04 TRENTINO A. A. 05 VENETO 06 FRIULI V. G 07 LIGURIA 08 EMILIA ROMAGNA 09 TOSCANA
    # 10 UMBRIA 11 MARCHE 12 LAZIO 13 ABRUZZI 14 MOLISE 15 CAMPANIA 16 PUGLIE 17 BASILICATA 18 CALABRIA 19 SICILIA 20 SARDEGNA
    # 21 BOLZANO 22 TRENTO
    if name == "regioni":
        data["regioni"] = {}
        for codice_regione in [x for x in range(1,23) if x != 4]:
            data_regione = dataframe[dataframe["codice_regione"] == codice_regione]
            data["regioni"][codice_regione] = data_regione
    elif name == "somministrazioni_vaccini_summary":
        data["somministrazioni_vaccini_summary"] = {"nazionale": dataframe}
        data["somministrazioni_vaccini_summary"]["regioni"] = {}
        for codice_regione in [x for x in range(1,22) if x != 4]:
            data_regione = dataframe[dataframe["codice_regione_ISTAT"] == codice_regione]
            data["somministrazioni_vaccini_summary"]["regioni"][codice_regione] = data_regione
        data["somministrazioni_vaccini_summary"]["regioni"][21] = dataframe[dataframe["nome_area"] == "Provincia Autonoma Trento"]
        data["somministrazioni_vaccini_summary"]["regioni"][22] = dataframe[dataframe["nome_area"] == "Provincia Autonoma Bolzano / Bozen"]
    elif name == "somministrazioni_vaccini":
        data["somministrazioni_vaccini"] = {"nazionale": dataframe}
        data["somministrazioni_vaccini"]["regioni"] = {}
        # In questo dataset le P.A. hanno lo stesso codice istat (4) ma differente denominazione 
        for codice_regione in [x for x in range(1,22) if x != 4]:
            data_regione = dataframe[dataframe["codice_regione_ISTAT"] == codice_regione]
            data["somministrazioni_vaccini"]["regioni"][codice_regione] = data_regione
        data["somministrazioni_vaccini"]["regioni"][21] = dataframe[dataframe["nome_area"] == "Provincia Autonoma Trento"]
        data["somministrazioni_vaccini"]["regioni"][22] = dataframe[dataframe["nome_area"] == "Provincia Autonoma Bolzano / Bozen"]
    else:
        data[name] = dataframe

def grafico_base(x, y, title, output, xlabel=None, ylabel=None, media_mobile=None, legend=None, color=None, grid="y", hline=None, vline=None, marker=None):
    fig, ax = plt.subplots()
    line, = ax.plot(x, y, marker=marker)
    if media_mobile:
        ax.plot(x, media_mobile, color="orange")
        ax.legend(legend, prop={"size": 7})
    
    if color:
        line.set_color(color)

    if grid:
        ax.grid(axis=grid)
    
    if hline:
        plt.axhline(hline, 0, 1, color="red")

    if vline:
        plt.axvline(vline, 0, 1, color="red")

    fig.autofmt_xdate()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    fig.savefig(CWD+output, dpi=200)
    plt.close('all')

def stackplot(x, y1, y2, title, label, output, soglia=None, yticks=None):
    fig, ax = plt.subplots()
    ax.stackplot(x, y1, y2, labels=label)

    if soglia:
        ax.axhline(soglia, color="red")
    if yticks:
        ax.set_yticks(yticks)
    ax.set_title(title)
    ax.legend(label, loc="upper left", prop={"size":7})
    ax.grid(axis="y")
    fig.autofmt_xdate()
    fig.savefig(CWD+output, dpi=200)
    plt.close('all')

def grafico_verticale(x, y, title, output):
    fig, ax = plt.subplots()
    color = ["orange" if x>=0 else "red" for x in y]
    plt.vlines(x=x, ymin=0, ymax=y, color=color, alpha=0.7)
    ax.set_title(title)
    fig.autofmt_xdate()
    ax.grid(axis="y")
    fig.savefig(CWD+output, dpi=200)
    plt.close('all')

def istogramma(x, y, title, output, horizontal=False, xticks=None, yticks=None, grid="y", bottom=None, ylabel=None, label1=None, label2=None, xticklabels=None):
    fig, ax = plt.subplots()

    if horizontal:
        ax.barh(x, y, label=label1)
    else:
        ax.bar(x, y, label=label1)
    
    plt.title(title)

    if grid:
        ax.grid(axis=grid)
    
    if xticks:
        plt.xticks(xticks)
    
    if yticks:
        plt.yticks(yticks)

    if bottom and horizontal:
        ax.barh(x, bottom, bottom=y, label=label2)
    elif bottom:
        ax.bar(x, bottom, bottom=y, label=label2)

    if label1 or label2:
        plt.legend()
    
    if ylabel:
        ax.set_ylabel(ylabel)

    if xticklabels:
        ax.set_xticklabels(xticklabels)

    fig.savefig(CWD+output, dpi=200)

    plt.close('all')

def torta(slices, labels, title, output):
    fig, ax = plt.subplots()
    ax.pie(slices, labels=labels)
    plt.title(title)

    fig.savefig(CWD+output, dpi=200)
    plt.close('all')

def create_media_mobile(data):
    count = []
    result = []
    
    for el in data:
        count.append(el)
        result.append(sum(count)/len(count))
        if len(count) == 7:
            count.pop(0)
    return result

def create_delta(data):
    latest = 0
    delta = []

    for row in data:
        delta.append(row-latest)
        latest = row
    
    return delta

def create_incidenza(data, regione):
    count = []
    result = []
    for row in data:
        count.append(row)
        result.append((sum(count)/FASCE_POPOLAZIONE["totale"][regione])*100000)
        if len(count) == 7:
            count.pop(0)
    return result

def nazionale():
    os.makedirs(f"{CWD}/graphs/epidemia", exist_ok=True)
    summary = "DATI NAZIONALI {}\n\n".format(data["nazionale"]["data"].iat[-1])
    # Grafico nuovi positivi
    print("Grafico nuovi positivi...")
    grafico_base(
        data["nazionale"]["data"],
        data["nazionale"]["nuovi_positivi"],
        "Andamento contagi giornalieri",
        "/graphs/epidemia/nuovi_positivi.jpg",
        media_mobile=create_media_mobile(data["nazionale"]["nuovi_positivi"]),
        legend=["Contagi giornalieri", "Media mobile settimanale"]
    )
    summary += "Nuovi positivi: {}\n".format(data["nazionale"]["nuovi_positivi"].iat[-1])
    print("Grafico completato")

    # Stackplot ospedalizzati
    print("Grafico ospedalizzati...")
    stackplot(
        data["nazionale"]["data"],
        data["nazionale"]["terapia_intensiva"],
        data["nazionale"]["ricoverati_con_sintomi"],
        "Andamento ospedalizzati",
        ["Soglia critica TI", "Terapie intensive", "Ricoverati con sintomi"],
        "/graphs/epidemia/andamento_ospedalizzati.jpg",
        soglia=(TOTALE_TERAPIA_INTENSIVA["nazionale"]/100)*30, 
    )
    summary += "Ospedalizzati ordinari: {}\nTerapie intensive: {}\n".format(data["nazionale"]["ricoverati_con_sintomi"].iat[-1], data["nazionale"]["terapia_intensiva"].iat[-1])
    print("Grafico completato")

    # Grafico ingressi in terapia intensiva
    print("Grafico ingressi TI...")
    grafico_base(
        data["nazionale"]["data"],
        data["nazionale"]["ingressi_terapia_intensiva"],
        "Ingressi giornalieri in terapia intensiva",
        "/graphs/epidemia/ingressi_ti.jpg",
        media_mobile=create_media_mobile(data["nazionale"]["ingressi_terapia_intensiva"]),
        legend=["Ingressi TI", "Media mobile settimanale"],
    )
    summary += "Ingressi TI: {}\n".format(data["nazionale"]["ingressi_terapia_intensiva"].iat[-1])
    print("Grafico completato")

    # Grafico variazione totale positivi
    print("Grafico variazione totale positivi...")
    grafico_verticale(
        data["nazionale"]["data"],
        data["nazionale"]["variazione_totale_positivi"],
        "Variazione giornaliera totale positivi",
        "/graphs/epidemia/variazione_totale_positivi.jpg"
    )
    summary += "Variazione totale totale positivi: {}\n".format(data["nazionale"]["variazione_totale_positivi"].iat[-1])
    print("Grafico completato")

    # Grafico variazione totale ospedalizzati
    print("Grafico variazione totale ospedalizzati...")
    delta = create_delta(data["nazionale"]["totale_ospedalizzati"])
    grafico_verticale(
        data["nazionale"]["data"],
        delta,
        "Variazione totale ospedalizzati",
        "/graphs/epidemia/variazione_totale_ospedalizzati.jpg"
    )
    summary += "Variazione totale ospedalizzati: {}\n".format(delta[-1])
    print("Grafico completato")

    # Grafico variazione occupazione TI
    print("Grafico variazione TI")
    delta = create_delta(data["nazionale"]["terapia_intensiva"])
    grafico_verticale(
        data["nazionale"]["data"],
        delta,
        "Variazione occupazione TI",
        "/graphs/epidemia/variazione_ti.jpg"
    )
    summary += "Variazione TI: {}\n".format(delta[-1])
    print("Grafico completato")

    # Grafico variazione totale ospedalizzati
    print("Grafico variazione ricoverati con sintomi...")
    delta = create_delta(data["nazionale"]["ricoverati_con_sintomi"])
    grafico_verticale(
        data["nazionale"]["data"],
        delta,
        "Variazione ospedalizzati ordinari",
        "/graphs/epidemia/variazione_ospedalizzati_ordinari.jpg"
    )
    summary += "Variazione ricoverati con sintomi: {}\n".format(delta[-1])
    print("Grafico completato")

    # Grafico deceduti
    print("Grafico deceduti...")
    grafico_base(
        data["nazionale"]["data"],
        data["nazionale"]["deceduti"],
        "Andamento deceduti",
        "/graphs/epidemia/deceduti.jpg",
        color="black"
    )
    summary += "Deceduti totali: {}\n".format(data["nazionale"]["deceduti"].iat[-1])
    print("Grafico completato")

    # Grafico deceduti giornalieri
    print("Grafico deceduti giornalieri...")
    delta = create_delta(data["nazionale"]["deceduti"])
    grafico_base(
        data["nazionale"]["data"],
        delta,
        "Deceduti giornalieri",
        "/graphs/epidemia/deceduti_giornalieri.jpg",
        media_mobile=create_media_mobile(create_delta(data["nazionale"]["deceduti"])),
        legend=["Deceduti giornalieri", "Media mobile settimanale"],
        color="black"
    )
    summary += "Deceduti giornalieri: {}\n".format(delta[-1])
    print("Grafico completato")

    print("Grafico incidenza...")
    incidenza = create_incidenza(data["nazionale"]["nuovi_positivi"], "nazionale")
    grafico_base(
        data["nazionale"]["data"],
        incidenza,
        "Incidenza di nuovi positivi ogni 100000 abitanti\nnell'arco di 7 giorni",
        "/graphs/epidemia/incidenza_contagio.jpg",
        hline=250
    )
    summary += f"Incidenza: {incidenza[-1]}\n\n"
    print("Grafico completato")

    return summary

def regioni():
    summary = "DATI REGIONI\n\n"
    for regione in data["regioni"].keys():
        denominazione_regione = data["regioni"][regione]["denominazione_regione"].iloc[0]
        summary += f"{denominazione_regione}\n"
        print(f"Regione {regione}...")
        print("Grafico nuovi positivi...")
        grafico_base(
            data["regioni"][regione]["data"],
            data["regioni"][regione]["nuovi_positivi"],
            f"Andamento contagi giornalieri {denominazione_regione}",
            f"/graphs/epidemia/nuovi_positivi_{denominazione_regione}.jpg",
            media_mobile=create_media_mobile(data["regioni"][regione]["nuovi_positivi"]),
            legend=["Contagi giornalieri", "Media mobile settimanale"]
        )
        summary += "Nuovi positivi: {}\n".format(data["regioni"][regione]["nuovi_positivi"].iat[-1])
        print("Grafico completato")

        # Stackplot ospedalizzati
        print("Grafico ospedalizzati...")
        stackplot(
            data["regioni"][regione]["data"],
            data["regioni"][regione]["terapia_intensiva"],
            data["regioni"][regione]["ricoverati_con_sintomi"],
            f"Andamento ospedalizzati {denominazione_regione}",
            ["Soglia critica TI", "Terapie intensive", "Ricoverati con sintomi"],
            f"/graphs/epidemia/andamento_ospedalizzati_{denominazione_regione}.jpg",
            soglia=(TOTALE_TERAPIA_INTENSIVA[denominazione_regione]/100)*30
        )
        summary += "TI: {}\nRicoverati con sintomi: {}\n".format(data["regioni"][regione]["terapia_intensiva"].iat[-1], data["regioni"][regione]["ricoverati_con_sintomi"].iat[-1])
        print("Grafico completato")

        # Grafico ingressi in terapia intensiva
        print("Grafico ingressi TI...")
        grafico_base(
            data["regioni"][regione]["data"],
            data["regioni"][regione]["ingressi_terapia_intensiva"],
            f"Ingressi giornalieri in terapia intensiva {denominazione_regione}",
            f"/graphs/epidemia/ingressi_ti_{denominazione_regione}.jpg",
            media_mobile=create_media_mobile(data["regioni"][regione]["ingressi_terapia_intensiva"]),
            legend=["Ingressi TI", "Media mobile settimanale"],
        )
        summary += "Ingressi TI: {}\n".format(data["regioni"][regione]["ingressi_terapia_intensiva"].iat[-1])
        print("Grafico completato")

        # Grafico variazione totale positivi
        print("Grafico variazione totale positivi...")
        grafico_verticale(
            data["regioni"][regione]["data"],
            data["regioni"][regione]["variazione_totale_positivi"],
            f"Variazione giornaliera totale positivi {denominazione_regione}",
            f"/graphs/epidemia/variazione_totale_positivi_{denominazione_regione}.jpg"
        )
        summary += "Variazione totale positivi: {}\n".format(data["regioni"][regione]["variazione_totale_positivi"].iat[-1])
        print("Grafico completato")

        # Grafico variazione totale ospedalizzati
        print("Grafico variazione totale ospedalizzati...")
        grafico_verticale(
            data["regioni"][regione]["data"],
            create_delta(data["regioni"][regione]["totale_ospedalizzati"]),
            f"Variazione totale ospedalizzati {denominazione_regione}",
            f"/graphs/epidemia/variazione_totale_ospedalizzati_{denominazione_regione}.jpg"
        )
        summary += "Variazione totale ospedalizzati: {}\n".format(create_delta(data["regioni"][regione]["totale_ospedalizzati"])[-1])
        print("Grafico completato")

        # Grafico variazione occupazione TI
        print("Grafico variazione TI")
        grafico_verticale(
            data["regioni"][regione]["data"],
            create_delta(data["regioni"][regione]["terapia_intensiva"]),
            f"Variazione occupazione TI {denominazione_regione}",
            f"/graphs/epidemia/variazione_ti_{denominazione_regione}.jpg"
        )
        summary += "Variazione TI: {}\n".format(create_delta(data["regioni"][regione]["terapia_intensiva"])[-1])
        print("Grafico completato")

        # Grafico variazione totale ospedalizzati
        print("Grafico variazione ricoverati con sintomi...")
        grafico_verticale(
            data["regioni"][regione]["data"],
            create_delta(data["regioni"][regione]["ricoverati_con_sintomi"]),
            "Variazione ospedalizzati ordinari",
            f"/graphs/epidemia/variazione_ospedalizzati_ordinari_{denominazione_regione}.jpg"
        )
        summary += "Variazione ricoverati con sintomi: {}\n".format(create_delta(data["regioni"][regione]["ricoverati_con_sintomi"])[-1])
        print("Grafico completato")

        # Grafico deceduti
        print("Grafico deceduti...")
        grafico_base(
            data["regioni"][regione]["data"],
            data["regioni"][regione]["deceduti"],
            f"Andamento deceduti {denominazione_regione}",
            f"/graphs/epidemia/deceduti_{denominazione_regione}.jpg",
            color="black"
        )
        summary += "Deceduti totali: {}\n".format(data["regioni"][regione]["deceduti"].iat[-1])
        print("Grafico completato")

        # Grafico deceduti giornalieri
        print("Grafico deceduti giornalieri...")
        grafico_base(
            data["regioni"][regione]["data"],
            create_delta(data["regioni"][regione]["deceduti"]),
            f"Deceduti giornalieri {denominazione_regione}",
            f"/graphs/epidemia/deceduti_giornalieri_{denominazione_regione}.jpg",
            media_mobile=create_media_mobile(create_delta(data["regioni"][regione]["deceduti"])),
            legend=["Deceduti giornalieri", "Media mobile settimanale"],
            color="black"
        )
        summary += "Deceduti giornalieri: {}\n".format(create_delta(data["regioni"][regione]["deceduti"])[-1])
        print("Grafico completato")

        print("Grafico incidenza...")
        incidenza = create_incidenza(data["regioni"][regione]["nuovi_positivi"], denominazione_regione)
        grafico_base(
            data["regioni"][regione]["data"],
            incidenza,
            f"Incidenza di nuovi positivi ogni 100000 abitanti\nnell'arco di 7 giorni in {denominazione_regione}",
            f"/graphs/epidemia/incidenza_contagio_{denominazione_regione}.jpg",
            hline=250
        )
        summary += f"Incidenza: {incidenza[-1]}\n\n"
        print("Grafico completato")
    
    return summary

def vaccini_nazionale():
    os.makedirs(f"{CWD}/graphs/vaccini", exist_ok=True)

    print("Grafico percentuale somministrazione...")
    istogramma(
        data["vaccini_summary"]["area"],
        data["vaccini_summary"]["percentuale_somministrazione"],
        "Percentuale dosi somministrate per regioni",
        "/graphs/vaccini/percentuale_somministrazione_regioni.jpg",
        xticks=range(0, 100, 5),
        horizontal=True
    )
    print("Grafico completato")

    print("Grafico popolazione vaccinata seconda dose...")
    vaccinati_seconda_dose = data["anagrafica_vaccini_summary"]["seconda_dose"].sum()
    popolazione_totale = FASCE_POPOLAZIONE["totale"]['nazionale']
    torta(
        [
            popolazione_totale,
            vaccinati_seconda_dose
        ],
        [
            f"Totale popolazione\n ({popolazione_totale})",
            f"Persone vaccinate\n ({vaccinati_seconda_dose}, {round((vaccinati_seconda_dose/popolazione_totale)*100, 2)}%)"
        ],
        "Persone che hanno completato il ciclo di vaccinazione\nsul totale della popolazione",
        "/graphs/vaccini/percentuale_vaccinati.jpg"
    )

    print("Grafico popolazione vaccinata prima dose...")
    vaccinati_prima_dose = data["anagrafica_vaccini_summary"]["prima_dose"].sum()
    torta(
        [
            popolazione_totale,
            vaccinati_prima_dose
        ],
        [
            f"Totale popolazione\n ({popolazione_totale})",
            f"Persone vaccinate\n ({vaccinati_prima_dose}, {round((vaccinati_prima_dose/popolazione_totale)*100, 2)}%)"
        ],
        "Persone che hanno ricevuto almeno una dose\nsul totale della popolazione",
        "/graphs/vaccini/percentuale_vaccinati_prima_dose.jpg"
    )

    print("Grafico vaccinazioni giornaliere...")
    somministrazioni = data["somministrazioni_vaccini_summary"]["nazionale"].groupby("data_somministrazione")["totale"].sum().to_dict()
    grafico_base(
        somministrazioni.keys(),
        somministrazioni.values(),
        "Vaccinazioni giornaliere",
        "/graphs/vaccini/vaccinazioni_giornaliere.jpg",
        media_mobile=create_media_mobile(somministrazioni.values()),
        legend=["Vaccinazioni giornaliere", "Media mobile settimanale"],
        marker="."
    )
    print("Grafico completato")    

    print("Grafico vaccinazione giornaliere, prima e seconda dose...")
    prima_dose = data["somministrazioni_vaccini_summary"]["nazionale"].groupby("data_somministrazione")["prima_dose"].sum().to_dict()
    seconda_dose = data["somministrazioni_vaccini_summary"]["nazionale"].groupby("data_somministrazione")["seconda_dose"].sum().to_dict()
    stackplot(
        somministrazioni.keys(),
        prima_dose.values(),
        seconda_dose.values(),
        "Vaccinazioni giornaliere",
        ["Prima dose", "Seconda dose"],
        "/graphs/vaccini/vaccinazioni_giornaliere_dosi.jpg",
        yticks=range(25000, 250000, 25000)
    )
    print("Grafico completato")

    print("Grafico fasce popolazione...")
    y_values_prima_dose  = []
    y_values_seconda_dose = []
    for index, row in data["anagrafica_vaccini_summary"].iterrows():
        perc_prima_dose = (row["prima_dose"]-row["seconda_dose"])/FASCE_POPOLAZIONE[row["fascia_anagrafica"]]["nazionale"]
        perc_seconda_dose = row["seconda_dose"]/FASCE_POPOLAZIONE[row["fascia_anagrafica"]]["nazionale"]
        y_values_prima_dose.append(perc_prima_dose*100)
        y_values_seconda_dose.append(perc_seconda_dose*100)
    
    istogramma(
        data["anagrafica_vaccini_summary"]["fascia_anagrafica"],
        y_values_prima_dose,
        "Somministrazione vaccini per fascia d'età",
        "/graphs/vaccini/somministrazione_fascia_eta.jpg",
        grid=None,
        bottom=y_values_seconda_dose,
        label1="Prima dose",
        label2="Seconda dose"
    )
    print("Grafico completato")

    print("Grafico somministrazione categorie...")
    x_values = ["categoria_altro", "categoria_operatori_sanitari_sociosanitari", "categoria_personale_non_sanitario", "categoria_ospiti_rsa", "categoria_over80", "categoria_forze_armate", "categoria_personale_scolastico"]
    istogramma(
        x_values,
        [data["anagrafica_vaccini_summary"][x].sum() for x in x_values],
        "Somministrazione vaccini per categoria",
        "/graphs/vaccini/somministrazione_categorie.jpg",
        grid=None,
        ylabel="in milioni di dosi",
        xticklabels=["Altro", "OSS", "Personale \nnon sanitario", "RSA", "Over 80", "FA", "Personale\nscolastico"]
    )
    print("Grafico completato")

    print("Grafico consegne vaccino...")
    consegne = data["consegne_vaccini"].groupby("data_consegna")["numero_dosi"].sum().to_dict()
    grafico_base(
        consegne.keys(),
        consegne.values(),
        "Dosi di vaccino consegnate",
        "/graphs/vaccini/consegne_vaccini.jpg",
        media_mobile=create_media_mobile(consegne.values()),
        legend=["Consegne vaccini", "Media mobile settimanale"],
        marker="."
    )
    print("Grafico completato")

    print("Grafico consegne totali vaccini")
    fornitori = data["consegne_vaccini"].groupby("fornitore")["numero_dosi"].sum().to_dict()
    istogramma(
        fornitori.keys(),
        fornitori.values(),
        "Consegne totali vaccini per fornitore",
        "/graphs/vaccini/consegne_totali_vaccini.jpg",
    )
    print("Grafico completato")

def vaccini_regioni():

    for regione in data["somministrazioni_vaccini_summary"]["regioni"].keys():
        print(f"Regione {regione}")
        denominazione_regione = data["regioni"][regione]["denominazione_regione"].iloc[0]

        print("Grafico popolazione vaccinata seconda dose...")
        vaccinati_seconda_dose = data["somministrazioni_vaccini_summary"]["regioni"][regione]["seconda_dose"].sum()
        popolazione_totale = FASCE_POPOLAZIONE["totale"][denominazione_regione]
        torta(
            [
                popolazione_totale,
                vaccinati_seconda_dose
            ],
            [
                f"Totale popolazione\n ({popolazione_totale})",
                f"Persone vaccinate\n ({vaccinati_seconda_dose}, {round((vaccinati_seconda_dose/popolazione_totale)*100, 2)}%)"
            ],
            f"Persone che hanno completato il ciclo di vaccinazione\nsul totale della popolazione in {denominazione_regione}",
            f"/graphs/vaccini/percentuale_vaccinati_{denominazione_regione}.jpg"
        )

        print("Grafico popolazione vaccinata prima dose...")
        vaccinati_prima_dose = data["somministrazioni_vaccini_summary"]["regioni"][regione]["prima_dose"].sum()
        torta(
            [
                popolazione_totale,
                vaccinati_prima_dose
            ],
            [
                f"Totale popolazione\n ({popolazione_totale})",
                f"Persone vaccinate\n ({vaccinati_prima_dose}, {round((vaccinati_prima_dose/popolazione_totale)*100, 2)}%)"
            ],
            f"Persone che hanno ricevuto almeno una dose\nsul totale della popolazione in {denominazione_regione}",
            f"/graphs/vaccini/percentuale_vaccinati_prima_dose_{denominazione_regione}.jpg"
        )

        print("Grafico vaccinazioni giornaliere...")
        somministrazioni = data["somministrazioni_vaccini_summary"]["regioni"][regione].groupby("data_somministrazione")["totale"].sum().to_dict()
        grafico_base(
            somministrazioni.keys(),
            somministrazioni.values(),
            f"Vaccinazioni giornaliere in {denominazione_regione}",
            f"/graphs/vaccini/vaccinazioni_giornaliere_{denominazione_regione}.jpg",
            media_mobile=create_media_mobile(somministrazioni.values()),
            legend=["Vaccinazioni giornaliere", "Media mobile settimanale"],
            marker="."
        )
        print("Grafico completato")    

        print("Grafico vaccinazione giornaliere, prima e seconda dose...")
        prima_dose = data["somministrazioni_vaccini_summary"]["regioni"][regione].groupby("data_somministrazione")["prima_dose"].sum().to_dict()
        seconda_dose = data["somministrazioni_vaccini_summary"]["regioni"][regione].groupby("data_somministrazione")["seconda_dose"].sum().to_dict()
        stackplot(
            somministrazioni.keys(),
            prima_dose.values(),
            seconda_dose.values(),
            f"Vaccinazioni giornaliere in {denominazione_regione}",
            ["Prima dose", "Seconda dose"],
            f"/graphs/vaccini/vaccinazioni_giornaliere_dosi_{denominazione_regione}.jpg"
        )
        print("Grafico completato")

        print("Grafico fasce popolazione...")
        dataframe = data["somministrazioni_vaccini"]["regioni"][regione]
        y_values_prima_dose  = []
        y_values_seconda_dose = []
        for fascia in FASCE_POPOLAZIONE:
            if fascia == "totale":
                continue
            prima_dose = dataframe[dataframe["fascia_anagrafica"] == fascia]["prima_dose"].sum()
            seconda_dose = dataframe[dataframe["fascia_anagrafica"] == fascia]["seconda_dose"].sum()
            perc_prima_dose = (prima_dose-seconda_dose)/FASCE_POPOLAZIONE[fascia][denominazione_regione]
            perc_seconda_dose = (seconda_dose/FASCE_POPOLAZIONE[fascia][denominazione_regione])
            y_values_prima_dose.append(perc_prima_dose*100)
            y_values_seconda_dose.append(perc_seconda_dose*100)

        istogramma(
            data["anagrafica_vaccini_summary"]["fascia_anagrafica"],
            y_values_prima_dose,
            f"Somministrazione vacini per fascia d'età in {denominazione_regione}",
            f"/graphs/vaccini/somministrazione_fascia_eta_{denominazione_regione}.jpg",
            grid=None,
            bottom=y_values_seconda_dose,
            label1="Prima dose",
            label2="Seconda dose"
        )
        print("Grafico completato")

        print("Grafico somministrazione categorie...")
        x_values = ["categoria_altro", "categoria_operatori_sanitari_sociosanitari", "categoria_personale_non_sanitario", "categoria_ospiti_rsa", "categoria_over80", "categoria_forze_armate", "categoria_personale_scolastico"]
        istogramma(
            x_values,
            [data["somministrazioni_vaccini"]["regioni"][regione][x].sum() for x in x_values],
            f"Somministrazione vaccini per categoria in {denominazione_regione}",
            f"/graphs/vaccini/somministrazione_categorie_{denominazione_regione}.jpg",
            grid=None,
            ylabel="in milioni di dosi",
            xticklabels=["Altro", "OSS", "Personale \nnon sanitario", "RSA", "Over 80", "FA", "Personale\nscolastico"]
        )
        print("Grafico completato")

        print("Grafico consegne vaccino...")
        if regione == 21:
            consegne_regione = data["consegne_vaccini"][data["consegne_vaccini"]["nome_area"] == "Provincia Autonoma Trento"]
        elif regione == 22:
            consegne_regione = data["consegne_vaccini"][data["consegne_vaccini"]["nome_area"] == "Provincia Autonoma Bolzano / Bozen"]
        else:
            consegne_regione = data["consegne_vaccini"][data["consegne_vaccini"]["codice_regione_ISTAT"] == regione]

        consegne = consegne_regione.groupby("data_consegna")["numero_dosi"].sum().to_dict()
        grafico_base(
            consegne.keys(),
            consegne.values(),
            f"Dosi di vaccino consegnate in {denominazione_regione}",
            f"/graphs/vaccini/consegne_vaccini_{denominazione_regione}.jpg",
            media_mobile=create_media_mobile(consegne.values()),
            legend=["Consegne vaccini", "Media mobile settimanale"],
            marker="."
        )
        print("Grafico completato")

        print("Grafico consegne totali vaccini")
        fornitori = consegne_regione.groupby("fornitore")["numero_dosi"].sum().to_dict()
        istogramma(
            fornitori.keys(),
            fornitori.values(),
            f"Consegne totali vaccini per fornitore in {denominazione_regione}",
            f"/graphs/vaccini/consegne_totali_vaccini_{denominazione_regione}.jpg",
        )
        print("Grafico completato")


if __name__ == "__main__":
    # Inizializza i dati
    print("--- Inizializzazione dataset...")
    for url_name in URLS.keys():
        download_csv(url_name, URLS[url_name])
    CWD = os.path.abspath(os.path.dirname(__file__))
    os.makedirs(f"{CWD}/graphs", exist_ok=True)
    
    print("Dati caricati con successo.\n-----------------------------")
    
    print("Inizio generazione grafici nazionali...")
    sum_nazionale = nazionale()
    
    print("-----------------------------\nInizio generazione grafici regionali...")
    sum_regioni = regioni()

    print("-----------------------------\nInizio generazione grafici vaccini nazionali...")
    vaccini_nazionale()

    print("-----------------------------\nInizio generazione grafici vaccini regioanli...")
    vaccini_regioni()

    with open(f"{CWD}/summary.txt", 'w') as f:
        f.write(sum_nazionale)
        f.write(sum_regioni)

    print("-----------------------------\nScript completato con successo. I risultati si trovano nella cartella graphs.")
