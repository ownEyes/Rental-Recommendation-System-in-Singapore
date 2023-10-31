import numpy as np
import pandas as pd
import joblib
import shap
import sklearn

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, StackingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from xgboost import XGBRegressor
import lightgbm as lgb


class Forcaster:
    def __init__(self,model_path,scaler_path,encoder_path,lambda_value):
        self.lambda_value=lambda_value
        self.model=None
        self.scaler=None
        self.encoder=None
        self.set_model(model_path,scaler_path,encoder_path)
        self.input=None
        self.result=None
        self.importance=None
        
    def load_input(self,input):
        input_df = pd.DataFrame([input])
        # 分类numeric_cols和text_cols
        numeric_cols = input_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        text_cols = input_df.select_dtypes('object').columns.tolist()
        # 缺失值填充
        imputer = np.nanmean(input_df[numeric_cols], axis=0)
        input_df[numeric_cols] = np.where(np.isnan(input_df[numeric_cols]), imputer, input_df[numeric_cols])
        # 独热编码
        prediction_encoded_cols = list(self.encoder.get_feature_names_out(text_cols))
        input_df[prediction_encoded_cols] = self.encoder.transform(input_df[text_cols].values)
        x_input = input_df[numeric_cols + prediction_encoded_cols]
        # 归一化
        self.input = self.scaler.transform(x_input)
    
    def set_model(self,model_path,scaler_path,encoder_path):
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.encoder = joblib.load(encoder_path)
    
    def perdict(self):
        stack_predicted_price_boxcox=self.model.predict(self.input)[0]
        if self.lambda_value != 0:
            predicted_price = (stack_predicted_price_boxcox * self.lambda_value + 1) ** (1 / self.lambda_value)
        else:
            predicted_price = np.exp(stack_predicted_price_boxcox) - 1
        self.result=predicted_price
        return self.result
        
    def get_feature_importance(self):
        base_models = list(self.model.named_estimators_.values())

        # Create a list to store SHAP values for each base model
        shap_values_list = []

        # Calculate SHAP values for each base model
        for model in base_models:
            if isinstance(model, (sklearn.tree.DecisionTreeRegressor, sklearn.ensemble.RandomForestRegressor)):
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(self.input)
                shap_values_list.append(shap_values)
            elif isinstance(model, (sklearn.linear_model.LinearRegression, sklearn.linear_model.Ridge)):
                explainer = shap.LinearExplainer(model, self.input)
                shap_values = explainer.shap_values(self.input)
                shap_values_list.append(shap_values)
            # Add more elif blocks for other supported model types

        # Calculate the mean SHAP values across base models
        stacking_shap_values = np.mean(shap_values_list, axis=0)

        # 将SHAP值转换为数据帧
        shap_df = pd.DataFrame(stacking_shap_values, columns=self.input.columns)
        self.importance=shap_df.to_dict()
        return self.importance
    
    