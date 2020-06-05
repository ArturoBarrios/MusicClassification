from itertools import chain
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import Imputer, StandardScaler
from sklearn.pipeline import Pipeline

# define transformer to scale numeric variables
# and one-hot encode categorical ones
class FeatureTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, transforms = [("impute", Imputer()), ("scale", StandardScaler())]):
        self.transforms = transforms
    def fit(self, X, y = None):
        self.columns_ = X.columns
        self.cat_columns_ = X.select_dtypes(include = ["object"]).columns
        self.non_cat_columns_ = X.columns.drop(self.cat_columns_)
        self.pipe = Pipeline(self.transforms).fit(X.ix[:, self.non_cat_columns_])
        self.cat_map_ = {col: X[col].astype("category").cat.categories
                         for col in self.cat_columns_}
        self.ordered_ = {col: X[col].astype("category").cat.ordered
                         for col in self.cat_columns_}
        self.dummy_columns_ = {col: ["_".join([col, v])
                                     for v in self.cat_map_[col]]
                               for col in self.cat_columns_}
        self.transformed_columns_ = pd.Index(
            self.non_cat_columns_.tolist() +
            list(chain.from_iterable(self.dummy_columns_[k]
                                     for k in self.cat_columns_))
        )
        return self
    def transform(self, X, y = None):
        scaled_cols = pd.DataFrame(self.pipe.transform(X.ix[:, self.non_cat_columns_]),
                                   columns = self.non_cat_columns_).reset_index(drop = True)
        cat_cols = X.drop(self.non_cat_columns_.values, 1).reset_index(drop = True)
        scaled_df = pd.concat([scaled_cols, cat_cols], axis = 1)
        final_matrix = (pd.get_dummies(scaled_df)
                        .reindex(columns = self.transformed_columns_)
                        .fillna(0).as_matrix())
        return final_matrix
