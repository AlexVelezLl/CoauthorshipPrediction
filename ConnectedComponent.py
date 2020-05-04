def getCompGrande(dic):
    compgrande = ""
    num = 0
    for key, value in dic.items():
        if value>num:
            num = value
            compgrande=key

    return compgrande

with open("edgesComponentsID.csv",encoding='utf-8') as f:
    nodesPerConectedComponents = {}
    f.readline()
    lines = f.readlines()
    for line in lines:
        line = line.strip().split('\",')
        component = line[-1][1:]
        if component not in nodesPerConectedComponents.keys():
            nodesPerConectedComponents[component] = 0
        nodesPerConectedComponents[component] +=1
    gr = getCompGrande(nodesPerConectedComponents)
    authors = set()
    for line in lines:
        line = line.strip().split('\",')
        component = line[-1][1:]
        if component==gr:
            authors.add(line[0][1:])

    g = open("coauthors-edgesGephi.csv",encoding="utf-8")
    h = open("coauthorsCC-edges.csv","w",encoding='utf-8')

    h.write("Source;Target;Weight\n")

    for line in g:
        print(line)
        line2 = line.strip().split(";")
        if line2[0] in authors:
            h.write(line)

    g.close()
    h.close()
    j = open("coauthorsCC-nodes.csv", "w", encoding='utf-8')
    j.write("ID;Label\n")
    for author in authors:
        j.write(author + ";" + author + "\n")
    j.close()
