# proyecto-dosificacion
Analisis de la dosificacion de hormigon
Este proyecto consiste en el análisis de la dosificación de hormigón mediante el método ACI 211.1 y desarrollo de un modelo predictivo de asentamiento usando aprendizaje automático

# Integrantes
-Mathias Hernan Viedma Alvarenga  
-Wolfgang Darwin Arsenio Pufal Barrios  
Agradecimiento especial al Ing. Antonio Medina por su ayuda con los procedimientos por la guia en el procedimiento y calculo del proceso de dosificacion

# Planteamiento del problema
La necesidad de desarrollar una herramienta analítica que permita predecir el asentamiento del hormigon a partir de variables como relación agua/cemento, TMA, cemento, etc. mediante el uso de técnicas de aprendizaje automatico y graficos interactivos para facilitar la interpretación de resultados surge de la incertidumbre que puede llegar a generar ineficiencias, ensayos repetitivos y costos adicionales en una obra, a modo de poder garantizar la trabajabilidad y durabilidad del material.

# Objetivos del proyecto:
Objetivo general: Desarrollar un modelo predictivo y visual interactivo para analizar y estimar el asentamiento del hormigon en función de las variables determinadas por el método ACI 211.1
Objetivos específicos:
-Identificar relaciones útiles entre las variables para el análisis de datos
-Diseñar graficos interactivos con Plotly para visualizar la influencia de la relación agua/cemento, el contenido de cemento y el TMA sobre el asentamiento
-Entrenar un modelo de árbol de decisión con sklearn para predecir el asentamiento.
-Evaluar el modelo y validar su precisión


# Librerias a utilizarse:
-pandas
-numpy
-matplotlib
-plotly
-sckikit-learn

# Requerimientos:
Lenguaje: Python 3.10+
Entorno: Jupyter Notebook o VS Code
Librerías: pandas, numpy, plotly, matplotlib, seaborn, scikit-learn
Dataset en formato .csv

# Estructura de los archivos
1)datos_lab_original.xlsx -> Dataframe original en formato excel
2)proyecto_borrador[1].ipynb -> Codigo que permita la limpieza y el procesado del dataframe original
3)funciones_calculohormigon.py -> Codigo que contiene modularmente las funciones a utilizarse en los calculos en formato .py
4)code_madre_hormigon.ipynb -> Codigo principal en formato ipynb.

# Link al video de la presentacion del codigo
https://youtu.be/8i_P1mQofhM
