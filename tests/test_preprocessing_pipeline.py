import os
import mlflow
from src.utils import (
    load_config,
    load_logger,
    load_parameters,
)
from src.ingest_split import ingest_split
from src.preprocessing_pipeline import create_preprocessing_pipeline


def test_preprocessing_pipeline():
    """Test the preprocessing_pipeline function"""

    # Load in the test configuration & parameters
    config = load_config(".env.test")
    logger = load_logger(
        app_name=config["app_name"],
        logs_path=config["logs_path"]
    )

    # Configure MLFlow
    mlflow.set_tracking_uri(config["mlflow_tracking_uri"])
    mlflow.set_experiment(config["mlflow_experiment"])

    # Start MLFlow Tracking
    with mlflow.start_run():

        parameters = load_parameters(parameters_path=config["parameters_path"])
        uid = parameters["uid"]

        # Ingest the data
        X_train, X_test, y_train, y_test, X_holdout = ingest_split(
            train_test_raw_path=config["train_test_raw_path"],
            holdout_raw_path=config["holdout_raw_path"],
            target=parameters["target"],
            ingest_split_parameters=parameters["ingest_split_parameters"]
        )

        # Run the function
        preprocessing_pipeline = create_preprocessing_pipeline(
            pipeline_parameters=parameters["pipeline_parameters"]
        )
        X_holdout = (
            preprocessing_pipeline.fit_transform(X_holdout)
            .sort_values(by=uid)
        )

        # Run the tests
        # Structure
        assert X_holdout.index.name == "PassengerId"
        assert X_holdout.shape == (57, 16)

        # Scaling
        assert X_holdout["Age"].min() == 0
        assert X_holdout["Age"].max() == 1

        # One Hot encoding
        assert X_holdout["Pclass_1"].min() == 0
        assert X_holdout["Pclass_1"].max() == 1
        assert X_holdout["Pclass_2"].min() == 0
        assert X_holdout["Pclass_2"].max() == 1
        assert X_holdout["Pclass_3"].min() == 0
        assert X_holdout["Pclass_3"].max() == 1

        # General
        assert round(X_holdout["Age"].loc[1], 3) == 0.071
        assert round(X_holdout["FamilySize"].loc[1], 3) == 0.500
        assert X_holdout["Pclass_1"].loc[2] == 0
        assert X_holdout["Pclass_2"].loc[3] == 0
        assert X_holdout["Pclass_3"].loc[4] == 0
        assert X_holdout["Sex_female"].loc[5] == 1
        assert X_holdout["Sex_male"].loc[6] == 0
        assert X_holdout["Embarked_C"].loc[7] == 0
        assert X_holdout["Embarked_Q"].loc[8] == 1
        assert X_holdout["Embarked_S"].loc[9] == 1
        assert X_holdout["TitleCategory_gen_female"].loc[10] == 0
        assert X_holdout["TitleCategory_gen_male"].loc[11] == 0
        assert X_holdout["TitleCategory_other_female"].loc[12] == 0
        assert X_holdout["TitleCategory_other_male"].loc[13] == 1
        assert X_holdout["TitleCategory_young_female"].loc[14] == 1
        assert X_holdout["TitleCategory_young_male"].loc[15] == 0

        mlflow.end_run()
