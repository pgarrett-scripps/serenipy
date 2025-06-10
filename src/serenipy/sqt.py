from io import StringIO, TextIOWrapper
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Tuple, Union

from .utils import serialize_val, deserialize_val


class SqtVersion(Enum):
    V1_4_0 = auto()
    V2_1_0 = auto()
    V2_1_0_ext = auto()
    V2_1_0_robin_random = auto()


@dataclass
class LLine:
    locus_name: str
    peptide_index_in_protein_sequence: int
    peptide_sequence: str


l_line_V1_4_0_template = (
    "L\t{locus_name}\t{peptide_index_in_protein_sequence}\t{peptide_sequence}\n"
)
l_line_V2_1_0_template = (
    "L\t{locus_name}\t{peptide_index_in_protein_sequence}\t{peptide_sequence}\n"
)
l_line_V2_1_0_ext_template = (
    "L\t{locus_name}\t{peptide_index_in_protein_sequence}\t{peptide_sequence}\n"
)
l_line_V2_1_0_robin_random_template = (
    "L\t{locus_name}\t{peptide_index_in_protein_sequence}\t{peptide_sequence}\n"
)


def _deserialize_l_line(line: str, sqt_version: SqtVersion) -> LLine:
    line_elems = line.rstrip().split("\t")
    if sqt_version == SqtVersion.V1_4_0:
        return LLine(
            locus_name=deserialize_val(line_elems[1], str),
            peptide_index_in_protein_sequence=deserialize_val(line_elems[2], int),
            peptide_sequence=deserialize_val(line_elems[3], str),
        )
    elif sqt_version == SqtVersion.V2_1_0:
        return LLine(
            locus_name=deserialize_val(line_elems[1], str),
            peptide_index_in_protein_sequence=deserialize_val(line_elems[2], int),
            peptide_sequence=deserialize_val(line_elems[3], str),
        )
    elif sqt_version == SqtVersion.V2_1_0_ext:
        return LLine(
            locus_name=deserialize_val(line_elems[1], str),
            peptide_index_in_protein_sequence=deserialize_val(line_elems[2], int),
            peptide_sequence=deserialize_val(line_elems[3], str),
        )
    elif sqt_version == SqtVersion.V2_1_0_robin_random:
        return LLine(
            locus_name=deserialize_val(line_elems[1], str),
            peptide_index_in_protein_sequence=deserialize_val(line_elems[2], int),
            peptide_sequence=deserialize_val(line_elems[3], str),
        )
    else:
        raise ValueError(f"Unsupported Sqt Version: {sqt_version}!")


def _serialize_l_line(line: LLine, sqt_version: SqtVersion) -> str:
    if sqt_version == SqtVersion.V1_4_0:
        return l_line_V1_4_0_template.format(
            locus_name=serialize_val(line.locus_name),
            peptide_index_in_protein_sequence=serialize_val(
                line.peptide_index_in_protein_sequence
            ),
            peptide_sequence=serialize_val(line.peptide_sequence),
        )
    elif sqt_version == SqtVersion.V2_1_0:
        return l_line_V2_1_0_template.format(
            locus_name=serialize_val(line.locus_name),
            peptide_index_in_protein_sequence=serialize_val(
                line.peptide_index_in_protein_sequence
            ),
            peptide_sequence=serialize_val(line.peptide_sequence),
        )
    elif sqt_version == SqtVersion.V2_1_0_ext:
        return l_line_V2_1_0_ext_template.format(
            locus_name=serialize_val(line.locus_name),
            peptide_index_in_protein_sequence=serialize_val(
                line.peptide_index_in_protein_sequence
            ),
            peptide_sequence=serialize_val(line.peptide_sequence),
        )
    elif sqt_version == SqtVersion.V2_1_0_robin_random:
        return l_line_V2_1_0_robin_random_template.format(
            locus_name=serialize_val(line.locus_name),
            peptide_index_in_protein_sequence=serialize_val(
                line.peptide_index_in_protein_sequence
            ),
            peptide_sequence=serialize_val(line.peptide_sequence),
        )
    else:
        raise ValueError(f"Unsupported Sqt Version: {sqt_version}!")


