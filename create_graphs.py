import matplotlib.pyplot as plt
import pandas as pd
import os
import json
import urllib.request as request
import numpy as np
from time import time
from datetime import datetime, timedelta

# COSTANTI
############################################################################################

# URL da cui scaricare i dati necessari
URLS = {
    "nazionale": "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv",
    "regioni": "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",
    "vaccini_summary": "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.csv",
    "anagrafica_vaccini_summary": "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/anagrafica-vaccini-summary-latest.csv",
    "somministrazioni_vaccini_summary": "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-summary-latest.csv",
    "consegne_vaccini": "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/consegne-vaccini-latest.csv",
    "somministrazioni_vaccini": "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv",
    "monitoraggi_iss": "https://raw.githubusercontent.com/sphoneix22/monitoraggi-ISS/main/dati/monitoraggio-nazionale.csv",
    "monitoraggi_iss_regioni": "https://raw.githubusercontent.com/sphoneix22/monitoraggi-ISS/main/dati/monitoraggio-regioni.csv"
}

# Colonne che necessitano la conversione in formato datetime (tutti i csv)
DATETIME_COLUMNS = ["data", "data_somministrazione",
                    "data_consegna", "inizio_range", "fine_range", "data_report"]

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

REGIONI = [
        "Abruzzo", 
        "Basilicata",
        "Calabria",
        "Campania",
        "Emilia-Romagna",
        "Friuli Venezia Giulia",
        "Lazio",
        "Liguria",
        "Lombardia",
        "Marche",
        "Molise",
        "P.A. Bolzano",
        "P.A. Trento", 
        "Piemonte",
        "Puglia",
        "Sardegna",
        "Sicilia",
        "Toscana",
        "Umbria",
        "Valle d'Aosta",
        "Veneto"
]

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

# ultimo aggiornamento 23/4/21
CONSEGNE_VACCINI = {
    # comprende anche le dosi iniziali di PF/BT
    "Q1": {
        "Janssen": 0,
        "Moderna": 1330000,
        "Pfizer/BioNTech": 8749260,
        "AstraZeneca": 4116000
    },
    "Q2": {
        "Jannsen": 7307292,
        "Moderna": 4650000,
        "Pfizer/BioNTech": 32714370,
        "AstraZeneca": 10042500
    }
}

# Contiene tutti i dati elaborati
data = {}


############################################################################################

# UTILS
############################################################################################
def download_csv(name, url):
    dataframe = pd.read_csv(url)

    for col in DATETIME_COLUMNS:
        if col in dataframe:
            dataframe[col] = pd.to_datetime(
                dataframe[col], format="%Y-%m-%dT%H:%M:%S")

    # Codici ISTAT delle regioni
    # 01 PIEMONTE 02 VALLE D’AOSTA 03 LOMBARDIA 04 TRENTINO A. A. 05 VENETO 06 FRIULI V. G 07 LIGURIA 08 EMILIA ROMAGNA 09 TOSCANA
    # 10 UMBRIA 11 MARCHE 12 LAZIO 13 ABRUZZI 14 MOLISE 15 CAMPANIA 16 PUGLIE 17 BASILICATA 18 CALABRIA 19 SICILIA 20 SARDEGNA
    # 21 BOLZANO 22 TRENTO
    if name == "regioni":
        data["regioni"] = {}
        for codice_regione in [x for x in range(1, 23) if x != 4]:
            data_regione = dataframe[dataframe["codice_regione"]
                                     == codice_regione]
            data["regioni"][codice_regione] = data_regione
    elif name == "somministrazioni_vaccini_summary":
        data["somministrazioni_vaccini_summary"] = {"nazionale": dataframe}
        data["somministrazioni_vaccini_summary"]["regioni"] = {}
        for codice_regione in [x for x in range(1, 22) if x != 4]:
            data_regione = dataframe[dataframe["codice_regione_ISTAT"]
                                     == codice_regione]
            data["somministrazioni_vaccini_summary"]["regioni"][codice_regione] = data_regione
        data["somministrazioni_vaccini_summary"]["regioni"][21] = dataframe[
            dataframe["nome_area"] == "Provincia Autonoma Trento"]
        data["somministrazioni_vaccini_summary"]["regioni"][22] = dataframe[
            dataframe["nome_area"] == "Provincia Autonoma Bolzano / Bozen"]
    elif name == "somministrazioni_vaccini":
        data["somministrazioni_vaccini"] = {"nazionale": dataframe}
        data["somministrazioni_vaccini"]["regioni"] = {}
        # In questo dataset le P.A. hanno lo stesso codice istat (4) ma differente denominazione
        for codice_regione in [x for x in range(1, 22) if x != 4]:
            data_regione = dataframe[dataframe["codice_regione_ISTAT"]
                                     == codice_regione]
            data["somministrazioni_vaccini"]["regioni"][codice_regione] = data_regione
        data["somministrazioni_vaccini"]["regioni"][21] = dataframe[
            dataframe["nome_area"] == "Provincia Autonoma Trento"]
        data["somministrazioni_vaccini"]["regioni"][22] = dataframe[
            dataframe["nome_area"] == "Provincia Autonoma Bolzano / Bozen"]
    elif name == "monitoraggi_iss_regioni":
        data["monitoraggi_iss_regioni"] = {}
        for regione in REGIONI:
            data_regione = dataframe[dataframe["regione"] == regione]
            data["monitoraggi_iss_regioni"][regione] = data_regione
    else:
        data[name] = dataframe


def create_media_mobile(data):
    count = []
    result = []

    for el in data:
        count.append(el)
        result.append(sum(count) / len(count))
        if len(count) == 7:
            count.pop(0)
    return result


def create_delta(data):
    latest = 0
    delta = []

    for row in data:
        delta.append(row - latest)
        latest = row

    return delta


def create_incidenza(data, regione):
    count = []
    result = []
    for row in data:
        count.append(row)
        result.append(
            (sum(count) / FASCE_POPOLAZIONE["totale"][regione]) * 100000)
        if len(count) == 7:
            count.pop(0)
    return result


def shape_adjust(data):
    start = min([list(x.keys())[0] for x in data])
    end = max([list(x.keys())[-1] for x in data])
    current = start

    while current <= end:
        for el in data:
            if current not in el.keys():
                el[current] = 0
        current = current + timedelta(days=1)
    return data


def order(data):
    start = min([list(x.keys())[0] for x in data])
    end = max([list(x.keys())[-1] for x in data])

    new_data = [{} for x in data]
    current = start
    while current <= end:
        for x in data:
            new_data[data.index(x)][current] = x[current]
        current += timedelta(days=1)
    return new_data


# GRAFICI
############################################################################################


