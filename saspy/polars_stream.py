"""
Polars Streaming engine for saspy.

This module implements the STREAM and DISK methods for bidirectional 
conversion between SAS data sets and Polars DataFrames/LazyFrames.
"""

import io
import os
import tempfile as tf
from typing import List, Any, Optional, Iterator
import logging

from .polars_types import PolarsTypeMapper, DataFrameConverter, POLARS_AVAILABLE

if POLARS_AVAILABLE:
    import polars as pl

logger = logging.getLogger('saspy')

class SASDataPolarsStream(io.RawIOBase):
    """
    A binary stream that reads from a SAS socket and provides bytes for Polars.
    This avoids materializing the entire data set in memory as a string.
    """
    def __init__(self, sock, blocksize: int = 32768):
        self.sock = sock
        self.blocksize = blocksize
        self._buffer = b""

    def readable(self):
        return True

    def readinto(self, b):
        n = len(b)
        if not self._buffer:
            try:
                self._buffer = self.sock.recv(self.blocksize)
            except Exception:
                return 0
        
        if not self._buffer:
            return 0
            
        chunk = self._buffer[:n]
        self._buffer = self._buffer[len(chunk):]
        b[:len(chunk)] = chunk
        return len(chunk)

def write_lazyframe_to_temp_csvs(df: Any, chunk_rows: int = 100000) -> List[str]:
    """Write a Polars DataFrame or LazyFrame to one or more temporary CSV files."""
    if not POLARS_AVAILABLE:
        raise ImportError("polars is not installed; install with extras 'polars'")

    # Materialize lazy with streaming enabled
    pl_df = DataFrameConverter.to_polars(df, streaming=True)

    if not isinstance(pl_df, pl.DataFrame):
        raise TypeError("write_lazyframe_to_temp_csvs expects a Polars DataFrame or LazyFrame")

    total = pl_df.height
    files = []

    for start in range(0, total, chunk_rows):
        end = min(start + chunk_rows, total)
        chunk = pl_df[start:end]
        with tf.NamedTemporaryFile(delete=False, suffix=".csv", prefix="saspy_polars_", mode="w", encoding="utf-8") as tmp:
            try:
                chunk.write_csv(tmp.name)
            except Exception:
                # fallback to pandas conversion
                try:
                    chunk.to_pandas().to_csv(tmp.name, index=False)
                except Exception as e:
                    try:
                        os.unlink(tmp.name)
                    except Exception:
                        pass
                    raise
            files.append(tmp.name)

    return files

def cleanup_temp_files(paths: List[str]) -> None:
    """Remove temporary files."""
    for p in paths:
        try:
            os.unlink(p)
        except Exception:
            pass

def sasdata2polarsSTREAM(sock, varlist: List[str], schema_overrides: dict, colsep: str = '\x02', **kwargs) -> Any:
    """
    Pipes SAS rows directly into Polars without intermediate pandas conversion using a socket.
    """
    if not POLARS_AVAILABLE:
        raise ImportError("polars is not installed")

    stream = SASDataPolarsStream(sock)
    polars_mode = kwargs.get('polars_mode', 'EAGER').upper()

    # Use Polars read_csv directly on the stream
    # Note: Polars read_csv is eager. 
    try:
        df = pl.read_csv(stream,
                        has_header=False,
                        new_columns=varlist,
                        separator=colsep,
                        quote_char='"',
                        schema_overrides=schema_overrides,
                        null_values='.',
                        ignore_errors=True)
        
        if polars_mode == 'LAZY':
            return df.lazy()
        return df
    except Exception as e:
        logger.error(f"Error in sasdata2polarsSTREAM: {e}")
        raise

def sasdata2polarsDISK(table_path: str, varlist: List[str], schema_overrides: dict, colsep: str = ',', **kwargs) -> Any:
    """
    Reads a temporary CSV file into Polars.
    """
    if not POLARS_AVAILABLE:
        raise ImportError("polars is not installed")

    polars_mode = kwargs.get('polars_mode', 'EAGER').upper()
    
    if polars_mode == 'LAZY':
        return pl.scan_csv(table_path,
                           has_header=True,
                           separator=colsep,
                           schema_overrides=schema_overrides,
                           null_values='.',
                           ignore_errors=True)
    else:
        return pl.read_csv(table_path,
                          has_header=True,
                          separator=colsep,
                          schema_overrides=schema_overrides,
                          null_values='.',
                          ignore_errors=True)

def polars2sasdataSTREAM(df: Any, sock: Any, colsep: str = '\x03', **kwargs) -> None:
    """
    Pipes Polars rows directly into SAS without intermediate pandas conversion using a socket.
    """
    if not POLARS_AVAILABLE:
        raise ImportError("polars is not installed")

    if isinstance(df, pl.LazyFrame):
        df = df.collect(streaming=True)

    # We need to ensure dates/datetimes are in a format SAS can read with B8601DT/DA
    # Polars default write_csv is generally compatible with ISO8601
    
    try:
        # If sock is a socket, we need to makefile
        import socket
        if hasattr(sock, 'makefile'):
            f = sock.makefile('wb')
        else:
            f = sock
            
        df.write_csv(f, separator=colsep, include_header=False, null_value='.', quote_style='always')
        
        if hasattr(sock, 'makefile'):
            f.close()
    except Exception as e:
        logger.error(f"Error in polars2sasdataSTREAM: {e}")
        raise
