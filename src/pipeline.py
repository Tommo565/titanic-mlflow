from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from src import (
    drop_columns,
    create_title_cat,
    impute_age,
    set_df_index
)


def create_pipeline(
    pipeline_parameters: dict
):
    """
    Description
    -----------
    Create a scikit learn pipeline as a series of functions applied to the
    dataframe via scikit-learn's FunctionTransformer class.

    Each transformation step has a function assigned with the keyword arguments
    applied through the supplied pipeline_parameters object.

    Parameters
    ----------
    pipeline_parameters: dict
        Parameters containing the metadata associated with the pipeline
        transformations.

    Returns
    -------
    pipeline: sklearn.pipeline.Pipeline
        The scikit-learn pipeline

    Raises:
    -------
    Exception: Exception
        Generic exception for logging

    Examples
    --------
    pipeline = create_pipeline(
        ("Step Description", FunctionTransformer(
            func=my_func_name,
            kw_args={"keyword_name" : "keyword_arg}
        ))
    )
    """
    # Unpack kw_args
    set_df_index_kw_args = pipeline_parameters["set_df_index_kw_args"]
    create_title_cat_kw_args = pipeline_parameters["create_title_cat_kw_args"]
    drop_columns_kw_args = pipeline_parameters["drop_columns_kw_args"]
    impute_age_kw_args = pipeline_parameters["impute_age_kw_args"]

    # Create the pipeline
    pipeline = Pipeline([
        ("Set dataframe index", FunctionTransformer(
            func=set_df_index,
            kw_args=set_df_index_kw_args
        )),
        ("Create title_cat column", FunctionTransformer(
            func=create_title_cat,
            kw_args=create_title_cat_kw_args
        )),
        ("Impute missing Age values", FunctionTransformer(
            func=impute_age,
            kw_args=impute_age_kw_args
        )),
        ("Drop columns", FunctionTransformer(
            func=drop_columns,
            kw_args=drop_columns_kw_args
        ))
    ])

    return pipeline