import sys
import os
import dill
from sklearn.metrics import r2_score
from src.exception import CustomException
from sklearn.model_selection import GridSearchCV

def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)# take that obj and write it in file_obj(path :- artifacts/processor) file
    except Exception as e:
        raise CustomException(e,sys)
    
# def evaluate_models(X_train,y_train,X_test,y_test,models,param):
#     try:
#         report={}

#         for i in range(len(list(models))):
#             model=list(models.values())[i]
#             model_name = list(models.keys())[i]
#             para=param[model_name] # <-- Yahan sahi karo

#             gs=GridSearchCV(model,para,cv=3)

#             gs.fit(X_train,y_train)

#             model.set_params(**gs.best_params_)
#             model.fit(X_train,y_train)

#             y_train_pred=model.predict(X_train)

#             y_test_pred=model.predict(X_test)

#             train_model_score=r2_score(y_train,y_train_pred)
#             test_model_score=r2_score(y_test,y_test_pred)

#             report[list(models.keys())[i]] = test_model_score

#         return report
        
#     except Exception as e:
#         raise CustomException(e,sys)

def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        for model_name, model in models.items():
            try:
                params = param.get(model_name, {})

                if params:  # Only run GridSearchCV if params exist
                    gs = GridSearchCV(model, params, cv=3, n_jobs=-1)
                    gs.fit(X_train, y_train)
                    model.set_params(**gs.best_params_)

                # Fit model (even if no params)
                model.fit(X_train, y_train)

                # Predictions
                y_train_pred = model.predict(X_train)
                y_test_pred = model.predict(X_test)

                # Scores
                train_score = r2_score(y_train, y_train_pred)
                test_score = r2_score(y_test, y_test_pred)

                report[model_name] = test_score

            except Exception as e:
                logging.error(f"Model {model_name} failed: {e}")
                continue  # Skip the failing model

        if not report:
            raise CustomException("No model was successfully trained.", sys)

        return report

    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)