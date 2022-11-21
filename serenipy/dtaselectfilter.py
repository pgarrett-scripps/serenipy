from __future__ import annotations

import _io
from dataclasses import dataclass
from enum import Enum, auto

from .utils import serialize_val, deserialize_val


class DtaSelectFilterVersion(Enum):
    V2_1_12 = auto()
    V2_1_12_paser = auto()
    V2_1_13 = auto()
    V2_1_13_timscore = auto()


@dataclass(slots=True)
class PeptideLine:
    unique: str | None
    file_name: str | None
    x_corr: float | None
    delta_cn: float | None
    conf: float | None
    mass_plus_hydrogen: float | None
    calc_mass_plus_hydrogen: float | None
    ppm: float | None
    total_intensity: float | None
    spr: int | None
    ion_proportion: float | None
    redundancy: int | None
    sequence: str | None
    prob_score: float | None
    pi: float | None
    measured_im_value: float | None
    predicted_im_value: float | None
    im_score: float | None
    ret_time: float | None
    ptm_index: str | None
    ptm_index_protein_list: str | None
    experimental_mz: float | None
    corrected_1k0: float | None
    ion_mobility: float | None

    @property
    def file_path(self) -> str | None:
        if self.file_name:
            return str(self.file_name.split('.')[0])
        return None

    @property
    def low_scan(self) -> int | None:
        if self.file_name:
            return int(self.file_name.split('.')[1])
        return None

    @property
    def high_scan(self) -> int | None:
        if self.file_name:
            return int(self.file_name.split('.')[2])
        return None

    @property
    def charge(self) -> int | None:
        if self.file_name:
            return int(self.file_name.split('.')[3])
        return None


peptide_line_V2_1_12_template = '{unique}\t{file_name}\t{x_corr}\t{delta_cn}\t{conf}\t{mass_plus_hydrogen}' \
                                '\t{calc_mass_plus_hydrogen}\t{total_intensity}\t{spr}\t{prob_score}' \
                                '\t{ion_proportion}\t{redundancy}\t{sequence}\n'
peptide_line_V2_1_12_paser_template = '{unique}\t{file_name}\t{x_corr}\t{delta_cn}\t{conf}\t{mass_plus_hydrogen}' \
                                      '\t{calc_mass_plus_hydrogen}\t{ppm}\t{total_intensity}\t{spr}\t{prob_score}' \
                                      '\t{pi}\t{ion_proportion}\t{redundancy}\t{sequence}\t{ret_time}\t{ptm_index}' \
                                      '\t{ptm_index_protein_list}\n'
peptide_line_V2_1_13_template = '{unique}\t{file_name}\t{x_corr}\t{delta_cn}\t{conf}\t{mass_plus_hydrogen}' \
                                '\t{calc_mass_plus_hydrogen}\t{ppm}\t{total_intensity}\t{spr}\t{prob_score}\t{pi}' \
                                '\t{ion_proportion}\t{redundancy}\t{measured_im_value}\t{predicted_im_value}' \
                                '\t{im_score}\t{sequence}\n'
peptide_line_V2_1_13_timscore_template = '{unique}\t{file_name}\t{x_corr}\t{delta_cn}\t{conf}\t{mass_plus_hydrogen}' \
                                         '\t{calc_mass_plus_hydrogen}\t{ppm}\t{total_intensity}\t{spr}\t{prob_score}' \
                                         '\t{pi}\t{ion_proportion}\t{redundancy}\t{measured_im_value}' \
                                         '\t{predicted_im_value}\t{im_score}\t{sequence}\t{experimental_mz}' \
                                         '\t{corrected_1k0}\t{ion_mobility}\t{ret_time}\t{ptm_index}' \
                                         '\t{ptm_index_protein_list}\n'


