# RUA - Rutas Universitarias de Auxilio

Sistema inteligente para gestión de rutas críticas en un campus universitario mediante grafos ponderados y el algoritmo de Dijkstra. Diseñado para optimizar la logística de emergencia y respuesta rápida.

## Características

- **Visualización de Grafos**: Mapa interactivo del campus con `networkx` y `matplotlib` en tema oscuro.
- **Interacción Dinámica**:
  - Seleccionar origen y destino desde panel lateral.
  - Bloquear tramos para simular rutas obstruidas.
  - Recalcular rutas dinámicamente según cambios en tiempo real.
- **Algoritmo Optimizado**: Implementación de Dijkstra con complejidad O((V + E) log V).
- **Visualización Diferenciada**: 
  - Nodos: verde (origen), rojo (destino), gris (regulares).
  - Aristas: azul (ruta óptima), rojo punteado (bloqueado), gris (normal).

## Archivos principales

- `app.py` - Interfaz interactiva construida con Streamlit.
- `engine.py` - Motor lógico: gestión del grafo y cálculo de rutas.

## Requisitos

- Python 3.13+
- Streamlit - Interfaz web interactiva.
- NetworkX - Manejo y análisis de grafos.
- Matplotlib - Visualización de grafos.

## Instalación rápida

1. Activar el entorno virtual:

```bash
source env/bin/activate
```

2. Instalar dependencias:

```bash
pip install streamlit networkx matplotlib
```

## Ejecución

Desde la carpeta del proyecto:

```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador por defecto en `http://localhost:8501`.

## Uso

1. **Seleccionar puntos**: Elige origen y destino en el panel lateral.
2. **Gestionar bloqueos**: Marca los tramos obstruidos o peligrosos.
3. **Visualizar ruta**: Observa la ruta calculada (azul) en el mapa del campus.
4. **Tiempo estimado**: Lee el tiempo total en minutos en el panel de resultados.

## Notas técnicas

- El grafo se actualiza en tiempo real sin necesidad de recargar.
- Los cálculos de Dijkstra se cachean para optimizar rendimiento.
- El layout del mapa se congela con `seed=42` para consistencia visual.
