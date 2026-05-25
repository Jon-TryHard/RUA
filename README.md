# 🗺️ RUA - Rutas Universitarias de Auxilio

**Sistema inteligente para gestión de rutas críticas en un campus universitario mediante grafos ponderados y el algoritmo de Dijkstra.**

Una aplicación interactiva diseñada para la planificación y optimización de trayectos de emergencia, utilizando estructuras de datos eficientes y visualización dinámica en tiempo real.

---

## 🚀 Características Principales

- **Visualización de Grafos**: Mapa interactivo del campus con `networkx` y `matplotlib` en tema oscuro.
- **Interacción Dinámica**:
  - Seleccionar origen y destino desde panel lateral.
  - Bloquear tramos para simular rutas obstruidas o peligrosas.
  - Recalcular rutas dinámicamente según cambios en tiempo real.
- **Algoritmo Optimizado**: Implementación de Dijkstra con complejidad O((V + E) log V).
- **Visualización Diferenciada**: 
  - Nodos: verde (origen), rojo (destino), gris (regulares).
  - Aristas: azul (ruta óptima), rojo punteado (bloqueado), gris (normal).
- **Gestión de Emergencias**: Encuentra la ruta más segura evitando zonas bloqueadas.

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|---|---|---|
| **Python** | 3.x | Lenguaje de programación base |
| **Streamlit** | 1.57.0 | Framework para interfaz web interactiva |
| **NetworkX** | 3.6.1 | Procesamiento y manipulación de grafos |
| **Matplotlib** | 3.10.9 | Visualización de grafos y mapas |
| **NumPy** | 2.4.6 | Computación numérica |

---

## 📁 Estructura del Proyecto

```
RUA/
├── README.md              # Este archivo
├── requirements.txt       # Dependencias del proyecto
├── app.py                 # Interfaz principal (Streamlit)
├── engine.py              # Motor de cálculo de rutas (Dijkstra)
└── LICENSE                # Licencia del proyecto
```

---

## 📚 Descripción Detallada de Códigos

### 1️⃣ **engine.py** - Motor de Cálculo de Rutas

**Propósito**: Implementar la lógica central del algoritmo de Dijkstra y gestionar la estructura del grafo.

#### Clase: `MotorRUA`

```python
class MotorRUA:
    """
    Motor lógico central para Rutas Universitarias de Auxilio.
    Gestiona la estructura de grafo y calcula rutas óptimas mediante Dijkstra.
    """
```

**Métodos principales:**

#### `__init__(self, nodos, aristas_base)`
- **Parámetros**:
  - `nodos`: Lista de ubicaciones del campus (ej: "Biblioteca", "Cafetería")
  - `aristas_base`: Lista de tuplas (origen, destino, peso) representando conexiones con tiempo
- **Función**: Inicializa el motor, almacena los nodos y construye la estructura del grafo

#### `_construir_grafo(self)` [Privado]
- **Retorna**: Diccionario de adyacencia bidireccional
- **Ejemplo de estructura**:
  ```python
  {
    "Plaza Central": {"Biblioteca": 3, "Canchas": 6},
    "Biblioteca": {"Plaza Central": 3, "Cafetería": 2}
  }
  ```
- **Detalle**: Crea un grafo **no dirigido** (conexiones bidireccionales)

#### `calcular_ruta_segura(self, inicio, fin, bloqueos=None)` ⭐ **MÉTODO PRINCIPAL**
- **Parámetros**:
  - `inicio`: Nodo de salida
  - `fin`: Nodo de destino
  - `bloqueos`: Lista de tuplas [(origen, destino), ...] con tramos prohibidos (opcional)
- **Retorna**: Tupla `(ruta_lista, tiempo_total)` o `(None, inf)` si no hay camino

**Algoritmo de Dijkstra implementado:**

