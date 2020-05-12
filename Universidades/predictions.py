import json
with open("predictions.json") as data:
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