def _serialize_peptide_line(line: PeptideLine, version: DtaSelectFilterVersion) -> str:
    if version == DtaSelectFilterVersion.V2_1_12:
        return peptide_line_V2_1_12_template.format(
                           unique=serialize_val(line.unique),
                           file_name=serialize_val(line.file_name),
                           x_corr=serialize_val(line.x_corr, 4),
                           delta_cn=serialize_val(line.delta_cn, 4),
                           conf=serialize_val(line.conf, 1),
                           mass_plus_hydrogen=serialize_val(line.mass_plus_hydrogen, 5),
                           calc_mass_plus_hydrogen=serialize_val(line.calc_mass_plus_hydrogen, 5),
                           total_intensity=serialize_val(line.total_intensity),
                           spr=serialize_val(line.spr),
                           prob_score=serialize_val(line.prob_score),
                           ion_proportion=serialize_val(line.ion_proportion),
                           redundancy=serialize_val(line.redundancy),
                           sequence=serialize_val(line.sequence),
                           )
    elif version == DtaSelectFilterVersion.V2_1_12_paser:
        return peptide_line_V2_1_12_paser_template.format(
                           unique=serialize_val(line.unique),
                           file_name=serialize_val(line.file_name),
                           x_corr=serialize_val(line.x_corr, 4),
                           delta_cn=serialize_val(line.delta_cn, 4),
                           conf=serialize_val(line.conf, 1),
                           mass_plus_hydrogen=serialize_val(line.mass_plus_hydrogen, 5),
                           calc_mass_plus_hydrogen=serialize_val(line.calc_mass_plus_hydrogen, 5),
                           ppm=serialize_val(line.ppm, 1),
                           total_intensity=serialize_val(line.total_intensity, 1),
                           spr=serialize_val(line.spr),
                           prob_score=serialize_val(line.prob_score, 7),
                           pi=serialize_val(line.pi, 2),
                           ion_proportion=serialize_val(line.ion_proportion, 2),
                           redundancy=serialize_val(line.redundancy),
                           sequence=serialize_val(line.sequence),
                           ret_time=serialize_val(line.ret_time, 4),
                           ptm_index=serialize_val(line.ptm_index),
                           ptm_index_protein_list=serialize_val(line.ptm_index_protein_list),
                           )
    elif version == DtaSelectFilterVersion.V2_1_13:
        return peptide_line_V2_1_13_template.format(
                           unique=serialize_val(line.unique),
                           file_name=serialize_val(line.file_name),
                           x_corr=serialize_val(line.x_corr, 4),
                           delta_cn=serialize_val(line.delta_cn, 4),
                           conf=serialize_val(line.conf, 14),
                           mass_plus_hydrogen=serialize_val(line.mass_plus_hydrogen, 5),
                           calc_mass_plus_hydrogen=serialize_val(line.calc_mass_plus_hydrogen, 5),
                           ppm=serialize_val(line.ppm, 1),
                           total_intensity=serialize_val(line.total_intensity, 1),
                           spr=serialize_val(line.spr),
                           prob_score=serialize_val(line.prob_score, 3),
                           pi=serialize_val(line.pi, 2),
                           ion_proportion=serialize_val(line.ion_proportion, 1),
                           redundancy=serialize_val(line.redundancy),
                           measured_im_value=serialize_val(line.measured_im_value, 4),
                           predicted_im_value=serialize_val(line.predicted_im_value, 16),
                           im_score=serialize_val(line.im_score, 4),
                           sequence=serialize_val(line.sequence),
                           )
    elif version == DtaSelectFilterVersion.V2_1_13_timscore:
        return peptide_line_V2_1_13_timscore_template.format(
                           unique=serialize_val(line.unique),
                           file_name=serialize_val(line.file_name),
                           x_corr=serialize_val(line.x_corr),
                           delta_cn=serialize_val(line.delta_cn),
                           conf=serialize_val(line.conf),
                           mass_plus_hydrogen=serialize_val(line.mass_plus_hydrogen),
                           calc_mass_plus_hydrogen=serialize_val(line.calc_mass_plus_hydrogen),
                           ppm=serialize_val(line.ppm),
                           total_intensity=serialize_val(line.total_intensity),
                           spr=serialize_val(line.spr),
                           prob_score=serialize_val(line.prob_score),
                           pi=serialize_val(line.pi),
                           ion_proportion=serialize_val(line.ion_proportion),
                           redundancy=serialize_val(line.redundancy),
                           measured_im_value=serialize_val(line.measured_im_value),
                           predicted_im_value=serialize_val(line.predicted_im_value),
                           im_score=serialize_val(line.im_score),
                           sequence=serialize_val(line.sequence),
                           experimental_mz=serialize_val(line.experimental_mz),
                           corrected_1k0=serialize_val(line.corrected_1k0),
                           ion_mobility=serialize_val(line.ion_mobility),
                           ret_time=serialize_val(line.ret_time),
                           ptm_index=serialize_val(line.ptm_index),
                           ptm_index_protein_list=serialize_val(line.ptm_index_protein_list),
                           )
    else:
        raise ValueError(f'Unsupported DtaSelectFilter Version: {version}!')


