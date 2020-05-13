import json
import pandas as pd
import numpy as np
"""with open("predictions.json") as data:
    with open("predictions.csv","w") as f:
        f.write("Metricas;Accuracy;Precision;Recall;Roc_auc;model;Universidad\n")
        universidades = json.load(data)
        for univ,featureDic in universidades.items():
            for feature,modelsDic in featureDic.items():
                for model, predDic in modelsDic.items():
                    f.write(feature+";"+
                            str(predDic["accuracy"])+";"+
                            str(predDic["precision"])+";"+
                            str(predDic["recall"])+";"+
                            str(predDic["roc_auc"])+";"+
                            model+";"+
                            univ+"\n")
    
"""


df = pd.read_csv("predictions.csv",delimiter = ";")
universidades = np.unique(df["Universidad"])
metricas = np.unique(df["Metricas"])
modelos = ["Bagging","SVC"]
for metrica in metricas:
    for modelo in modelos:
        with open("tablas/"+modelo+"_"+metrica+".csv","w") as f:
            f.write("Universidad;Accuracy;Precision;Reacall;Roc_auc\n")
            for universidad in universidades:
                dataU = df[(df["Metricas"]==metrica) &  (df["model"]==modelo) & (df["Universidad"]==universidad)]
                dataU.reset_index(inplace=True)
                acc = str(dataU["Accuracy"][0])
                pre = str(dataU["Precision"][0])
                rec = str(dataU["Recall"][0])
                roc = str(dataU["Roc_auc"][0])
                f.write(
                    universidad+";"+
                    acc+";"+
                    pre+";"+
                    rec+";"+
                    roc+"\n"
                )



