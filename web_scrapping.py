import pandas as pd

def clean_df_header(df):
    df = df[0]
    del df["Mapa administrativo"]
    del df["Capital"]
    df.rename(columns={
        "Región":"Region",
        "Población [8]​":"Poblacion",
        "Superficie (km²)[4]​":"Superficie"
    }, inplace=True)
    return df

def clean_df_data(df):
    df = clean_df_header(df)
    df.replace(to_replace = r'\u00A0', value = '', regex = True, inplace=True)
    df.replace(to_replace = r'\u200b', value = '', regex = True, inplace=True)
    df.replace(to_replace = r'\xa0', value = '', regex = True, inplace=True)
    df.replace(to_replace = r'\[[0-9]{1,8}\]', value = '', regex = True, inplace=True)
    df.replace(to_replace = r'\([0-9]\)', value = '', regex = True, inplace=True)
    df.replace(to_replace = r',[0-9]', value = '', regex = True, inplace=True)
    df['Poblacion'].replace(to_replace = r'\u0020', value='', regex=True, inplace=True)
    return df

def calc_population_porcentage(df):
    new_col = []
    for i in range(16):
        num = int(df.iloc[i][1]) / int(df.iloc[16][1])
        per = "{:.2%}".format(num)
        new_col.append(per)
    new_col.append('100%')
    df['% Poblacion'] = new_col
    return df

def sum_numbers(df, col, start, stop):
    sum = 0
    for i in range(start, stop):
        sum += int(df.iloc[i][col])
    return sum

def make_new_column(df, col, df2, new_col_name):
    new_col = []
    new_col.append(sum_numbers(df, col, 0, 5))
    new_col.append(sum_numbers(df, col, 5, 10))
    new_col.append(sum_numbers(df, col, 10, 16))
    df2[new_col_name] = new_col
    return df2

def setup_chile_zones_df():
    zones = ['Norte', 'Centro', 'Sur']
    df2 = pd.DataFrame(zones, columns=['Zona'])
    df2 = make_new_column(df, 1, df2, 'Poblacion')
    df2 = make_new_column(df, 2, df2, 'Superficie')
    df2 = make_new_column(df, 3, df2, 'Densidad')
    return df2

def setup_chile_regions_df():
    url = "https://es.wikipedia.org/wiki/Chile"
    df = pd.read_html(url, attrs={"class":"wikitable col1izq col2der col3der col4der col5der col6izq"}, header=1)
    df = clean_df_data(df)
    df = calc_population_porcentage(df)
    return df

df = setup_chile_regions_df()

print(df)

print("")

df2 = setup_chile_zones_df()

print(df2)