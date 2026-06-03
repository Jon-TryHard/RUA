import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
# Importamos el motor y el dataset real de la UTP desde engine.py
from engine import MotorRUA, NODOS_UTP, ARISTAS_UTP

# Configuración inicial de la página: título en pestaña del navegador y layout ancho
st.set_page_config(page_title="RUA - Rutas Universitarias de Auxilio", layout="wide")

st.title("🚨 RUA - Rutas Universitarias de Auxilio")
st.markdown("Plataforma de Logística Crítica mediante Grafos Ponderados y Algoritmo de Dijkstra.")

# Enlazamos las variables locales con el dataset expandido de la UTP (16 nodos)
nodos = NODOS_UTP
aristas_base = ARISTAS_UTP

# Crea e inicializa el motor una sola vez para optimizar el rendimiento
@st.cache_resource
def inicializar_motor():
    return MotorRUA(nodos, aristas_base)

motor = inicializar_motor()

# Panel lateral: entrada de usuario para seleccionar origen, destino y bloqueos
st.sidebar.header("⚙️ Panel de Control de Emergencia")

# Ordenamos alfabéticamente para que sea más fácil de buscar en la interfaz
nodos_ordenados = sorted(nodos)
origen = st.sidebar.selectbox("Punto de Origen (Ingreso):", nodos_ordenados, index=nodos_ordenados.index("Entrada_La_Julita"))
destino = st.sidebar.selectbox("Punto de Destino (Incidente):", nodos_ordenados, index=nodos_ordenados.index("Bloque_1_Sistemas"))

st.sidebar.markdown("---")
st.sidebar.subheader("🚧 Gestión de Bloqueos")
opciones_aristas = [f"{u} - {v}" for u, v, w in aristas_base]
bloqueos_seleccionados = st.sidebar.multiselect(
    "Seleccione tramos obstruidos o peligrosos:",
    opciones_aristas
)

# Convierte las selecciones de texto en tuplas de nodos para el motor
aristas_bloqueadas = []
for seleccion in bloqueos_seleccionados:
    u, v = seleccion.split(" - ")
    aristas_bloqueadas.append((u, v))

# Calcula la ruta más corta evadiendo tramos bloqueados
ruta_optima, tiempo_total = motor.calcular_ruta_segura(origen, destino, aristas_bloqueadas)

# Divide la pantalla en dos secciones: resultados (izquierda) y mapa (derecha)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 Resultados de Ruta")
    if ruta_optima:
        st.success(f"**Distancia/Esfuerzo estimado:** {tiempo_total} metros")
        st.markdown("**Camino dinámico calculado:**")
        for i, paso in enumerate(ruta_optima):
            # Formateamos estéticamente reemplazando guiones bajos por espacios
            nombre_limpio = paso.replace("_", " ")
            if i == 0:
                st.markdown(f"🟢 **{nombre_limpio}** (Inicio)")
            elif i == len(ruta_optima) - 1:
                st.markdown(f"🏁 **{nombre_limpio}** (Destino)")
            else:
                st.markdown(f"⬇️ {nombre_limpio}")
    else:
        st.error("🚨 **ALERTA CRÍTICA:** No existe una ruta disponible hacia el destino. Todos los accesos viables se encuentran bloqueados.")

# --- RENDERIZADO DEL GRAFO (DIFERENCIACIÓN VISUAL) ---
with col2:
    st.subheader("🗺️ Mapa Dinámico del Campus (UTP)")

    # Estructura el grafo con nodos y aristas para visualización
    G = nx.Graph()
    G.add_nodes_from(nodos)
    for u, v, w in aristas_base:
        G.add_edge(u, v, weight=w)

    # Calculamos posiciones. Subimos el factor 'k' para dispersar los 16 nodos en el espacio
    pos = nx.spring_layout(G, k=0.8, seed=42)

    # Configura la figura con fondo oscuro (Ampliada a 12x8 para albergar la red de la UTP)
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')

    # Obtiene aristas que forman parte de la ruta óptima
    edges_ruta = []
    if ruta_optima:
        edges_ruta = [(ruta_optima[i], ruta_optima[i+1]) for i in range(len(ruta_optima)-1)]
        edges_ruta = [e if e in G.edges() else (e[1], e[0]) for e in edges_ruta]

    # Obtiene aristas que están bloqueadas (verifica ambas direcciones)
    edges_bloqueadas_procesadas = []
    for u, v in aristas_bloqueadas:
        if (u, v) in G.edges(): edges_bloqueadas_procesadas.append((u, v))
        elif (v, u) in G.edges(): edges_bloqueadas_procesadas.append((v, u))

    # Aristas normales: sin bloqueo y que no son parte de la ruta activa
    edges_normales = [e for e in G.edges() if e not in edges_ruta and e not in edges_bloqueadas_procesadas]

    # Dibuja nodos base del grafo
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='#1f2937', node_size=1800, edgecolors='#3b82f6', linewidths=2)

    # Resalta puntos críticos: origen en verde y destino en rojo
    nx.draw_networkx_nodes(G, pos, nodelist=[origen], ax=ax, node_color='#10b981', node_size=2200)
    nx.draw_networkx_nodes(G, pos, nodelist=[destino], ax=ax, node_color='#ef4444', node_size=2200)

    # Dibuja aristas con colores según estado: gris (normal), rojo punteado (bloqueado), azul (ruta)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=edges_normales, edge_color='#4b5563', width=2)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=edges_bloqueadas_procesadas, edge_color='#ef4444', style='dashed', width=3)
    if ruta_optima:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=edges_ruta, edge_color='#3b82f6', width=5)

    # Añade etiquetas de nodos convirtiendo los nombres internos a formato legible (sin barras bajas)
    etiquetas_legibles = {nodo: nodo.replace("_", "\n") for nodo in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=etiquetas_legibles, ax=ax, font_color='white', font_size=7, font_weight='bold')
    
    # Añade los pesos de las aristas (distancias en metros)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='#9ca3af', font_size=9, ax=ax)

    plt.axis('off')
    st.pyplot(fig)
    plt.close(fig)