def _deserialize_peptide_line(line: str, version: DtaSelectFilterVersion) -> PeptideLine:
    line_elems = line.rstrip().split('\t')
    if version == DtaSelectFilterVersion.V2_1_12:
        return PeptideLine(
            unique=deserialize_val(line_elems[0], str),
            file_name=deserialize_val(line_elems[1], str),
            x_corr=deserialize_val(line_elems[2], float),
            delta_cn=deserialize_val(line_elems[3], float),
            conf=deserialize_val(line_elems[4], float),
            mass_plus_hydrogen=deserialize_val(line_elems[5], float),
            calc_mass_plus_hydrogen=deserialize_val(line_elems[6], float),
            total_intensity=deserialize_val(line_elems[7], float),
            spr=deserialize_val(line_elems[8], int),
            prob_score=deserialize_val(line_elems[9], float),
            ion_proportion=deserialize_val(line_elems[10], float),
            redundancy=deserialize_val(line_elems[11], int),
            sequence=deserialize_val(line_elems[12], str),
            corrected_1k0=None,
            experimental_mz=None,
            im_score=None,
            ion_mobility=None,
            measured_im_value=None,
            pi=None,
            ppm=None,
            predicted_im_value=None,
            ptm_index=None,
            ptm_index_protein_list=None,
            ret_time=None,
        )
    elif version == DtaSelectFilterVersion.V2_1_12_paser:
        return PeptideLine(
            unique=deserialize_val(line_elems[0], str),
            file_name=deserialize_val(line_elems[1], str),
            x_corr=deserialize_val(line_elems[2], float),
            delta_cn=deserialize_val(line_elems[3], float),
            conf=deserialize_val(line_elems[4], float),
            mass_plus_hydrogen=deserialize_val(line_elems[5], float),
            calc_mass_plus_hydrogen=deserialize_val(line_elems[6], float),
            ppm=deserialize_val(line_elems[7], float),
            total_intensity=deserialize_val(line_elems[8], float),
            spr=deserialize_val(line_elems[9], int),
            prob_score=deserialize_val(line_elems[10], float),
            pi=deserialize_val(line_elems[11], float),
            ion_proportion=deserialize_val(line_elems[12], float),
            redundancy=deserialize_val(line_elems[13], int),
            sequence=deserialize_val(line_elems[14], str),
            ret_time=deserialize_val(line_elems[15], float),
            ptm_index=deserialize_val(line_elems[16], str),
            ptm_index_protein_list=deserialize_val(line_elems[17], str),
            corrected_1k0=None,
            experimental_mz=None,
            im_score=None,
            ion_mobility=None,
            measured_im_value=None,
            predicted_im_value=None,

        )
    elif version == DtaSelectFilterVersion.V2_1_13:
        return PeptideLine(
            unique=deserialize_val(line_elems[0], str),
            file_name=deserialize_val(line_elems[1], str),
            x_corr=deserialize_val(line_elems[2], float),
            delta_cn=deserialize_val(line_elems[3], float),
            conf=deserialize_val(line_elems[4], float),
            mass_plus_hydrogen=deserialize_val(line_elems[5], float),
            calc_mass_plus_hydrogen=deserialize_val(line_elems[6], float),
            ppm=deserialize_val(line_elems[7], float),
            total_intensity=deserialize_val(line_elems[8], float),
            spr=deserialize_val(line_elems[9], int),
            prob_score=deserialize_val(line_elems[10], float),
            pi=deserialize_val(line_elems[11], float),
            ion_proportion=deserialize_val(line_elems[12], float),
            redundancy=deserialize_val(line_elems[13], int),
            measured_im_value=deserialize_val(line_elems[14], float),
            predicted_im_value=deserialize_val(line_elems[15], float),
            im_score=deserialize_val(line_elems[16], float),
            sequence=deserialize_val(line_elems[17], str),
            experimental_mz=None,
            corrected_1k0=None,
            ion_mobility=None,
            ret_time=None,
            ptm_index=None,
            ptm_index_protein_list=None,
        )
    elif version == DtaSelectFilterVersion.V2_1_13_timscore:
        return PeptideLine(
            unique=deserialize_val(line_elems[0], str),
            file_name=deserialize_val(line_elems[1], str),
            x_corr=deserialize_val(line_elems[2], float),
            delta_cn=deserialize_val(line_elems[3], float),
            conf=deserialize_val(line_elems[4], float),
            mass_plus_hydrogen=deserialize_val(line_elems[5], float),
            calc_mass_plus_hydrogen=deserialize_val(line_elems[6], float),
            ppm=deserialize_val(line_elems[7], float),
            total_intensity=deserialize_val(line_elems[8], float),
            spr=deserialize_val(line_elems[9], int),
            prob_score=deserialize_val(line_elems[10], float),
            pi=deserialize_val(line_elems[11], float),
            ion_proportion=deserialize_val(line_elems[12], float),
            redundancy=deserialize_val(line_elems[13], int),
            measured_im_value=deserialize_val(line_elems[14], float),
            predicted_im_value=deserialize_val(line_elems[15], float),
            im_score=deserialize_val(line_elems[16], float),
            sequence=deserialize_val(line_elems[17], str),
            experimental_mz=deserialize_val(line_elems[18], float),
            corrected_1k0=deserialize_val(line_elems[19], float),
            ion_mobility=deserialize_val(line_elems[20], float),
            ret_time=deserialize_val(line_elems[21], float),
            ptm_index=deserialize_val(line_elems[22], str),
            ptm_index_protein_list=deserialize_val(line_elems[23], str),
        )
    else:
        raise ValueError(f'Unsupported DtaSelectFilter Version: {version}!')


