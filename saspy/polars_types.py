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

import logging
from typing import Any, Dict, Optional, Union

logger = logging.getLogger('saspy')

# Try to import Polars, but don't fail if not available
try:
    import polars as pl

    POLARS_AVAILABLE = True
except ImportError:
    pl = None
    POLARS_AVAILABLE = False
    logger.debug('Polars not available. Native Polars support disabled.')


class PolarsTypeMapper:
    """
    Handles SAS <-> Polars type conversions without pandas.

    This class provides bidirectional mapping between SAS data types
    and Polars data types, enabling native Polars DataFrame support.
    """

    # Mapping from Polars dtype to SAS kind character
    # SAS kinds: 'N' = numeric, 'C' = character, 'D' = datetime, 'B' = boolean
    POLARS_TO_SAS_KIND = {
        pl.String: 'C',
        pl.Utf8: 'C',
        pl.Categorical: 'C',
        pl.Enum: 'C',
        pl.Boolean: 'B',
        pl.Date: 'D',
        pl.Datetime: 'D',
        pl.Time: 'D',
        pl.Duration: 'D',
        pl.Float32: 'N',
        pl.Float64: 'N',
        pl.Int8: 'N',
        pl.Int16: 'N',
        pl.Int32: 'N',
        pl.Int64: 'N',
        pl.UInt8: 'N',
        pl.UInt16: 'N',
        pl.UInt32: 'N',
        pl.UInt64: 'N'
    }

    # Mapping from SAS type + format to Polars dtype
    SAS_TO_POLARS = {
        'CHAR': pl.String,
        'NUM': {
            'date': pl.Date,
            'datetime': pl.Datetime,
            'time': pl.Time,
            'numeric': pl.Float64,
            'default': pl.Float64
        },
    }

    # Mapping from Polars dtype to SAS variable attributes (type, format)
    POLARS_TO_SAS = {
        pl.String: ('CHAR', None),
        pl.Utf8: ('CHAR', None),
        pl.Categorical: ('CHAR', None),
        pl.Enum: ('CHAR', None),
        pl.Boolean: ('NUM', None),
        pl.Date: ('NUM', 'E8601DA.'),
        pl.Datetime: ('NUM', 'E8601DT26.6'),
        pl.Time: ('NUM', 'E8601TM.'),
        pl.Float32: ('NUM', None),
        pl.Float64: ('NUM', None),
        pl.Int8: ('NUM', None),
        pl.Int16: ('NUM', None),
        pl.Int32: ('NUM', None),
        pl.Int64: ('NUM', None),
        pl.UInt8: ('NUM', None),
        pl.UInt16: ('NUM', None),
        pl.UInt32: ('NUM', None),
        pl.UInt64: ('NUM', None)
    }

    @classmethod
    def get_polars_dtype(cls, sas_type: str, sas_format: Optional[str] = None) -> Any:
        """
        Get Polars dtype from SAS type and format.

        :param sas_type: SAS variable type ('NUM' or 'CHAR')
        :param sas_format: SAS format string (e.g., 'DATE.', 'DATETIME.')
        :return: Polars dtype
        """
        if not POLARS_AVAILABLE:
            return None

        if sas_type == 'C' or sas_type == 'CHAR':
            return pl.String

        if sas_type == 'N' or sas_type == 'NUM':
            if sas_format:
                fmt_upper = sas_format.upper()
                if fmt_upper.endswith('.'):
                    fmt_upper = fmt_upper[:-1]
                if fmt_upper == 'DATE':
                    return pl.Date
                if fmt_upper.startswith('DDMMYY'):
                    return pl.Date
                if fmt_upper.startswith('MMDDYY'):
                    return pl.Date
                if fmt_upper.startswith('YYMMDD'):
                    return pl.Date
                if fmt_upper == 'YYQ' or fmt_upper == 'YYQR':
                    return pl.Date
                if fmt_upper in ('PDJULG', 'PDJULI', 'ENGDFTD'):
                    return pl.Date
                if fmt_upper == 'E8601DA':
                    return pl.Date
                if fmt_upper == 'DATETIME':
                    return pl.Datetime
                if (
                    fmt_upper.startswith('E8601DT')
                    or fmt_upper.startswith('B8601DT')
                    or fmt_upper.startswith('IS8601DT')
                ):
                    return pl.Datetime
                if fmt_upper == 'DATEAMPM':
                    return pl.Datetime
                if fmt_upper == 'TIME':
                    return pl.Time
                if (
                    fmt_upper.startswith('E8601TM')
                    or fmt_upper.startswith('B8601TM')
                    or fmt_upper.startswith('IS8601TM')
                ):
                    return pl.Time
                if fmt_upper == 'TOD':
                    return pl.Datetime
            if not sas_format or sas_format.upper() in (
                'BEST',
                'BEST12',
                'BEST32',
                'BEST.',
                'BEST12.',
                'BEST32.',
                'EBEST',
            ):
                return pl.Float64
            fmt_check = sas_format.upper()
            if fmt_check.startswith('$LOGICAL') or fmt_check.endswith('LOGICAL'):
                return pl.Boolean
            return pl.Float64

        return pl.String

    @classmethod
    def get_sas_attributes(cls, polars_dtype) -> tuple[str, Optional[str]]:
        """
        Get SAS type and format from Polars dtype.

        :param polars_dtype: Polars data type
        :return: Tuple of (SAS type, SAS format)
        """
        if not POLARS_AVAILABLE:
            return ('CHAR', None)

        # Check for matching type in mapping, handle nested types like pl.Datetime
        dtype_class = (
            type(polars_dtype) if not isinstance(polars_dtype, type) else polars_dtype
        )

        # Exact match or base class match
        res = cls.POLARS_TO_SAS.get(polars_dtype)
        if not res:
            res = cls.POLARS_TO_SAS.get(dtype_class, ('NUM', None))

        return res

    @classmethod
    def get_schema_kinds(cls, df: 'pl.DataFrame') -> Dict[str, str]:
        """
        Get a dictionary mapping column names to SAS kind characters.

        :param df: Polars DataFrame
        :return: Dictionary of {column_name: sas_kind}
        """
        if not POLARS_AVAILABLE or not isinstance(df, pl.DataFrame):
            return {}

        return {
            name: cls.get_sas_kind(dtype) or 'C' for name, dtype in df.schema.items()
        }

    @classmethod
    def get_schema_from_sasdata(
        cls, sas, table: str, libref: str = '', dsopts: dict = None
    ) -> Dict[str, Any]:
        """
        Get Polars schema from SAS data metadata.

        :param sas: SASsession object
        :param table: SAS table name
        :param libref: SAS libref
        :param dsopts: Dataset options
        :return: Dictionary mapping column names to Polars dtypes
        """
        if not POLARS_AVAILABLE:
            return {}

        try:
            lib = libref if libref else 'WORK'
            # Use the SASdata object's columnInfo method which returns pandas df
            sd = sas.sasdata(table, libref, dsopts=dsopts if dsopts else {})
            sd.set_results('PANDAS')
            col_info = sd.columnInfo()

            if col_info is None or len(col_info) == 0:
                return {}

            schema = {}
            for _, row in col_info.iterrows():
                var_name = row.get('Variable', row.get('Name', ''))
                var_type = row.get('Type', '')
                var_fmt = row.get('Format', '')

                if var_type.upper() in ('NUM', 'NUMERIC'):
                    schema[var_name] = cls.get_polars_dtype('NUM', var_fmt)
                else:
                    schema[var_name] = pl.String

            return schema
        except Exception:
            return {}

    @classmethod
    def get_sas_transfer_metadata(
        cls,
        df: Union['pl.DataFrame', 'pl.LazyFrame', Dict[str, Any]],
        datetimes: Dict[str, str] = None,
        outfmts: Dict[str, str] = None,
        labels: Dict[str, str] = None,
        char_lengths: Dict[str, int] = None,
        keep_outer_quotes: bool = False,
        embedded_newlines: bool = True,
        LF: str = '\x01',
        CR: str = '\x02',
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
            return {}

        schema = df if isinstance(df, dict) else df.collect_schema()

        # Prepare lookup dictionaries
        dts_upper = {k.upper(): v for k, v in (datetimes or {}).items()}
        fmt_upper = {k.upper(): v for k, v in (outfmts or {}).items()}
        lab_upper = {k.upper(): v for k, v in (labels or {}).items()}
        chr_upper = {k.upper(): v for k, v in (char_lengths or {}).items()}

        length_stmt = ''
        format_stmt = ''
        input_stmt = ''
        label_stmt = ''
        xlate_stmt = ''

        # Use formatting suitable for SAS hex constants
        lf_hex = f"'{ord(LF):02x}'x"
        cr_hex = f"'{ord(CR):02x}'x"

        for name, dtype in schema.items():
            colname = str(name).replace("'", "''")
            col_up = str(name).upper()

            input_stmt += f"input '{colname}'n "

            if col_up in lab_upper:
                label_stmt += f"label '{colname}'n = {lab_upper[col_up]};\n"

            if col_up in fmt_upper:
                format_stmt += f"'{colname}'n {fmt_upper[col_up]} "

            # Determine SAS type and attributes
            if dtype == pl.String:
                # Use provided length or default to 8
                l = chr_upper.get(col_up)
                if l is None:
                    if not isinstance(df, dict):
                        # If we have the actual dataframe, we can calculate the max length
                        try:
                            if isinstance(df, pl.DataFrame):
                                l = max(8, df[name].str.len_bytes().max() or 8)
                            else:  # LazyFrame
                                # For LazyFrame, we might not want to collect just for length
                                # Fallback to a safe default if not provided
                                l = 32767
                        except:
                            l = 8
                    else:
                        l = 8

                length_stmt += f" '{colname}'n ${l}"
                if keep_outer_quotes:
                    input_stmt += '~ '

                if embedded_newlines:
                    xlate_stmt += (
                        f" '{colname}'n = translate('{colname}'n, '0A'x, {lf_hex});\n"
                    )
                    xlate_stmt += (
                        f" '{colname}'n = translate('{colname}'n, '0D'x, {cr_hex});\n"
                    )

            elif dtype in [pl.Date, pl.Datetime, pl.Time]:
                length_stmt += f" '{colname}'n 8"
                input_stmt += ':B8601DT26.6 '

                if col_up not in dts_upper:
                    if col_up not in fmt_upper:
                        format_stmt += f"'{colname}'n E8601DT26.6 "
                else:
                    requested = dts_upper[col_up].lower()
                    if requested == 'date':
                        if col_up not in fmt_upper:
                            format_stmt += f"'{colname}'n E8601DA. "
                        xlate_stmt += f" '{colname}'n = datepart('{colname}'n);\n"
                    elif requested == 'time':
                        if col_up not in fmt_upper:
                            format_stmt += f"'{colname}'n E8601TM. "
                        xlate_stmt += f" '{colname}'n = timepart('{colname}'n);\n"
                    else:
                        if col_up not in fmt_upper:
                            format_stmt += f"'{colname}'n E8601DT26.6 "

            elif dtype == pl.Boolean:
                length_stmt += f" '{colname}'n 8"

            else:  # Numeric
                length_stmt += f" '{colname}'n 8"

            input_stmt += ';\n'

        return {
            'length': length_stmt,
            'format': format_stmt,
            'input': input_stmt,
            'label': label_stmt,
            'xlate': xlate_stmt,
        }

    @classmethod
    def convert_datetime_to_string(
        cls, df: 'pl.DataFrame', columns: list
    ) -> 'pl.DataFrame':
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
                        pl.col(col_name).dt.to_string('%Y-%m-%d').alias(col_name)
                    )
                elif dtype == pl.Datetime:
                    exprs.append(
                        pl.col(col_name)
                        .dt.to_string('%Y-%m-%dT%H:%M:%S%.6f')
                        .alias(col_name)
                    )
                elif dtype == pl.Time:
                    exprs.append(
                        pl.col(col_name).dt.to_string('%H:%M:%S%.6f').alias(col_name)
                    )
                else:
                    exprs.append(pl.col(col_name))
            else:
                exprs.append(pl.col(col_name))

        return df.with_columns(exprs)

    @classmethod
    def convert_numeric_to_boolean(cls, df: 'pl.DataFrame') -> 'pl.DataFrame':
        """
        Convert Int64 or Float64 columns that contain only 0 and 1 (plus nulls) to Boolean type.

        This handles SAS boolean columns which are stored as numeric 1/0.

        :param df: Polars DataFrame
        :return: DataFrame with boolean-like columns converted to Boolean type
        """
        if not POLARS_AVAILABLE or not isinstance(df, pl.DataFrame):
            return df

        conversions = []
        for col_name, dtype in df.schema.items():
            if dtype in (pl.Int64, pl.Float64):
                try:
                    unique_vals = df[col_name].unique()
                    unique_vals = [v for v in unique_vals if v is not None]
                    if all(v in (0, 1) for v in unique_vals):
                        conversions.append(
                            pl.col(col_name).cast(pl.Boolean).alias(col_name)
                        )
                except Exception:
                    pass

        if conversions:
            return df.with_columns(conversions)
        return df

    @classmethod
    def convert_numeric_to_integer(cls, df: 'pl.DataFrame') -> 'pl.DataFrame':
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
                    all_whole = (non_null.cast(pl.Int64).cast(pl.Float64) == non_null).all()
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
    def convert_numeric_to_integer(cls, df: 'pl.DataFrame') -> 'pl.DataFrame':
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
                    all_whole = (non_null.cast(pl.Int64).cast(pl.Float64) == non_null).all()
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
    def convert_numeric_to_integer(cls, df: 'pl.DataFrame') -> 'pl.DataFrame':
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
                    all_whole = (non_null.cast(pl.Int64).cast(pl.Float64) == non_null).all()
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
    def convert_numeric_to_integer(cls, df: 'pl.DataFrame') -> 'pl.DataFrame':
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
                    all_whole = (non_null.cast(pl.Int64).cast(pl.Float64) == non_null).all()
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
    def convert_numeric_to_integer(cls, df: 'pl.DataFrame') -> 'pl.DataFrame':
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
                    all_whole = (non_null.cast(pl.Int64).cast(pl.Float64) == non_null).all()
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
    def convert_numeric_to_integer(cls, df: 'pl.DataFrame') -> 'pl.DataFrame':
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
                    all_whole = (non_null.cast(pl.Int64).cast(pl.Float64) == non_null).all()
                    if all_whole:
                        conversions.append(
                            pl.col(col_name).cast(pl.Int64).alias(col_name)
                        )
                except Exception:
                    pass

        if conversions:
            return df.with_columns(conversions)
        return df


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


def get_sas_kind(polars_dtype) -> Optional[str]:
    """Get SAS kind character from Polars dtype."""
    return PolarsTypeMapper.get_sas_kind(polars_dtype)


def convert_to_polars(df: Any, streaming: bool = False) -> Any:
    """Convert any DataFrame to Polars."""
    return DataFrameConverter.to_polars(df, streaming=streaming)


def convert_to_pandas(df: Any, streaming: bool = False) -> Any:
    """Convert any DataFrame to Pandas."""
    return DataFrameConverter.to_pandas(df, streaming=streaming)
