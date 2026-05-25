# 🗺️ RUA - Rutas Universitarias de Auxilio

Sistema inteligente para gestión de rutas críticas en un campus universitario mediante grafos ponderados y el algoritmo de Dijkstra.

Una aplicación interactiva diseñada para la planificación, enfocada en la optimización de trayectos utilizando estructuras de datos eficientes.

## 🚀 Características Principales:

- **Visualización de Grafos**: Mapa interactivo del campus con `networkx` y `matplotlib` en tema oscuro.
- **Interacción Dinámica**:
  - Seleccionar origen y destino desde panel lateral.
  - Bloquear tramos para simular rutas obstruidas.
  - Recalcular rutas dinámicamente según cambios en tiempo real.
- **Algoritmo Optimizado**: Implementación de Dijkstra con complejidad O((V + E) log V).
- **Visualización Diferenciada**: 
  - Nodos: verde (origen), rojo (destino), gris (regulares).
  - Aristas: azul (ruta óptima), rojo punteado (bloqueado), gris (normal).

## 🛠️ Tecnologías Utilizadas

* **Lenguaje Base:** Python 3.x
* **Frontend/Framework:** Streamlit
* **Procesamiento de Grafos:** 

## ⚙️ Instalación y Configuración


1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/Jon-TryHard/RUA.git](https://github.com/Jon-TryHard/RUA.git)
    cd RUA
    ```

2.  **Crear un entorno virtual (Recomendado):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    Asegúrate de tener todas las librerías necesarias ejecutando:
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Uso

Para levantar la interfaz gráfica localmente, ejecuta el siguiente comando en tu terminal:

```bash
streamlit run app.py

