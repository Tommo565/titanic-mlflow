import pandas as pd
import numpy as np
import mlflow
from sklearn.model_selection import train_test_split
from loguru import logger


def ingest_split(
    train_test_raw_path: str,
    holdout_raw_path: str,
    target: str,
    ingest_split_parameters: dict,
):
    """
    Description
    -----------
    Ingest the training dataset and holdout datasets and split the training
    dataset into train and test.

    Paramaters
    ----------
    train_raw_path: str
        Location of the raw train.csv file to be ingested

    train_clean: str
        Location to export the processed train_clean.csv file to

    test_ingest: str
        Location of the raw testcsv file to be ingested

    test_clean: str
        Location to export the processed test_clean.csv file to

    parameters: dict
        Dictionary containing the parameters for the function.

    Returns
    -------
    df_train: pandas.DataFrame
        The processed training dataframe

    df_test: pandas.DataFrame
        The processed test dataframe

    Raises
    ------
    None

    Examples
    --------

    df_train, df_test = ingest_clean(
        train_ingest="path/to/ingest.csv",
        train_clean="path/to/export.csv",
        test_ingest="path/to/ingest.csv",
        test_clean="path/to/export.csv",
        parameters=dict(
            drop_column_names=["Cols", "To", "Drop"],
            rename_column_names={"old_name": "new_name"}
        )
    )
    """

    logger.info("Running ingest_split()")

    # Unpack Parameters
    train_size = ingest_split_parameters["train_size"]
    test_size = ingest_split_parameters["test_size"]
    random_state = ingest_split_parameters["random_state"]

    # Log MLflow parameters
    mlflow.log_param("train_size", train_size)
    mlflow.log_param("test_size", test_size)
    mlflow.log_param("random_state", random_state)

    # Import train & holdout datasets
    df_train = pd.read_csv(train_test_raw_path)
    df_holdout = pd.read_csv(holdout_raw_path)

    # Convert ints to floats
    for column in df_train.columns.tolist():
        if isinstance(df_train[column], np.int64):
            df_train[column] = df_train[column].astype(float)

    for column in df_holdout.columns.tolist():
        if isinstance(df_train[column], np.int64):
            df_train[column] = df_train[column].astype(float)

    # Split the features and target
    X = df_train.drop(target, axis=1)
    y = df_train[[target]]
    X_holdout = df_holdout

    # Train Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        train_size=train_size,
        test_size=test_size,
        random_state=random_state
    )

    return X_train, X_test, y_train, y_test, X_holdout
