# **SPRINT 4.** Projecte individual- Recol·lecció de dades

### ***Tasca 4.2***
- Objectius: Documentar un procés de recol·lecció de dades.
- Utilitza la plantilla "Documentació_Recol·lecció_de_dades.md" disponible a GitHub. Dissenya el teu document a Jupyter Notebook i després exporta a Markdown. Puja'l al teu repositori de GitHub i insereix l'URL per a la seva avaluació. Recorda que el repositori ha d'estar públic.

#### Exercici 1. Documenta el procés de recol·lecció de dades.
Explora el conjunt de dades 'bank dataset.csv' que ja coneixes i utilitza la teva creativitat per dissenyar el document de recol·lecció de dades.

## Descripció del fitxer 'bank_dataset.csv' 
https://archive.ics.uci.edu/dataset/222/bank+marketing

### Input variables:
   
#### **bank client data:**
1. **age** (numeric)
2. **job** : type of job (categorical: "admin.","unknown","unemployed","management","housemaid","entrepreneur","student",
                                    "blue-collar","self-employed","retired","technician","services") 
3. **marital** : marital status (categorical: "married","divorced","single"; note: "divorced" means divorced or widowed)
4. **education** (categorical: "unknown","secondary","primary","tertiary")
5. **default**: has credit in default? (binary: "yes","no")
6. **balance**: average yearly balance, in euros (numeric) 
7. **housing**: has housing loan? (binary: "yes","no")
8. **loan**: has personal loan? (binary: "yes","no")

#### **related with the last contact of the current campaign:**
9. **contact**: contact communication type (categorical: "unknown","telephone","cellular") 
10. **day**: last contact day of the month (numeric)
11. **month**: last contact month of year (categorical: "jan", "feb", "mar", ..., "nov", "dec")
12. **duration**: last contact duration, in seconds (numeric)

#### **other attributes:**
13. **campaign**: number of contacts performed during this campaign and for this client (numeric, includes last contact)
14. **pdays**: number of days that passed by after the client was last contacted from a previous campaign (numeric, -1 means client was not previously contacted)
15. **previous**: number of contacts performed before this campaign and for this client (numeric)
16. **poutcome**: outcome of the previous marketing campaign (categorical: "unknown","other","failure","success")

#### **Output variable (desired target):**
17.**y** - has the client subscribed a term deposit? (binary: "yes","no")

# Documentació del Procés de Recol·lecció de Dades per al Projecte de Predicció de Contractació de un Dipòsit 
## 1. Fonts

**Identificació de Fonts:**
- Base de dades interna del banc per les dades des de la caracteristica a fins a la 8 (1.age - 8.loan). En el dataset proporcionat hi ha poc més de 11.000 registres, pel que es pot deduir que s'ha agafat una mostra de clients i no es treballa amb el llistat complet de clients. Unes gráfiques de histogrames bàsics permet veure la distribució de les dades de tipus numeric (```df.plot.hist(bins=30)```). Per les caracteristiques categòriques es pot contar i representar gràficament cadascún dels seus valors(```df['education'].value_count()```). Per altra banda, hem d'assegurar que la mostra es representativa de la base de dades total del banc, el que es pot fer calculant els paràmetres representatius de la mostra (mitja, desviació, distribució, ...) i comparar-les amb els paràmetres de la base total de clients de l'entitat. Com veurem mes endavant, hi ha dades que s'han de protegir perquè són de caracter personal.
- La resta de caracteristiques corresponen als resultats de la darrera campanya de màrqueting (9 - 12) i les campanyes anteriors (13 - 16). Aquestes dades vindran del departament de màrqueting, encarregat de les campanyes per vendre productes als clients.
- Finalment tenim la etiqueta que volem predir (variable objetivo), que correspon a si el client va contractar o no un dipòsit.

**Descripció de les Fonts:**
- La extracció de les dades del primer bloc correspon al departament d'IT i només cal fer-ho un cop. El CRM de l'empresa ja preveu aquest tipus d'extracció i facilita la exportació en diferents formats estàndars, com ara Excel i CSV. La resta vindrà del departament de màrqueting que s'encarrega de fer la campanya de trucades. El llistat s'anirà omplint periòricament segons es vagin fent els contactes i es vagin omplint els formularis amb els resultats dels contactes amb els clients. És responsabilitat del departament d'IT que el format sigui l'adient i permiti emparellar correctament les dades de màrqueting amb les dades del clients.
  
## 2. Mètodes de recol·lecció de dades

