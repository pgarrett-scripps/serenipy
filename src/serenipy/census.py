from dataclasses import dataclass
from io import StringIO, TextIOWrapper
from typing import Tuple, Union, List

from .utils import deserialize_val


def apply_transformation(val, t):
    if val is not None:
        val = t(val)
    return val


@dataclass
class ExperimentLine:
    num: Union[int, None]
    sequence: Union[str, None]
    file_name: Union[str, None]
    scan: Union[int, None]
    cstate: Union[int, None]
    intensity: Union[float, None]
    corrioninjection_intensity: Union[int, None]
    profile_score: Union[float, None]
    mhplus: Union[float, None]
    calc_mhplus: Union[float, None]
    total_intensity: Union[float, None]
    xcorr: Union[float, None]
    delta_cn: Union[float, None]
    dmass: Union[float, None]
    sprank: Union[int, None]
    sp_score: Union[float, None]
    redundancy: Union[int, None]
    start_range: Union[float, None]
    end_range: Union[float, None]
    retention_time: Union[float, None]
    ion_injection_time: Union[float, None]


def _deserialize_experiment_line(line_elems: list[str]) -> ExperimentLine:
    return ExperimentLine(
        num=deserialize_val(line_elems[0], lambda x: int(x.strip("[").strip("]"))),
        sequence=deserialize_val(line_elems[1], str),
        file_name=deserialize_val(line_elems[2], str),
        scan=deserialize_val(line_elems[3], int),
        cstate=deserialize_val(line_elems[4], int),
        intensity=deserialize_val(line_elems[5], float),
        corrioninjection_intensity=deserialize_val(line_elems[6], int),
        profile_score=deserialize_val(line_elems[7], float),
        mhplus=deserialize_val(line_elems[8], float),
        calc_mhplus=deserialize_val(line_elems[9], float),
        total_intensity=deserialize_val(line_elems[10], float),
        xcorr=deserialize_val(line_elems[11], float),
        delta_cn=deserialize_val(line_elems[12], float),
        dmass=deserialize_val(line_elems[13], float),
        sprank=deserialize_val(line_elems[14], int),
        sp_score=deserialize_val(line_elems[15], float),
        redundancy=deserialize_val(line_elems[16], int),
        start_range=deserialize_val(line_elems[17], float),
        end_range=deserialize_val(line_elems[18], float),
        retention_time=deserialize_val(line_elems[19], float),
        ion_injection_time=deserialize_val(line_elems[20], float),
    )


@dataclass
class CensusLine:
    norm_intensities: List[float]
    pvalue: Union[float, None]
    qvalue: Union[float, None]
    protein: Union[str, None]
    protein_description: Union[str, None]

    experiment_lines: List[ExperimentLine]


def _deserialize_census_line(line: str, census_columns: List[str]) -> CensusLine:
    line_elems = line.rstrip().split("\t")
    experiment_lines_strs = []
    for i, col_name in enumerate(census_columns):
        if col_name.startswith("NORM"):
            break
        if col_name.startswith("EXP_"):
            experiment_lines_strs.append([])
        if experiment_lines_strs:
            experiment_lines_strs[-1].append(line_elems[i])
    experiment_lines = [
        _deserialize_experiment_line(expt_strs) for expt_strs in experiment_lines_strs
    ]
    norm_intensity_strs = line_elems[i : i + len(experiment_lines)]
    norm_intensities = [
        deserialize_val(norm_intensity_strs, float)
        for norm_intensity_strs in norm_intensity_strs
    ]

    return CensusLine(
        norm_intensities=norm_intensities,
        pvalue=deserialize_val(line_elems[i + len(experiment_lines)], float),
        qvalue=deserialize_val(line_elems[i + len(experiment_lines) + 1], float),
        protein=deserialize_val(line_elems[i + len(experiment_lines) + 2], str),
        protein_description=deserialize_val(
            line_elems[i + len(experiment_lines) + 3], str
        ),
        experiment_lines=experiment_lines,
    )


def from_census(
    census_input: Union[str, TextIOWrapper, StringIO],
) -> Tuple[List[str], List[CensusLine]]:
    if type(census_input) is str:
        lines = census_input.split("\n")
    elif type(census_input) is TextIOWrapper or type(census_input) == StringIO:
        lines = census_input
    else:
        raise ValueError(f"Unsupported input type: {type(census_input)}!")
    header_lines = []
    census_lines = []

    census_columns = None
    for line in lines:
        line = line

        if line.startswith("H"):
            header_lines.append(line.rstrip())
        elif line.startswith("SLINE"):
            census_columns = line.split("\t")
        elif line.startswith("S"):
            census_lines.append(_deserialize_census_line(line, census_columns))

    return header_lines, census_lines


def to_df(census_input: Union[str, TextIOWrapper, StringIO]):
    import pandas as pd

    if type(census_input) is str:
        lines = census_input.split("\n")
    elif type(census_input) is TextIOWrapper or type(census_input) is StringIO:
        lines = census_input
    else:
        raise ValueError(f"Unsupported input type: {type(census_input)}!")

    filtered_census_lines = filter(lambda line: not line.startswith("H"), lines)
    census_string_io = StringIO("\n".join(filtered_census_lines))
    return pd.read_csv(
        census_string_io, sep="\t", index_col=False, mangle_dupe_cols=True
    )