def plot(x, y, title, output, xlabel=None, ylabel=None, media_mobile=None, legend=None, color=None, grid="y",
         hline=None, vline=None, marker=None, footer=None, alpha=0.8):
    fig, ax = plt.subplots()
    line, = ax.plot(x, y, linestyle="solid", marker=marker, alpha=alpha)
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
    plt.figtext(0.99, 0.01, footer, horizontalalignment='right')

    fig.savefig(CWD + output, dpi=200)
    plt.close('all')


def stackplot(x, y1, y2, title, label, output, soglia=None, yticks=None, footer=None, y3=None):
    fig, ax = plt.subplots()

    if y3:
        ax.stackplot(x, y1, y2, y3, labels=label)
    else:
        ax.stackplot(x, y1, y2, labels=label)

    if soglia:
        ax.axhline(soglia, color="red")
    if yticks:
        ax.set_yticks(yticks)
    ax.set_title(title)
    ax.legend(label, loc="upper left", prop={"size": 7})
    ax.grid(axis="y")
    fig.autofmt_xdate()
    plt.figtext(0.99, 0.01, footer, horizontalalignment='right')
    fig.savefig(CWD + output, dpi=200)
    plt.close('all')


def deltaplot(x, y, title, output, footer=None):
    fig, ax = plt.subplots()
    color = ["orange" if x >= 0 else "red" for x in y]
    plt.vlines(x=x, ymin=0, ymax=y, color=color, alpha=0.7)
    ax.set_title(title)
    fig.autofmt_xdate()
    ax.grid(axis="y")
    plt.figtext(0.99, 0.01, footer, horizontalalignment='right')

    fig.savefig(CWD + output, dpi=200)
    plt.close('all')


def barplot(x, y, title, output, horizontal=False, xticks=None, yticks=None, grid="y", bottom=None, ylabel=None,
            label1=None, label2=None, xticklabels=None, footer=None):
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
        plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        ax.set_xticklabels(xticklabels)

    plt.figtext(0.99, 0.01, footer, horizontalalignment='right')
    plt.tight_layout()
    fig.savefig(CWD + output, dpi=200)

    plt.close('all')


def pieplot(slices, labels, title, output, footer=None):
    fig, ax = plt.subplots()
    ax.pie(slices, labels=labels)
    plt.title(title)
    plt.figtext(0.99, 0.01, footer, horizontalalignment='right')

    fig.savefig(CWD + output, dpi=200)
    plt.close('all')


def grafico_vaccinati_fascia_anagrafica(x, prima_dose, seconda_dose, monodose, title, footer, output):
    fig, ax = plt.subplots()

    ax.bar(x, prima_dose, label="Prima dose")
    ax.bar(x, seconda_dose, bottom=prima_dose, label="Seconda dose")
    ax.bar(x, monodose, bottom=np.array(prima_dose)+np.array(seconda_dose), label="Monodose")

    ax.grid()

    plt.title(title)
    plt.figtext(0.99, 0.01, footer, horizontalalignment='right')
    plt.legend()
    
    fig.savefig(CWD + output, dpi=200)

    plt.close('all')


def grafico_vaccini_fascia_eta(data, media_mobile, title, footer, output):
    fig, ax = plt.subplots()

    start = min([min(list(x.keys())) for x in data])
    end = max([max(list(x.keys())) for x in data])
    ordered_data = [{}, {}, {}, {}, {}, {}, {}, {}, {}]
    current = start
    while current <= end:
        for index in range(len(data)):
            ordered_data[index][current] = data[index][current]
        current = current + timedelta(days=1)

    xvalues = np.array(list(ordered_data[4].keys()))
    arrays = [np.array(list(x.values())) for x in ordered_data]
    ax.bar(xvalues, arrays[0], label="16-19")
    ax.bar(xvalues, arrays[1], label="20-29", bottom=arrays[0])
    ax.bar(xvalues, arrays[2], label="30-39", bottom=arrays[0]+arrays[1])
    ax.bar(xvalues, arrays[3], label="40-49",
           bottom=arrays[0]+arrays[1]+arrays[2])
    ax.bar(xvalues, arrays[4], label="50-59",
           bottom=arrays[0]+arrays[1]+arrays[2]+arrays[3])
    ax.bar(xvalues, arrays[5], label="60-69",
           bottom=arrays[0]+arrays[1]+arrays[2]+arrays[3]+arrays[4])
    ax.bar(xvalues, arrays[6], label="70-79", bottom=arrays[0] +
           arrays[1]+arrays[2]+arrays[3]+arrays[4]+arrays[5])
    ax.bar(xvalues, arrays[7], label="80-89", bottom=arrays[0] +
           arrays[1]+arrays[2]+arrays[3]+arrays[4]+arrays[5]+arrays[6])
    ax.bar(xvalues, arrays[8], label="90+", bottom=arrays[0]+arrays[1] +
           arrays[2]+arrays[3]+arrays[4]+arrays[5]+arrays[6]+arrays[7])
    ax.grid("y")
    ax.plot(media_mobile[0], media_mobile[1], color="black",
            linewidth=1, label="Media mobile settimanale")
    plt.title(title)
    plt.legend()
    plt.figtext(0.99, 0.01, footer, horizontalalignment='right')
    fig.autofmt_xdate()
    plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)

    fig.savefig(CWD + output, dpi=200)

    plt.close("all")


def grafico_vaccini_fornitore(pfizer, moderna, astrazeneca, janssen, media_mobile, title, footer, output):
    fig, ax = plt.subplots()

    x_pfizer = list(pfizer.keys())
    x_pfizer.sort()

    y_pfizer = []
    y_moderna = []
    y_astrazeneca = []
    y_janssen = []
    for x_value in x_pfizer:
        y_pfizer.append(pfizer[x_value])
        y_moderna.append(moderna[x_value])
        y_astrazeneca.append(astrazeneca[x_value])
        y_janssen.append(janssen[x_value])

    moderna_array = np.array(y_moderna)
    pfizer_array = np.array(y_pfizer)
    astrazeneca_array = np.array(y_astrazeneca)

    ax.bar(x_pfizer, y_pfizer, label="Pfizer/BioNTech")
    ax.bar(x_pfizer, y_moderna,
           bottom=y_pfizer, label="Moderna")
    ax.bar(x_pfizer, y_astrazeneca,
           bottom=moderna_array+pfizer_array, label="AstraZeneca")
    ax.bar(x_pfizer, y_janssen, bottom=astrazeneca_array +
           moderna_array+pfizer_array, label="Janssen")
    ax.grid(axis="y")
    ax.plot(media_mobile[0], media_mobile[1], color="black",
            linewidth=1, label="Media mobile settimanale")
    plt.title(title)
    plt.legend()
    plt.figtext(0.99, 0.01, footer, horizontalalignment='right')
    fig.autofmt_xdate()
    plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)

    fig.savefig(CWD + output, dpi=200)

    plt.close("all")