@dataclass
class MLine:
    xcorr_rank: Union[int, None]
    sp_rank: Union[int, None]
    calculated_mass: Union[float, None]
    delta_cn: Union[float, None]
    xcorr: Union[float, None]
    sp: Union[float, None]
    matched_ions: Union[int, None]
    expected_ions: Union[int, None]
    sequence: Union[str, None]
    validation_status: Union[str, None]
    predicted_ook0: Union[float, None]
    tims_score: Union[float, None]
    tims_b_score_m2: Union[float, None]
    tims_b_score_best_m: Union[float, None]

    l_lines: List[LLine] = field(default_factory=list)


m_line_V1_4_0_template = (
    "M\t{xcorr_rank}\t{sp_rank}\t{calculated_mass}\t{delta_cn}\t{xcorr}\t{sp}\t{matched_ions}"
    "\t{expected_ions}\t{sequence}\t{validation_status}\n"
)
m_line_V2_1_0_template = (
    "M\t{xcorr_rank}\t{sp_rank}\t{calculated_mass}\t{delta_cn}\t{xcorr}\t{sp}\t{matched_ions}"
    "\t{expected_ions}\t{sequence}\t{validation_status}\t{predicted_ook0}\t{tims_score}\n"
)
m_line_V2_1_0_ext_template = (
    "M\t{xcorr_rank}\t{sp_rank}\t{calculated_mass}\t{delta_cn}\t{xcorr}\t{sp}"
    "\t{matched_ions}\t{expected_ions}\t{sequence}\t{validation_status}\t{predicted_ook0}"
    "\t{tims_score}\t{tims_b_score_m2}\t{tims_b_score_best_m}\n"
)
m_line_V2_1_0_robin_random_template = (
    "M\t{xcorr_rank}\t{sp_rank}\t{calculated_mass}\t{delta_cn}\t{xcorr}\t{sp}"
    "\t{matched_ions}\t{expected_ions}\t{sequence}\t{validation_status}\t{predicted_ook0}"
    "\t{tims_score}\n"
)


