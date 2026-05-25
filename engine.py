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
