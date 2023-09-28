# project: p7
# submitter: cmbatchelor
# partner: none
# hours: 4

import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import make_column_transformer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import *


class UserPredictor:
    def __init__(self):
        pass
    def fit(self, train_user, train_log, train_y):
        self.train_user = train_user
        self.train_log = train_log
        self.train_y = train_y
        
        self.train_user = self.train_user.set_index('user_id')
        
        total_sec = self.train_log.groupby(['user_id'])['seconds'].sum()
        self.train_user['seconds'] = total_sec
        self.train_user['seconds'].fillna(0, inplace=True)
        
        self.model = Pipeline([
            ("poly", PolynomialFeatures(degree=2)),
            ("std", StandardScaler()),
            ("lr", LogisticRegression())
        ])
        
        self.xcols = ['past_purchase_amt', 'seconds', 'age']
        
        self.model.fit(self.train_user[self.xcols], self.train_y['y'])
        
        return self.model
        
    def predict(self, test_user, test_log):
        self.test_user = test_user
        self.test_log = test_log
        
        self.test_user = self.test_user.set_index('user_id')

        total_sec = self.test_log.groupby(['user_id'])['seconds'].sum()
        self.test_user['seconds'] = total_sec
        self.test_user['seconds'].fillna(0, inplace=True)
        
        self.pred = self.model.predict(self.test_user[self.xcols])
        
        return self.pred
        
        
        
        
        
        