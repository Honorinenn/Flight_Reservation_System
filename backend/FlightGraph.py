
import networkx as nx
 
class FlightGraph:

    def __init__(self):

        self.flightGraph = nx.DiGraph()
 
    # ... other methods (unchanged)
 
    def Dijkstra(self, source, destination):

        # Convert NetworkX graph to adjacency list format

        adjacency_list = {node: [(neighbor, data['weight']) for neighbor, data in G[node].items()] for node in G.nodes()}
 
        pq = []

        dist = {node: float('inf') for node in adjacency_list}

        vis = set()

        parent = {}

        path = {}
 
        dist[source] = 0

        heapq.heappush(pq, (0, source))
 
        while pq:

            currw, currv = heapq.heappop(pq)

            if currv in vis:

                continue

            vis.add(currv)
 
            for nextw, nextv in adjacency_list[currv]:

                if nextv not in vis:

                    newWeight = currw + nextw

                    if newWeight < dist[nextv]:

                        dist[nextv] = newWeight

                        parent[nextv] = currv

                        path[nextv] = nextv  # Store the flight information

                        heapq.heappush(pq, (newWeight, nextv))
 
        pathTaken = []

        if dist[destination] == float('inf'):

            return pathTaken
 
        i = destination

        while i != source:

            pathTaken.append(i)

            i = parent[i]

        pathTaken.reverse()

        return pathTaken
 
    def buildGraph(self):

        for flight in self.flight:

            originIndex = self.flightMap[flight.OCity]

            destinationIndex = self.flightMap[flight.Dcity]

            probability = random.uniform(0, 1)  # Example: Random probability of delay

            self.flightGraph.add_edge(originIndex, destinationIndex, weight=flight.distance, flight=flight.flightnumer, probability=probability)
 