@dataclass(slots=True)
class ProteinLine:

    locus_name: str | None
    sequence_count: int | None
    spectrum_count: int | None
    sequence_coverage: float | None
    length: int | None
    molWt: int | None
    pi: float | None
    validation_status: str | None
    nsaf: float | None
    empai: float | None
    description_name: str | None
    h_redundancy: int | None
    l_redundancy: int | None
    m_redundancy: int | None


protein_line_V2_1_12_template = '{locus_name}\t{sequence_count}\t{spectrum_count}\t{sequence_coverage}' \
                                '\t{length}\t{molWt}\t{pi}\t{validation_status}\t{nsaf}\t{empai}\t{description_name}\n'
protein_line_V2_1_12_paser_template = '{locus_name}\t{sequence_count}\t{spectrum_count}\t{sequence_coverage}' \
                                      '\t{length}\t{molWt}\t{pi}\t{validation_status}\t{nsaf}\t{empai}' \
                                      '\t{description_name}\t{h_redundancy}\t{l_redundancy}\t{m_redundancy}\n'
protein_line_V2_1_13_template = '{locus_name}\t{sequence_count}\t{spectrum_count}\t{sequence_coverage}' \
                                '\t{length}\t{molWt}\t{pi}\t{validation_status}\t{nsaf}\t{empai}\t{description_name}\n'
