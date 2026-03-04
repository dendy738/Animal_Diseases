import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin

class NumericalImputer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.animals_heart_rate = {}        
        
    def fit(self, X, y=None):
        self.is_fitted_ = True
        X_c = X.dropna()
        heart = X_c.groupby('Animal_Type')['Heart_Rate'].mean()
        for a, v in zip(heart.index, heart.values):
            self.animals_heart_rate[a] = int(np.round(v))
        
        return self
  
        
    def transform(self, X, y=None):
        X_c = X.copy()
        for col in ('Heart_Rate', 'Duration_in_days', 'Body_Temperature_°C'):
            if col == 'Heart_Rate':
                if X_c[col].isna().sum() > 0:
                    X_c = X_c.fillna({f'{col}': X_c['Animal_Type'].map(func=lambda x: self.animals_heart_rate[x])})
                    X_c[col] = X_c[col].astype('int64')
                    continue
                else:
                    continue
            elif col == 'Body_Temperature_°C':
                if X_c[col].isna().sum() > 0:
                    X_c = X_c.fillna({f'{col}': X_c.apply(func=lambda r: 39.6 if r['Fever'] == 1 else 38.7, axis=1)})
                    X_c[col] = X_c[col].astype('float64')
                    continue
                else:
                    continue
            else:
                if X_c[col].isna().sum() > 0:
                    X_c = X_c.fillna({f'{col}': int(X_c[col].mean())})
                    X_c[col] = X_c[col].astype('int64')
                    continue
                else:
                    continue
        self.get_feature_names_out = lambda x=None: [c for c in X_c.columns]
        return X_c

    
class CategoricalImputer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.animals = {}
        self.data = None

    
    def fit(self, X, y=None):
        self.is_fitted_ = True
        X_c = X.dropna()
        data = X_c.groupby('Animal_Type')['Breed'].value_counts()
        for a, b in data.index:
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
                    X_c = X_c.fillna({f'{col}': X_c['Breed'].map(func=self.search_by_breed)})
                    X_c[col] = X_c[col].astype('str')
                    continue
                else:
                    continue
            else:
                if X_c[col].isna().sum() > 0:
                    X_c = X_c.fillna({f'{col}': X_c['Animal_Type'].map(func=lambda x: self.animals[x][0])})
                    X_c[col] = X_c[col].astype('str')
                    continue
                else:
                    continue
        self.get_feature_names_out = lambda x=None: [x for x in X_c.columns]
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
        self.get_feature_names_out = lambda x=None: [c for c in X_c.columns]
        return X_c