def grafico_consegne_totale(consegne, consegne_previste, footer, output):
    fig, ax = plt.subplots()

    x_axis = np.arange(len(consegne.keys()))

    ax.ticklabel_format(useOffset=False, style='plain')
    ax.bar(x_axis - 0.2, consegne.values(), 0.35, label="Consegne avvenute")

    plt.title("Consegne totali vaccini (al 23/4/2021)")

    ax.grid()

    ax.bar(x_axis + 0.2, consegne_previste["Q2"].values(), 0.35, label="Consegne previste Q2", bottom=np.array(list(
        consegne_previste["Q1"].values())))
    ax.bar(x_axis + 0.2, consegne_previste["Q1"].values(), 0.35, label="Consegne previste Q1")

    plt.xticks(x_axis, ["Janssen", "Moderna",
               "Pfizer/BioNTech", "AstraZeneca"])
    plt.legend()

    plt.figtext(0.99, 0.01, footer, horizontalalignment='right')
    plt.tight_layout()
    fig.savefig(CWD + output, dpi=200)

    plt.close('all')


def grafico_rt(x_rt, x_contagi, rt, contagi, title, footer, output):
    fig, ax = plt.subplots()

    ax.set_ylabel("Positivi giornalieri")
    ax2 = ax.twinx()
    ax2.set_ylabel("Valore R")
    
    ax.plot(x_contagi, contagi, alpha=0.4, linestyle="dashed")
    ax2.plot(x_rt, rt, marker=".")
    ax2.axhline(y=1, color="red", linestyle="dashed")
    fig.autofmt_xdate()

    ax.legend(["Nuovi positivi giornalieri"])
    ax2.legend(["Andamento Rt"])
    plt.title(title)
    plt.figtext(0.99, 0.01, footer, horizontalalignment='right')
    plt.grid()

    fig.savefig(CWD + output, dpi=200)

    plt.close('all')


def grafico_vaccini_cumulativo(data, title, footer, output):
    fig, ax = plt.subplots()

    ax.plot(data[0].keys(), create_media_mobile(data[0].values()), label="16-19")
    ax.plot(data[1].keys(), create_media_mobile(data[1].values()), label="20-29")
    ax.plot(data[2].keys(), create_media_mobile(data[2].values()), label="30-39")
    ax.plot(data[3].keys(), create_media_mobile(data[3].values()), label="40-49")
    ax.plot(data[4].keys(), create_media_mobile(data[4].values()), label="50-59")
    ax.plot(data[5].keys(), create_media_mobile(data[5].values()), label="60-69")
    ax.plot(data[6].keys(), create_media_mobile(data[6].values()), label="70-79")
    ax.plot(data[7].keys(), create_media_mobile(data[7].values()), label="80-89")
    ax.plot(data[8].keys(), create_media_mobile(data[8].values()), label="90+")

    plt.title(title)
    plt.figtext(0.99, 0.01, footer, horizontalalignment='right')
    plt.legend()

    fig.autofmt_xdate()
    fig.savefig(CWD + output, dpi=200)

    plt.close('all')


############################################################################################