protein_line_V2_1_13_timscore_template = '{locus_name}\t{sequence_count}\t{spectrum_count}\t{sequence_coverage}' \
                                         '\t{length}\t{molWt}\t{pi}\t{validation_status}\t{nsaf}\t{empai}' \
                                         '\t{description_name}\t{h_redundancy}\t{l_redundancy}\t{m_redundancy}\n'


def _serialize_protein_line(line: ProteinLine, version: DtaSelectFilterVersion) -> str:
    if version == DtaSelectFilterVersion.V2_1_12:
        return protein_line_V2_1_12_template.format(
            locus_name=serialize_val(line.locus_name),
            sequence_count=serialize_val(line.sequence_count),
            spectrum_count=serialize_val(line.spectrum_count),
            sequence_coverage=serialize_val(line.sequence_coverage, 1) + "%",
            length=serialize_val(line.length),
            molWt=serialize_val(line.molWt),
            pi=serialize_val(line.pi, 1),
            validation_status=serialize_val(line.validation_status),
            nsaf=serialize_val(line.nsaf, 10),
            empai=serialize_val(line.empai, 8),
            description_name=serialize_val(line.description_name),
        )
    elif version == DtaSelectFilterVersion.V2_1_12_paser:
        return protein_line_V2_1_12_paser_template.format(
            locus_name=serialize_val(line.locus_name),
            sequence_count=serialize_val(line.sequence_count),
            spectrum_count=serialize_val(line.spectrum_count),
            sequence_coverage=serialize_val(line.sequence_coverage, 1) + "%",
            length=serialize_val(line.length),
            molWt=serialize_val(line.molWt),
            pi=serialize_val(line.pi, 1),
            validation_status=serialize_val(line.validation_status),
            nsaf=serialize_val(line.nsaf, 10),
            empai=serialize_val(line.empai, 8),
            description_name=serialize_val(line.description_name),
            h_redundancy=serialize_val(line.h_redundancy),
            l_redundancy=serialize_val(line.l_redundancy),
            m_redundancy=serialize_val(line.m_redundancy)
        )
    elif version == DtaSelectFilterVersion.V2_1_13:
        return protein_line_V2_1_13_template.format(
            locus_name=serialize_val(line.locus_name),
            sequence_count=serialize_val(line.sequence_count),
            spectrum_count=serialize_val(line.spectrum_count),
            sequence_coverage=serialize_val(line.sequence_coverage, 1) + "%",
            length=serialize_val(line.length),
            molWt=serialize_val(line.molWt),
            pi=serialize_val(line.pi, 1),
            validation_status=serialize_val(line.validation_status),
            nsaf=serialize_val(line.nsaf, 10),
            empai=serialize_val(line.empai, 8),
            description_name=serialize_val(line.description_name),
        )
    elif version == DtaSelectFilterVersion.V2_1_13_timscore:
        return protein_line_V2_1_13_timscore_template.format(
            locus_name=serialize_val(line.locus_name),
            sequence_count=serialize_val(line.sequence_count),
            spectrum_count=serialize_val(line.spectrum_count),
            sequence_coverage=serialize_val(line.sequence_coverage, 1) + "%",
            length=serialize_val(line.length),
            molWt=serialize_val(line.molWt),
            pi=serialize_val(line.pi, 1),
            validation_status=serialize_val(line.validation_status),
            nsaf=serialize_val(line.nsaf, 10),
            empai=serialize_val(line.empai, 8),
            description_name=serialize_val(line.description_name),
            h_redundancy=serialize_val(line.h_redundancy),
            l_redundancy=serialize_val(line.l_redundancy),
            m_redundancy=serialize_val(line.m_redundancy)
        )
    else:
        raise ValueError(f'Unsupported DtaSelectFilter Version: {version}!')