def _deserialize_m_line(line: str, sqt_version: SqtVersion) -> MLine:
    line_elems = line.rstrip().split("\t")
    if sqt_version == SqtVersion.V1_4_0:
        return MLine(
            xcorr_rank=deserialize_val(line_elems[1], int),
            sp_rank=deserialize_val(line_elems[2], int),
            calculated_mass=deserialize_val(line_elems[3], float),
            delta_cn=deserialize_val(line_elems[4], float),
            xcorr=deserialize_val(line_elems[5], float),
            sp=deserialize_val(line_elems[6], float),
            matched_ions=deserialize_val(line_elems[7], int),
            expected_ions=deserialize_val(line_elems[8], int),
            sequence=deserialize_val(line_elems[9], str),
            validation_status=deserialize_val(line_elems[10], str),
            predicted_ook0=None,
            tims_score=None,
            tims_b_score_m2=None,
            tims_b_score_best_m=None,
        )
    elif sqt_version == SqtVersion.V2_1_0:
        return MLine(
            xcorr_rank=deserialize_val(line_elems[1], int),
            sp_rank=deserialize_val(line_elems[2], int),
            calculated_mass=deserialize_val(line_elems[3], float),
            delta_cn=deserialize_val(line_elems[4], float),
            xcorr=deserialize_val(line_elems[5], float),
            sp=deserialize_val(line_elems[6], float),
            matched_ions=deserialize_val(line_elems[7], int),
            expected_ions=deserialize_val(line_elems[8], int),
            sequence=deserialize_val(line_elems[9], str),
            validation_status=deserialize_val(line_elems[10], str),
            predicted_ook0=deserialize_val(line_elems[11], float),
            tims_score=deserialize_val(line_elems[12], float),
            tims_b_score_m2=None,
            tims_b_score_best_m=None,
        )
    elif sqt_version == SqtVersion.V2_1_0_ext:
        return MLine(
            xcorr_rank=deserialize_val(line_elems[1], int),
            sp_rank=deserialize_val(line_elems[2], int),
            calculated_mass=deserialize_val(line_elems[3], float),
            delta_cn=deserialize_val(line_elems[4], float),
            xcorr=deserialize_val(line_elems[5], float),
            sp=deserialize_val(line_elems[6], float),
            matched_ions=deserialize_val(line_elems[7], int),
            expected_ions=deserialize_val(line_elems[8], int),
            sequence=deserialize_val(line_elems[9], str),
            validation_status=deserialize_val(line_elems[10], str),
            predicted_ook0=deserialize_val(line_elems[11], float),
            tims_score=deserialize_val(line_elems[12], float),
            tims_b_score_m2=deserialize_val(line_elems[13], float),
            tims_b_score_best_m=deserialize_val(line_elems[14], float),
        )
    elif sqt_version == SqtVersion.V2_1_0_robin_random:
        return MLine(
            xcorr_rank=deserialize_val(line_elems[1], int),
            sp_rank=deserialize_val(line_elems[2], int),
            calculated_mass=deserialize_val(line_elems[3], float),
            delta_cn=deserialize_val(line_elems[4], float),
            xcorr=deserialize_val(line_elems[5], float),
            sp=deserialize_val(line_elems[6], float),
            matched_ions=deserialize_val(line_elems[7], int),
            expected_ions=deserialize_val(line_elems[8], int),
            sequence=deserialize_val(line_elems[9], str),
            validation_status=deserialize_val(line_elems[10], str),
            predicted_ook0=deserialize_val(line_elems[11], float),
            tims_score=deserialize_val(line_elems[12], float),
            tims_b_score_m2=None,
            tims_b_score_best_m=None,
        )
    else:
        raise ValueError(f"Unsupported Sqt Version: {sqt_version}!")


def _serialize_m_line(line: MLine, sqt_version: SqtVersion) -> str:
    if sqt_version == SqtVersion.V1_4_0:
        return m_line_V1_4_0_template.format(
            xcorr_rank=serialize_val(line.xcorr_rank),
            sp_rank=serialize_val(line.sp_rank),
            calculated_mass=serialize_val(line.calculated_mass, 5),
            delta_cn=serialize_val(line.delta_cn, 4),
            xcorr=serialize_val(line.xcorr, 4),
            sp=serialize_val(line.sp),
            matched_ions=serialize_val(line.matched_ions),
            expected_ions=serialize_val(line.expected_ions),
            sequence=serialize_val(line.sequence),
            validation_status=serialize_val(line.validation_status),
        )
    elif sqt_version == SqtVersion.V2_1_0:
        return m_line_V2_1_0_template.format(
            xcorr_rank=serialize_val(line.xcorr_rank),
            sp_rank=serialize_val(line.sp_rank),
            calculated_mass=serialize_val(line.calculated_mass, 5),
            delta_cn=serialize_val(line.delta_cn, 4),
            xcorr=serialize_val(line.xcorr, 4),
            sp=serialize_val(line.sp, 3),
            matched_ions=serialize_val(line.matched_ions),
            expected_ions=serialize_val(line.expected_ions),
            sequence=serialize_val(line.sequence),
            validation_status=serialize_val(line.validation_status),
            predicted_ook0=serialize_val(line.predicted_ook0, 4),
            tims_score=serialize_val(line.tims_score, 4),
        )
    elif sqt_version == SqtVersion.V2_1_0_ext:
        return m_line_V2_1_0_ext_template.format(
            xcorr_rank=serialize_val(line.xcorr_rank),
            sp_rank=serialize_val(line.sp_rank),
            calculated_mass=serialize_val(line.calculated_mass, 5),
            delta_cn=serialize_val(line.delta_cn, 4),
            xcorr=serialize_val(line.xcorr, 4),
            sp=serialize_val(line.sp, 3),
            matched_ions=serialize_val(line.matched_ions),
            expected_ions=serialize_val(line.expected_ions),
            sequence=serialize_val(line.sequence),
            validation_status=serialize_val(line.validation_status),
            predicted_ook0=serialize_val(line.predicted_ook0, 4),
            tims_score=serialize_val(line.tims_score, 4),
            tims_b_score_m2=serialize_val(line.tims_b_score_m2, 4),
            tims_b_score_best_m=serialize_val(line.tims_b_score_best_m, 4),
        )
    elif sqt_version == SqtVersion.V2_1_0_robin_random:
        return m_line_V2_1_0_robin_random_template.format(
            xcorr_rank=serialize_val(line.xcorr_rank),
            sp_rank=serialize_val(line.sp_rank),
            calculated_mass=serialize_val(line.calculated_mass, 5),
            delta_cn=serialize_val(line.delta_cn, 4),
            xcorr=serialize_val(line.xcorr, 4),
            sp=serialize_val(line.sp, 3),
            matched_ions=serialize_val(line.matched_ions),
            expected_ions=serialize_val(line.expected_ions),
            sequence=serialize_val(line.sequence),
            validation_status=serialize_val(line.validation_status),
            predicted_ook0=serialize_val(line.predicted_ook0, 4),
            tims_score=serialize_val(line.tims_score, 4),
        )
    else:
        raise ValueError(f"Unsupported Sqt Version: {sqt_version}!")


