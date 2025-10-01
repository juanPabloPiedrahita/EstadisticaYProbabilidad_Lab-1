# ------------------------------
# LABORATORIO ESTADÍSTICA - PUNTOS 1 a 5
# ------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Configuración de estilo
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (8,5)

# Carpeta para guardar imágenes
output_dir = "Imagenes_Puntos"
os.makedirs(output_dir, exist_ok=True)

# 1. CARGA DE DATOS
file_path = "bd2S.xlsx"
df = pd.read_excel(file_path, sheet_name="bd2S")

# Diccionarios para etiquetas
sexo_dict = {1:"Masculino", 2:"Femenino"}
est_civ_dict = {1:"Soltero", 2:"Casado", 3:"Union Libre", 4:"Separado", 5:"Viudo"}
educ_dict = {
    1:"Primaria", 2:"Secundaria Incomp.", 3:"Secundaria Completa",
    4:"Técnico", 5:"Tecnológico", 6:"Profesional", 7:"Postgrado"
}
bin_dict = {1:"Si",2:"No"}

# Numero total de encuestados
total = len(df)

# Reemplazar códigos por etiquetas
df['sexo_label'] = df['sexo'].map(sexo_dict)
df['est_civ_label'] = df['est_civ'].map(est_civ_dict)
df['educ_label'] = df['educ'].map(educ_dict)
df['desemp_label'] = df['desemp'].map(bin_dict)
df['des_est_label'] = df['des_est'].map(bin_dict)
df['eps_label'] = df['eps'].map(bin_dict)

# ------------------------------
# PUNTOS DEL LABORATORIO
# ------------------------------

# 1. Histograma tiempo desempleado (<1 año)
print(f"Punto 1 - Cantidad de personas que se demoraron menos de 1 año en conseguir empleo")

max_meses = df['tiemp_des'].max()
bins = np.arange(0, max_meses + 2, 2)

plt.figure()
sns.histplot(df['tiemp_des'], bins=bins, kde=False, color="skyblue", edgecolor="black")
plt.axvline(12, color='red', linestyle='--', label='1 año')
plt.title("Histograma - Tiempo desempleado (intervalos de 2 meses)")
plt.xlabel("Meses desempleado")
plt.ylabel("Frecuencia")
plt.xticks(np.arange(0, max_meses+1, 2))
plt.legend()
plt.savefig(f"{output_dir}/Punto_1.png")
plt.close()

#Exactamente, cuantas personas se demoraros menos de 1 año en conseguir empleo
menos_un_anio = (df['tiemp_des'] < 12).sum()
porcentaje = (menos_un_anio / total) * 100
print(f"Total encuestados: {total}")
print(f"Personas desempleadas por < 12 meses: {menos_un_anio} ({porcentaje:.2f}%)\n")


# 2. % desempleados vs país
print(f"Punto 2 - % Desempleo muestra VS Pais")

poblacion_desemp = (df['desemp']==1).mean()*100
print(f"Porcentaje desempleados en la muestra: {poblacion_desemp:.2f}%")
print(f"Dato oficial DANE (2025, hasta agosto): 8.6%\n")


# 3. Promedio ingresos profesional vs bachiller
print(f"Punto 3 - Promedio ingreso bachiller vs profesional")
prof = df[df['educ_label']=="Profesional"]['ing'].mean()
bach = df[df['educ_label']=="Secundaria Completa"]['ing'].mean()
print(f"Promedio ingresos Profesional: {prof:.0f} $")
print(f"Promedio ingresos Bachiller: {bach:.0f} $\n")


# Punto 4 - Ingresos atípicos por sexo
print(f"Punto 4 - Datos atipicos por sexo\n")
# Función para detectar outliers usando IQR
def detectar_outliers(data, columna):
    Q1 = data[columna].quantile(0.25)
    Q3 = data[columna].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    outliers = data[(data[columna] < limite_inferior) | (data[columna] > limite_superior)]
    return outliers, limite_inferior, limite_superior

# Detectar outliers por sexo
for sexo in df['sexo_label'].unique():
    subset = df[df['sexo_label'] == sexo]
    outliers, li, ls = detectar_outliers(subset, 'ing')
    print(f"\n--- {sexo} ---")
    print(f"Rango típico de ingresos: {li:.0f} a {ls:.0f}")
    print(f"Número de outliers detectados: {len(outliers)}")
    if not outliers.empty:
        print("Ejemplos de ingresos atípicos:", outliers['ing'].head().tolist())

# Grafico
plt.figure(figsize=(8,6))
sns.boxplot(
    x='sexo_label', 
    y='ing', 
    data=df, 
    palette="Set2",
    fliersize=5  # tamaño de los puntos de outliers
)
plt.title("Distribución de ingresos por sexo (con valores atípicos)", fontsize=14)
plt.xlabel("Sexo", fontsize=12)
plt.ylabel("Ingresos Mill($)", fontsize=12)
plt.savefig(f"{output_dir}/Punto_4.png")
plt.close()

# Punto 5 - Variabilidad de la edad por sexo
fem = df[df['sexo_label']=="Femenino"]['edad']
masc = df[df['sexo_label']=="Masculino"]['edad']

var_fem = fem.var()
var_masc = masc.var()

std_fem = fem.std()
std_masc = masc.std()

print("Punto 5 - Variabilidad edad")
print(f"Femenino -> Varianza: {var_fem:.2f}, Desviación Estándar: {std_fem:.2f}")
print(f"Masculino -> Varianza: {var_masc:.2f}, Desviación Estándar: {std_masc:.2f}")

#Grafica para el punto 5:
plt.figure(figsize=(7,5))
sns.boxplot(x='sexo_label', y='edad', data=df, palette="pastel")
plt.title("Distribución de la edad según el sexo")
plt.xlabel("Sexo")
plt.ylabel("Edad")
plt.savefig(f"{output_dir}/Punto_5.png")
plt.close()
