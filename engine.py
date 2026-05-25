import heapq

class MotorRUA:
    """
    Motor lógico para Rutas Universitarias de Auxilio.
    Maneja la estructura de datos del grafo y el cálculo de rutas óptimas.
    """
    def __init__(self, nodos, aristas_base):
        self.nodos = nodos
        self.aristas_base = aristas_base
        self.grafo = self._construir_grafo()

    def _construir_grafo(self):
        """
        Construye el diccionario de adyacencia para un grafo no dirigido.
        """
        grafo = {n: {} for n in self.nodos}
        for u, v, peso in self.aristas_base:
            grafo[u][v] = peso
            grafo[v][u] = peso
        return grafo

    def calcular_ruta_segura(self, inicio, fin, bloqueos=None):
        """
        Calcula la ruta más corta usando Dijkstra, evadiendo los bloques dinámicos.
        Complejidad: O((V + E) log V)
        """
        if bloqueos is None:
            bloqueos = []

        distancias = {n: float('inf') for n in self.nodos}
        distancias[inicio] = 0
        padres = {n: None for n in self.nodos}
        pq = [(0, inicio)]

        while pq:
            dist_actual, nodo_actual = heapq.heappop(pq)

            # Early exit: Alcanzamos el destino óptimo
            if nodo_actual == fin:
                break

            if dist_actual > distancias[nodo_actual]:
                continue

            for vecino, peso in self.grafo[nodo_actual].items():
                # Validación de bloqueo dinámico (arista en ambos sentidos)
                if (nodo_actual, vecino) in bloqueos or (vecino, nodo_actual) in bloqueos:
                    continue

                nueva_distancia = dist_actual + peso

                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    padres[vecino] = nodo_actual
                    heapq.heappush(pq, (nueva_distancia, vecino))

        return self._reconstruir_ruta(padres, inicio, fin, distancias[fin])

    def _reconstruir_ruta(self, padres, inicio, fin, distancia_total):
        """
        Reconstruye el camino recorrido desde el nodo final usando el diccionario de padres.
        """
        if distancia_total == float('inf') and inicio != fin:
            return None, float('inf')

        ruta = []
        actual = fin
        while actual is not None:
            ruta.insert(0, actual)
            actual = padres[actual]

        return ruta, distancia_total
