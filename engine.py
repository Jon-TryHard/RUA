import heapq

class MotorRUA:
    """
    Motor lógico central para Rutas Universitarias de Auxilio.
    Gestiona la estructura de grafo y calcula rutas óptimas mediante Dijkstra.
    """
    def __init__(self, nodos, aristas_base):
        self.nodos = nodos
        self.aristas_base = aristas_base
        self.grafo = self._construir_grafo()

    def _construir_grafo(self):
        """
        Construye una representación de diccionario de adyacencia del grafo no dirigido.
        Cada nodo mapea a sus vecinos con sus pesos asociados.
        """
        grafo = {n: {} for n in self.nodos}
        for u, v, peso in self.aristas_base:
            grafo[u][v] = peso
            grafo[v][u] = peso
        return grafo

    def calcular_ruta_segura(self, inicio, fin, bloqueos=None):
        """
        Calcula la ruta más corta usando el algoritmo de Dijkstra.
        Evita dinámicamente los tramos bloqueados.
        Complejidad temporal: O((V + E) log V) donde V es número de nodos y E de aristas.
        """
        if bloqueos is None:
            bloqueos = []

        # Inicializa distancias infinitas, excepto el nodo inicio
        distancias = {n: float('inf') for n in self.nodos}
        distancias[inicio] = 0
        padres = {n: None for n in self.nodos}
        pq = [(0, inicio)]

        while pq:
            dist_actual, nodo_actual = heapq.heappop(pq)

            # Optimización: detiene al alcanzar el destino
            if nodo_actual == fin:
                break

            # Salta si encontramos una ruta más corta desde otra rama
            if dist_actual > distancias[nodo_actual]:
                continue

            # Expande vecinos del nodo actual
            for vecino, peso in self.grafo[nodo_actual].items():
                # Valida que la arista no esté bloqueada (considera ambas direcciones)
                if (nodo_actual, vecino) in bloqueos or (vecino, nodo_actual) in bloqueos:
                    continue

                nueva_distancia = dist_actual + peso

                # Actualiza distancia si encontramos un camino más corto
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    padres[vecino] = nodo_actual
                    heapq.heappush(pq, (nueva_distancia, vecino))

        return self._reconstruir_ruta(padres, inicio, fin, distancias[fin])

    def _reconstruir_ruta(self, padres, inicio, fin, distancia_total):
        """
        Reconstruye la ruta completa desde el nodo inicio hasta el fin usando el diccionario de padres.
        Retorna (ruta, distancia_total) o (None, inf) si no hay camino disponible.
        """
        if distancia_total == float('inf') and inicio != fin:
            return None, float('inf')

        # Retrocede desde el fin hasta el inicio mediante padres
        ruta = []
        actual = fin
        while actual is not None:
            ruta.insert(0, actual)
            actual = padres[actual]

        return ruta, distancia_total


# =====================================================================
# DATASET EXPANDIDO: 16 NODOS DE LA UNIVERSIDAD TECNOLÓGICA DE PEREIRA
# =====================================================================

NODOS_UTP = [
    # Nodos originales del documento base
    "Entrada_La_Julita", "Biblioteca_JRM", "Bloque_1_Sistemas", "Bloque_15_Educacion",
    # Primer bloque de expansión (8 nodos)
    "El_Galpon", "Bloque_13_Ciencias_Basicas", "Bloque_14_Mecanica", "Bloque_L_Medicina",
    "Bloque_Y_Bellas_Artes", "Canchas_Multiples", "Planetario", "Jardin_Botanico",
    # ¡4 NUEVOS NODOS AÑADIDOS AHORA!
    "Entrada_Alamos", "Bloque_A_Administrativo", "Bloque_11_Industrial", "Bloque_17_Postgrados"
]

ARISTAS_UTP = [
    # Conexiones principales originales
    ("Entrada_La_Julita", "Biblioteca_JRM", 150),
    ("Entrada_La_Julita", "Bloque_1_Sistemas", 200),
    ("Biblioteca_JRM", "Bloque_15_Educacion", 120),
    
    # Interconexiones de la primera expansión
    ("Biblioteca_JRM", "El_Galpon", 80),
    ("El_Galpon", "Canchas_Multiples", 110),
    ("El_Galpon", "Bloque_13_Ciencias_Basicas", 70),
    ("Bloque_1_Sistemas", "Bloque_13_Ciencias_Basicas", 90),
    ("Bloque_13_Ciencias_Basicas", "Bloque_14_Mecanica", 50),
    ("Bloque_14_Mecanica", "Planetario", 140),
    ("Planetario", "Bloque_L_Medicina", 190),
    ("Bloque_L_Medicina", "Jardin_Botanico", 160),
    ("Jardin_Botanico", "Entrada_La_Julita", 320),
    ("Bloque_15_Educacion", "Bloque_Y_Bellas_Artes", 260),
    ("Bloque_Y_Bellas_Artes", "Canchas_Multiples", 170),
    
    # NUEVAS CONEXIONES MÁSTRÁNSITO (Para los 4 nuevos nodos)
    ("Entrada_Alamos", "Bloque_L_Medicina", 110),         # Acceso directo desde Álamos a Medicina
    ("Entrada_Alamos", "Bloque_A_Administrativo", 130),   # Subida hacia la zona administrativa
    ("Bloque_A_Administrativo", "Biblioteca_JRM", 95),     # Conexión central de Rectoría a la Biblioteca
    ("Bloque_1_Sistemas", "Bloque_11_Industrial", 65),     # Cercanía física entre el Bloque 1 y el Bloque 11
    ("Bloque_11_Industrial", "Bloque_14_Mecanica", 55),    # Conexión interna del sector de ingenierías
    ("Bloque_17_Postgrados", "Bloque_15_Educacion", 85),   # Proximidad con la facultad de Educación
    ("Bloque_17_Postgrados", "Bloque_13_Ciencias_Basicas", 105) # Sendero hacia Ciencias Básicas
]
