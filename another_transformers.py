import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin

class NumericalImputer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.animals_heart_rate = {}        
        
    def fit(self, X, y=None):
        self.is_fitted_ = True
        heart = X.groupby('Animal_Type')['Heart_Rate'].mean()
        for a, v in zip(heart.index, heart.values):
            self.animals_heart_rate[a] = int(np.round(v))
        return self
  
        
    def transform(self, X, y=None):
        X_c = X.copy()
        X_c.fillna({'Heart_Rate': X_c['Animal_Type'].map(func=lambda x: int(np.round(self.animals_heart_rate[x])))}, inplace=True)
        self.get_feature_names_out = lambda x: [x for x in X_c.columns]
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
        for col in ['Animal_Type', 'Breed']:
            if col == 'Animal_Type':
                if X_c[col].isna().sum() > 0:
                    X_c.fillna({f'{col}': X_c['Breed'].apply(func=self.search_by_breed)}, axis=0, inplace=True)
                    continue
                else:
                    continue
            else:
                if X_c[col].isna().sum() > 0:
                    X_c.fillna({f'{col}': X_c['Animal_Type'].apply(func=lambda x: self.animals[x][0])}, axis=0, inplace=True)
                    continue
                else:
                    continue
        self.get_feature_names_out = lambda x: [x for x in X_c.columns]
        return X_c


class AnimalImputer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.animals = {}

    def fit(self, X, y=None):
        self.is_fitted_ = True
        animals = X.groupby('Animal_Type')['Breed'].value_counts()
        for a, b in animals.index:
            if a not in self.animals:
                self.animals[a] = [b]
                continue
            else:
                self.animals[a].append(b)
        return self

    def transform(self, X, y=None):
        X_c = X.copy()
        for col in ['Animal_Type', 'Breed']:
            if col == 'Animal_Type':
                if X_c[col].isna().sum() > 0:
                    X_c.fillna({f'{col}': X_c['Breed'].map(func=lambda x: int(str(x).split('.')[0]))}, inplace=True)
                    continue
                else:
                    continue
            else:
                if X_c[col].isna().sum() > 0:
                    X_c.fillna({f'{col}': X_c['Animal_Type'].map(func=lambda x: self.animals[x][0])}, inplace=True)
                    continue
                else:
                    continue
        self.get_feature_names_out = lambda x: [c for c in X_c.columns]
        return X_c
        