1. **Inicialización**:
   - Todas las distancias = ∞, excepto el nodo inicial = 0
   - Cola de prioridad con el nodo inicial
   - Diccionario de "padres" para reconstruir la ruta

2. **Procesamiento**:
   - Extrae el nodo con menor distancia de la cola
   - Si alcanza el destino, termina (optimización)
   - Para cada vecino, calcula nueva distancia: `distancia_actual + peso_arista`
   - Si encuentra un camino más corto, actualiza y añade a la cola

3. **Validación de bloqueos**:
   - Verifica si (nodo_actual, vecino) está bloqueado
   - También verifica (vecino, nodo_actual) por simetría del grafo

**Complejidad Temporal**: O((V + E) log V) usando heap
- V = número de vértices (nodos)
- E = número de aristas (conexiones)

#### `_reconstruir_ruta(self, padres, inicio, fin, distancia_total)` [Privado]
- **Función**: Reconstruye el camino completo retrocediendo desde fin hasta inicio
- **Lógica**:
  ```
  Fin → padres[fin] → padres[padres[fin]] → ... → Inicio
  ```
- **Retorna**: Lista ordenada de nodos [inicio, intermedio1, ..., fin]

---

### 2️⃣ **app.py** - Interfaz Interactiva

**Propósito**: Crear la interfaz web usando Streamlit con visualización dinámica del grafo.

#### Inicialización de Streamlit
```python
st.set_page_config(page_title="RUA - Rutas Universitarias de Auxilio", layout="wide")
```
- Configura el título de la pestaña y layout en modo ancho

#### Definición de Campus
```python
nodos = [
    "Portería Principal", "Plaza Central", "Bloque Sistemas",
    "Biblioteca", "Canchas", "Cafetería", "Edificio Administrativo"
]

aristas_base = [
    ("Portería Principal", "Plaza Central", 5),      # 5 minutos
    ("Plaza Central", "Biblioteca", 3),               # 3 minutos
    # ... más conexiones
]
```
- Define 7 ubicaciones clave del campus
- Cada arista incluye el tiempo estimado de trayecto en minutos

#### Caché de Recursos
```python
@st.cache_resource
def inicializar_motor():
    return MotorRUA(nodos, aristas_base)
```
- Inicializa el motor una sola vez
- Streamlit lo mantiene en memoria para evitar recalcular en cada interacción

#### Panel Lateral de Control
```python
origen = st.sidebar.selectbox("Punto de Origen (Ingreso):", nodos, index=0)
destino = st.sidebar.selectbox("Punto de Destino (Incidente):", nodos, index=2)
```
- Selector dropdown para elegir punto de partida y llegada
- `index=0` y `index=2` establecen valores por defecto

#### Gestión de Bloqueos
```python
bloqueos_seleccionados = st.sidebar.multiselect(
    "Seleccione tramos obstruidos o peligrosos:",
    opciones_aristas
)

for seleccion in bloqueos_seleccionados:
    u, v = seleccion.split(" - ")
    aristas_bloqueadas.append((u, v))
```
- Permite seleccionar múltiples tramos a bloquear
- Convierte la selección de texto a tuplas para el motor

#### Cálculo de Ruta
```python
ruta_optima, tiempo_total = motor.calcular_ruta_segura(
    origen, destino, aristas_bloqueadas
)
```
- Invoca el motor con los parámetros actuales
- Se recalcula cada vez que el usuario cambia origen, destino o bloqueos

#### Visualización en Dos Columnas

**Columna 1: Resultados** (25% del ancho)
```python
st.success(f"**Tiempo estimado:** {tiempo_total} minutos")
for i, paso in enumerate(ruta_optima):
    if i == 0:
        st.markdown(f"🟢 **{paso}** (Inicio)")
    elif i == len(ruta_optima) - 1:
        st.markdown(f"🏁 **{paso}** (Destino)")
    else:
        st.markdown(f"⬇️ {paso}")
```
- Muestra tiempo total de trayecto
- Lista cada paso de la ruta con iconos visuales

