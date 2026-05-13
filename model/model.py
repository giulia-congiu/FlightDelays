import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self._airports = DAO.getAllAirports() #tutti gli areoporti de database
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a

    def buildGraph(self, nMin):
        nodes= DAO.getAllNodes(nMin, self._idMapAirports)
        self.graph.add_nodes_from(nodes)
        self.addEdges1()
        print(f"N nodi: {len(self.graph.nodes)}, n archi {len(self.graph.edges)}")
        self.addEdges2()
        print(f"N nodi: {len(self.graph.nodes)}, n archi {len(self.graph.edges)}")

    def getGraphDetails(self):
        return len(self.graph.nodes), len(self.graph.edges)

    def addEdges1(self):
        allTratte = DAO.getAllEdges1(self._idMapAirports)
        #problema 1 = ho archi diretti e inversi quindi devo fare la somma a mano
        #problema 2 = ho archi fra aereoporti che avevo filtrato
        for t in allTratte:
            if t.areoportoP in self.graph and t.areoportoA in self.graph:
                #allora posso aggiungerlo
                if self.graph.has_edge(t.areoportoP, t.areoportoA):
                    #se esiste già incrementane semplicemente il peso
                    self.graph[t.areoportoP][t.areoportoA]['weight'] += t.pesp
            else:
                self.graph.add_edge(t.areoportoP, t.areoportoA, weight = t.peso)

    def addEdges2(self):
        allTratte = DAO.getAllEdges2(self._idMapAirports)
        for t in allTratte:
            if t.areoportoP in self.graph and t.areoportoA in self.graph:
                self.graph.add_edge(t.areoportoP, t.areoportoA, weight=t.peso)

