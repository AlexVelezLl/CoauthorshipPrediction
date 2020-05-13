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
        with open("tablas/"+metrica+".csv","w") as f:
            f.write("Universidad;Accuracy-Bagging;Accuracy-SVM;Precision-Bagging;Precision-SVM;Recall-Bagging;Recall-SVM;Roc_auc-Bagging;Roc_auc-SVM\n")
            for universidad in universidades:
                dataUBag = df[(df["Metricas"]==metrica) & (df["model"]=="Bagging") & (df["Universidad"]==universidad)]
                dataUSVM = df[(df["Metricas"]==metrica) & (df["model"]=="SVC") & (df["Universidad"]==universidad)]
                dataUBag.reset_index(inplace=True)
                dataUSVM.reset_index(inplace=True)

                accBag = str(dataUBag["Accuracy"][0])
                accSVM = str(dataUSVM["Accuracy"][0])

                preBag = str(dataUBag["Precision"][0])
                preSVM = str(dataUSVM["Precision"][0])

                recBag = str(dataUBag["Recall"][0])
                recSVM = str(dataUSVM["Recall"][0])

                rocBag = str(dataUBag["Roc_auc"][0])
                rocSVM = str(dataUSVM["Roc_auc"][0])

                f.write(
                    universidad+";"+
                    accBag+";"+accSVM+";"+
                    preBag+";"+preSVM+";"+
                    recBag+";"+recSVM+";"+
                    rocBag+";"+rocSVM+"\n"
                )



