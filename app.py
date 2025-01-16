import streamlit as st
import pickle
import pandas as pd
from PIL import Image
from sklearn.preprocessing import OrdinalEncoder


FILENAME_STATS="ecommerce_stats.csv"
FILENAME_ENCODER="rf_ordinal_encoder.pkl"
FILENAME_MODEL="rf_model.pkl"
FILENAME_LOGO="logo.png"


def calculate_stats(filename):
    ''' 
    Recupera del fitxer CSV les estadistiques necesaries per el processament EDA del dataset
    Entrada:
        filename: nom del fitxer CSV per recuperar les estadistiques del dataset d'entrenament
    Sortida:
        stats: dictionari amb les estadistiques necesaries per aplicar EDA
    '''
    stats = dict(pd.read_csv(filename).iloc[0])
    # print()
    # print("Estadisticas leidas: ", stats)
    # print("Tipo 'stats':", type(stats))
    return stats


def get_ordinal_encoder(filename):
    '''
    Recupera el codificador que es va desar en format 'pickle' a la fase de codificación de varibles categóriques
    Entrada:
        filename: nom del fitxer pickle on es va desar el codificador
    Sortida:
        encoder: objecte codificador
    '''
    with open(filename, "rb") as f:
        encoder = pickle.load(f)
    return encoder    


def get_model(filename):
    '''    
    Recupera el model Machine Learning (Random Forest) previament desat en format pickle
    entrada:
        filename: nom del fitxer amb el que es va desar el model
    sortida:
        model: model ML recuperat
    '''
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    return model


def apply_eda_to_df(df, stats):
    '''
    Processar les dades de la web per mantenir la consistència amb les dades d'entrenament 
    Básicament es la mateixa funció que es va fer servir al sprint 6 amb petites modificacions
    Aplica tots els processos de EDA al dataframe de entrada
    Entrada:
        df: dataframe original
    Sortida:
        df: dataframe modificat amb els processos EDA
    '''
    # Omplim valors faltans (en aquesta fase no cal)
    # age_mediana = stats["age_mediana"]
    # df["age"] = df["age"].fillna(age_mediana)
    # df["education"] = df['education'].fillna("unknown")
    # df["marital"] = df["marital"].fillna("unknown")
    
    # Binning de la variable "day" ([1-10]->"begin", [11-20]->"mid", [21-31]->"end")
    df["day"] = df["day"].apply(lambda x: "begin" if x <= 10 else ("mid" if x <= 20 else "end"))
    
    # Binning de la variable "balance"
    q75 = stats["balance_q75"]
    df["balance"] = df["balance"].apply(lambda x: 0 if x <= q75 else 1)
    
    # Binning de la la variable "campaign"
    q75 = stats["campaign_q75"]
    q95 = stats["campaign_q95"]                 # Error en el EDA del sprint 6 !!!!!
    df["campaign"] = df["campaign"].apply(lambda x: 0 if x <= q75 else (1 if x <= q95 else 2))

    # Binning de la variable "pdays"
    q75 = stats["pdays_q75"]
    df["pdays"] = df["pdays"].apply(lambda x: 0 if x == -1 else (1 if x <= q75 else 2))
 
    # Eliminem les variables que hem identificat com menys importants o són redundants (en aquesta fase no cal)
    # col_del = ["duration", "previous", "age", "default"]
    # df.drop(col_del, axis=1, inplace=True)

    return df


