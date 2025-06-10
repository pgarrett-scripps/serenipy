# SereniPy

SereniPy is a Python library for parsing and processing IP2 specific MS files. Might work with some sequest file too.


## Supported File Formats

### MS2 Files
MS2 files containing mz, intensity and optionally charge
### SQT Files (Sequest Results)
- **V1.4.0**: Basic SQT format
- **V2.1.0**: Extended format with ion mobility data
- **V2.1.0_ext**: Extended format with additional TIMS scores
- **V2.1.0_robin_random**: Specialized variant

### DTASelect-filter Files
- **V2.1.12**: Basic DTASelect format
- **V2.1.12_rt**: With retention time data
- **V2.1.12_paser**: With PASER-specific fields
- **V2.1.13**: Updated format with ion mobility
- **V2.1.13_timscore**: With TIMS scoring data

### Other formats (Not tested)
census, dtaselect, project, idx

## Installation

```bash
pip install serenipy
```