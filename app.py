import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from engine import MotorRUA

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="RUA - Rutas Universitarias de Auxilio", layout="wide")

st.title("🚨 RUA - Rutas Universitarias de Auxilio")
st.markdown("Plataforma de Logística Crítica mediante Grafos Ponderados y Algoritmo de Dijkstra.")

# --- 2. DEFINICIÓN DEL GRAFO DEL CAMPUS ---
nodos = [
    "Portería Principal", "Plaza Central", "Bloque Sistemas",
    "Biblioteca", "Canchas", "Cafetería", "Edificio Administrativo"
]

aristas_base = [
    ("Portería Principal", "Plaza Central", 5),
    ("Portería Principal", "Edificio Administrativo", 4),
    ("Plaza Central", "Biblioteca", 3),
    ("Plaza Central", "Canchas", 6),
    ("Edificio Administrativo", "Bloque Sistemas", 7),
    ("Bloque Sistemas", "Biblioteca", 4),
    ("Biblioteca", "Cafetería", 2),
    ("Canchas", "Cafetería", 5),
    ("Bloque Sistemas", "Cafetería", 8)
]

# Inicializar y cachear el motor lógico para rendimiento eficiente
@st.cache_resource
def inicializar_motor():
    return MotorRUA(nodos, aristas_base)

motor = inicializar_motor()

# --- 3. INTERFAZ INTERACTIVA (PANEL LATERAL) ---
st.sidebar.header("⚙️ Panel de Control de Emergencia")

origen = st.sidebar.selectbox("Punto de Origen (Ingreso):", nodos, index=0)
destino = st.sidebar.selectbox("Punto de Destino (Incidente):", nodos, index=2)

st.sidebar.markdown("---")
st.sidebar.subheader("🚧 Gestión de Bloqueos")
opciones_aristas = [f"{u} - {v}" for u, v, w in aristas_base]
bloqueos_seleccionados = st.sidebar.multiselect(
    "Seleccione tramos obstruidos o peligrosos:",
    opciones_aristas
)

# Parsear los bloqueos seleccionados a tuplas para el motor
aristas_bloqueadas = []
for seleccion in bloqueos_seleccionados:
    u, v = seleccion.split(" - ")
    aristas_bloqueadas.append((u, v))

# --- 4. CÁLCULO DE RUTA ---
ruta_optima, tiempo_total = motor.calcular_ruta_segura(origen, destino, aristas_bloqueadas)

# Distribución de la pantalla en columnas
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 Resultados de Ruta")
    if ruta_optima:
        st.success(f"**Tiempo estimado de respuesta:** {tiempo_total} minutos")
        st.markdown("**Camino dinámico calculado:**")
        for i, paso in enumerate(ruta_optima):
            if i == 0:
                st.markdown(f"🟢 **{paso}** (Inicio)")
            elif i == len(ruta_optima) - 1:
                st.markdown(f"🏁 **{paso}** (Destino)")
            else:
                st.markdown(f"⬇️ {paso}")
    else:
        st.error("🚨 **ALERTA CRÍTICA:** No existe una ruta disponible hacia el destino. Todos los accesos viables se encuentran bloqueados.")

# --- 5. RENDERIZADO DEL GRAFO (DIFERENCIACIÓN VISUAL) ---
with col2:
    st.subheader("🗺️ Mapa Dinámico del Campus")

    # Grafo base para visualización estática de posiciones
    G = nx.Graph()
    G.add_nodes_from(nodos)
    for u, v, w in aristas_base:
        G.add_edge(u, v, weight=w)

    # Layout con semilla fija para congelar las posiciones de los edificios
    pos = nx.spring_layout(G, seed=42)

    # Configuración del contenedor del mapa en modo oscuro
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')

    # Identificación de aristas que componen la ruta activa
    edges_ruta = []
    if ruta_optima:
        edges_ruta = [(ruta_optima[i], ruta_optima[i+1]) for i in range(len(ruta_optima)-1)]
        edges_ruta = [e if e in G.edges() else (e[1], e[0]) for e in edges_ruta]

    # Identificación de aristas bajo bloqueo
    edges_bloqueadas_procesadas = []
    for u, v in aristas_bloqueadas:
        if (u, v) in G.edges(): edges_bloqueadas_procesadas.append((u, v))
        elif (v, u) in G.edges(): edges_bloqueadas_procesadas.append((v, u))

    # El resto son aristas operativas estándar
    edges_normales = [e for e in G.edges() if e not in edges_ruta and e not in edges_bloqueadas_procesadas]

    # Render de Nodos Base
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='#1f2937', node_size=2500, edgecolors='#3b82f6', linewidths=2)

    # Resaltado de puntos críticos operativos
    nx.draw_networkx_nodes(G, pos, nodelist=[origen], ax=ax, node_color='#10b981', node_size=3000)
    nx.draw_networkx_nodes(G, pos, nodelist=[destino], ax=ax, node_color='#ef4444', node_size=3000)

    # Render de Aristas por Categorías (Normal, Bloqueo, Ruta Óptima)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=edges_normales, edge_color='#4b5563', width=2)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=edges_bloqueadas_procesadas, edge_color='#ef4444', style='dashed', width=3)
    if ruta_optima:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=edges_ruta, edge_color='#3b82f6', width=5)

    # Etiquetas de texto y pesos del mapa
    nx.draw_networkx_labels(G, pos, ax=ax, font_color='white', font_size=9, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='#9ca3af', font_size=10, ax=ax)

    plt.axis('off')
    st.pyplot(fig)
    plt.close(fig) # Limpieza de memoria para prevenir advertencias en la terminal
