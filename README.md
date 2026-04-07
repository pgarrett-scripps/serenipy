# SereniPy

[![PyPI version](https://badge.fury.io/py/serenipy.svg)](https://pypi.org/project/serenipy/)
[![Python](https://img.shields.io/pypi/pyversions/serenipy)](https://pypi.org/project/serenipy/)
[![CI](https://github.com/pgarrett-scripps/serenipy/actions/workflows/python-package.yml/badge.svg)](https://github.com/pgarrett-scripps/serenipy/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Python library for parsing and serializing mass spectrometry file formats used in [IP2](https://ip2.scripps.edu/) proteomics pipelines.

## Installation

```bash
pip install serenipy
```

## Quick Start

### MS2 Files

```python
from serenipy import from_ms2, to_ms2

with open("sample.ms2", "r") as f:
    header, spectra = from_ms2(f)

for s in spectra:
    print(s.low_scan, s.mz, s.charge, len(s.mz_spectra))

# Write back to MS2 format
ms2_string = to_ms2(header, spectra)
```

### SQT Files

```python
from serenipy import from_sqt, to_sqt

with open("results.sqt", "r") as f:
    version, header, s_lines = from_sqt(f)

for s_line in s_lines:
    for m_line in s_line.m_lines:
        print(m_line.xcorr, m_line.sequence)

# Write back to SQT format
sqt_string = to_sqt(version, header, s_lines)
```

### DTASelect-filter Files

```python
from serenipy import from_dta_select_filter, to_dta_select_filter

with open("DTASelect-filter.txt", "r") as f:
    version, head, results, tail = from_dta_select_filter(f)

for result in results:
    for protein in result.protein_lines:
        print(protein.locus_name, protein.sequence_coverage)
    for peptide in result.peptide_lines:
        print(peptide.sequence, peptide.x_corr, peptide.charge)

# Write back to DTASelect-filter format
output = to_dta_select_filter(version, head, results, tail)
```

### Census Files

```python
from serenipy import from_census

with open("census.txt", "r") as f:
    header, census_lines = from_census(f)

for line in census_lines:
    print(line.protein, line.pvalue, len(line.experiment_lines))
```

## Supported Formats

| Format | Versions | Parse | Serialize |
|--------|----------|-------|-----------|
| MS2 | Standard | `from_ms2()` | `to_ms2()` |
| SQT | V1.4.0, V2.1.0, V2.1.0_ext, V2.1.0_robin_random | `from_sqt()` | `to_sqt()` |
| DTASelect-filter | V2.1.12, V2.1.12_rt, V2.1.12_paser, V2.1.13, V2.1.13_timscore | `from_dta_select_filter()` | `to_dta_select_filter()` |
| Census | Standard | `from_census()` | - |
| Census (label-free) | Standard | `from_censuslf()` | - |

All parsers accept either a file-like object or a string as input. Format versions are auto-detected during parsing.

## Development

```bash
git clone https://github.com/pgarrett-scripps/serenipy.git
cd serenipy
uv sync
just check     # lint + ty + tests
```

## License

MIT
