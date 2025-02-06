import sys
import os 
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.compose import ColumnTransformer

from src.constants import *
from src.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact, DataIngestionArtifact
from src.entity.config_entity import DataTransformationConfig
from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import save_object, save_numpy_array_data, read_yaml_file


class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        try:
            self.data_ingestion_artifact= data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e,sys)
        

    def get_data_transform_object(self) -> Pipeline:
        """
        Creates and returns a data transformer object for the data, 
        including gender mapping, dummy variable creation, column renaming,
        feature scaling, and type adjustments.
        """
        logging.info("Enter get_data_transform_object method of data transformation class")
        try:
            #initializer transformation
            numeric_tranformer = StandardScaler()
            min_max_scaler = MinMaxScaler()
            logging.info("Transformers Initialized - standarscaler and Minmaxscaler")

            #Load schema Configuration
            num_features = self._schema_config['num_features']
            mm_columns = self._schema_config['mm_columns']
            logging.info("Cols loaded from schema")

            #Creating the preprocess pipeline
            preprocesor = ColumnTransformer(
                transformers=[
                    ("StandardScaler", numeric_tranformer, num_features),
                    ("MinMaxScaler", min_max_scaler, mm_columns)
                ],
                remainder="passthrough" #Leaves  other columns as they are
            )

            #Wrapping everything in a singlepipeline
            final_pipeline = Pipeline(steps=[("preprocesor", preprocesor)])
            logging.info("Final pipeline ready")
            logging.info("Exited get_data_transformer_object method of DataTransformation class")
            return final_pipeline

        except Exception as e:
            logging.exception("Exception occurred in get_data_transformer_object method of DataTransformation class")
            raise MyException(e,sys) from e
        
    def _map_gender_colum(self, df):
        """Map Gender column to 0 for Female and 1 for Male."""
        logging.info("Mapping gender column to the binary values")
        df['Gender'] = df['Gender'].map( {'Female': 0, 'Male': 1} ).astype(int)
        return df
    
    def _creates_dummy_columns(self, df):
        """Create dummy variables for categorical features."""
        logging.info("Creating dummy variables for categorical features")
        df=pd.get_dummies(df,drop_first=True)
        return df
    

    def _rename_columes(self,df):
        """Rename specific columns and ensure integer types for dummy columns."""
        logging.info("Renaming specific columns and casting to int")
        df = df.rename(columns={"Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year", "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"})
        df['Vehicle_Age_lt_1_Year'] = df['Vehicle_Age_lt_1_Year'].astype('int')
        df['Vehicle_Age_gt_2_Years'] = df['Vehicle_Age_gt_2_Years'].astype('int')
        df['Vehicle_Damage_Yes'] = df['Vehicle_Damage_Yes'].astype('int')
        return df
    def _drop_id_columns(self,df):
        """Drop the id column if exits"""
        logging.info("Dropping the id columns")
        drop_col = self._schema_config['drop_columns']
        if drop_col in df.columns:
            df = df.drop(drop_col, axis = 1)
        return df
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """Initiates the data transformation component for the pipeline"""
        try:
            logging.info(" Data transformation Started !!!")
            if not self.data_validation_artifact.validation_status:
                raise Exception(self.data_validation_artifact.message)
            
            # Load train and test data
            train_df = self.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(file_path=self.data_ingestion_artifact.test_file_path)
            logging.info("Train-test data loaded")

            input_feature_train_df = train_df.drop(columns=[TRARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TRARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TRARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TRARGET_COLUMN]
            logging.info("Input and target cols defined for both train and test df")

            #Apply custom tranformation in specific sequence
            input_feature_train_df = self._map_gender_colum(input_feature_train_df)
            input_feature_train_df = self._drop_id_columns(input_feature_train_df)
            input_feature_train_df = self._creates_dummy_columns(input_feature_train_df)
            input_feature_train_df = self._rename_columes(input_feature_train_df)

            input_feature_test_df = self._map_gender_colum(input_feature_test_df)
            input_feature_test_df = self._drop_id_columns(input_feature_test_df)
            input_feature_test_df = self._creates_dummy_columns(input_feature_test_df)
            input_feature_test_df = self._rename_columes(input_feature_test_df)
            logging.info("Custom transformation applied to the train and test data")

            logging.info("Starting the data transformation")
            preprocessor = self.get_data_transform_object()
            logging.info("Get the preprocessor object")

            logging.info("Initalizing the transformation for the train data")
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            logging.info("Initalizing the transformation for the test data")
            input_feature_test_arr = preprocessor.fit_transform(input_feature_test_df)
            logging.info("I transformation  doen for the test train data")

            logging.info("Applying SMOTEENN for handling the imblanced dataset")
            smt = SMOTEENN(sampling_strategy="minority")
            input_feature_train_final, target_feature_train_final = smt.fit_resample(input_feature_train_arr, target_feature_train_df)
            input_feature_test_final, target_feature_test_final = smt.fit_resample(input_feature_test_arr, target_feature_test_df)
            logging.info("SMOTEEN applied to train-test data")

            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]
            logging.info("feature-target concatenation done for train-test df.")

            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            logging.info("Saving the transformation object and transformed files")

            logging.info("Data transformation completed sucessfullyt")
            return DataTransformationArtifact(
                transformed_object_file_path=(self.data_transformation_config.transformed_object_file_path),
                transformed_train_file_path= (self.data_transformation_config.transformed_train_file_path),
                transformed_test_file_path=(self.data_transformation_config.transformed_test_file_path)
            )
        
        except Exception as e:
             raise MyException(e,sys)