**Procediments i Eines:**
- Selecció i exportació de la mostra de clients en format CSV, i emmagatzematge en un repositori intern del banc d'accés restringit, ja que conté dades sensibles. Tasca a càrrec del departament d'IT amb la col·laboració dels responsables de la protecció de dades. El programa CRM ja permet exportació en CSV.

- Les dades de màrqueting es recopilaran diariament dels formularis utilitzats per les persones que fan els contactes i es convertiran en un fitxer CSV mitjançant un script Python. Un cop finalitzada la campanya s'ajuntaran els dos fitxers per crer-ne un de sol amb el que treballarem posteriorment.

**Freqüència de Recol·lecció:**
- Un sol cop per les dades de clients i diariament per les dades amb els resultats de la campanya de màrqueting.
  
**Scripts de Descàrrega:**
El script de descàrrega ha de tenir en compte que les dades venen de dos fitxer diferents, un amb la mostra de cliente i l'altre amb els resultats de la campanya de màrqueting. Un cop finalitzada la campanya s'han d'unificar en un únic dataset.

## 3. Format i Estructura de les Dades

**Tipus de Dades:**
Amb el següent script python tenim informació del tipus de dades de cadascuna de les característiques del dataset:

```
import pandas as pd 

FILE = "https://github.com/ITACADEMYprojectes/projecteML/blob/main/bank_dataset.CSV"
df = pd.read_csv(FILE)
df.info()
```
```
 0   age        11152 non-null  float64
 1   job        11162 non-null  object 
 2   marital    11157 non-null  object 
 3   education  11155 non-null  object 
 4   default    11162 non-null  object 
 5   balance    11162 non-null  int64  
 6   housing    11162 non-null  object 
 7   loan       11162 non-null  object 
 8   contact    11162 non-null  object 
 9   day        11162 non-null  int64  
 10  month      11162 non-null  object 
 11  duration   11162 non-null  int64  
 12  campaign   11162 non-null  int64  
 13  pdays      11162 non-null  int64  
 14  previous   11162 non-null  int64  
 15  poutcome   11162 non-null  object 
 16  deposit    11162 non-null  object 
```

- Numèrics: `age`, `balance`, `day`, `duration`, `campaign`, `pdays`, `previous`
- Categòric: `job`, `marital`, `education`, `default`, `housing`, `loan`, `contact`, `month`, `poutcome`, `deposit` 

**Format d'Emmagatzematge:**
- Dades tabulars emmagatzemades en fitxer csv, tant les dades de clients com les de màrqueting.

## 4. Limitacions de les dades

- Les dades de clients son una mostra de tots els clients. Hem d'assegurar que es representativa. L'extracció es fa un sol cop abans d'iniciar la campanya.
- Les dades de la campanya de màrqueting provenen dels formularis dels contactes que s'omplen diariament i que posteriorment es converteixen a CSV i s'enllacen amb el fitxer de clients. Aquesta correspondencia client-contacte es crítica per la consistencia i la utilitat de les dades.

## 5. Consideracions sobre Dades Sensibles

**Tipus de Dades Sensibles:**
- Informació Personal Identificable (PII): `age`, `job`, `marital`, `education`
- Informació Financera Sensible: `default`, `balance`, `housing`, `loan`, `poutcome`, `deposit`
- Dades Comportamentals Sensibles:`duration`

**Mesures de Protecció:**
- **Anonimització i Pseudonimització:**
  - La dada `age` es canviarà per rangs d'edat (0-20, 20-30, 30-40...). Els camps `job`, `marital`, `education` es canviaran per codis numèrics, el que permetrà la anonimització i a l'hora el correcte funcionament del models de ML que només treballen amb dades numériques. Amb aquest canvis ja no serà possible la identificació univoca d'un client, i per tant la resta d'informació es manté sense canvis. Es tindrà en compte que la resta de camps de tipus categoric s'hauran de pasar a numèrics en etapes posteriors i abans d'entrenar els models.
- **Accés Restringit:**
  - S'utilitzarà un repositori intern del banc tant pel fitxer CSV final com pels fitxer diaris de la campanya de màrqueting amb accés restringit només a personal autoritzat amb necessitat de conèixer aquestes dades per a fins específics del projecte. Un cop entrenat el model de machine learning s'eliminaran de forma segura (sobreescribint el contingut dels fitxer, no només borrant-los) tant el fitxer final com els intermitjos i les copies de seguretat.
- **Compliment de Regulacions:**
  - Compliment amb la GDPR, supervisada pels responsables de les dades del banc i el Chief Data Officer. Durant la trucada de contacte s'informarà al client del seu dret a l'accés, rectificació i eliminació d'aquestes dades i s'explicarà la seva finalitat.