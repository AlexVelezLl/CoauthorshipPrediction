import os
import pandas as pd
import networkx as nx

def devolverArchivos(carpeta):
    lista_archivos = []
    universidades = []

    for archivo in os.listdir(carpeta):
        nom = "coauthors-edgesCG-"
        if nom in os.path.join(carpeta,archivo):
            lista_archivos.append(os.path.join(carpeta,archivo))
            universidades.append(archivo[len(nom):-4])
    return (lista_archivos,universidades)

archivos, universidades = devolverArchivos("data/componente_gigante")

with open("infoGrafo.csv","w",encoding="utf-8") as f:
    f.write("Universidad;Nodos;Edges\n")
    for univ, archivo in zip(universidades,archivos):
        data = pd.read_csv(archivo,delimiter=";")
        G = nx.from_pandas_edgelist(data,"Source","Target",['Weight','Year'],create_using=nx.Graph())
        f.write(univ+";"+str(len(G.nodes))+";"+str(len(G.edges))+"\n")