def encode_categorical_X(df, encoder):
    '''
    Codificació de les variables categòriques d'entrada
    Basicament es la mateixa funció que al sprint 6 (amb petitesalgunes modificacions) per mantenir la consistència de les dades
    La funció 'get_dummies' per aplicar 'one-hot-encoder' no es pot desar en format 'pickle' i s'ha d'aplicar manualment en producció
    Entrada:
        df: dataframe de variables d'entrada
        encoder: objecte 'ordinal_encoder' utilitzat a la fase de codificació de les varibles categóriques  
    Sortida:
        df: dataframe codificat
    '''
    # "job": Reducció de 12 categories a 3. 
    job_map = {
        "student"       : "low",
        "unemployed"    : "low",
        "housemaid"     : "low",
        "unknown"       : "low",
        "admin."        : "mid", 
        "services"      : "mid",
        "retired"       : "mid",
        "blue-collar"   : "mid",
        "entrepreneur"  : "mid",
        "self-employed" : "mid",
        "technician"    : "high", 
        "management"    : "high"
    }
    df["job_level"] = df["job"].replace(job_map)    # Crea la nova categoria
    df.drop("job", axis=1, inplace=True)            # Elimina la categoria antiga

    # Reducció de 12 categorias a 4, mantenint part de la estacionalitat
    # Codificarem amb "one-hot" ja que no hi ha distancia de relació entre categories
    month_map = {
        "jan" : "Q1", 
        "feb" : "Q1", 
        "mar" : "Q1",
        "apr" : "Q2", 
        "may" : "Q2", 
        "jun" : "Q2",
        "jul" : "Q3", 
        "aug" : "Q3", 
        "sep" : "Q3",
        "oct" : "Q4", 
        "nov" : "Q4", 
        "dec" : "Q4"
    }
    df["quarter"] = df["month"].replace(month_map)  # Crea la nova categoria
    df.drop("month", axis=1, inplace=True)          # Elimina la categoria antiga

    # Llistat de variables que es codificaran amb 'one-hot-encoder'
    ### TIP: 'pd.get_dummies()' genera una columna per cada valor que troba en el dataframe
    ###      En producció només tenim un valor i per tant només generará una columna nova
    ###      Això produeix un desajust en el dataset de usuario (només un valor) i el model desat (tots els valors)
    ###      Per solucionar-ho, crearem una funció posterior per omplir els valors faltans (solució no gaire neta)   

    col_to_one_hot = [
        "marital",                  
        "contact",                  
        "poutcome",                 
        "day",                      
        "quarter"                   
    ]
    df = pd.get_dummies(df, columns=col_to_one_hot)

    ### TIP: Mateix problema que a 'One-Hot-Encoder', mateixa solució
    col_to_ordinal = {
        "job_level" : ["low", "mid", "high"],
        "education" : ["unknown", "primary", "secondary", "tertiary"],
        "housing"   : ["no", "yes"],
        "loan"      : ["no", "yes"],
    }
    # encoder = OrdinalEncoder(categories=list(col_to_ordinal.values()))
    df[list(col_to_ordinal.keys())] = encoder.fit_transform(df[list(col_to_ordinal.keys())])

    return df


def normalize_df(model_features, df_production):
    '''
    Normalitzar el dataframe de dades d'usuari (producció) segons estructura del dataframe d'entrenament
    Aquesta funció es conseqüència del sistema empleat durant la fase de 'one-hot-encodign y 'ordinal_encoding'
    No és un solució gaire neta, pero hem conseguit que funcioni correctament
    Entrada:
        model_features: array amb les caracteristiques del model entrenat
        df_production: dataframe de dades d'usuari (producció)
    Sortida:
        df_production: dataframe de dades d'usuari normalitzat
    '''
    df_normalize = pd.DataFrame(columns=model_features)
    for col in model_features:
        df_normalize[col] = df_production[col] if col in df_production.columns else False
  
    return df_normalize



# Recupera el model ML     
model = get_model(filename=FILENAME_MODEL)

# Declaració de les opcions d'entrada de valors
yes_no = ("no", "yes")
job_list = ("unknown", "admin.", "blue-collar", "entrepreneur", "housemaid", "management", 
            "retired", "self-employed", "services", "student", "technician", "unemployed")
marital_list = ("single", "married", "divorced")
education_list = ("unknown", "primary", "secondary", "tertiary")
month_list = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
month_days = {"jan":31, "feb":28, "mar":31, "apr":30, "may":31, "jun":30, "jul":31, "aug":31, "sep":30, "oct":31, "nov":30, "dec":31}
contact_list = ("unknown", "cellular", "telephone")
poutcome_list = ("unknown", "success", "failure")

# Capçalera del formulari Web
st.image(FILENAME_LOGO)
st.title("Predicción Contratación Depósito Bancario")
st.header("(_Random Forest_  :deciduous_tree: :deciduous_tree: :deciduous_tree:)") 

# DEBUG
st.write("Version libreria sckikit-learn", sklearn.__version__)
# DEBUG

