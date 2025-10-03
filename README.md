
# ♻️ Proyecto:   Plataforma tecnológica con modelos de predicción de la capacidad, diseño de la red y simulación de escenarios para la toma de decisiones

**Análisis de la implementación del modelo de retornabilidad de envases para una organización encargada de la gestión de los envases al final de su ciclo de vida**

Este repositorio contiene notebooks, datos y configuraciones utilizadas en el desarrollo del proyecto, impulsado por **Alianza Circular**, con el fin de tomar decisiones a nivel estratégico. El desarrollo de la plataforma tecnológica permite abordar el problema de diseño de redes, determinando la localización óptima de las facilidades logísticas, facilitando la operación de un sistema multiperiodo y multiproducto, con el objetivo de maximizar el valor presente neto de las utilidades.
evaluar escenarios de implementación de envases retornables y su impacto ambiental y económico.

---

## 📁 Estructura del repositorio

### 1. `calculate_distances` (Cálculo de distancias logísticas)  
Permite calcular las distancias entre diferentes puntos de la cadena logística (recolección, clasificación, lavado y productores) usando la API pública de **OSRM**.  

**Entrada**  
Archivo CSV con:  
- `id`: identificador único del punto  
- `latitude`: coordenada de latitud  
- `longitude`: coordenada de longitud  
- `type`: tipo de nodo (`collection`, `clasification`, `washing`, `producer`)  

**Proceso**  
- Filtra los puntos por tipo.  
- Calcula distancias en km entre:  
  - Recolección → Clasificación  
  - Clasificación → Lavado  
  - Lavado → Productor  
- Genera un archivo temporal `.csv`.  

**Salida**  
Archivo **`distances.csv`** con:  
- `origin`  
- `type_origin`  
- `destination`  
- `tipo_destination`  
- `distance_geo`  

---

### 2. `opt_pyomo` (Modelo de optimización en Pyomo + solver)  
Contiene una implementación del modelo de optimización usando **Pyomo**, que puede resolverse con diferentes solvers (ej. CBC, GLPK, CPLEX o Gurobi).  

**Funciones principales**:  
- `create_model_pyomo(instance, model_integer=False)`: construye el modelo a partir de la instancia de datos.  
- `get_vars_sol_pyomo(model)`: extrae las soluciones en **DataFrames de Pandas**.  

Incluye definición de variables de decisión, función objetivo (maximizar utilidad descontada) y restricciones de capacidad, inventario, demanda y apertura de instalaciones.  

---

### 3. `opt_gurobipy` (Modelo de optimización en Gurobi)  
Implementación directa del modelo con la API de **Gurobi**.  

**Funciones principales**:  
- `create_model_gb(instance, model_integer=False)`: construye el modelo.  
- `get_vars_sol_gb(model)`: obtiene soluciones organizadas en DataFrames.  
- `get_obj_components(model)`: descompone la función objetivo en ingresos, costos y emisiones.  
- `distancia_geo(punto1, punto2)`: calcula la distancia entre puntos usando OSRM.  

---

### 4. `utilities` (Funciones de apoyo)  
Incluye funciones para preparar, procesar y visualizar datos.  

- Lectura de archivos JSON y CSV.  
- Construcción de instancias (`create_instance`).  
- Procesamiento de resultados (`create_df_coord`, `create_df_OF`, `create_df_util`).  
- Visualizaciones:  
  - Mapas interactivos (`create_map`)  
  - Gráficos de costos (`graph_costs`)  
  - Utilización de capacidades (`graph_utilization`)  

**Entradas:** JSON y CSV (coordenadas, distancias, demanda).  
**Salidas:** instancias listas para el modelo, resultados procesados y gráficos.  

---

## 📂 Ejemplos de uso  

El repositorio incluye archivos de ejemplo en la carpeta `datos/` para facilitar la ejecución de los modelos:  

- **`data.json`** → Establece los parámetros de entrada del modelo.  
- **`coordenadas.csv`** → Define el mapa de la red logística, indicando qué nodos existen, de qué tipo son y en qué lugar están ubicados. El modelo lo utiliza junto con el archivo de parámetros (JSON) para calcular distancias, flujos y costos.  



---

## 🧪 Tecnologías utilizadas

- Python 
- Jupyter Notebooks
- Pandas, NumPy, Matplotlib, Seaborn


---

## 🚀 ¿Cómo ejecutar el proyecto?

1. Clona este repositorio:
   ```bash
   git clone https://github.com/alianzacircular/2025_Retornable.git
   cd 2025_Retornable
2. Instala las dependencias:
   pip install -r requirements.txt
3. Ejecuta los notebooks:



## 🤝 Contacto
Para dudas o sugerencias, puedes contactar al equipo de **Alianza Circular** a través de:

🌐 Sitio web: https://www.alianzacircular.com/acerca-de-nosotros
✉️ Correo electrónico: alianzacircular@gmail.com