def _deserialize_protein_line(line: str, version: DtaSelectFilterVersion) -> ProteinLine:
    line_elems = line.rstrip().split('\t')
    if version == DtaSelectFilterVersion.V2_1_12:
        return ProteinLine(
            locus_name=deserialize_val(line_elems[0], str),
            sequence_count=deserialize_val(line_elems[1], int),
            spectrum_count=deserialize_val(line_elems[2], int),
            sequence_coverage=deserialize_val(line_elems[3], lambda x: float(x.rstrip("%"))),
            length=deserialize_val(line_elems[4], int),
            molWt=deserialize_val(line_elems[5], int),
            pi=deserialize_val(line_elems[6], float),
            validation_status=deserialize_val(line_elems[7], str),
            nsaf=deserialize_val(line_elems[8], float),
            empai=deserialize_val(line_elems[9], float),
            description_name=deserialize_val(line_elems[10], str),
            h_redundancy=None,
            l_redundancy=None,
            m_redundancy=None,
        )
    elif version == DtaSelectFilterVersion.V2_1_12_paser:
        return ProteinLine(
            locus_name=deserialize_val(line_elems[0], str),
            sequence_count=deserialize_val(line_elems[1], int),
            spectrum_count=deserialize_val(line_elems[2], int),
            sequence_coverage=deserialize_val(line_elems[3], lambda x: float(x.rstrip("%"))),
            length=deserialize_val(line_elems[4], int),
            molWt=deserialize_val(line_elems[5], int),
            pi=deserialize_val(line_elems[6], float),
            validation_status=deserialize_val(line_elems[7], str),
            nsaf=deserialize_val(line_elems[8], float),
            empai=deserialize_val(line_elems[9], float),
            description_name=deserialize_val(line_elems[10], str),
            h_redundancy=deserialize_val(line_elems[11], int),
            l_redundancy=deserialize_val(line_elems[12], int),
            m_redundancy=deserialize_val(line_elems[13], int),
        )
    elif version == DtaSelectFilterVersion.V2_1_13:
        return ProteinLine(
            locus_name=deserialize_val(line_elems[0], str),
            sequence_count=deserialize_val(line_elems[1], int),
            spectrum_count=deserialize_val(line_elems[2], int),
            sequence_coverage=deserialize_val(line_elems[3], lambda x: float(x.rstrip("%"))),
            length=deserialize_val(line_elems[4], int),
            molWt=deserialize_val(line_elems[5], int),
            pi=deserialize_val(line_elems[6], float),
            validation_status=deserialize_val(line_elems[7], str),
            nsaf=deserialize_val(line_elems[8], float),
            empai=deserialize_val(line_elems[9], float),
            description_name=deserialize_val(line_elems[10], str),
            h_redundancy=None,
            l_redundancy=None,
            m_redundancy=None,
        )
    elif version == DtaSelectFilterVersion.V2_1_13_timscore:
        return ProteinLine(
            locus_name=deserialize_val(line_elems[0], str),
            sequence_count=deserialize_val(line_elems[1], int),
            spectrum_count=deserialize_val(line_elems[2], int),
            sequence_coverage=deserialize_val(line_elems[3], lambda x: float(x.rstrip("%"))),
            length=deserialize_val(line_elems[4], int),
            molWt=deserialize_val(line_elems[5], int),
            pi=deserialize_val(line_elems[6], float),
            validation_status=deserialize_val(line_elems[7], str),
            nsaf=deserialize_val(line_elems[8], float),
            empai=deserialize_val(line_elems[9], float),
            description_name=deserialize_val(line_elems[10], str),
            h_redundancy=deserialize_val(line_elems[11], int),
            l_redundancy=deserialize_val(line_elems[12], int),
            m_redundancy=deserialize_val(line_elems[13], int),
        )
    else:
        raise ValueError(f'Unsupported DtaSelectFilter Version: {version}!')