**Columna 2: Mapa Dinámico** (75% del ancho)

**Construcción del grafo para visualización:**
```python
G = nx.Graph()
G.add_nodes_from(nodos)
for u, v, w in aristas_base:
    G.add_edge(u, v, weight=w)
```

**Cálculo de posiciones:**
```python
pos = nx.spring_layout(G, seed=42)
```
- Usa spring_layout para posicionar nodos de forma equilibrada
- `seed=42` garantiza que el layout sea consistente en cada ejecución

**Identificación de aristas por tipo:**
```python
# Aristas de la ruta óptima
edges_ruta = [(ruta_optima[i], ruta_optima[i+1]) for i in range(len(ruta_optima)-1)]

# Aristas bloqueadas (verifica ambas direcciones)
edges_bloqueadas_procesadas = []
for u, v in aristas_bloqueadas:
    if (u, v) in G.edges(): edges_bloqueadas_procesadas.append((u, v))
    elif (v, u) in G.edges(): edges_bloqueadas_procesadas.append((v, u))

# Aristas normales (las restantes)
edges_normales = [e for e in G.edges() 
                  if e not in edges_ruta and e not in edges_bloqueadas_procesadas]
```

**Renderizado con colores diferenciados:**
```python
# Nodos base (gris oscuro)
nx.draw_networkx_nodes(G, pos, node_color='#1f2937', node_size=2500)

# Origen (verde) y Destino (rojo)
nx.draw_networkx_nodes(G, pos, nodelist=[origen], node_color='#10b981', node_size=3000)
nx.draw_networkx_nodes(G, pos, nodelist=[destino], node_color='#ef4444', node_size=3000)

# Aristas normales (gris)
nx.draw_networkx_edges(G, pos, edgelist=edges_normales, edge_color='#4b5563', width=2)

# Aristas bloqueadas (rojo punteado)
nx.draw_networkx_edges(G, pos, edgelist=edges_bloqueadas_procesadas, 
                       edge_color='#ef4444', style='dashed', width=3)

# Ruta óptima (azul grueso)
nx.draw_networkx_edges(G, pos, edgelist=edges_ruta, edge_color='#3b82f6', width=5)
```

**Etiquetas:**
```python
nx.draw_networkx_labels(G, pos, font_color='white', font_size=9)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
```
- Muestra nombres de ubicaciones en cada nodo
- Muestra tiempos (pesos) en cada arista

---

### 3️⃣ **requirements.txt** - Dependencias

**Dependencias principales:**

| Librería | Uso |
|---|---|
| `streamlit` | Framework web interactivo |
| `networkx` | Manejo de grafos |
| `matplotlib` | Visualización de gráficos |
| `numpy` | Cálculos numéricos |
| `pandas` | Manipulación de datos (dependencia de Streamlit) |

**Instalación**: `pip install -r requirements.txt`

---

## ⚙️ Instalación y Configuración

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/Jon-TryHard/RUA.git
cd RUA
```

### Paso 2: Crear entorno virtual (Recomendado)
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar la aplicación
```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

---

## 💻 Uso

### Interfaz Principal

1. **Selecciona punto de origen**: Dropdown en el panel lateral izquierdo
2. **Selecciona punto de destino**: Segunda opción en el panel
3. **Bloquea tramos (opcional)**: Marca los tramos obstruidos/peligrosos
4. **Visualiza resultados**:
   - Tiempo total en minutos
   - Lista de pasos a seguir
   - Mapa del campus con la ruta resaltada

### Ejemplo de Flujo

**Escenario**: Hay una emergencia en la Biblioteca y el equipo de respuesta está en la Portería Principal

1. **Origen**: Portería Principal
2. **Destino**: Biblioteca
3. **Bloqueos**: "Bloque Sistemas - Cafetería" (zona peligrosa)
4. **Resultado**: 
   - Ruta: Portería Principal → Plaza Central → Biblioteca
   - Tiempo: 8 minutos

