import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin

class NumericalImputer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.animals_age = {}
        self.animals_weight = {}
        
        
    def fit(self, X, y=None):
        self.is_fitted_ = True
        # super().fit(X, y=None)
        # animals_age = X.groupby('Animal_Type')['Age'].mean().sort_index() 
        animals_weight = X.groupby('Animal_Type')['Weight'].mean().sort_index()
        # for a, v in zip(animals_age.index, animals_age.values):
        #     self.animals_age[a] = v
            
        for a, v in zip(animals_weight.index, animals_weight.values):
            self.animals_weight[a] = v
        return self
  
        
    def transform(self, X, y=None):
        X_c = X.copy()
        for col in ['Weight', 'Heart_Rate', 'Body_Temperature_°C']:
            # if col == 'Age':
            #     if X_c[col].isna().sum() > 0:
            #         X_c.fillna({f'{col}': X_c['Animal_Type'].map(func=lambda x: np.round(self.animals_age[x]) if x else 3)}, axis=0, inplace=True)
            #         continue
            #     else:
            #         continue
            if col == 'Weight':
                if X_c[col].isna().sum() > 0:
                    X_c.fillna({f'{col}': X_c['Animal_Type'].map(func=lambda x: np.round(self.animals_weight[x], decimals=1))}, axis=0, inplace=True)
                    continue
                else:
                    continue
            else:
                if X_c[col].isna().sum() > 0:
                    X_c.fillna({f'{col}': np.round(X_c[col].mean())}, inplace=True)
                    continue
                else:
                    continue
        self.get_feature_names_out = lambda x: [x for x in X_c.columns]
        # return X_c[[x for x in X_c.select_dtypes(include='number').columns]]
        return X_c

    
class CategoricalImputer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.animals = {}
        self.data = None

    def fit(self, X, y=None):
        self.is_fitted_ = True
        self.data = X.groupby('Animal_Type')['Breed'].value_counts()
        for a, b in self.data.index:
            if a not in self.animals:
                self.animals[a] = [b]
                continue
            else:
                self.animals[a].append(b)
                continue
        return self

    def search_by_breed(self, breed):
        animal = 'Unknown'
        for a, brds in self.animals.items():
            if breed in brds:
                animal = a
                break
        return animal
    
    def transform(self, X, y=None):
        X_c = X.copy()
        for col in X_c.columns:
            if col == 'Animal_Type':
                # X_c.loc[X_c[col].isna(), col] = X_c.loc[X_c[col].isna(), 'Breed'].apply(func=self.search_by_breed)
                if X_c[col].isna().sum() > 0:
                    X_c.fillna({f'{col}': X_c['Breed'].apply(func=self.search_by_breed)}, axis=0, inplace=True)
                    continue
                else:
                    continue
            else:
                if X_c[col].isna().sum() > 0:
                # X_c.loc[X_c[col].isna(), col] = X_c.loc[X_c[col].isna(), 'Animal_Type'].apply(func=lambda x: self.animals[x][0])
                    X_c.fillna({f'{col}': X_c['Animal_Type'].apply(func=lambda x: self.animals[x][0])}, axis=0, inplace=True)
                    continue
                else:
                    continue
        self.get_feature_names_out = lambda x: [x for x in X_c.columns]
        return X_c


