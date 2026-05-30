#
# Copyright SAS Institute
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

"""
Native Polars type conversion utilities for saspy.

This module provides utilities for working with Polars DataFrames and LazyFrames
without requiring conversion to pandas. It handles type mappings between SAS
and Polars data types.
"""

from __future__ import annotations

import logging
from datetime import date, datetime, time
from typing import Any, Dict, List, Optional, Tuple, Union

logger = logging.getLogger("saspy")

# Try to import Polars, but don't fail if not available
try:
    import polars as pl

    POLARS_AVAILABLE = True
except ImportError:
    pl = None
    POLARS_AVAILABLE = False
    logger.debug("Polars not available. Native Polars support disabled.")


class PolarsTypeMapper:
    """
    Handles SAS <-> Polars type conversions without pandas.

    This class provides bidirectional mapping between SAS variable types and formats
    to Polars data types, enabling native Polars DataFrame support.
    """

    # Mapping from Polars dtype to SAS kind character
    # SAS kinds: 'N' = numeric, 'C' = character, 'D' = datetime, 'B' = boolean
    POLARS_TO_SAS_KIND = {
        pl.String: "C",
        pl.Utf8: "C",
        pl.Categorical: "C",
        pl.Enum: "C",
        pl.Boolean: "B",
        pl.Date: "D",
        pl.Datetime: "D",
        pl.Time: "D",
        pl.Duration: "D",
        pl.Float32: "N",
        pl.Float64: "N",
        pl.Int8: "N",
        pl.Int16: "N",
        pl.Int32: "N",
        pl.Int64: "N",
        pl.UInt8: "N",
        pl.UInt16: "N",
        pl.UInt32: "N",
        pl.UInt64: "N",
    }

    # Mapping from SAS type + format to Polars dtype
    SAS_TO_POLARS = {
        "CHAR": pl.String,
        "NUM": {
            "date": pl.Date,
            "datetime": pl.Datetime,
            "time": pl.Time,
            "numeric": pl.Float64,
            "default": pl.Float64,
        },
    }

    # Mapping from Polars dtype to SAS variable attributes (type, format)
    POLARS_TO_SAS: Dict[Any, Tuple[str, Optional[str]]] = {
        pl.String: ("CHAR", None),
        pl.Utf8: ("CHAR", None),
        pl.Categorical: ("CHAR", None),
        pl.Enum: ("CHAR", None),
        pl.Boolean: ("NUM", "$LOGICAL"),
        pl.Int8: ("NUM", "IB"),
        pl.Int16: ("NUM", "IBS"),
        pl.Int32: ("NUM", "IB"),
        pl.Int64: ("NUM", "IB"),
        pl.UInt8: ("NUM", "IB"),
        pl.UInt16: ("NUM", "IBS"),
        pl.UInt32: ("NUM", "IB"),
        pl.UInt64: ("NUM", "IB"),
        pl.Float32: ("NUM", "RB4"),
        pl.Float64: ("NUM", "RB8"),
        pl.Date: ("NUM", "DATE"),
        pl.Datetime: ("NUM", "DATETIME"),
        pl.Time: ("NUM", "TIME"),
        # pl.Date: ("NUM", "E8601DA."),
        # pl.Datetime: ("NUM", "E8601DT26.6"),
        # pl.Time: ("NUM", "E8601TM."),
        #
        # Note: Duration types don't have direct SAS equivalents
    }

    @classmethod
    def get_polars_dtype(cls, sas_type: Optional[str], sas_format: Optional[str] = None) -> Any:
        """
        Get Polars dtype from SAS type and format.

        :param sas_type: SAS variable type ('NUM' or 'CHAR') or None
        :param sas_format: SAS format string (e.g., 'DATE.', 'DATETIME.') or None
        :return: Polars dtype or None if unavailable
        """

        if sas_type is not None:
            assert isinstance(sas_type, str), "sas_type must be string or None"
        if sas_format is not None:
            assert isinstance(sas_format, str), "sas_format must be string or None"

        # Handle None input gracefully
        if not POLARS_AVAILABLE:
            return None

        if sas_type is None:
            # Return a sensible default when type is unknown
            logger.debug("Received None for sas_type, defaulting to String")
            return pl.String

        # Normalize input (work with copy to avoid modifying caller's data)
        sas_type_clean = sas_type.strip().upper() if sas_type else ""
        sas_format_clean = sas_format.strip().upper() if sas_format else None

        # Handle character types
        if sas_type_clean in ("C", "CHAR"):
            return pl.String

        # Handle numeric types
        if sas_type_clean in ("N", "NUM"):
            if sas_format_clean:
                # Remove trailing period if present
                if sas_format_clean.endswith("."):
                    fmt_upper = sas_format_clean[:-1]
                else:
                    fmt_upper = sas_format_clean

                # Date formats
                if fmt_upper == "DATE":
                    return pl.Date
                if fmt_upper.startswith(("DDMMYY", "MMDDYY", "YYMMDD")):
                    return pl.Date
                if fmt_upper in ("YYQ", "YYQR"):
                    return pl.Date
                if fmt_upper in ("PDJULG", "PDJULI", "ENGDFTD", "E8601DA"):
                    return pl.Date
                if fmt_upper == "E8601DA":
                    return pl.Date

                # Datetime formats
                if fmt_upper == "DATETIME":
                    return pl.Datetime
                if fmt_upper.startswith(("E8601DT", "B8601DT", "IS8601DT")):
                    return pl.Datetime
                if fmt_upper == "DATEAMPM":
                    return pl.Datetime

                # Time formats
                if fmt_upper == "TIME":
                    return pl.Time
                if fmt_upper.startswith(("E8601TM", "B8601TM", "IS8601TM")):
                    return pl.Time
                if fmt_upper == "TOD":
                    return pl.Datetime

            # Default numeric handling
            if not sas_format_clean or sas_format_clean in (
                "BEST",
                "BEST12",
                "BEST32",
                "BEST.",
                "BEST12.",
                "BEST32.",
                "EBEST",
            ):
                return pl.Float64

            fmt_check = sas_format_clean
            if fmt_check.startswith("$LOGICAL") or fmt_check.endswith("LOGICAL"):
                return pl.Boolean

            logger.debug(f"Unknown SAS format '{sas_format}' for numeric column. Falling back to Float64.")
            return pl.Float64

        # Default to String for unknown types
        return pl.String

    @classmethod
    def get_sas_attributes(cls, polars_dtype) -> Tuple[str, Optional[str]]:
        """
        Get SAS type and format from Polars dtype.

        :param polars_dtype: Polars data type
        :return: Tuple of (SAS type, SAS format)
        """
        assert polars_dtype is not None, "polars_dtype cannot be None"

        if not POLARS_AVAILABLE:
            return ("CHAR", None)

        # Handle the case where polars_dtype might be a type object vs instance
        # Check for matching type in mapping, handle nested types like pl.Datetime
        dtype_class = (
            type(polars_dtype) if not isinstance(polars_dtype, type) else polars_dtype
        )

        # Exact match or base class match
        res = cls.POLARS_TO_SAS.get(polars_dtype)
        if not res:
            res = cls.POLARS_TO_SAS.get(dtype_class, ("NUM", None))

        return res

    @classmethod
    def get_schema_kinds(cls, df: "pl.DataFrame") -> Dict[str, str]:
        """
        Get a dictionary mapping column names to SAS kind characters.

        :param df: Polars DataFrame
        :return: Dictionary of {column_name: sas_kind}
        """
        assert df is not None, "DataFrame cannot be None"
        assert hasattr(df, "schema"), "Object must have schema attribute"

        if not POLARS_AVAILABLE or not isinstance(df, pl.DataFrame):
            return {}

        schema_kinds = {}
        for col_name, polars_dtype in df.schema.items():
            sas_type, _ = cls.get_sas_attributes(polars_dtype)
            schema_kinds[col_name] = sas_type

        return schema_kinds

    @classmethod
    def convert_numeric_to_boolean(cls, df: "pl.DataFrame") -> "pl.DataFrame":
        """
        Convert Int64 or Float64 columns that contain only 0 and 1 (plus nulls) to Boolean type.

        This handles SAS boolean columns which are stored as numeric 1/0.

        :param df: Polars DataFrame
        :return: DataFrame with boolean-like columns converted to Boolean type
        """
        if not POLARS_AVAILABLE or not isinstance(df, pl.DataFrame):
            return df

        bool_cols = []
        for col_name, dtype in df.schema.items():
            if dtype in (pl.Float64, pl.Float32, pl.Int64, pl.Int32):
                unique_vals = df[col_name].unique().drop_nulls()
                if unique_vals.is_empty():
                    continue
                vals = unique_vals.to_list()
                if all(v in (0, 1, 0.0, 1.0) for v in vals):
                    bool_cols.append(col_name)
        if bool_cols:
            df = df.with_columns(
                [pl.col(c).cast(pl.Boolean).alias(c) for c in bool_cols]
            )
        return df

    @classmethod
    def convert_numeric_to_integer(cls, df: "pl.DataFrame") -> "pl.DataFrame":
        """
        Convert Float64 columns that contain only whole numbers (plus nulls) to Int64 type.

        This handles SAS numeric columns that represent integers but are stored as floats.

        :param df: Polars DataFrame
        :return: DataFrame with integer-like columns converted to Int64 type
        """
        if not POLARS_AVAILABLE or not isinstance(df, pl.DataFrame):
            return df

        conversions = []
        for col_name, dtype in df.schema.items():
            if dtype == pl.Float64:
                try:
                    non_null = df[col_name].drop_nulls()
                    if len(non_null) == 0:
                        continue
                    all_whole = (
                        non_null.cast(pl.Int64).cast(pl.Float64) == non_null
                    ).all()
                    if all_whole:
                        conversions.append(
                            pl.col(col_name).cast(pl.Int64).alias(col_name)
                        )
                except Exception:
                    pass

        if conversions:
            return df.with_columns(conversions)
        return df

    @classmethod
    def convert_numeric_to_integer(cls, df: "pl.DataFrame") -> "pl.DataFrame":
        """
        Convert Float64 columns that contain only whole numbers (plus nulls) to Int64 type.

        This handles SAS numeric columns that represent integers but are stored as floats.

        :param df: Polars DataFrame
        :return: DataFrame with integer-like columns converted to Int64 type
        """
        if not POLARS_AVAILABLE or not isinstance(df, pl.DataFrame):
            return df

        conversions = []
        for col_name, dtype in df.schema.items():
            if dtype == pl.Float64:
                try:
                    non_null = df[col_name].drop_nulls()
                    if len(non_null) == 0:
                        continue
                    all_whole = (
                        non_null.cast(pl.Int64).cast(pl.Float64) == non_null
                    ).all()
                    if all_whole:
                        conversions.append(
                            pl.col(col_name).cast(pl.Int64).alias(col_name)
                        )
                except Exception:
                    pass

        if conversions:
            return df.with_columns(conversions)
        return df

    @classmethod
    def convert_numeric_to_integer(cls, df: "pl.DataFrame") -> "pl.DataFrame":
        """
        Convert Float64 columns that contain only whole numbers (plus nulls) to Int64 type.

        This handles SAS numeric columns that represent integers but are stored as floats.

        :param df: Polars DataFrame
        :return: DataFrame with integer-like columns converted to Int64 type
        """
        if not POLARS_AVAILABLE or not isinstance(df, pl.DataFrame):
            return df

        int_cols = []
        for col_name, dtype in df.schema.items():
            if dtype in (pl.Float64, pl.Float32):
                col = df[col_name].drop_nulls()
                if col.is_empty():
                    continue
                if col.cast(pl.Int64).cast(pl.Float64).eq(col).all():
                    int_cols.append(col_name)
        if int_cols:
            df = df.with_columns([pl.col(c).cast(pl.Int64).alias(c) for c in int_cols])
        return df

    @classmethod
    def get_schema_from_sasdata(
        cls, sas, table: str, libref: str = "", dsopts: dict = None
    ) -> Dict[str, Any]:
        """
        Get Polars schema from sas data metadata.

        :param sas: SASsession object
        :param table: SAS table name
        :param libref: SAS libref
        :param dsopts: Dataset options
        :return: Dictionary mapping column names to Polars dtypes
        """
        if not POLARS_AVAILABLE:
            return {}

        try:
            lib = libref if libref else "WORK"
            # Use the SASdata object's columnInfo method which returns pandas df
            sd = sas.sasdata(table, libref, dsopts=dsopts if dsopts else {})
            sd.set_results("PANDAS")
            col_info = sd.columnInfo()

            if col_info is None or len(col_info) == 0:
                return {}

            schema = {}
            for _, row in col_info.iterrows():
                var_name = row.get("Variable", row.get("Name", ""))
                var_type = row.get("Type", "")
                var_fmt = row.get("Format", "")

                if var_type.upper() in ("NUM", "NUMERIC"):
                    schema[var_name] = cls.get_polars_dtype("NUM", var_fmt)
                else:
                    schema[var_name] = pl.String

            return schema
        except Exception as e:
            logger.debug(f"Failed to get schema from SAS data: {e}")
            return {}

    @classmethod
    def convert_datetime_to_string(
        cls, df: "pl.DataFrame", columns: List[str]
    ) -> "pl.DataFrame":
        """
        Convert datetime columns to strings for SAS transfer.

        SAS expects datetimes in ISO8601 format for proper parsing.

        :param df: Polars DataFrame
        :param columns: List of column names to convert
        :return: DataFrame with converted columns
        """
        if not POLARS_AVAILABLE or not isinstance(df, pl.DataFrame):
            return df

        exprs = []
        for col_name, dtype in df.schema.items():
            if col_name in columns:
                if dtype == pl.Date:
                    exprs.append(
                        pl.col(col_name).dt.to_string("%Y-%m-%d").alias(col_name)
                    )
                elif dtype == pl.Datetime:
                    exprs.append(
                        pl.col(col_name)
                        .dt.to_string("%Y-%m-%dT%H:%M:%S%.6f")
                        .alias(col_name)
                    )
                elif dtype == pl.Time:
                    exprs.append(
                        pl.col(col_name).dt.to_string("%H:%M:%S%.6f").alias(col_name)
                    )
                else:
                    exprs.append(pl.col(col_name))
            else:
                exprs.append(pl.col(col_name))

        return df.with_columns(exprs)

    @classmethod
    def get_sas_transfer_metadata(
        cls,
        df: Union["pl.DataFrame", "pl.LazyFrame", Dict[str, Any]],
        datetimes: Dict[str, str] = None,
        outfmts: Dict[str, str] = None,
        labels: Dict[str, str] = None,
        char_lengths: Dict[str, int] = None,
        keep_outer_quotes: bool = False,
        embedded_newlines: bool = False,
        LF: str = "\x01",
        CR: str = "\x02",
    ) -> Dict[str, str]:
        """
        Generate SAS code components for transferring Polars data to SAS.

        :param df: Polars DataFrame, LazyFrame, or Schema dictionary
        :param datetimes: Dict mapping column names to 'date' or 'time'
        :param outfmts: Dict mapping column names to SAS formats
        :param labels: Dict mapping column names to SAS labels
        :param char_lengths: Dict mapping column names to byte lengths
        :param keep_outer_quotes: Whether to keep outer quotes for strings
        :param embedded_newlines: Whether to handle embedded newlines
        :param LF: Character for LF replacement
        :param CR: Character for CR replacement
        :return: Dict containing 'length', 'format', 'input', 'label', 'xlate' strings
        """
        if not POLARS_AVAILABLE:
            return {"length": "", "format": "", "label": "", "input": "", "xlate": ""}

        if datetimes is None:
            datetimes = {}
        if outfmts is None:
            outfmts = {}
        if labels is None:
            labels = {}
        if char_lengths is None:
            char_lengths = {}

        is_lazy = hasattr(df, "collect")
        if is_lazy:
            df = df.collect()

        length_parts = []
        format_parts = []
        label_parts = []
        input_parts = []
        xlate_parts = []

        for col_name, polars_dtype in df.schema.items():
            col_name_n = f"'{col_name}'n"
            sas_type, sas_fmt = cls.get_sas_attributes(polars_dtype)

            if polars_dtype == pl.String:
                if is_lazy or char_lengths.get(col_name):
                    max_len = char_lengths.get(col_name, 32767)
                else:
                    max_len = max(df[col_name].str.len_bytes().max() or 8, 8)
                length_parts.append(f"{col_name_n} ${max_len}")
                input_parts.append(f"input {col_name_n} ${max_len}.")
            elif polars_dtype in (pl.Float64, pl.Float32):
                length_parts.append(f"{col_name_n} 8")
                input_parts.append(f"input {col_name_n} best32.")
            elif polars_dtype in (pl.Int64, pl.Int32, pl.Int16, pl.Int8):
                length_parts.append(f"{col_name_n} 8")
                input_parts.append(f"input {col_name_n} best12.")
            elif polars_dtype == pl.Boolean:
                length_parts.append(f"{col_name_n} 8")
                input_parts.append(f"input {col_name_n} best12.")
            elif polars_dtype in (pl.Date, pl.Datetime, pl.Time,):
                length_parts.append(f"{col_name_n} 8")
                if col_name in datetimes:
                    dt_type = datetimes[col_name]
                    if dt_type == "date":
                        format_parts.append(f"{col_name_n} E8601DA.")
                        xlate_parts.append(f"{col_name_n} = datepart({col_name_n})")
                    elif dt_type == "time":
                        format_parts.append(f"{col_name_n} E8601TM.")
                        xlate_parts.append(f"{col_name_n} = timepart({col_name_n})")
                    else:
                        format_parts.append(f"{col_name_n} E8601DT26.6")
                else:
                    format_parts.append(f"{col_name_n} E8601DT26.6")
                input_parts.append(f"input {col_name_n} best32.")
            else:
                length_parts.append(f"{col_name_n} 8")
                input_parts.append(f"input {col_name_n} best32.")

        if embedded_newlines:
            for col_name, polars_dtype in df.schema.items():
                if polars_dtype == pl.String:
                    cn = f"'{col_name}'n"
                    xlate_parts.append(
                        f"{cn} = translate({cn}, '0A'x, '{ord(LF):02X}'x)"
                    )
                    xlate_parts.append(
                        f"{cn} = translate({cn}, '0D'x, '{ord(CR):02X}'x)"
                    )

        for col_name, outfmt in outfmts.items():
            col_name_n = f"'{col_name}'n"
            format_parts.append(f"{col_name_n} {outfmt}")

        label_lines = []
        for col_name, label in labels.items():
            col_name_n = f"'{col_name}'n"
            label_lines.append(f"label {col_name_n} = {label}")

        return {
            "length": " ".join(length_parts),
            "format": " ".join(format_parts),
            "label": "; ".join(label_lines),
            "input": "; ".join(input_parts) if input_parts else "",
            "xlate": "; ".join(xlate_parts),
        }


