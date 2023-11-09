####### ON UTILISE NETWORKX 
# LE RESTE EST JUSTE UN EXEMPLE DE L'UTILISATION DE NX

# Allez voir ça !! 
# https://networkx.org/documentation/stable/tutorial.html
# https://networkx.org/documentation/stable/reference/algorithms/index.html

# imports 
import networkx as nx

# On crée un graphe 
G = nx.Graph()
DirectedG = nx.DiGraph()
MultipleEdgesG = nx.MultiGraph()

# On ajoute des noeuds, avec des attributs si besoin
for i in range(10):
    G.add_nodes_from(
        [
            (
                i,
                {"color":['green', 'red', 'blue'][i%3]}
            ),
            (
                i+100,
                {"color":['green', 'red', 'blue'][i%3]}
            ),
        ]
    )

# On ajoute des edges, avec des attributs aussi 
from random import choice, random

for _ in range(12):
    
    G.add_edges_from(
        [
            (
                choice(list(G._node)),
                choice(list(G._node)),
                {"weight" : random()}
            )
        ]
    )

# --- On peut trouver la data comme ceci

#  Renvoie None si pas d'Edge
G.get_edge_data(u=1, v=2)

# Renvoie tous les noeuds avec leurs attributs (dictionnaire)
G._node

# Renvoie un noeud en particulier (pour _node, clé = le noeud, valeur = attributs)
G._node[102]

# Calcule les noeuds adjacents d'un noeud (avec les attributs des edges)
# adj a pour clés les noeuds, valeurs des dictionnaires avec clés noeuds et 
#   et valeurs = attributs des edges
G.adj[102]
G[102] # Syntaxe différente

# --- On peut plot le graph aussi 
import matplotlib.pyplot as plt

subax1 = plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
subax1 = plt.subplot(122)
nx.draw_shell(G, with_labels=True, font_weight='bold')

plt.show()