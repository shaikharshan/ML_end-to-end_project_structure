import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from dataclasses import dataclass
import numpy as np
from src.utils import save_obj
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')
    # used to get required file paths

class DataTransformation:
    def __init__(self):
        self.dataTransformationconfig = DataTransformationConfig()
    def get_data_transformer_object(self):
        try:
            cat_col = ['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']
            num_col = ['reading_score', 'writing_score']

            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")), #outliers are present in dataset so mean not used
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            logging.info("numerical columns imputing and scaling completed")
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("onehot",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )

            logging.info("categorical columns encoding completed")

            # combine both pipelines using columntransformer

            # logging.info("Categorical columns: ",cat_col)
            # logging.info("Numerical columns: ",num_col)
            preprocessor = ColumnTransformer(
                [
                    ("num_col_pipeline",num_pipeline,num_col),
                    ("cat_col_pipeline",cat_pipeline,cat_col)
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Train/test data read")
            logging.info("Obtaining preprocessor object")

            preprocessing_obj = self.get_data_transformer_object()
            
            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_obj(
                file_path=self.dataTransformationconfig.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            logging.info(f"Saved preprocessing object.")


            return(
                train_arr,test_arr,self.dataTransformationconfig.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)