class DataFrameConverter:
    """
    Utility class for converting between DataFrame types.

    This class handles conversion between Polars, Pandas, and other DataFrame
    types while preserving native Polars types when possible.
    """

    @staticmethod
    def to_polars(df: Any, streaming: bool = False) -> Any:
        """
        Convert a DataFrame to Polars if needed.

        If the DataFrame is already Polars, return it as-is.

        :param df: DataFrame to convert
        :param streaming: Whether to use Polars' streaming engine for LazyFrames (default: False)
        :return: Polars DataFrame or original if conversion not possible
        """
        if PolarsTypeMapper.is_polars_dataframe(df):
            return PolarsTypeMapper.collect_if_lazy(df, streaming=streaming)
        # Try to convert from pandas
        try:
            import pandas as pd

            if isinstance(df, pd.DataFrame):
                return pl.from_pandas(df) if POLARS_AVAILABLE else df
        except (ImportError, Exception):
            pass

        return df

    @staticmethod
    def to_pandas(df: Any, streaming: bool = False) -> Any:
        """
        Convert a DataFrame to Pandas if needed.

        :param df: DataFrame to convert
        :param streaming: Whether to use Polars' streaming engine for LazyFrames (default: False)
        :return: Pandas DataFrame or original if conversion not possible
        """
        if PolarsTypeMapper.is_polars_dataframe(df):
            df = PolarsTypeMapper.collect_if_lazy(df, streaming=streaming)
            try:
                return df.to_pandas()
            except Exception:
                pass
        try:
            import pandas as pd

            if isinstance(df, pd.DataFrame):
                return df
        except ImportError:
            pass

        return df

    @staticmethod
    def is_supported_dataframe(df: Any) -> bool:
        """
        Check if an object is a supported DataFrame type.

        :param df: Object to check
        :return: True if df is a supported DataFrame type
        """
        if PolarsTypeMapper.is_polars_dataframe(df):
            return True
        try:
            import pandas as pd

            if isinstance(df, pd.DataFrame):
                return True
        except ImportError:
            pass

        return False


# Convenience functions for module-level access


def is_polars_df(df: Any) -> bool:
    """Check if object is a Polars DataFrame or LazyFrame."""
    return PolarsTypeMapper.is_polars_dataframe(df)


def is_polars_lazy(df: Any) -> bool:
    """Check if object is a Polars LazyFrame."""
    return PolarsTypeMapper.is_polars_lazyframe(df)


def collect_lazy(df: Any, streaming: bool = False) -> Any:
    """Collect a LazyFrame to a DataFrame if needed."""
    return PolarsTypeMapper.collect_if_lazy(df, streaming=streaming)


def convert_to_polars(df: Any, streaming: bool = False) -> Any:
    """Convert any DataFrame to Polars."""
    return DataFrameConverter.to_polars(df, streaming=streaming)


def convert_to_pandas(df: Any, streaming: bool = False) -> Any:
    """Convert any DataFrame to Pandas."""
    return DataFrameConverter.to_pandas(df, streaming=streaming)
