import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from src.exception import CustomException
from src.logger import logging

from src.utils import save_object,evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        
        try:
            logging.info("split trianing and test input data")
            X_train,y_train,X_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbors Classifier": KNeighborsRegressor(),
                "XGBRegressor": XGBRegressor(),
                "CatBoost Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor()
            }

            # evaluate_models->utils will use all models as fit data
            model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models)
            
            # to get the best model score from dict
            best_model_score = max(sorted(model_report.values()))

            # convert the keys to list to access values using index and then access value using its index and then get the model name with best_model_score 
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            # example list(model_report.keys())[2] -> will give key with best_model_score suppose Gradient Boosting
            
            #ab model ke naam se dict main dundke nikalo uska instance or object
            best_model=models[best_model_name]
            # suppose Ye aapko GradientBoostingRegressor() object dega

            # setting threshold
            if best_model_score<0.6:
                raise CustomException("No best model found")
            
            logging.info("best found model on both training and testing dataset")
            # loading the model into pkl file into model_path
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)

            test_r2_score = r2_score(y_test, predicted)
            return test_r2_score
        
        except Exception as e:
            raise CustomException(e,sys)
