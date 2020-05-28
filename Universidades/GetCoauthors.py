import pandas as pd
import networkx as nx
import os

def devolverArchivos(carpeta):
    lista_archivos = []
    universidades = []

    for archivo in os.listdir(carpeta):
        nom = "Publicaciones con Abstract"
        if nom in os.path.join(carpeta,archivo):
            lista_archivos.append(os.path.join(carpeta,archivo))
            universidades.append(archivo[len(nom)+1:-5])
    return (lista_archivos,universidades)

def indexCS(data):
    indices = []
    topic = data["Topic"]
    for i,t in enumerate(topic):
        if "Computer Science" in t:
            indices.append(i)
    return indices

def public2015_2019(data):
    cont = 0
    for p in data["Year"]:
        if p>=2015 and p<=2019:
            cont+=1
    return cont

def formating(author):
    author = author.strip()
    if not (author.endswith(".")):
        author = author+"."
    return author

def connected_component_subgraphs(G):
    for c in nx.connected_components(G):
        yield G.subgraph(c)

archivos, universidades = devolverArchivos("publicaciones")
"""univ = "Universidad de Antioquia"
archivo_edges = "data/componente_gigante/coauthors-edgesCG-"+univ+".csv"
archivo_nodes = "data/componente_gigante/coauthors-nodesCG-"+univ+".csv"
#coau_df = pd.read_csv(archivo_edges,delimiter=";")
#nodos_df = pd.read_csv(archivo_nodes,delimiter=";")
with open(archivo_nodes,encoding='utf-8') as f:
    for line in f:
        line2 = line.split(";")
        if len(line2)==5:
            print(line)"""
publicaciones = 0
pub2015_2019 = 0
n_auth2015_2019=0
totAuth = 0
totArist= 0
totNodesCG=0
totEdgesCG=0
for univ, archivo in zip(universidades,archivos):
    data = pd.read_excel(archivo)
    indices = indexCS(data)
    publicaciones += len(indices)
    data = data.loc[indices]
    data.reset_index(inplace=True)
    pub2015_2019+=public2015_2019(data)
    coauthors = []
    auth2015_2019 = set()
    for author in data['Authors']:
        author = str(author)
        if ";" in author:
            coauthors.append(author.split(";"))
        else:
            coauthors.append(author.split(".,"))

    dic = {}
    dicTot = {}
    authors = {}
    for i, publ in enumerate(coauthors):

        keywords = str(data['Keywords'][i]).split(",")
        year = data['Year'][i]

        for offset, author1 in enumerate(publ):
            author1 = formating(author1)
            if author1 not in authors.keys():
                authors[author1] = {'Before':set(),'After':set()}
            if year>=2015 and year<=2017:
                for keyword in keywords:
                    keyword = keyword.strip()
                    if (keyword != 'nan'):
                        authors[author1]['Before'].add(keyword)
            elif year==2018 or year ==2019:
                for keyword in keywords:
                    keyword = keyword.strip()
                    if (keyword != 'nan'):
                        authors[author1]['After'].add(keyword)
            offset += 1
            author1 = formating(author1)
            for author2 in publ[offset:]:
                author2 = formating(author2)

                key = author1 + ";" + author2
                altkey = author2 + ";" + author1
                if key in dicTot.keys():
                    dicTot[key]['n'] += 1

                    if year < dicTot[key]['firstColab']:
                        dicTot[key]['firstColab'] = year
                elif altkey in dicTot.keys():
                    dicTot[altkey]['n'] += 1
                    if year < dicTot[altkey]['firstColab']:
                        dicTot[altkey]['firstColab'] = year
                else:
                    dicTot[key] = {"n": 1, "firstColab": year}

                if year >= 2015 and year <= 2019:
                    auth2015_2019.add(author1)
                    auth2015_2019.add(author2)
                    if key in dic.keys():
                        dic[key]['n'] += 1

                        if year < dic[key]['firstColab']:
                            dic[key]['firstColab'] = year
                    elif altkey in dic.keys():
                        dic[altkey]['n'] += 1
                        if year < dic[altkey]['firstColab']:
                            dic[altkey]['firstColab'] = year
                    else:
                        dic[key] = {"n": 1, "firstColab": year}

    with open("data/grafo_completo/coauthors-edges-"+univ+".csv", "w", encoding="utf-8") as f:
        f.write("Source;Target;Weight;Year\n")
        for key, value in dic.items():
            ath = key.split(";")
            f.write(ath[0] + ";" + ath[1] + ";" + str(value['n']) + ";" + str(int(value['firstColab'])) + "\n")

    with open("data/grafo_completo/coauthors-nodes-"+univ+".csv", "w", encoding="utf-8") as g:
        g.write("ID;Label;KeywordsB2018;KeywordsA2018\n")
        for auth, keywords in authors.items():
            g.write(auth + ";" + auth + ";" + (",".join(keywords['Before'])).replace(";","") +";"+(",".join(keywords['After'])).replace(";","")+ "\n")


    coau_df = pd.read_csv("data/grafo_completo/coauthors-edges-"+univ+".csv", delimiter=";")

    G = nx.from_pandas_edgelist(coau_df, "Source", "Target", ['Weight', 'Year'], create_using=nx.Graph())
    G = sorted(connected_component_subgraphs(G), key=len, reverse=True)[0]
    nodosCG = list(G.nodes)
    totNodesCG+=len(nodosCG)
    totEdgesCG+=len(dic.keys())
    with open("data/componente_gigante/coauthors-edgesCG-"+univ+".csv", "w", encoding="utf-8") as f:
        f.write("Source;Target;Weight;Year\n")
        for key, value in dic.items():
            ath = key.split(";")
            if ath[0] in nodosCG:
                f.write(ath[0] + ";" + ath[1] + ";" + str(value['n']) + ";" + str(int(value['firstColab'])) + "\n")

    with open("data/componente_gigante/coauthors-nodesCG-"+univ+".csv", "w", encoding="utf-8") as g:
        g.write("ID;Label;KeywordsB2018;KeywordsA2018\n")
        for auth, keywords in authors.items():
            if auth in nodosCG:
                g.write(auth + ";" + auth + ";" + (",".join(keywords['Before'])).replace(";","") +";"+(",".join(keywords['After'])).replace(";","")+ "\n")
    totAuth += len(authors.keys())
    totArist += len(dicTot.keys())
    n_auth2015_2019 += len(auth2015_2019)

print(totNodesCG)
print(totEdgesCG)