# Entrada de dades del usuari (totes excepte 'age', 'duration', 'previous', 'default' ja es van descartar)
st.subheader("Bank client data:", divider="gray")
# age=st.slider("**1 - Age:**", min_value=18, max_value=120, value=30, step=1, disabled=True)    # 
job=st.radio("**2 - Type of job:**", job_list, horizontal=True, index=0)
marital=st.radio("**3 - Marital status:**", marital_list, horizontal=True, index=0)   
education=st.radio("**4 - Education:**", education_list, horizontal=True, index=0)
# default=st.radio("**5 - Has credit in default?**", yes_no, horizontal=True)
balance=st.number_input("**6 - Average yearly balance (euros):**", step=1, value=0)
housing=st.radio("**7 - Has housing loan?**", yes_no, horizontal=True, index=0)
loan=st.radio("**8 - Has personal loan?**", yes_no, horizontal=True, index=0)

st.subheader("Last contact of the current campaign:", divider="gray")
contact=st.radio("**9 - Contact communication type**", contact_list, horizontal=True, index=0)
month=st.radio("**11 - Last contact month of year**", month_list, horizontal=True, index=0)
day=st.slider("**10 - Last contact day of the month**", min_value=1, max_value=month_days[month], step=1)

st.header("Other attributes:", divider='gray')
campaign=st.number_input("**13 - Number of contacts performed during this campaign and for this client**", min_value=0, step=1)
pdays=st.number_input("**14 - Number of days that passed by after the client was last contacted from a previous campaign**", min_value=-1, step=1)
# previous=st.number_input("**15 - Number of contacts performed before this campaign and for this client**", min_value=0, step=1)
poutcome=st.radio("**16 - Outcome of the previous marketing**", poutcome_list, horizontal=True, index=0)

# Crear un DataFrame con las entradas (ja no surten les 4 caracteristiques abans descartades (age, default, previous, duration))
user_data = pd.DataFrame({
    'job': [job],
    'marital': [marital],
    'education': [education],
    'balance': [balance],
    'housing': [housing],
    'loan': [loan],
    'contact': [contact],
    'day': [day],
    'month': [month],
    'campaign': [campaign],
    'pdays': [pdays],
    'poutcome': [poutcome]
})
# print()
# print(user_data)
# st.write(f"Datos recogidos: {user_data.columns}")
# st.write(f"Datos recogidos: {user_data.iloc[0].values}")
# user_data.to_csv("_user_data.csv", index=False)

# Recupera estadístiques originals per aplicar EDA
stats=calculate_stats(filename=FILENAME_STATS)
user_data_eda=apply_eda_to_df(user_data, stats=stats)
# print(user_data_eda)
# st.write(f"Datos procesados: {user_data_eda.columns}")
# st.write(f"Datos procesados: {user_data_eda.iloc[0].values}")
# user_data_eda.to_csv("_user_data_eda.csv", index=False)

# Recupera el codificador original d'entrenament
encoder = get_ordinal_encoder(filename=FILENAME_ENCODER)
user_data_coded=encode_categorical_X(user_data_eda, encoder=encoder)
# print(user_data_coded)
# st.write(f"Datos codificados: {user_data_coded.columns}")
# st.write(f"Datos codificados: {user_data_coded.iloc[0].values}")
# user_data_coded.to_csv("_user_data_coded.csv", index=False)

# Normalitza i asegura el format de les dades d'usuari
user_data_norm = normalize_df(model_features=model.feature_names_in_, df_production=user_data_coded)
# print(user_data_norm)
# st.write(f"Datos normalizados: {user_data_norm.columns}")
# st.write(f"Datos normalizados: {user_data_norm.iloc[0].values}")
user_data_norm.to_csv("_user_data_norm.csv", index=False)

# Finalment, calcula i presenta la predicció
st.header("Prediction:", divider='gray')
deposit=model.predict(user_data_norm)
# st.write(f"Deposit: {deposit}")
st.write("Will the client subscribe a term deposit: ", "**YES**" if deposit else "no")

st.subheader("", divider="gray")
st.subheader("(c) Manu Cañete 2025 [manuel.canete023@gmail.com]")