@dataclass
class SLine:
    low_scan: Union[int, None]
    high_scan: Union[int, None]
    charge: Union[int, None]
    process_time: Union[int, None]
    server: Union[str, None]
    experimental_mass: Union[float, None]
    total_ion_intensity: Union[float, None]
    lowest_sp: Union[float, None]
    number_matches: Union[int, None]
    experimental_ook0: Union[float, None]
    experimental_mz: Union[float, None]
    corrected_ook0: Union[float, None]

    m_lines: List[MLine] = field(default_factory=list)


s_line_V1_4_0_template = (
    "S\t{low_scan}\t{high_scan}\t{charge}\t{process_time}\t{server}\t{experimental_mass}"
    "\t{total_ion_intensity}\t{lowest_sp}\t{number_matches}\n"
)
s_line_V2_1_0_template = (
    "S\t{low_scan}\t{high_scan}\t{charge}\t{process_time}\t{server}\t{experimental_mass}"
    "\t{total_ion_intensity}\t{lowest_sp}\t{number_matches}\t{experimental_ook0}\n"
)
s_line_V2_1_0_ext_template = (
    "S\t{low_scan}\t{high_scan}\t{charge}\t{process_time}\t{server}\t{experimental_mass}"
    "\t{total_ion_intensity}\t{lowest_sp}\t{number_matches}\t{experimental_ook0}"
    "\t{experimental_mz}\t{corrected_ook0}\n"
)
s_line_V2_1_0_robin_random_template = (
    "S\t{low_scan}\t{high_scan}\t{charge}\t{process_time}\t{server}\t{experimental_mass}"
    "\t{total_ion_intensity}\t{lowest_sp}\t{number_matches}\t{experimental_ook0}"
    "\t{experimental_mz}\n"
)


