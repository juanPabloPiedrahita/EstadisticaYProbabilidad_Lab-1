# Configuraciones previas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Configuración
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (8,5)

# Crear carpeta para guardar imágenes
output_dir = "Imagenes Puntos"
os.makedirs(output_dir, exist_ok=True)

# 1. CARGA DE DATOS
file_path = "bd2S.xlsx"
df = pd.read_excel(file_path, sheet_name="bd2S")

# Diccionarios para etiquetas
sexo_dict = {1:"Masculino", 2:"Femenino"}
est_civ_dict = {1:"Soltero", 2:"Casado", 3:"Union Libre", 4:"Separado", 5:"Viudo"}
educ_dict = {1:"Primaria", 2:"Secundaria Incomp.", 3:"Secundaria Completa",
             4:"Técnico", 5:"Tecnológico", 6:"Profesional", 7:"Postgrado"}
bin_dict = {1:"Si",2:"No"}

# Reemplazar códigos
df['sexo_label'] = df['sexo'].map(sexo_dict)
df['est_civ_label'] = df['est_civ'].map(est_civ_dict)
df['educ_label'] = df['educ'].map(educ_dict)
df['desemp_label'] = df['desemp'].map(bin_dict)
df['des_est_label'] = df['des_est'].map(bin_dict)
df['eps_label'] = df['eps'].map(bin_dict)

# Puntos Laboratorio

# 1. Histograma tiempo desempleado (<1 año)
plt.figure()
sns.histplot(df['tiemp_des'], bins=20, kde=False)
plt.axvline(12, color='red', linestyle='--', label='1 año')
plt.title("Histograma - Tiempo desempleado (meses)")
plt.xlabel("Meses desempleado")
plt.ylabel("Frecuencia")
plt.legend()
plt.savefig(f"{output_dir}/Punto_1.png")
plt.close()

# 2. % desempleados vs país
poblacion_desemp = (df['desemp']==1).mean()*100
print(f"Punto 2 - Porcentaje desempleados en la muestra: {poblacion_desemp:.2f}%")
print("Comparar con DANE y concluir")

# 3. Promedio ingresos profesional vs bachiller
prof = df[df['educ_label']=="Profesional"]['ing'].mean()
bach = df[df['educ_label']=="Secundaria Completa"]['ing'].mean()
print(f"Punto 3 - Promedio ingresos Profesional: {prof:.0f}")
print(f"Punto 3 - Promedio ingresos Bachiller: {bach:.0f}")

# 4. Boxplot ingresos por sexo
plt.figure()
sns.boxplot(x='sexo_label', y='ing', data=df)
plt.title("Ingresos por sexo (atípicos)")
plt.savefig(f"{output_dir}/Punto_4.png")
plt.close()

# 5. Variabilidad edad Fem vs Masc
var_fem = df[df['sexo_label']=="Femenino"]['edad'].var()
var_masc = df[df['sexo_label']=="Masculino"]['edad'].var()
print(f"Punto 5 - Varianza edad Femenino: {var_fem:.2f}")
print(f"Punto 5 - Varianza edad Masculino: {var_masc:.2f}")

# 6. % desempleados sin EPS
tabla_eps = pd.crosstab(df['desemp_label'], df['eps_label'], normalize='index')*100
print("Punto 6 - % desempleados con/sin EPS:\n", tabla_eps)

# 7. Estado civil más frecuente
estado_freq = df['est_civ_label'].value_counts(normalize=True)*100
print("Punto 7 - Distribución estado civil (%):\n", estado_freq)
plt.figure()
estado_freq.plot(kind='bar')
plt.title("Distribución estado civil")
plt.ylabel("%")
plt.savefig(f"{output_dir}/Punto_7.png")
plt.close()

# 8. Asimetría tiempo desempleado
skew = df['tiemp_des'].skew()
if skew > 0:
    skew_text = "Asimetría positiva"
elif skew < 0:
    skew_text = "Asimetría negativa"
else:
    skew_text = "Distribución simétrica"
print(f"Punto 8 - Asimetría de tiempo desempleado: {skew:.2f} ({skew_text})")

# 9. Mediana ingresos desempeño
med_si = df[df['des_est_label']=="Si"]['ing'].median()
med_no = df[df['des_est_label']=="No"]['ing'].median()
print(f"Punto 9 - Mediana ingresos Si se desempeña: {med_si:.0f}")
print(f"Punto 9 - Mediana ingresos No se desempeña: {med_no:.0f}")

# 10. Heterogeneidad ingresos
print("Punto 10 - Desviación estándar ingresos:", df['ing'].std())

# 11. Ojiva tiempo desempleado
counts, bins = np.histogram(df['tiemp_des'], bins=20)
cum_counts = np.cumsum(counts)/len(df)
plt.figure()
plt.plot(bins[1:], cum_counts*100, marker='o')
plt.title("Ojiva - Tiempo desempleado (%)")
plt.xlabel("Meses desempleado")
plt.ylabel("% acumulado")
plt.savefig(f"{output_dir}/Punto_11.png")
plt.close()

# 12. Histograma ingresos por sexo
plt.figure()
sns.histplot(data=df, x='ing', hue='sexo_label', kde=True)
plt.title("Distribución ingresos por sexo")
plt.savefig(f"{output_dir}/Punto_12.png")
plt.close()

# 13. Diagrama de cajas ingresos por sexo
plt.figure()
sns.boxplot(x='sexo_label', y='ing', data=df)
plt.title("Boxplot ingresos por sexo")
plt.savefig(f"{output_dir}/Punto_13.png")
plt.close()

# 14. Ingreso por nivel educativo
plt.figure()
sns.boxplot(x='educ_label', y='ing', data=df)
plt.xticks(rotation=45)
plt.title("Ingresos por nivel educativo")
plt.savefig(f"{output_dir}/Punto_14.png")
plt.close()

# 15. Tiempo desempleado vs nivel educativo
plt.figure()
sns.boxplot(x='educ_label', y='tiemp_des', data=df)
plt.xticks(rotation=45)
plt.title("Tiempo desempleado vs nivel educativo")
plt.savefig(f"{output_dir}/Punto_15.png")
plt.close()

# 16. Estado civil vs edad
labels = ["16-25","26-35","36-45","46-55","56-65","66+"]
df['edad_intervalo'] = pd.cut(df['edad'], bins=[15,25,35,45,55,65,100], labels=labels)
tabla_est_civ = pd.crosstab(df['edad_intervalo'], df['est_civ_label'], normalize='index')*100
print("Punto 16 - Cruce edad (intervalos) vs estado civil (%):\n", tabla_est_civ)

# 17. Nivel educativo vs ingresos
ingresos_educ = df.groupby('educ_label')['ing'].agg(['mean','median','std','count'])
print("Punto 17 - Ingresos por nivel educativo:\n", ingresos_educ)