def epidemia():
    os.makedirs(f"{CWD}/graphs/epidemia", exist_ok=True)
    last_update = data["nazionale"]["data"].iat[-1]
    summary = f"DATI NAZIONALI {last_update}\n\n"
    # Grafico nuovi positivi
    print("Grafico nuovi positivi...")
    plot(
        data["nazionale"]["data"],
        data["nazionale"]["nuovi_positivi"],
        "Andamento contagi giornalieri",
        "/graphs/epidemia/nuovi_positivi.jpg",
        media_mobile=create_media_mobile(data["nazionale"]["nuovi_positivi"]),
        legend=["Contagi giornalieri", "Media mobile settimanale"],
        footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
    )
    today = data["nazionale"]["nuovi_positivi"].iat[-1]
    last_week = data["nazionale"]["nuovi_positivi"].iat[-8]
    delta = round((today-last_week)/last_week*100, 0)
    summary += "Nuovi positivi: {} ({:+}%)\n".format(
        today, delta)

    # Stackplot ospedalizzati
    print("Grafico ospedalizzati...")
    stackplot(
        data["nazionale"]["data"],
        data["nazionale"]["terapia_intensiva"],
        data["nazionale"]["ricoverati_con_sintomi"],
        "Andamento ospedalizzati",
        ["Soglia critica TI", "Terapie intensive", "Ricoverati con sintomi"],
        "/graphs/epidemia/andamento_ospedalizzati.jpg",
        soglia=(TOTALE_TERAPIA_INTENSIVA["nazionale"] / 100) * 30,
        footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
    )
    summary += "Ospedalizzati ordinari: {}\nTerapie intensive: {}\n".format(
        data["nazionale"]["ricoverati_con_sintomi"].iat[-1], data["nazionale"]["terapia_intensiva"].iat[-1])

    # Grafico ingressi in terapia intensiva
    print("Grafico ingressi TI...")
    plot(
        data["nazionale"]["data"],
        data["nazionale"]["ingressi_terapia_intensiva"],
        "Ingressi giornalieri in terapia intensiva",
        "/graphs/epidemia/ingressi_ti.jpg",
        media_mobile=create_media_mobile(
            data["nazionale"]["ingressi_terapia_intensiva"]),
        legend=["Ingressi TI", "Media mobile settimanale"],
        footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
    )
    today = data["nazionale"]["ingressi_terapia_intensiva"].iat[-1]
    last_week = data["nazionale"]["ingressi_terapia_intensiva"].iat[-8]
    if last_week == 0:
        delta = 0
    else:
        delta = round((today-last_week)/last_week*100, 0)
    summary += "Ingressi TI: {} ({:+}%)\n".format(
        today, delta)

    # Grafico variazione totale positivi
    print("Grafico variazione totale positivi...")
    deltaplot(
        data["nazionale"]["data"],
        data["nazionale"]["variazione_totale_positivi"],
        "Variazione giornaliera totale positivi",
        "/graphs/epidemia/variazione_totale_positivi.jpg",
        footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
    )
    summary += "Variazione totale totale positivi: {}\n".format(
        data["nazionale"]["variazione_totale_positivi"].iat[-1])

    # Grafico variazione totale ospedalizzati
    print("Grafico variazione totale ospedalizzati...")
    delta = create_delta(data["nazionale"]["totale_ospedalizzati"])
    deltaplot(
        data["nazionale"]["data"],
        delta,
        "Variazione totale ospedalizzati",
        "/graphs/epidemia/variazione_totale_ospedalizzati.jpg",
        footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
    )
    summary += "Variazione totale ospedalizzati: {}\n".format(delta[-1])

    # Grafico variazione occupazione TI
    print("Grafico variazione TI")
    delta = create_delta(data["nazionale"]["terapia_intensiva"])
    deltaplot(
        data["nazionale"]["data"],
        delta,
        "Variazione occupazione TI",
        "/graphs/epidemia/variazione_ti.jpg",
        footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
    )
    summary += "Variazione TI: {}\n".format(delta[-1])

    # Grafico variazione totale ospedalizzati
    print("Grafico variazione ricoverati con sintomi...")
    delta = create_delta(data["nazionale"]["ricoverati_con_sintomi"])
    deltaplot(
        data["nazionale"]["data"],
        delta,
        "Variazione ospedalizzati ordinari",
        "/graphs/epidemia/variazione_ospedalizzati_ordinari.jpg",
        footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
    )
    summary += "Variazione ricoverati con sintomi: {}\n".format(delta[-1])

    # Grafico deceduti
    print("Grafico deceduti...")
    plot(
        data["nazionale"]["data"],
        data["nazionale"]["deceduti"],
        "Andamento deceduti",
        "/graphs/epidemia/deceduti.jpg",
        color="black",
        footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
    )
    summary += "Deceduti totali: {}\n".format(
        data["nazionale"]["deceduti"].iat[-1])

    # Grafico deceduti giornalieri
    print("Grafico deceduti giornalieri...")
    delta = create_delta(data["nazionale"]["deceduti"])
    plot(
        data["nazionale"]["data"],
        delta,
        "Deceduti giornalieri",
        "/graphs/epidemia/deceduti_giornalieri.jpg",
        media_mobile=create_media_mobile(
            create_delta(data["nazionale"]["deceduti"])),
        legend=["Deceduti giornalieri", "Media mobile settimanale"],
        color="black",
        footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
    )
    today = delta[-1]
    last_week = delta[-8]
    delta_perc = round((today-last_week)/last_week*100, 0)
    summary += "Deceduti giornalieri: {} ({:+}%)\n".format(
        delta[-1], delta_perc)

    print("Grafico incidenza...")
    incidenza = create_incidenza(
        data["nazionale"]["nuovi_positivi"], "nazionale")
    plot(
        data["nazionale"]["data"],
        incidenza,
        "Incidenza di nuovi positivi ogni 100000 abitanti\nnell'arco di 7 giorni",
        "/graphs/epidemia/incidenza_contagio.jpg",
        hline=250,
        footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
    )
    today = incidenza[-1]
    last_week = incidenza[-8]
    delta = round((today-last_week)/last_week*100, 0)
    summary += f"Incidenza: {incidenza[-1]} ({delta:+}%)\n\n"

    print("Grafico rt")
    grafico_rt(
        data["monitoraggi_iss"]["fine_range"],
        data["nazionale"]["data"],
        data["monitoraggi_iss"]["rt_puntuale"],
        data["nazionale"]["nuovi_positivi"],
        "Andamento Rt nazionale",
        f"Fonte dati: ISS | Ultimo aggiornamento: {last_update}",
        "/graphs/epidemia/rt.jpg",
    )

    summary += "DATI REGIONI\n\n"
    for regione in data["regioni"].keys():
        denominazione_regione = data["regioni"][regione]["denominazione_regione"].iloc[0]
        summary += f"{denominazione_regione}\n"
        print(f"Regione {regione}...")
        print("Grafico nuovi positivi...")
        plot(
            data["regioni"][regione]["data"],
            data["regioni"][regione]["nuovi_positivi"],
            f"Andamento contagi giornalieri {denominazione_regione}",
            f"/graphs/epidemia/nuovi_positivi_{denominazione_regione}.jpg",
            media_mobile=create_media_mobile(
                data["regioni"][regione]["nuovi_positivi"]),
            legend=["Contagi giornalieri", "Media mobile settimanale"],
            footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
        )
        today = data["regioni"][regione]["nuovi_positivi"].iat[-1]
        last_week = data["regioni"][regione]["nuovi_positivi"].iat[-8]
        delta = round((today-last_week)/last_week*100, 0)
        summary += "Nuovi positivi: {} ({:+}%)\n".format(
            today, delta)

        # Stackplot ospedalizzati
        print("Grafico ospedalizzati...")
        stackplot(
            data["regioni"][regione]["data"],
            data["regioni"][regione]["terapia_intensiva"],
            data["regioni"][regione]["ricoverati_con_sintomi"],
            f"Andamento ospedalizzati {denominazione_regione}",
            ["Soglia critica TI", "Terapie intensive", "Ricoverati con sintomi"],
            f"/graphs/epidemia/andamento_ospedalizzati_{denominazione_regione}.jpg",
            soglia=(
                TOTALE_TERAPIA_INTENSIVA[denominazione_regione] / 100) * 30,
            footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
        )
        summary += "TI: {}\nRicoverati con sintomi: {}\n".format(data["regioni"][regione]["terapia_intensiva"].iat[-1],
                                                                 data["regioni"][regione]["ricoverati_con_sintomi"].iat[
                                                                     -1])

        # Grafico ingressi in terapia intensiva
        print("Grafico ingressi TI...")
        plot(
            data["regioni"][regione]["data"],
            data["regioni"][regione]["ingressi_terapia_intensiva"],
            f"Ingressi giornalieri in terapia intensiva {denominazione_regione}",
            f"/graphs/epidemia/ingressi_ti_{denominazione_regione}.jpg",
            media_mobile=create_media_mobile(
                data["regioni"][regione]["ingressi_terapia_intensiva"]),
            legend=["Ingressi TI", "Media mobile settimanale"],
            footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
        )
        today = data["regioni"][regione]["ingressi_terapia_intensiva"].iat[-1]
        last_week = data["regioni"][regione]["ingressi_terapia_intensiva"].iat[-8]
        if last_week == 0:
            delta = 0
        else:
            delta = round((today-last_week)/last_week*100, 0)
        summary += "Ingressi TI: {} ({:+}%)\n".format(
            today, delta)

        # Grafico variazione totale positivi
        print("Grafico variazione totale positivi...")
        deltaplot(
            data["regioni"][regione]["data"],
            data["regioni"][regione]["variazione_totale_positivi"],
            f"Variazione giornaliera totale positivi {denominazione_regione}",
            f"/graphs/epidemia/variazione_totale_positivi_{denominazione_regione}.jpg",
            footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
        )
        summary += "Variazione totale positivi: {}\n".format(
            data["regioni"][regione]["variazione_totale_positivi"].iat[-1])

        # Grafico variazione totale ospedalizzati
        print("Grafico variazione totale ospedalizzati...")
        deltaplot(
            data["regioni"][regione]["data"],
            create_delta(data["regioni"][regione]["totale_ospedalizzati"]),
            f"Variazione totale ospedalizzati {denominazione_regione}",
            f"/graphs/epidemia/variazione_totale_ospedalizzati_{denominazione_regione}.jpg",
            footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
        )
        summary += "Variazione totale ospedalizzati: {}\n".format(
            create_delta(data["regioni"][regione]["totale_ospedalizzati"])[-1])

        # Grafico variazione occupazione TI
        print("Grafico variazione TI")
        deltaplot(
            data["regioni"][regione]["data"],
            create_delta(data["regioni"][regione]["terapia_intensiva"]),
            f"Variazione occupazione TI {denominazione_regione}",
            f"/graphs/epidemia/variazione_ti_{denominazione_regione}.jpg",
            footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
        )
        summary += "Variazione TI: {}\n".format(create_delta(
            data["regioni"][regione]["terapia_intensiva"])[-1])

        # Grafico variazione totale ospedalizzati
        print("Grafico variazione ricoverati con sintomi...")
        deltaplot(
            data["regioni"][regione]["data"],
            create_delta(data["regioni"][regione]["ricoverati_con_sintomi"]),
            f"Variazione ospedalizzati ordinari {denominazione_regione}",
            f"/graphs/epidemia/variazione_ospedalizzati_ordinari_{denominazione_regione}.jpg",
            footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
        )
        summary += "Variazione ricoverati con sintomi: {}\n".format(
            create_delta(data["regioni"][regione]["ricoverati_con_sintomi"])[-1])

        # Grafico deceduti
        print("Grafico deceduti...")
        plot(
            data["regioni"][regione]["data"],
            data["regioni"][regione]["deceduti"],
            f"Andamento deceduti {denominazione_regione}",
            f"/graphs/epidemia/deceduti_{denominazione_regione}.jpg",
            color="black",
            footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
        )
        summary += "Deceduti totali: {}\n".format(
            data["regioni"][regione]["deceduti"].iat[-1])

        # Grafico deceduti giornalieri
        print("Grafico deceduti giornalieri...")
        delta = create_delta(data["regioni"][regione]["deceduti"])
        plot(
            data["regioni"][regione]["data"],
            delta,
            f"Deceduti giornalieri {denominazione_regione}",
            f"/graphs/epidemia/deceduti_giornalieri_{denominazione_regione}.jpg",
            media_mobile=create_media_mobile(
                create_delta(data["regioni"][regione]["deceduti"])),
            legend=["Deceduti giornalieri", "Media mobile settimanale"],
            color="black",
            footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
        )
        today = delta[-1]
        last_week = delta[-8]
        if last_week == 0:
            delta_perc = 0
        else:
            delta_perc = round((today-last_week)/last_week*100, 0)
        summary += "Deceduti giornalieri: {} ({:+}%)\n".format(
            today, delta_perc)

        print("Grafico incidenza...")
        incidenza = create_incidenza(
            data["regioni"][regione]["nuovi_positivi"], denominazione_regione)
        plot(
            data["regioni"][regione]["data"],
            incidenza,
            f"Incidenza di nuovi positivi ogni 100000 abitanti\nnell'arco di 7 giorni in {denominazione_regione}",
            f"/graphs/epidemia/incidenza_contagio_{denominazione_regione}.jpg",
            hline=250,
            footer=f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}"
        )
        today = incidenza[-1]
        last_week = incidenza[-8]
        delta_perc = round((today-last_week)/last_week*100, 0)
        summary += f"Incidenza: {incidenza[-1]} ({delta_perc:+}%)\n\n"

        print("Grafico rt")
        grafico_rt(
            data["monitoraggi_iss_regioni"][denominazione_regione]["fine_range"],
            data["regioni"][regione]["data"],
            data["monitoraggi_iss_regioni"][denominazione_regione]["rt_puntuale"],
            data["regioni"][regione]["nuovi_positivi"],
            f"Andamento Rt - {denominazione_regione}",
            f"Fonte dati: PCM-DPC | Ultimo aggiornamento: {last_update}",
            f"/graphs/epidemia/rt_{denominazione_regione}.jpg",
        )

    return summary