def _deserialize_s_line(line: str, sqt_version: SqtVersion) -> SLine:
    line_elems = line.rstrip().split("\t")
    if sqt_version == SqtVersion.V1_4_0:
        return SLine(
            low_scan=deserialize_val(line_elems[1], int),
            high_scan=deserialize_val(line_elems[2], int),
            charge=deserialize_val(line_elems[3], int),
            process_time=deserialize_val(line_elems[4], int),
            server=deserialize_val(line_elems[5], str),
            experimental_mass=deserialize_val(line_elems[6], float),
            total_ion_intensity=deserialize_val(line_elems[7], float),
            lowest_sp=deserialize_val(line_elems[8], float),
            number_matches=deserialize_val(line_elems[9], int),
            experimental_ook0=None,
            experimental_mz=None,
            corrected_ook0=None,
        )
    elif sqt_version == SqtVersion.V2_1_0:
        return SLine(
            low_scan=deserialize_val(line_elems[1], int),
            high_scan=deserialize_val(line_elems[2], int),
            charge=deserialize_val(line_elems[3], int),
            process_time=deserialize_val(line_elems[4], int),
            server=deserialize_val(line_elems[5], str),
            experimental_mass=deserialize_val(line_elems[6], float),
            total_ion_intensity=deserialize_val(line_elems[7], float),
            lowest_sp=deserialize_val(line_elems[8], float),
            number_matches=deserialize_val(line_elems[9], int),
            experimental_ook0=deserialize_val(line_elems[10], float),
            experimental_mz=None,
            corrected_ook0=None,
        )
    elif sqt_version == SqtVersion.V2_1_0_ext:
        return SLine(
            low_scan=deserialize_val(line_elems[1], int),
            high_scan=deserialize_val(line_elems[2], int),
            charge=deserialize_val(line_elems[3], int),
            process_time=deserialize_val(line_elems[4], int),
            server=deserialize_val(line_elems[5], str),
            experimental_mass=deserialize_val(line_elems[6], float),
            total_ion_intensity=deserialize_val(line_elems[7], float),
            lowest_sp=deserialize_val(line_elems[8], float),
            number_matches=deserialize_val(line_elems[9], int),
            experimental_ook0=deserialize_val(line_elems[10], float),
            experimental_mz=deserialize_val(line_elems[11], float),
            corrected_ook0=deserialize_val(line_elems[12], float),
        )
    elif sqt_version == SqtVersion.V2_1_0_robin_random:
        return SLine(
            low_scan=deserialize_val(line_elems[1], int),
            high_scan=deserialize_val(line_elems[2], int),
            charge=deserialize_val(line_elems[3], int),
            process_time=deserialize_val(line_elems[4], int),
            server=deserialize_val(line_elems[5], str),
            experimental_mass=deserialize_val(line_elems[6], float),
            total_ion_intensity=deserialize_val(line_elems[7], float),
            lowest_sp=deserialize_val(line_elems[8], float),
            number_matches=deserialize_val(line_elems[9], int),
            experimental_ook0=deserialize_val(line_elems[10], float),
            experimental_mz=deserialize_val(line_elems[11], float),
            corrected_ook0=None,
        )
    else:
        raise ValueError(f"Unsupported Sqt Version: {sqt_version}!")


