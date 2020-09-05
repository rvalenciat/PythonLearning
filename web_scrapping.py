import pandas as pd

# this function cleans up the dataframe
def clean_df(df):
    df = df[0]
    del df["Mapa administrativo"]
    del df["Capital"]
    
    return df

def clean_titles(df):
    df.rename(columns={
        "Región":"Region",
        "Población [8]​":"Poblacion",
        "Superficie (km²)[4]​":"Superficie"
    }, inplace=True)

    return df

url = "https://es.wikipedia.org/wiki/Chile"

df = pd.read_html(url, attrs={"class":"wikitable col1izq col2der col3der col4der col5der col6izq"}, header=1)

df = clean_df(df)
df = clean_titles(df)

print(df)

df.replace()