@dataclass
class DTAFilterResult:
    protein_lines: list[ProteinLine]
    peptide_lines: list[PeptideLine]

    def serialize(self, version):
        protein_line_strings = [_serialize_protein_line(line, version) for line in self.protein_lines]
        peptide_line_strings = [_serialize_peptide_line(line, version) for line in self.peptide_lines]
        return ''.join(protein_line_strings + peptide_line_strings)


def determine_dta_select_filter_version(peptide_line_header) -> DtaSelectFilterVersion:
    line_elems = peptide_line_header.rstrip().split('\t')
    if len(line_elems) == 24:
        return DtaSelectFilterVersion.V2_1_13_timscore
    elif len(line_elems) == 18 and line_elems[-1] =='Sequence':
        return DtaSelectFilterVersion.V2_1_13
    elif len(line_elems) == 18:
        return DtaSelectFilterVersion.V2_1_12_paser
    elif len(line_elems) == 13:
        return DtaSelectFilterVersion.V2_1_12
    else:
        raise ValueError(f'Cannot parse version from peptide header: {peptide_line_header}!')


def from_dta_select_filter(file_input: str | _io.TextIOWrapper, version: DtaSelectFilterVersion = None) -> (DtaSelectFilterVersion, [str], [DTAFilterResult], [str]):
    if type(file_input) is str:
        lines = file_input.split('\n')
    elif type(file_input) is _io.TextIOWrapper:
        lines = file_input
    else:
        raise ValueError(f'Unsupported input type: {type(file_input)}!')

    class FileState(Enum):
        HEADER = 1
        DATA = 2
        INFO = 3

    file_state = FileState.HEADER

    h_lines, dta_filter_results, end_lines = [], [], []
    peptide_lines, protein_lines = [], []

    for line in lines:
        line_elements = line.rstrip().split("\t")

        # update file state
        if len(line_elements) > 0 and line_elements[0] == 'Unique':
            h_lines.append(line)
            file_state = FileState.DATA

            if version is None:
                version = determine_dta_select_filter_version(h_lines[-1])

            print(f'Version: {version}')
            continue

        if len(line_elements) > 1 and line_elements[1] == "Proteins":
            dta_filter_results.append(DTAFilterResult(protein_lines=protein_lines, peptide_lines=peptide_lines))
            file_state = FileState.INFO

        if file_state == FileState.HEADER:
            h_lines.append(line)

        if file_state == FileState.DATA:
            if line_elements[0] == '' or '*' in line_elements[0] or line_elements[0].isnumeric():
                peptide_lines.append(_deserialize_peptide_line(line, version))
            else:
                if protein_lines:
                    dta_filter_results.append(DTAFilterResult(protein_lines=protein_lines, peptide_lines=peptide_lines))
                    peptide_lines, protein_lines = [], []
                protein_lines.append(_deserialize_protein_line(line, version))

        if file_state == FileState.INFO:
            end_lines.append(line)

    return version, h_lines, dta_filter_results, end_lines


def to_dta_select_filter(version: DtaSelectFilterVersion, h_lines: [str], dta_filter_results: [DTAFilterResult], end_lines: [str]) -> str:
    lines = []
    for h_line in h_lines:
        if h_line.endswith('\n'):
            lines.append(h_line)
        else:
            lines.append(h_line + '\n')

    for dta_filter_result in dta_filter_results:
        lines.append(dta_filter_result.serialize(version))

    for end_line in end_lines:
        if end_line.endswith('\n'):
            lines.append(end_line)
        else:
            lines.append(end_line + '\n')

    return ''.join(lines)