def _serialize_s_line(line: SLine, sqt_version: SqtVersion) -> str:
    if sqt_version == SqtVersion.V1_4_0:
        return s_line_V1_4_0_template.format(
            low_scan=serialize_val(line.low_scan),
            high_scan=serialize_val(line.high_scan),
            charge=serialize_val(line.charge),
            process_time=serialize_val(line.process_time),
            server=serialize_val(line.server),
            experimental_mass=serialize_val(line.experimental_mass, 5),
            total_ion_intensity=serialize_val(line.total_ion_intensity, 2),
            lowest_sp=serialize_val(line.lowest_sp, 4),
            number_matches=serialize_val(line.number_matches),
        )
    elif sqt_version == SqtVersion.V2_1_0:
        return s_line_V2_1_0_template.format(
            low_scan=serialize_val(line.low_scan),
            high_scan=serialize_val(line.high_scan),
            charge=serialize_val(line.charge),
            process_time=serialize_val(line.process_time),
            server=serialize_val(line.server),
            experimental_mass=serialize_val(line.experimental_mass, 5),
            total_ion_intensity=serialize_val(line.total_ion_intensity, 2),
            lowest_sp=serialize_val(line.lowest_sp, 4),
            number_matches=serialize_val(line.number_matches),
            experimental_ook0=serialize_val(line.experimental_ook0, 4),
        )
    elif sqt_version == SqtVersion.V2_1_0_ext:
        return s_line_V2_1_0_ext_template.format(
            low_scan=serialize_val(line.low_scan),
            high_scan=serialize_val(line.high_scan),
            charge=serialize_val(line.charge),
            process_time=serialize_val(line.process_time),
            server=serialize_val(line.server),
            experimental_mass=serialize_val(line.experimental_mass, 5),
            total_ion_intensity=serialize_val(line.total_ion_intensity, 2),
            lowest_sp=serialize_val(line.lowest_sp, 4),
            number_matches=serialize_val(line.number_matches),
            experimental_ook0=serialize_val(line.experimental_ook0, 4),
            experimental_mz=serialize_val(line.experimental_mz, 4),
            corrected_ook0=serialize_val(line.corrected_ook0, 4),
        )
    elif sqt_version == SqtVersion.V2_1_0_robin_random:
        return s_line_V2_1_0_robin_random_template.format(
            low_scan=serialize_val(line.low_scan),
            high_scan=serialize_val(line.high_scan),
            charge=serialize_val(line.charge),
            process_time=serialize_val(line.process_time),
            server=serialize_val(line.server),
            experimental_mass=serialize_val(line.experimental_mass, 5),
            total_ion_intensity=serialize_val(line.total_ion_intensity, 2),
            lowest_sp=serialize_val(line.lowest_sp, 4),
            number_matches=serialize_val(line.number_matches),
            experimental_ook0=serialize_val(line.experimental_ook0, 4),
            experimental_mz=serialize_val(line.experimental_mz, 4),
        )
    else:
        raise ValueError(f"Unsupported Sqt Version: {sqt_version}!")


def determine_sqt_version(s_line: str) -> SqtVersion:
    line_elems = s_line.rstrip().split("\t")

    if len(line_elems) == 10:
        return SqtVersion.V1_4_0
    elif len(line_elems) == 11:
        return SqtVersion.V2_1_0
    elif len(line_elems) == 13:
        return SqtVersion.V2_1_0_ext
    elif len(line_elems) == 12:
        return SqtVersion.V2_1_0_robin_random
    else:
        raise ValueError(f"Cannot parse version from s_line: {s_line}!")


def from_sqt(
    sqt_input: Union[str, TextIOWrapper, StringIO],
) -> Tuple[SqtVersion, List[str], List[SLine]]:
    if type(sqt_input) is str:
        lines = sqt_input.split("\n")
    elif type(sqt_input) is TextIOWrapper or type(sqt_input) is StringIO:
        lines = sqt_input
    else:
        raise ValueError(f"Unsupported input type: {type(sqt_input)}!")

    version = None
    h_lines, s_lines = [], []
    for line in lines:

        if line == "" or line == "\n":
            continue

        if line.startswith("H"):
            h_lines.append(line)
        elif line.startswith("S"):
            if version is None:
                version = determine_sqt_version(line)
                print(f"Version: {version}")
            s_lines.append(_deserialize_s_line(line, version))
        elif line.startswith("M"):
            s_lines[-1].m_lines.append(_deserialize_m_line(line, version))
        elif line.startswith("L"):
            s_lines[-1].m_lines[-1].l_lines.append(_deserialize_l_line(line, version))
    return version, h_lines, s_lines


def to_sqt(version: SqtVersion, h_lines: List[str], s_lines: List[SLine]) -> str:
    lines = []
    for h_line in h_lines:
        if h_line.endswith("\n"):
            lines.append(h_line)
        else:
            lines.append(h_line + "\n")

    for s_line in s_lines:
        lines.append(_serialize_s_line(s_line, version))
        for m_line in s_line.m_lines:
            lines.append(_serialize_m_line(m_line, version))
            for l_line in m_line.l_lines:
                lines.append(_serialize_l_line(l_line, version))
        lines.append("\n")
    return "".join(lines[:-1]).rstrip("\n")
