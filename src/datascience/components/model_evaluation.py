import os
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
import joblib
from pathlib import Path
from src.datascience.entity.config_entity import ModelEvaluationConfig
from src.datascience.constants import *
from src.datascience.utils.common import read_yaml, create_directories,save_json

import os
os.environ["MLFLOW_TRACKING_URI"]="https://dagshub.com/danialasimbashir/machinelearningproject.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"]="danialasimbashir"
os.environ["MLFLOW_TRACKING_PASSWORD"]="e37ce21752ebf32affc46b58f9fb1733099ec7d5"

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self,actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2
    
    def log_into_mlflow(self):

        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_x = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[[self.config.target_column]]


        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():

            predicted_qualities = model.predict(test_x)

            (rmse, mae, r2) = self.eval_metrics(test_y, predicted_qualities)
            
            # Saving metrics as local
            scores = {"rmse": rmse, "mae": mae, "r2": r2}
            save_json(path=Path(self.config.metric_file_name), data=scores)

            mlflow.log_params(self.config.all_params)

            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)
            mlflow.log_metric("mae", mae)

            # Handle model logging
            if "dagshub.com" in self.config.mlflow_uri:
                print("Saving model artifacts for DagsHub...")
                
                # Save model artifacts locally first
                import tempfile
                import shutil
                
                # Create a temporary directory for model artifacts
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_model_path = Path(temp_dir) / "model_artifacts"
                    
                    # Save model using MLflow format
                    mlflow.sklearn.save_model(
                        sk_model=model,
                        path=str(temp_model_path),
                        signature=None,
                        input_example=test_x.iloc[:1].values if len(test_x) > 0 else None
                    )
                    
                    # Log individual model files as artifacts to MLflow
                    try:
                        print("📤 Uploading model artifacts to DagsHub MLflow...")
                        
                        # Log the model pickle file
                        model_pkl_path = temp_model_path / "model.pkl"
                        if model_pkl_path.exists():
                            mlflow.log_artifact(str(model_pkl_path), "model")
                        
                        # Log the MLmodel file
                        mlmodel_path = temp_model_path / "MLmodel"
                        if mlmodel_path.exists():
                            mlflow.log_artifact(str(mlmodel_path), "model")
                        
                        # Log conda.yaml
                        conda_path = temp_model_path / "conda.yaml"
                        if conda_path.exists():
                            mlflow.log_artifact(str(conda_path), "model")
                        
                        # Log requirements.txt
                        req_path = temp_model_path / "requirements.txt"
                        if req_path.exists():
                            mlflow.log_artifact(str(req_path), "model")
                        
                        # Log python_env.yaml
                        python_env_path = temp_model_path / "python_env.yaml"
                        if python_env_path.exists():
                            mlflow.log_artifact(str(python_env_path), "model")
                        
                        print("✅ Model artifacts successfully uploaded to DagsHub MLflow!")
                        
                    except Exception as upload_error:
                        print(f"⚠️ Failed to upload artifacts to DagsHub: {str(upload_error)}")
                    
                    # Also save locally for backup
                    local_model_path = Path(self.config.root_dir) / "model_artifacts_backup"
                    if local_model_path.exists():
                        shutil.rmtree(local_model_path)
                    
                    shutil.copytree(temp_model_path, local_model_path)
                    print(f"💾 Model artifacts also saved locally at: {local_model_path}")
                
            else:
                # For non-DagsHub platforms (standard MLflow servers)
                if tracking_url_type_store != "file":
                    # Register the model
                    mlflow.sklearn.log_model(model, "model", registered_model_name="ElasticnetModel")
                else:
                    mlflow.sklearn.log_model(model, "model")