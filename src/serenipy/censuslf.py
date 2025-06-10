from io import StringIO, TextIOWrapper
from typing import Iterable, List, Tuple, Union
import pandas as pd


def _parse_header_lines(lines):
    """Parse header (H) lines into a dataframe."""
    header_data = []
    
    for line in lines:
        if line.startswith('H\t'):
            parts = line.strip().split('\t')
            # Skip empty lines or malformed header lines
            if len(parts) < 3:
                continue
                
            # Extract header type, key, and value(s)
            h_type = parts[1]
            if len(parts) >= 4:
                key = parts[2]
                value = parts[3] if len(parts) > 3 else ""
                # Add any additional values
                if len(parts) > 4:
                    value = [value] + parts[4:]
            else:
                key = parts[2]
                value = ""
            
            header_data.append({"Type": h_type, "Key": key, "Value": value})
    
    # Create dataframe from header data
    if header_data:
        return pd.DataFrame(header_data)
    else:
        return pd.DataFrame(columns=["Type", "Key", "Value"])

def _parse_sline_definition(sline_def):
    """Parse the SLINE definition to identify column names and experiment structure."""
    parts = sline_def.strip().split('\t')
    
    # Get column names
    column_names = parts[1:]  # Skip the 'SLINE' prefix
    
    # Identify experiment columns and their indices
    exp_columns = {}
    exp_indices = {}
    common_columns = []
    
    curr_exp = None
    for i, col in enumerate(column_names):
        if col.startswith('EXP_'):
            curr_exp = col
            exp_columns[curr_exp] = []
            exp_indices[curr_exp] = []
        elif col in ['NORM_INTENSITY1', 'NORM_INTENSITY2', 'NORM_INTENSITY3', 
                    'NORM_INTENSITY4', 'NORM_INTENSITY5', 'NORM_INTENSITY6',
                    'PVALUE', 'QVALUE', 'PROTEIN', 'PROTEIN DESCRIPTION']:
            common_columns.append((i+1, col))  # +1 to account for the 'S' column
        elif curr_exp is not None:
            exp_columns[curr_exp].append(col)
            exp_indices[curr_exp].append(i+1)  # +1 to account for the 'S' column
    
    return {
        'column_names': column_names,
        'exp_columns': exp_columns,
        'exp_indices': exp_indices,
        'common_columns': common_columns
    }

def _parse_data_lines(lines, sline_info):
    """Parse S lines (data lines) into multiple dataframes, one per experiment."""
    # Prepare dataframes for each experiment and one for common columns
    exp_dfs = {}
    for exp in sline_info['exp_columns']:
        cols = sline_info['exp_columns'][exp]
        # Add experiment identifier column
        exp_dfs[exp] = pd.DataFrame(columns=['ID'] + cols)
    
    # Prepare dataframe for common columns
    common_cols = [col for _, col in sline_info['common_columns']]
    common_df = pd.DataFrame(columns=['ID'] + common_cols)
    
    # Parse data lines
    for line in lines:
        if line.startswith('S\t'):
            parts = line.strip().split('\t')
            # Skip if line is too short
            if len(parts) < 2:
                continue
            
            # Extract line ID (we'll use this to join tables later if needed)
            line_id = parts[0] + '_' + parts[1]  # Something like "S_[1]"
            
            # Extract data for each experiment
            for exp, indices in sline_info['exp_indices'].items():
                # Create a row with the experiment's columns and values
                row = {'ID': line_id}
                for col_idx, col_name in zip(indices, sline_info['exp_columns'][exp]):
                    if col_idx < len(parts):
                        row[col_name] = parts[col_idx]
                    else:
                        row[col_name] = None
                
                # Add row to dataframe
                exp_dfs[exp] = pd.concat([exp_dfs[exp], pd.DataFrame([row])], ignore_index=True)
            
            # Extract common columns (NORM_INTENSITY, PVALUE, etc.)
            common_row = {'ID': line_id}
            for col_idx, col_name in sline_info['common_columns']:
                if col_idx < len(parts):
                    common_row[col_name] = parts[col_idx]
                else:
                    common_row[col_name] = None
            
            # Add common row to dataframe
            common_df = pd.concat([common_df, pd.DataFrame([common_row])], ignore_index=True)
    
    # Also create a combined dataframe with all experiment data
    all_exp_dfs = {**exp_dfs, 'COMMON': common_df}
    
    return all_exp_dfs

def _parse_censuslf(lines: Iterable[str]) -> Tuple[pd.DataFrame, List[pd.DataFrame]]:
    """
    Parse a census-label-free file into multiple dataframes.
    
    Returns:
        header_df: Dataframe with header information
        data_dfs: Dictionary of dataframes, one per experiment plus one for common columns
    """
    # Read file
    
    # Extract header lines, SLINE definition, and data lines
    header_lines = []
    sline_def = None
    data_lines = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('H\t'):
            header_lines.append(line)
        elif line.startswith('SLINE\t'):
            sline_def = line
        elif line.startswith('S\t'):
            data_lines.append(line)
    
    # Parse header lines
    header_df = _parse_header_lines(header_lines)
    
    # Parse SLINE definition
    if sline_def is None:
        raise ValueError("No SLINE definition found in the file.")
    
    sline_info = _parse_sline_definition(sline_def)
    
    # Parse data lines
    data_dfs = _parse_data_lines(data_lines, sline_info)
    
    return header_df, data_dfs
    

def from_censuslf(census_input: Union[str, TextIOWrapper, StringIO]) -> Tuple[pd.DataFrame, List[pd.DataFrame]]:
    """
    Parse a census-label-free file into multiple dataframes.
    
    Args:
        census_input: Path to the census-label-free file or a file-like object.
    
    Returns:
        header_df: Dataframe with header information
        data_dfs: Dictionary of dataframes, one per experiment plus one for common columns
    """
    if isinstance(census_input, str):
        return _parse_censuslf(census_input)
    else:
        raise ValueError(f"Unsupported input type: {type(census_input)}")

def to_censuslf(header_df: pd.DataFrame, data_dfs: List[pd.DataFrame], output_prefix: str) -> None:
    pass
    
    