---

## 🔬 Algoritmo de Dijkstra - Explicación Técnica

### ¿Por qué Dijkstra?

- ✅ Encuentra el camino más corto garantizado
- ✅ Eficiente con grafos ponderados (tiempos)
- ✅ Complejidad manejable para grafos medianos
- ✅ Ideal para aplicaciones de logística y emergencias

### Pasos del Algoritmo

1. **Inicialización**: Distancia a todos = ∞, excepto inicio = 0
2. **Selección**: Escoge nodo no visitado con menor distancia
3. **Relajación**: Para cada vecino, si `distancia_actual + peso < distancia_vecino`, actualiza
4. **Repetición**: Hasta visitar todos los nodos o alcanzar el destino
5. **Reconstrucción**: Retrocede usando el diccionario de padres

### Ejemplo Numérico

```
Grafo:
  A --5-- B --3-- C
  |              /
  4            2
  |           /
  D ---------

Dijkstra de A a C:
Iteración 1: dist[A]=0, cola=[(0,A)]
Iteración 2: Procesa A, dist[B]=5, dist[D]=4, cola=[(4,D),(5,B)]
Iteración 3: Procesa D, cola=[(5,B)]
Iteración 4: Procesa B, dist[C]=8, cola=[]
Resultado: A → B → C = 8 minutos
```

---

## 🎨 Personalización

### Cambiar Campus
Edita los nodos y aristas en `app.py`:

```python
nodos = [
    "Tu Ubicación 1", "Tu Ubicación 2", ...
]

aristas_base = [
    ("Tu Ubicación 1", "Tu Ubicación 2", 10),  # 10 minutos
    ...
]
```

### Cambiar Colores
Modifica los valores HEX en `app.py`:
```python
# Origen
nx.draw_networkx_nodes(..., node_color='#10b981', ...)  # Verde

# Destino
nx.draw_networkx_nodes(..., node_color='#ef4444', ...)  # Rojo

# Ruta
nx.draw_networkx_edges(..., edge_color='#3b82f6', ...)  # Azul
```

---

## 📊 Complejidad Computacional

| Operación | Complejidad |
|---|---|
| Construcción del grafo | O(E) |
| Algoritmo Dijkstra | O((V + E) log V) |
| Reconstrucción de ruta | O(V) |
| **Total** | **O((V + E) log V)** |

**Para el campus de ejemplo** (7 nodos, 9 aristas):
- Tiempo de cálculo: < 1ms
- Ideal para interacciones en tiempo real

---

## 🐛 Troubleshooting

### "Streamlit no se reconoce"
```bash
python -m streamlit run app.py
```

### "No existe ruta disponible"
- Todos los caminos están bloqueados
- Desbloquea algunos tramos o cambia origen/destino

### "El mapa se ve cortado"
- La interfaz requiere navegador en modo pantalla completa
- O amplia la ventana del navegador

---

## 📝 Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para detalles.

---

## 👨‍💻 Autor

**Jon-TryHard**

---

## 🚀 Casos de Uso

- 🚨 **Sistemas de Emergencia**: Rutas de evacuación y respuesta
- 🏥 **Hospitales**: Transporte de pacientes optimizado
- 🏢 **Campus Universitarios**: Logística interna
- 🏭 **Complejos Industriales**: Rutas de inspección
- 🗺️ **Cualquier grafo ponderado**: Problemas de optimización de rutas

---

## ✨ Mejoras Futuras

- [ ] Guardar configuraciones de rutas favoritas
- [ ] Exportar rutas a PDF
- [ ] Integrar datos en tiempo real de GPS
- [ ] Algoritmo A* para mejor optimización
- [ ] Base de datos para múltiples campus
- [ ] API REST para integración externa

---

**Última actualización**: Enero 2026  
**Versión**: 1.0.0
