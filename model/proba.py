import json
import pickle

import os

import streamlit as st
import pandas as pd

class ProbaModel:
    def __init__(self, source = "model/base", 
                #  model_name = "XGBClassifier",
                 model_name = "RandomForestClassifier",
                 fs = "before fs",
                 phases = ["before", "during"],
                 labels = ["got", "employed"],
                 n_trim = 6,
                 start_trim = 1):
        
        self.source = source
        self.labels = labels
        self.fs = fs
        self.phases = phases

        self.features = {phase: json.load(open(f"{source}/{phase}_cols.json")) for phase in phases}

        self.encoder = {"_".join(file.split("_")[:-1]): self._load_obj(file, file_f = False) for file in os.listdir(source) if "encoder" in file}
    
        self.model = {}
        self.scaler = {}
        
        for label in labels:
            if "before" in phases:
                before_idx = phases.index("before")
                self.model[label] = {phases[before_idx]: self._load_obj(f"{phases[before_idx]}_{label}_{model_name}")}
                self.scaler[label] = {phases[before_idx]: self._load_obj(f"{label}_{phases[before_idx]}_resampled_scaler")}
            else:
                self.model[label] = {}
                self.scaler[label] = {}

            if "during" in phases:
                for trim in range(start_trim, n_trim + 1):
                    during_idx = phases.index("during")
            
                    self.model[label][trim] = self._load_obj(f"{phases[during_idx]}_{label} t{trim}_{model_name}")
                    self.scaler[label][trim] = self._load_obj(f"{label}_t{trim}_{phases[during_idx]}_resampled_scaler")

    def _load_obj(self, file_name, file_f = True):
        if file_f: file_name += ".pkl"
        return pickle.load(open(f"{self.source}/{file_name}", "rb"))
    
    def _encode(self, X):
        for col in X.columns:
            uniq = X[col].unique()
            if "yes" in uniq or "no" in uniq:
                if "no_data" in uniq:
                    encoded = X[col].replace({"no_data": 0, "yes": 2, "no": 1})
                else:
                    encoded = X[col].replace({"yes": 1, "no": 0})
                X[col] = encoded

        X["muet_score"] = X["muet_score"].replace({"irrelavant": 0, "band 1": 1, "band 2": 2, "band 3": 3, "band 4": 4, "band 5": 5, "band 6": 6})

        for col in ['bm_score', 'bi_score', 'matematik', 'sejarah', 'matematik_tambahan', 'fizik', 'kimia', 'biologi', 'pendidikan_moral']:
            X[col] = X[col].replace({"irrelavant": 0, "a": 4, "b": 3, "c": 2, "d": 1})

        for col, encoder in self.encoder.items():
            X[col] = encoder.transform(X[col])

        return X
    
    def predict(self, X):
        # data preprocessing
        
        X.columns = X.columns.str.lower().str.replace(" ", "_").str.strip()

        for col in X.select_dtypes(object).columns:
            X[col] = X[col].str.lower()
        
        eng_m_v = dict(zip(["malay_language", "english_language", "muet", "mathematics", 
                            "history", "additional_mathematics", "physics", "chemistry", "biology", "moral_education"], 
                           ['bm_score', 'bi_score', 'muet_score', 'matematik', 
                            'sejarah', 'matematik_tambahan', 'fizik', 'kimia', 
                            'biologi', 'pendidikan_moral'] ))
       
        X = X.rename(columns = eng_m_v)
      
        # data encoding
        X = self._encode(X)
        
        pred = {}
        proba = {}

        for label in self.labels:
            
            pred_temp = {}
            proba_temp = {}

            for phase, model in self.model[label].items():

                # feature selection
                if type(phase) == int:
                    X_selected = self.features[self.phases[self.phases.index("during")]][f"{label} t{phase}"][self.fs]
                else:
                    X_selected = self.features[self.phases[self.phases.index("before")]][label][self.fs]
                
                X_selected = X[X_selected]

                # class imbalance
                X_scaled = self.scaler[label][phase].transform(X_selected)
                X_scaled = pd.DataFrame(X_scaled, columns = X_selected.columns)
               
                # model prediction
                pred_temp[phase] = model.predict(X_scaled)
                proba_temp[phase] = model.predict_proba(X_scaled)

            pred[label] = pred_temp
            proba[label] = proba_temp

        return pred, proba