def vaccini():
    os.makedirs(f"{CWD}/graphs/vaccini", exist_ok=True)
    last_update = json.loads(request.urlopen(
        "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/last-update-dataset.json").read())["ultimo_aggiornamento"]
    last_update = pd.to_datetime(last_update).strftime("%d-%m alle %H:%M %Z")

    summary = f"DATI VACCINAZIONE\n\nDATI NAZIONALI\nUltimo aggiornamento:\n{last_update}\n"

    print("Grafico percentuale somministrazione...")
    barplot(
        data["vaccini_summary"]["area"],
        data["vaccini_summary"]["percentuale_somministrazione"],
        "Percentuale dosi somministrate per regioni",
        "/graphs/vaccini/percentuale_somministrazione_regioni.jpg",
        xticks=range(0, 100, 5),
        horizontal=True,
        grid="x",
        footer=f"Fonte dati: Covid19 Opendata Vaccini | Ultimo aggiornamento: {last_update}"
    )

    summary += "Percentuale somministrazione:\n"
    for i in range(0, 21):
        regione = data["vaccini_summary"]["area"][i]
        perc = data["vaccini_summary"]["percentuale_somministrazione"][i]
        summary += f"{regione}: {perc}%\n"

    print("Grafico popolazione vaccinata seconda dose...")
    
    janssen = data["somministrazioni_vaccini"]["nazionale"][data["somministrazioni_vaccini"]
                                                            ["nazionale"]["fornitore"] == "Janssen"]
    monodose = janssen["prima_dose"].sum()    
    vaccinati_seconda_dose = data["anagrafica_vaccini_summary"]["seconda_dose"].sum(
    )
    popolazione_totale = FASCE_POPOLAZIONE["totale"]['nazionale']
    pieplot(
        [
            popolazione_totale,
            vaccinati_seconda_dose+monodose
        ],
        [
            f"Totale popolazione\n ({popolazione_totale})",
            f"Persone vaccinate\n ({vaccinati_seconda_dose}, {round((vaccinati_seconda_dose / popolazione_totale) * 100, 2)}%)"
        ],
        "Persone che hanno completato il ciclo di vaccinazione\nsul totale della popolazione",
        "/graphs/vaccini/percentuale_vaccinati.jpg",
        footer=f"Fonte dati: Covid19 Opendata Vaccini | Ultimo aggiornamento: {last_update}"
    )
    summary += f"\nPercentuale popolazione vaccinata con la seconda dose: {vaccinati_seconda_dose} ({round((vaccinati_seconda_dose / popolazione_totale) * 100, 2)}%)\n"

    print("Grafico popolazione vaccinata prima dose...")
    vaccinati_prima_dose = data["anagrafica_vaccini_summary"]["prima_dose"].sum(
    )
    pieplot(
        [
            popolazione_totale,
            vaccinati_prima_dose
        ],
        [
            f"Totale popolazione\n ({popolazione_totale})",
            f"Persone vaccinate\n ({vaccinati_prima_dose}, {round((vaccinati_prima_dose / popolazione_totale) * 100, 2)}%)"
        ],
        "Persone che hanno ricevuto almeno una dose\nsul totale della popolazione",
        "/graphs/vaccini/percentuale_vaccinati_prima_dose.jpg",
        footer=f"Fonte dati: Covid19 Opendata Vaccini | Ultimo aggiornamento: {last_update}"
    )
    summary += f"\nPercentuale popolazione vaccinata con la prima dose: {vaccinati_prima_dose} ({round((vaccinati_prima_dose / popolazione_totale) * 100, 2)}%)\n"

    print("Grafico vaccinazione giornaliere, prima e seconda dose...")
    somministrazioni = data["somministrazioni_vaccini_summary"]["nazionale"].groupby("data_somministrazione")[
        "totale"].sum().to_dict()
    prima_dose = data["somministrazioni_vaccini_summary"]["nazionale"].groupby("data_somministrazione")[
        "prima_dose"].sum().to_dict()
    seconda_dose = data["somministrazioni_vaccini_summary"]["nazionale"].groupby("data_somministrazione")[
        "seconda_dose"].sum().to_dict()
    monodose = janssen.groupby("data_somministrazione")["prima_dose"].sum().to_dict()
    for day in prima_dose:
        if day in monodose.keys():
            prima_dose[day] -= monodose[day]
    adjusted = shape_adjust([prima_dose, seconda_dose, monodose])

    stackplot(
        somministrazioni.keys(),
        adjusted[0].values(),
        adjusted[1].values(),
        "Vaccinazioni giornaliere",
        ["Prima dose", "Seconda dose", "Monodose"],
        "/graphs/vaccini/vaccinazioni_giornaliere_dosi.jpg",
        footer=f"Fonte dati: Covid19 Opendata Vaccini | Ultimo aggiornamento: {last_update}",
        y3=adjusted[2].values()
    )
    today = list(somministrazioni.values())[-1]
    yesterday = list(somministrazioni.values())[-2]
    yeyesterday = list(somministrazioni.values())[-3]
    last_week_1 = list(somministrazioni.values())[-8]
    last_week_2 = list(somministrazioni.values())[-9]
    last_week_3 = list(somministrazioni.values())[-10]
    delta_perc_1 = round((today-last_week_1)/last_week_1*100, 0)
    delta_perc_2 = round((yesterday-last_week_2)/last_week_2*100, 0)
    delta_perc_3 = round((yeyesterday-last_week_3)/last_week_3*100, 0)
    summary += f"\nVaccinazioni giornaliere:\nOggi:{today} ({delta_perc_1:+}%)\nIeri:{yesterday} ({delta_perc_2:+}%)\nL'altro ieri: {yeyesterday} ({delta_perc_3:+}%)\n\n"

    print("Grafico somministrazioni giornaliere per fornitore")
    astrazeneca = data["somministrazioni_vaccini"]["nazionale"][data["somministrazioni_vaccini"]
                                                                ["nazionale"]["fornitore"] == "Vaxzevria (AstraZeneca)"]
    astrazeneca = (astrazeneca.groupby("data_somministrazione")["prima_dose"].sum(
    ) + astrazeneca.groupby("data_somministrazione")["seconda_dose"].sum()).to_dict()

    pfizer = data["somministrazioni_vaccini"]["nazionale"][data["somministrazioni_vaccini"]
                                                           ["nazionale"]["fornitore"] == "Pfizer/BioNTech"]
    pfizer = (pfizer.groupby("data_somministrazione")["prima_dose"].sum(
    ) + pfizer.groupby("data_somministrazione")["seconda_dose"].sum()).to_dict()

    moderna = data["somministrazioni_vaccini"]["nazionale"][data["somministrazioni_vaccini"]
                                                            ["nazionale"]["fornitore"] == "Moderna"]
    moderna = (moderna.groupby("data_somministrazione")["prima_dose"].sum(
    ) + moderna.groupby("data_somministrazione")["seconda_dose"].sum()).to_dict()

    adjusted = shape_adjust([pfizer, moderna, astrazeneca, monodose])

    media_mobile_somministrazioni = create_media_mobile(
        somministrazioni.values())
    grafico_vaccini_fornitore(
        adjusted[0],
        adjusted[1],
        adjusted[2],
        adjusted[3],
        [somministrazioni.keys(), media_mobile_somministrazioni],
        "Somministrazioni giornaliere per fornitore",
        f"Fonte dati: Covid19 Opendata Vaccini | Ultimo aggiornamento: {last_update}",
        "/graphs/vaccini/somministrazioni_giornaliere_fornitore.jpg"
    )

    print("Grafico somministrazioni giornaliere per fascia d'età")
    somministrazioni_fasce = []
    prime_dosi_fasce = []
    for i in range(len(data["anagrafica_vaccini_summary"]["fascia_anagrafica"])):
        fascia = data["anagrafica_vaccini_summary"]["fascia_anagrafica"].iat[i]
        prima_dose = data["somministrazioni_vaccini"]["nazionale"][data["somministrazioni_vaccini"]["nazionale"]
                                                                   ["fascia_anagrafica"] == fascia].groupby("data_somministrazione")["prima_dose"].sum().to_dict()
        seconda_dose = data["somministrazioni_vaccini"]["nazionale"][data["somministrazioni_vaccini"]["nazionale"]
                                                                     ["fascia_anagrafica"] == fascia].groupby("data_somministrazione")["seconda_dose"].sum().to_dict()
        result = {}
        for date in prima_dose.keys():
            result[date] = prima_dose[date] + seconda_dose[date]
        somministrazioni_fasce.append(result)
        prime_dosi_fasce.append(prima_dose)
    adjusted = shape_adjust(somministrazioni_fasce)

    grafico_vaccini_fascia_eta(
        adjusted,
        [somministrazioni.keys(), media_mobile_somministrazioni],
        "Somministrazioni giornaliere per fascia d'età",
        f"Fonte dati: Covid19 Opendata Vaccini | Ultimo aggiornamento: {last_update}",
        "/graphs/vaccini/somministrazioni_giornaliere_fascia_anagrafica.jpg"
    )

    grafico_vaccini_cumulativo(
        prime_dosi_fasce,
        "Prime dosi giornaliere per fascia d'età MM7",
        f"Fonte dati: Covid19 Opendata Vaccini | Ultimo aggiornamento: {last_update}",
        "/graphs/vaccini/prime_dosi_fascia.jpg"
    )

    print("Grafico fasce popolazione...")
    y_values_prima_dose = []
    y_values_seconda_dose = []
    y_values_monodose = []
    for index, row in data["anagrafica_vaccini_summary"].iterrows():
        janssen_fascia = janssen[janssen["fascia_anagrafica"] == row["fascia_anagrafica"]]["prima_dose"].sum()
        perc_prima_dose = (row["prima_dose"] - row["seconda_dose"] - janssen_fascia) / FASCE_POPOLAZIONE[row["fascia_anagrafica"]][
            "nazionale"]
        perc_seconda_dose = row["seconda_dose"] / \
            FASCE_POPOLAZIONE[row["fascia_anagrafica"]]["nazionale"]
        perc_monodose = janssen_fascia / FASCE_POPOLAZIONE[row["fascia_anagrafica"]]["nazionale"]
        y_values_prima_dose.append(perc_prima_dose * 100)
        y_values_seconda_dose.append(perc_seconda_dose * 100)
        y_values_monodose.append(perc_monodose * 100)

    grafico_vaccinati_fascia_anagrafica(
        data["anagrafica_vaccini_summary"]["fascia_anagrafica"],
        y_values_prima_dose,
        y_values_seconda_dose,
        y_values_monodose,
        "Somministrazione vaccini per fascia d'età",
        f"Fonte dati: Covid19 Opendata Vaccini | Ultimo aggiornamento: {last_update}",
        "/graphs/vaccini/somministrazione_fascia_eta.jpg"
    )

    summary += "Percentuali fascia anagrafica:\n"

    for i in range(len(data["anagrafica_vaccini_summary"]["fascia_anagrafica"])):
        fascia = data["anagrafica_vaccini_summary"]["fascia_anagrafica"].iat[i]
        summary += f"{fascia}: {y_values_seconda_dose[i]}% ({y_values_prima_dose[i]}%)\n"

    print("Grafico consegne vaccino...")
    consegne = data["consegne_vaccini"].groupby(
        "data_consegna")["numero_dosi"].sum().to_dict()
    consegne_astrazeneca = data["consegne_vaccini"][data["consegne_vaccini"]["fornitore"]
                                                    == "Vaxzevria (AstraZeneca)"].groupby("data_consegna")["numero_dosi"].sum().to_dict()
    consegne_moderna = data["consegne_vaccini"][data["consegne_vaccini"]["fornitore"]
                                                == "Moderna"].groupby("data_consegna")["numero_dosi"].sum().to_dict()
    consegne_pfizer = data["consegne_vaccini"][data["consegne_vaccini"]["fornitore"]
                                               == "Pfizer/BioNTech"].groupby("data_consegna")["numero_dosi"].sum().to_dict()
    consegne_janssen = data["consegne_vaccini"][data["consegne_vaccini"]["fornitore"]
                                                == "Janssen"].groupby("data_consegna")["numero_dosi"].sum().to_dict()
    adjusted = shape_adjust(
        [consegne_pfizer, consegne_moderna, consegne_astrazeneca, consegne_janssen])
    media_mobile = create_media_mobile(consegne.values())

    grafico_vaccini_fornitore(
        adjusted[0],
        adjusted[1],
        adjusted[2],
        adjusted[3],
        [consegne.keys(), media_mobile],
        "Consegne vaccini",
        f"Fonte dati: Covid19 Opendata Vaccini | Ultimo aggiornamento: {last_update}",
        "/graphs/vaccini/consegne_vaccini.jpg"
    )
    summary += f"\nMedia consegne vaccino:\n{media_mobile[-1]}\n\n"

    print("Grafico consegne totali vaccini")
    fornitori = data["consegne_vaccini"].groupby(
        "fornitore")["numero_dosi"].sum().to_dict()
    grafico_consegne_totale(
        fornitori,
        CONSEGNE_VACCINI,
        f"Fonte dati: Covid19 Opendata Vaccini | Ultimo aggiornamento: {last_update}",
        "/graphs/vaccini/consegne_totali_vaccini.jpg"
    )

    summary += "Consegne totali:\n"
    for el in fornitori:
        summary += f"{el}: {fornitori[el]}\n"

    summary += "\nDATI REGIONALI\n\n"
    for regione in data["somministrazioni_vaccini_summary"]["regioni"].keys():
        print(f"Regione {regione}")
        denominazione_regione = data["regioni"][regione]["denominazione_regione"].iloc[0]
        summary += f"\n{denominazione_regione}\n"

        print("Grafico vaccinazione giornaliere, prima e seconda dose...")
        dataframe = data["somministrazioni_vaccini"]["regioni"][regione]
        janssen = dataframe[dataframe["fornitore"] == "Janssen"]
        somministrazioni = \
            data["somministrazioni_vaccini_summary"]["regioni"][regione].groupby("data_somministrazione")[
                "totale"].sum().to_dict()
        prima_dose = data["somministrazioni_vaccini_summary"]["regioni"][regione].groupby("data_somministrazione")[
            "prima_dose"].sum().to_dict()
        seconda_dose = data["somministrazioni_vaccini_summary"]["regioni"][regione].groupby("data_somministrazione")[
            "seconda_dose"].sum().to_dict()
        monodose = janssen.groupby("data_somministrazione")["prima_dose"].sum().to_dict()

        for day in prima_dose:
            if day in monodose.keys():
                prima_dose[day] -= monodose[day]
        
        # TODO: Rimuovere quando tutte le regioni avranno fatto somministrazioni Janssen
        if len(monodose) == 0:
            end = max([list(x.keys())[-1] for x in [prima_dose, seconda_dose]])
            monodose[end] = 0

        adjusted = order(shape_adjust([prima_dose, seconda_dose, monodose]))

        stackplot(
            adjusted[0].keys(),
            adjusted[0].values(),
            adjusted[1].values(),
            f"Vaccinazioni giornaliere in {denominazione_regione}",
            ["Prima dose", "Seconda dose", "Monodose"],
            f"/graphs/vaccini/vaccinazioni_giornaliere_dosi_{denominazione_regione}.jpg",
            footer=f"Fonte dati: Covid19 Opendata Vaccini | Ultimo aggiornamento: {last_update}",
            y3=adjusted[2].values()
        )
        today = list(somministrazioni.values())[-1]
        yesterday = list(somministrazioni.values())[-2]
        yeyesterday = list(somministrazioni.values())[-3]
        last_week_1 = list(somministrazioni.values())[-8]
        last_week_2 = list(somministrazioni.values())[-9]
        last_week_3 = list(somministrazioni.values())[-10]
        delta_perc_1 = round((today-last_week_1)/last_week_1*100, 0)
        delta_perc_2 = round((yesterday-last_week_2)/last_week_2*100, 0)
        delta_perc_3 = round((yeyesterday-last_week_3)/last_week_3*100, 0)
        summary += f"\nVaccinazioni giornaliere:\nOggi:{today} ({delta_perc_1:+}%)\nIeri:{yesterday} ({delta_perc_2:+}%)\nL'altro ieri: {yeyesterday} ({delta_perc_3:+}%)\n\n"


        print("Grafico somministrazioni giornaliere per fornitore")
        astrazeneca = dataframe[dataframe["fornitore"]
                                == "Vaxzevria (AstraZeneca)"]
        astrazeneca = (astrazeneca.groupby("data_somministrazione")["prima_dose"].sum(
        ) + astrazeneca.groupby("data_somministrazione")["seconda_dose"].sum()).to_dict()

        pfizer = dataframe[dataframe["fornitore"] == "Pfizer/BioNTech"]
        pfizer = (pfizer.groupby("data_somministrazione")["prima_dose"].sum(
        ) + pfizer.groupby("data_somministrazione")["seconda_dose"].sum()).to_dict()

        moderna = dataframe[dataframe["fornitore"] == "Moderna"]
        moderna = (moderna.groupby("data_somministrazione")["prima_dose"].sum(
        ) + moderna.groupby("data_somministrazione")["seconda_dose"].sum()).to_dict()

        adjusted = shape_adjust([pfizer, moderna, astrazeneca, monodose])

        media_mobile_somministrazioni = create_media_mobile(
            somministrazioni.values())

        grafico_vaccini_fornitore(
            adjusted[0],
            adjusted[1],
            adjusted[2],
            adjusted[3],
            [somministrazioni.keys(), media_mobile_somministrazioni],
            f"Somministrazioni giornaliere per fornitore - {denominazione_regione}",
            f"Fonte dati: Covid19 Opendata Vaccini | Ultimo aggiornamento: {last_update}",
            f"/graphs/vaccini/somministrazioni_giornaliere_fornitore_{denominazione_regione}.jpg"
        )

        print("Grafico somministrazioni giornaliere per fascia d'età")
        somministrazioni_fasce = []
        prima_dose_fasce = []
        for i in range(len(data["anagrafica_vaccini_summary"]["fascia_anagrafica"])):
            fascia = data["anagrafica_vaccini_summary"]["fascia_anagrafica"].iat[i]
            prima_dose = data["somministrazioni_vaccini"]["regioni"][regione][data["somministrazioni_vaccini"]["regioni"]
                                                                              [regione]["fascia_anagrafica"] == fascia].groupby("data_somministrazione")["prima_dose"].sum().to_dict()
            seconda_dose = data["somministrazioni_vaccini"]["regioni"][regione][data["somministrazioni_vaccini"]["regioni"]
                                                                                [regione]["fascia_anagrafica"] == fascia].groupby("data_somministrazione")["seconda_dose"].sum().to_dict()
            result = {}
            for date in prima_dose.keys():
                result[date] = prima_dose[date] + seconda_dose[date]
            prima_dose_fasce.append(prima_dose)
            somministrazioni_fasce.append(result)
        adjusted = shape_adjust(somministrazioni_fasce)

        grafico_vaccini_fascia_eta(
            adjusted,
            [somministrazioni.keys(), media_mobile_somministrazioni],
            f"Somministrazioni giornaliere per fascia d'età - {denominazione_regione}",
            f"Fonte dati: Covid19 Opendata Vaccini | Ultimo aggiornamento: {last_update}",
            f"/graphs/vaccini/somministrazioni_giornaliere_fascia_anagrafica_{denominazione_regione}.jpg"
        )

        grafico_vaccini_cumulativo(
            prima_dose_fasce,
            f"Prime dosi giornaliere per fascia d'età - {denominazione_regione} MM7",
            f"Fonte dati: Covid19 Opendata Vaccini | Ultimo aggiornamento: {last_update}",
            f"/graphs/vaccini/prime_dosi_fascia_{denominazione_regione}.jpg"
        )

        print("Grafico fasce popolazione...")

        y_values_prima_dose = []
        y_values_seconda_dose = []
        y_values_monodose = []
        for fascia in FASCE_POPOLAZIONE:
            if fascia == "totale":
                continue
            prima_dose = dataframe[dataframe["fascia_anagrafica"]
                                   == fascia]["prima_dose"].sum()
            seconda_dose = dataframe[dataframe["fascia_anagrafica"]
                                     == fascia]["seconda_dose"].sum()
            monodose = janssen[janssen["fascia_anagrafica"] == fascia]["prima_dose"].sum()
            perc_prima_dose = (prima_dose - seconda_dose - monodose) / \
                FASCE_POPOLAZIONE[fascia][denominazione_regione]
            perc_seconda_dose = (
                seconda_dose / FASCE_POPOLAZIONE[fascia][denominazione_regione])
            y_values_prima_dose.append(perc_prima_dose * 100)
            y_values_seconda_dose.append(perc_seconda_dose * 100)
            y_values_monodose.append(perc_monodose * 100)

        grafico_vaccinati_fascia_anagrafica(
            data["anagrafica_vaccini_summary"]["fascia_anagrafica"],
            y_values_prima_dose,
            y_values_seconda_dose,
            y_values_monodose,
            f"Somministrazione vaccini per fascia d'età in {denominazione_regione}",
            f"Fonte dati: Covid19 Opendata Vaccini | Ultimo aggiornamento: {last_update}",
            f"/graphs/vaccini/somministrazione_fascia_eta_{denominazione_regione}.jpg"
        )

        for i in range(len(data["anagrafica_vaccini_summary"]["fascia_anagrafica"])):
            fascia = data["anagrafica_vaccini_summary"]["fascia_anagrafica"].iat[i]
            summary += f"{fascia}: {y_values_seconda_dose[i]}% ({y_values_prima_dose[i]} %)\n"

    return summary


if __name__ == "__main__":
    # Inizializza i dati
    start_time = time()
    print("--- Inizializzazione dataset...")
    for url_name in URLS.keys():
        download_csv(url_name, URLS[url_name])
    CWD = os.path.abspath(os.path.dirname(__file__))
    os.makedirs(f"{CWD}/graphs", exist_ok=True)
    plt.style.use("seaborn-dark")

    print("Dati caricati con successo.\n-----------------------------")

    print("Inizio generazione grafici epidemia...")
    sum_epidemia = epidemia()

    print("-----------------------------\nInizio generazione grafici vaccini...")
    sum_vaccini = vaccini()

    with open(f"{CWD}/summary_epidemia.txt", 'w') as f:
        f.write(sum_epidemia)

    with open(f"{CWD}/summary_vaccini.txt", "w") as f:
        f.write(sum_vaccini)

    delta = (time() - start_time)//1

    print(
        f"-----------------------------\nScript completato con successo in {int(delta)} s. I risultati si trovano nella cartella graphs.")
