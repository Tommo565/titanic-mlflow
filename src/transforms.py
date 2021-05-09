from loguru import logger
import pandas as pd
import re


def set_df_index(
    df: pd.core.frame.DataFrame,
    df_index_col: str,
):
    """
    Description
    -----------
    Sets an index of the supplied column name for the supplied DataFrame

    Parameters
    ----------
    df: pandas.core.frame.DataFrame
        The dataframe to be processed

    df_index: list
        The names of the column to set as the index

    Returns
    -------
    df_out: pandas.DataFrame
        The processed pandas Dataframe

    Raises
    ------
    Exception: Exception
        Generic exception for logging

    Examples
    --------
    df_out = set_df_index(
        df=df
        df_index_col="col1"
    )
    """

    logger.info("Running set_df_index()")

    try:
        df_out = df.set_index(df_index_col, drop=True)

    except Exception:
        logger.exception("Error in set_df_index()")

    return df_out


def drop_columns(
    df: pd.core.frame.DataFrame,
    drop_column_names: list,
):
    """
    Description
    -----------
    Removes the specified columns from the supplied DataFrame

    Parameters
    ----------
    df: pandas.core.frame.DataFrame
        The dataframe to be processed

    drop_column_names: list
        The names of the columns to remove

    Returns
    -------
    df_out: pandas.DataFrame
        The processed pandas Dataframe

    Raises
    ------
    Exception: Exception
        Generic exception for logging

    Examples
    --------
    df_out = drop_columns(
        df=df
        drop_column_names=["col1, "col2]
    )
    """

    logger.info("Running drop_columns()")

    try:
        df_out = df.drop(labels=drop_column_names, axis=1)

        return df_out

    except Exception:
        logger.exception("Error in drop_columns()")


def create_title_cat(
    df: pd.core.frame.DataFrame,
    source_column: str,
    dest_column: str,
    title_codes: dict
):
    """
    Description
    -----------
    Feature Engineers the title column of a pandas Dataframe by extracting the
    title from the source column via regex, coding the values and creating the
    dest_column.

    Contains the extract title sub-function which extracts the blocks of text
    and picks the group containing the title which will always be at index 1.

    Parameters
    ----------
    df: pandas.core.frame.DataFrame
        The dataframe to be processed

    source_column: str
        The coulumn containing the data from which to extract the title.

    dest_column: str
        The new column to create containing the extracted title.

    title_codes: dict
        Dictionary containing the title values as keys (e.g. Mr, Mrs, mme etc.)
        and the corresponding codes as values (e.g. gen_male, other_female etc.)

    Returns
    -------
    df_out: pandas.DataFrame
        The processed pandas Dataframe

    Raises
    ------
    Exception: Exception
        Generic exception for logging

    Examples
    --------
    df_out = create_title_cat(
        df=df
        source_column="col1",
        dest_column="col2"
        title_codes: {
            "Mr": "gen_male".
            "Mrs: "gen_female"s
        }
    )
    """

    logger.info("Running create_title_cat()")

    # Define the extract_title function
    def extract_title(
        row: pd.core.series.Series,
        source_column: str
    ):
        """
        Extracts the title from the supplied specified title_source_column via
        a regex. Applied to a pandas DataFrame
        """

        title_search = re.search(r' ([A-Za-z]+)\.', row[source_column])

        if title_search:
            title = title_search.group(1)

        else:
            title = ""

        return title

    # Apply the extract_title function to the dataframe
    try:
        df_out = df.copy()

        df_out[dest_column] = (
            df_out.apply(
                extract_title,
                args=([source_column]),
                axis=1
            )
            .replace(title_codes)
        )

        return df_out

    except Exception:
        logger.exception("Error in create_title_cat()")


def impute_age(
    df: pd.core.frame.DataFrame,
    source_column: str,
    title_column: str,
    age_codes: dict
):
    """
    If the age of a passenger is missing, infer this based upon the passenger
    title.

    Parameters
    ----------
    df: pandas.DataFrame
        The dataframe to be processed.

    source_column: str
        The column containing the age values.

    title_column: str
        The column containing the title_values.

    age_codes: dict
        Dictionary containing the title category values as keys (e.g. "gen_male"
        "gen_female", and the age to infer as values.

    Returns
    -------
    df: pandas.DataFrame
        The processed dataframe.

    Raises
    ------
    Exception: Exception
        Generic exception for logging

    Examples
    --------
    df = impute_age(
        df=df,
        source_column="Age",
        title_column="TitleCat",
        age_codes=dict(
            gen_male=30,
            gen_female=35
            . . .
        )
    )
    """

    logger.info("Running impute_age()")

    def infer_age(
        row: pd.core.series.Series,
        source_column: str,
        title_column: str,
        age_codes: dict
    ):
        """Infers the age of a passenger based upon the passenger title,
        Applied to a pandas dataframe"""

        if(pd.isnull(row[source_column])):

            # Iterate through the codes and assign an age based upon the title
            for key, value in age_codes.items():
                if row[title_column] == key:
                    age = value

        # Else return the age as an integer
        else:
            age = int(row[source_column])

        return age

    try:

        # Apply the infer_age function to the pandas dataframe
        df_out = df.copy()
        df_out[source_column] = (
            df_out.apply(
                infer_age,
                args=([source_column, title_column, age_codes]),
                axis=1
            )
        )

        return df_out

    except Exception:
        logger.exception("Error in impute_age()")


def create_family_size(
    df: pd.core.frame.DataFrame,
    source_columns: list,
    dest_column: str
):
    """
    Description
    -----------
    Create a column for family_size via summing the source_columns.

    Parameters
    ----------
    df: pd.core.frame.DataFrame
        The dataframe to be processed.

    source_columns: list
        The columns to be summed to calculate the family size.

    dest_column: str
        The destination column to contain the family size values.

    Returns
    -------
    df_out: pd.core.frame.DataFrame.
        The processed dataframe

    Raises
    ------
    Exception: Exception
        Generic exception for logging
    """

    logger.info("Running create_family_size()")

    try:
        df_out = df.copy()
        df_out[dest_column] = df_out.apply(
            lambda row: row[source_columns].sum() + 1,
            axis=1
        )

        return df_out

    except Exception:
        logger.exception("Error in create_family_size()")
