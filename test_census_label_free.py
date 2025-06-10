import sys


def write_dataframes(header_df, data_dfs, output_prefix=None):
    """Write dataframes to CSV files."""
    if output_prefix is None:
        output_prefix = "census_output"
    
    # Write header dataframe
    header_file = f"{output_prefix}_header.csv"
    header_df.to_csv(header_file, index=False)
    print(f"Header information written to {header_file}")
    
    # Write data dataframes
    for exp, df in data_dfs.items():
        data_file = f"{output_prefix}_{exp.lower()}.csv"
        df.to_csv(data_file, index=False)
        print(f"{exp} data written to {data_file}")

def main():
    # Parse command-line arguments
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input_file> [output_prefix]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_prefix = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(os.path.basename(input_file))[0]
    
    # Parse file
    try:
        header_df, data_dfs = parse_census_label_free(input_file)
        
        # Print summary information
        print(f"Parsed {input_file}")
        print(f"Found {len(header_df)} header lines")
        print(f"Created {len(data_dfs)} data dataframes")
        
        # Write dataframes to CSV files
        write_dataframes(header_df, data_dfs, output_prefix)
        
        return header_df, data_dfs
    
    except Exception as e:
        print(f"Error parsing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()