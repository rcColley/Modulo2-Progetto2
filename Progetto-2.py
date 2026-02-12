import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

np.random.seed(42)

n_ordini = 100_000

ordini = pd.DataFrame({
    "ClienteID": np.random.randint(1, 5001, n_ordini),
    "ProdottoID": np.random.randint(1, 21, n_ordini),
    "Quantita": np.random.randint(1, 6, n_ordini),
    "DataOrdine": pd.to_datetime("2024-01-01") + 
                  pd.to_timedelta(np.random.randint(0, 365, n_ordini), unit="D")
})

ordini.to_csv("ordini.csv", index=False)
#--------------------------------------------------------------------------------------
categorie = ["Elettronica", "Casa", "Sport", "Abbigliamento"]
fornitori = ["SupplierA", "SupplierB", "SupplierC"]

prodotti = []

for i in range(1, 21):
    prodotti.append({
        "ProdottoID": i,
        "Categoria": np.random.choice(categorie),
        "Fornitore": np.random.choice(fornitori),
        "Prezzo": round(np.random.uniform(10, 500), 2)
    })

with open("prodotti.json", "w") as f:
    json.dump(prodotti, f, indent=2)

#--------------------------------------------------------------------------------------
regioni = ["Nord", "Centro", "Sud"]
segmenti = ["Retail", "Business", "VIP"]

clienti = pd.DataFrame({
    "ClienteID": range(1, 5001),
    "Regione": np.random.choice(regioni, 5000),
    "Segmento": np.random.choice(segmenti, 5000)
})

clienti.to_csv("clienti.csv", index=False)

#----------------------------------------------------------------------------------------
ordini = pd.read_csv("ordini.csv", parse_dates=["DataOrdine"])
clienti = pd.read_csv("clienti.csv")

with open("prodotti.json") as f:
    prodotti = pd.DataFrame(json.load(f))

df = ordini.merge(prodotti, on="ProdottoID", how="left")
df = df.merge(clienti, on="ClienteID", how="left")

df["ClienteID"] = df["ClienteID"].astype("int32")
df["ProdottoID"] = df["ProdottoID"].astype("int16")
df["Quantita"] = df["Quantita"].astype("int8")

df["Categoria"] = df["Categoria"].astype("category")
df["Fornitore"] = df["Fornitore"].astype("category")
df["Regione"] = df["Regione"].astype("category")
df["Segmento"] = df["Segmento"].astype("category")

print(df.info(memory_usage="deep"))


df["ValoreTotale"] = df["Prezzo"] * df["Quantita"]

ordini_grandi = df[df["ValoreTotale"] > 100]

#vendite per categoria
vendite_categoria = (
    df.groupby("Categoria")["ValoreTotale"]
    .sum()
    .sort_values(ascending=False)
)
#top clienti
df.groupby("Segmento")["ValoreTotale"].mean()
#vendite per regione
df.groupby("Regione")["ValoreTotale"].sum()


print(ordini_grandi)
print(vendite_categoria)