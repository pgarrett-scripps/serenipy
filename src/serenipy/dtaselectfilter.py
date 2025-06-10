from dataclasses import dataclass, asdict
from enum import Enum, auto
from io import StringIO, TextIOWrapper
from typing import Tuple, Union, List

import pandas as pd

from .utils import serialize_val, deserialize_val
from collections import defaultdict


class DtaSelectFilterVersion(Enum):
    V2_1_12 = auto()
    V2_1_12_rt = auto()
    V2_1_12_paser = auto()
    V2_1_13 = auto()
    V2_1_13_timscore = auto()


@dataclass
class PeptideLine:
    unique: Union[str, None] = None
    file_name: Union[str, None] = None
    x_corr: Union[float, None] = None
    delta_cn: Union[float, None] = None
    conf: Union[float, None] = None
    mass_plus_hydrogen: Union[float, None] = None
    calc_mass_plus_hydrogen: Union[float, None] = None
    ppm: Union[float, None] = None
    total_intensity: Union[float, None] = None
    spr: Union[int, None] = None
    ion_proportion: Union[float, None] = None
    redundancy: Union[int, None] = None
    sequence: Union[str, None] = None
    prob_score: Union[float, None] = None
    pi: Union[float, None] = None
    measured_im_value: Union[float, None] = None
    predicted_im_value: Union[float, None] = None
    im_score: Union[float, None] = None
    ret_time: Union[float, None] = None
    ptm_index: Union[str, None] = None
    ptm_index_protein_list: Union[str, None] = None
    experimental_mz: Union[float, None] = None
    corrected_1k0: Union[float, None] = None
    ion_mobility: Union[float, None] = None

    @property
    def file_path(self) -> Union[str, None]:
        if self.file_name:
            return str(self.file_name.split(".")[0])
        return None

    @property
    def low_scan(self) -> Union[int, None]:
        if self.file_name:
            return int(self.file_name.split(".")[1])
        return None

    @property
    def high_scan(self) -> Union[int, None]:
        if self.file_name:
            return int(self.file_name.split(".")[2])
        return None

    @property
    def charge(self) -> Union[int, None]:
        if self.file_name:
            return int(self.file_name.split(".")[3])
        return None


peptide_line_V2_1_12_template = (
    "{unique}\t{file_name}\t{x_corr}\t{delta_cn}\t{conf}\t{mass_plus_hydrogen}"
    "\t{calc_mass_plus_hydrogen}\t{total_intensity}\t{spr}\t{prob_score}"
    "\t{ion_proportion}\t{redundancy}\t{sequence}\n"
)
peptide_line_V2_1_12_rt_template = (
    "{unique}\t{file_name}\t{x_corr}\t{delta_cn}\t{conf}\t{mass_plus_hydrogen}"
    "\t{calc_mass_plus_hydrogen}\t{ppm}\t{total_intensity}\t{spr}\t{prob_score}\t{pi}"
    "\t{ion_proportion}\t{redundancy}\t{sequence}\t{ret_time}\n"
)
peptide_line_V2_1_12_paser_template = (
    "{unique}\t{file_name}\t{x_corr}\t{delta_cn}\t{conf}\t{mass_plus_hydrogen}"
    "\t{calc_mass_plus_hydrogen}\t{ppm}\t{total_intensity}\t{spr}\t{prob_score}"
    "\t{pi}\t{ion_proportion}\t{redundancy}\t{sequence}\t{ret_time}\t{ptm_index}"
    "\t{ptm_index_protein_list}\n"
)
peptide_line_V2_1_13_template = (
    "{unique}\t{file_name}\t{x_corr}\t{delta_cn}\t{conf}\t{mass_plus_hydrogen}"
    "\t{calc_mass_plus_hydrogen}\t{ppm}\t{total_intensity}\t{spr}\t{prob_score}\t{pi}"
    "\t{ion_proportion}\t{redundancy}\t{measured_im_value}\t{predicted_im_value}"
    "\t{im_score}\t{sequence}\n"
)
peptide_line_V2_1_13_timscore_template = (
    "{unique}\t{file_name}\t{x_corr}\t{delta_cn}\t{conf}\t{mass_plus_hydrogen}"
    "\t{calc_mass_plus_hydrogen}\t{ppm}\t{total_intensity}\t{spr}\t{prob_score}"
    "\t{pi}\t{ion_proportion}\t{redundancy}\t{measured_im_value}"
    "\t{predicted_im_value}\t{im_score}\t{sequence}\t{experimental_mz}"
    "\t{corrected_1k0}\t{ion_mobility}\t{ret_time}\t{ptm_index}"
    "\t{ptm_index_protein_list}\n"
)


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
    elif version == DtaSelectFilterVersion.V2_1_12_rt:
        return peptide_line_V2_1_12_rt_template.format(
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
            pi=serialize_val(line.pi),
            ion_proportion=serialize_val(line.ion_proportion),
            redundancy=serialize_val(line.redundancy),
            sequence=serialize_val(line.sequence),
            ret_time=serialize_val(line.ret_time),
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
        raise ValueError(f"Unsupported DtaSelectFilter Version: {version}!")


def _deserialize_peptide_line(
    line: str, version: DtaSelectFilterVersion
) -> PeptideLine:
    line_elems = line.rstrip().split("\t")
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
    elif version == DtaSelectFilterVersion.V2_1_12_rt:
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
            corrected_1k0=None,
            experimental_mz=None,
            im_score=None,
            ion_mobility=None,
            measured_im_value=None,
            predicted_im_value=None,
            ptm_index=None,
            ptm_index_protein_list=None,
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
            ptm_index=(
                None if len(line_elems) == 22 else deserialize_val(line_elems[22], str)
            ),
            ptm_index_protein_list=(
                None if len(line_elems) == 22 else deserialize_val(line_elems[23], str)
            ),
        )
    else:
        raise ValueError(f"Unsupported DtaSelectFilter Version: {version}!")


@dataclass
class ProteinLine:
    locus_name: Union[str, None] = None
    sequence_count: Union[int, None] = None
    spectrum_count: Union[int, None] = None
    sequence_coverage: Union[float, None] = None
    length: Union[int, None] = None
    molWt: Union[float, None] = None
    pi: Union[float, None] = None
    validation_status: Union[str, None] = None
    nsaf: Union[float, None] = None
    empai: Union[float, None] = None
    description_name: Union[str, None] = None
    h_redundancy: Union[int, None] = None
    l_redundancy: Union[int, None] = None
    m_redundancy: Union[int, None] = None


protein_line_V2_1_12_template = (
    "{locus_name}\t{sequence_count}\t{spectrum_count}\t{sequence_coverage}"
    "\t{length}\t{molWt}\t{pi}\t{validation_status}\t{nsaf}\t{empai}\t{description_name}\n"
)
protein_line_V2_1_12_rt_template = (
    "{locus_name}\t{sequence_count}\t{spectrum_count}\t{sequence_coverage}"
    "\t{length}\t{molWt}\t{pi}\t{validation_status}\t{nsaf}\t{empai}\t{description_name}\n"
)
protein_line_V2_1_12_paser_template = (
    "{locus_name}\t{sequence_count}\t{spectrum_count}\t{sequence_coverage}"
    "\t{length}\t{molWt}\t{pi}\t{validation_status}\t{nsaf}\t{empai}"
    "\t{description_name}\t{h_redundancy}\t{l_redundancy}\t{m_redundancy}\n"
)
protein_line_V2_1_13_template = (
    "{locus_name}\t{sequence_count}\t{spectrum_count}\t{sequence_coverage}"
    "\t{length}\t{molWt}\t{pi}\t{validation_status}\t{nsaf}\t{empai}\t{description_name}\n"
)
protein_line_V2_1_13_timscore_template = (
    "{locus_name}\t{sequence_count}\t{spectrum_count}\t{sequence_coverage}"
    "\t{length}\t{molWt}\t{pi}\t{validation_status}\t{nsaf}\t{empai}"
    "\t{description_name}\t{h_redundancy}\t{l_redundancy}\t{m_redundancy}\n"
)


def _serialize_protein_line(line: ProteinLine, version: DtaSelectFilterVersion) -> str:
    if (
        version == DtaSelectFilterVersion.V2_1_12
        or version == DtaSelectFilterVersion.V2_1_12_rt
    ):
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
            m_redundancy=serialize_val(line.m_redundancy),
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
            m_redundancy=serialize_val(line.m_redundancy),
        )
    else:
        raise ValueError(f"Unsupported DtaSelectFilter Version: {version}!")


def _deserialize_protein_line(
    line: str, version: DtaSelectFilterVersion
) -> ProteinLine:
    line_elems = line.rstrip().split("\t")
    if (
        version == DtaSelectFilterVersion.V2_1_12
        or version == DtaSelectFilterVersion.V2_1_12_rt
    ):
        return ProteinLine(
            locus_name=deserialize_val(line_elems[0], str),
            sequence_count=deserialize_val(line_elems[1], int),
            spectrum_count=deserialize_val(line_elems[2], int),
            sequence_coverage=deserialize_val(
                line_elems[3], lambda x: float(x.rstrip("%"))
            ),
            length=deserialize_val(line_elems[4], int),
            molWt=deserialize_val(line_elems[5], float),
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
            sequence_coverage=deserialize_val(
                line_elems[3], lambda x: float(x.rstrip("%"))
            ),
            length=deserialize_val(line_elems[4], int),
            molWt=deserialize_val(line_elems[5], float),
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
            sequence_coverage=deserialize_val(
                line_elems[3], lambda x: float(x.rstrip("%"))
            ),
            length=deserialize_val(line_elems[4], int),
            molWt=deserialize_val(line_elems[5], float),
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
            sequence_coverage=deserialize_val(
                line_elems[3], lambda x: float(x.rstrip("%"))
            ),
            length=deserialize_val(line_elems[4], int),
            molWt=deserialize_val(line_elems[5], float),
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
        raise ValueError(f"Unsupported DtaSelectFilter Version: {version}!")


@dataclass
class DTAFilterResult:
    protein_lines: List[ProteinLine]
    peptide_lines: List[PeptideLine]

    def serialize(self, version):
        protein_line_strings = [
            _serialize_protein_line(line, version) for line in self.protein_lines
        ]
        peptide_line_strings = [
            _serialize_peptide_line(line, version) for line in self.peptide_lines
        ]
        return "".join(protein_line_strings + peptide_line_strings)

    def filter(self, level: int) -> None:
        self.peptide_lines.sort(key=lambda x: (x.conf, x.x_corr), reverse=True)
        if level == 0:
            pass
        elif level == 1:
            seen = set()
            filtered_peptide_lines = []
            for peptide_line in self.peptide_lines:
                key = (
                    peptide_line.sequence,
                    peptide_line.charge,
                    peptide_line.file_path,
                )
                if key not in seen:
                    filtered_peptide_lines.append(peptide_line)
                    seen.add(key)
            self.peptide_lines = filtered_peptide_lines
        elif level == 2:
            seen = set()
            filtered_peptide_lines = []
            for peptide_line in self.peptide_lines:
                key = (peptide_line.sequence, peptide_line.charge)
                if key not in seen:
                    filtered_peptide_lines.append(peptide_line)
                    seen.add(key)
            self.peptide_lines = filtered_peptide_lines
        else:
            raise ValueError("Level: {level} not valid. Supported levels: [0,1,2]")

    def mod_filter(self, level: int) -> None:
        self.peptide_lines.sort(key=lambda x: (x.conf, x.x_corr), reverse=True)
        if level == 0:
            self.peptide_lines = [
                peptide_line
                for peptide_line in self.peptide_lines
                if "(" in peptide_line.sequence
            ]
        elif level == 1:
            self.peptide_lines = self.peptide_lines
        elif level == 2:
            self.peptide_lines = [
                peptide_line
                for peptide_line in self.peptide_lines
                if "(" not in peptide_line.sequence
            ]
        else:
            raise ValueError("Level: {level} not valid. Supported levels: [0,1,2]")

    def best_peptide_delta_mass_filter(self, delta_mass: float) -> None:

        if delta_mass is None:
            return

        contains_dm_peptide = False
        for peptide_line in self.peptide_lines:
            if abs(peptide_line.ppm) <= delta_mass:
                contains_dm_peptide = True
                break

        if not contains_dm_peptide:
            self.peptide_lines = []

    def best_peptide_fdr_filter(self, fdr: float) -> None:

        if fdr is None:
            return

        contains_fdr_peptide = False
        for peptide_line in self.peptide_lines:
            if 1 - peptide_line.conf <= fdr:
                contains_fdr_peptide = True
                break

        if not contains_fdr_peptide:
            self.peptide_lines = []

    def unique_peptide_filter(self):
        new_peptide_lines = [
            peptide_line
            for peptide_line in self.peptide_lines
            if peptide_line.unique == "*"
        ]
        self.peptide_lines = new_peptide_lines


def results_to_df(results: List[DTAFilterResult]) -> pd.DataFrame:
    data = defaultdict(list)
    for i, result in enumerate(results):
        protein_grp = " ".join(
            sorted([protein_line.locus_name for protein_line in result.protein_lines])
        )

        protein_dicts = []
        for protein_line in result.protein_lines:
            protein_dict = protein_line.__dict__
            protein_pi = protein_dict.pop("pi")
            protein_dict["protein_pi"] = protein_pi
            protein_dict["protein_group"] = protein_grp
            protein_dicts.append(protein_dict)

        peptide_dicts = []
        for peptide_line in result.peptide_lines:
            peptide_dict = peptide_line.__dict__
            peptide_dict["low_scan"] = peptide_line.low_scan
            peptide_dict["high_scan"] = peptide_line.high_scan
            peptide_dict["file_path"] = peptide_line.file_path
            peptide_dict["charge"] = peptide_line.charge
            # peptide_dict.pop('file_name')
            peptide_dicts.append(peptide_dict)

        for protein_dict in protein_dicts:
            for peptide_dict in peptide_dicts:

                for k in peptide_dict:
                    data[k].append(peptide_dict[k])

                for k in protein_dict:
                    data[k].append(protein_dict[k])

    df = pd.DataFrame(data)
    df.drop(["file_name"], axis=1, inplace=True)
    df["file_path"] = pd.Categorical(df["file_path"])
    df["unique"] = pd.Categorical(df["unique"])

    return df


def results_from_df(df: pd.DataFrame) -> List[DTAFilterResult]:
    grp_to_peptide_lines = {}
    grp_to_protein_lines = {}
    for i, row in df.iterrows():
        protein_line = ProteinLine(
            locus_name=row.get("locus_name"),
            sequence_count=row.get("sequence_count"),
            spectrum_count=row.get("spectrum_count"),
            sequence_coverage=row.get("sequence_coverage"),
            length=row.get("length"),
            molWt=row.get("molWt"),
            pi=row.get("protein_pi"),
            validation_status=row.get("validation_status"),
            nsaf=row.get("nsaf"),
            empai=row.get("empai"),
            description_name=row.get("description_name"),
            h_redundancy=row.get("h_redundancy"),
            l_redundancy=row.get("l_redundancy"),
            m_redundancy=row.get("m_redundancy"),
        )
        file_name = ".".join(
            [
                row.get("file_path"),
                str(row.get("low_scan")),
                str(row.get("high_scan")),
                str(row.get("charge")),
            ]
        )
        peptide_line = PeptideLine(
            unique=row.get("unique"),
            file_name=file_name,
            x_corr=row.get("x_corr"),
            delta_cn=row.get("delta_cn"),
            conf=row.get("conf"),
            mass_plus_hydrogen=row.get("mass_plus_hydrogen"),
            calc_mass_plus_hydrogen=row.get("calc_mass_plus_hydrogen"),
            ppm=row.get("ppm"),
            total_intensity=row.get("total_intensity"),
            spr=row.get("spr"),
            ion_proportion=row.get("ion_proportion"),
            redundancy=row.get("redundancy"),
            sequence=row.get("sequence"),
            prob_score=row.get("prob_score"),
            pi=row.get("pi"),
            measured_im_value=row.get("measured_im_value"),
            predicted_im_value=row.get("predicted_im_value"),
            im_score=row.get("im_score"),
            ret_time=row.get("ret_time"),
            ptm_index=row.get("ptm_index"),
            ptm_index_protein_list=row.get("ptm_index_protein_list"),
            experimental_mz=row.get("experimental_mz"),
            corrected_1k0=row.get("corrected_1k0"),
            ion_mobility=row.get("ion_mobility"),
        )
        grp_to_peptide_lines.setdefault(row.get("protein_group"), {}).setdefault(
            peptide_line.file_name, peptide_line
        )
        grp_to_protein_lines.setdefault(row.get("protein_group"), {}).setdefault(
            protein_line.locus_name, protein_line
        )

    results = []
    for grp in grp_to_peptide_lines:
        result = DTAFilterResult(
            protein_lines=list(grp_to_protein_lines[grp].values()),
            peptide_lines=list(grp_to_peptide_lines[grp].values()),
        )
        results.append(result)
    return results


def results_to_protein_df(protein_lines: List[ProteinLine]):
    data = []
    for protein_line in protein_lines:
        data.append(asdict(protein_line))
    return pd.DataFrame(data)


def results_to_peptide_df(peptide_lines: List[PeptideLine]):
    data = []
    for peptide_line in peptide_lines:
        d = asdict(peptide_line)
        d["low_scan"] = peptide_line.low_scan
        d["high_scan"] = peptide_line.high_scan
        d["file"] = peptide_line.file_path
        d["charge"] = peptide_line.charge
        d.pop("file_name")
        data.append(d)
    return pd.DataFrame(data)


def determine_dta_select_filter_version(peptide_line_header) -> DtaSelectFilterVersion:
    line_elems = peptide_line_header.rstrip().split("\t")
    if len(line_elems) == 24:
        return DtaSelectFilterVersion.V2_1_13_timscore
    elif len(line_elems) == 22:
        return DtaSelectFilterVersion.V2_1_13_timscore
    elif len(line_elems) == 18 and line_elems[-1] == "Sequence":
        return DtaSelectFilterVersion.V2_1_13
    elif len(line_elems) == 18:
        return DtaSelectFilterVersion.V2_1_12_paser
    elif len(line_elems) == 13:
        return DtaSelectFilterVersion.V2_1_12
    elif len(line_elems) == 16:
        return DtaSelectFilterVersion.V2_1_12_rt
    else:
        raise ValueError(
            f"Cannot parse version from peptide header: {peptide_line_header}!"
        )


def from_dta_select_filter(
    file_input: Union[str, TextIOWrapper, StringIO],
    version: DtaSelectFilterVersion = None,
) -> Tuple[DtaSelectFilterVersion, List[str], List[DTAFilterResult], List[str]]:
    if type(file_input) is str:
        lines = file_input.split("\n")
    elif type(file_input) is TextIOWrapper or type(file_input) is StringIO:
        lines = file_input
    else:
        raise ValueError(f"Unsupported input type: {type(file_input)}!")

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
        if len(line_elements) > 0 and line_elements[0] == "Unique":
            h_lines.append(line)
            file_state = FileState.DATA

            if version is None:
                version = determine_dta_select_filter_version(h_lines[-1])

            print(f"Version: {version}")
            continue

        if len(line_elements) > 1 and line_elements[1] == "Proteins":
            dta_filter_results.append(
                DTAFilterResult(
                    protein_lines=protein_lines, peptide_lines=peptide_lines
                )
            )
            file_state = FileState.INFO

        if file_state == FileState.HEADER:
            h_lines.append(line)

        if file_state == FileState.DATA:
            if (
                line_elements[0] == ""
                or "*" in line_elements[0]
                or line_elements[0].isnumeric()
            ):
                peptide_lines.append(_deserialize_peptide_line(line, version))
            else:
                if protein_lines and peptide_lines:
                    dta_filter_results.append(
                        DTAFilterResult(
                            protein_lines=protein_lines, peptide_lines=peptide_lines
                        )
                    )
                    peptide_lines, protein_lines = [], []
                protein_lines.append(_deserialize_protein_line(line, version))

        if file_state == FileState.INFO:
            end_lines.append(line)

    return version, h_lines, dta_filter_results, end_lines


def convert_to_best_datatype(values):
    for datatype in (float, int, str):
        try:
            converted_values = [datatype(value) for value in values]
            return converted_values
        except (ValueError, TypeError):
            continue
    raise ValueError("Unable to convert values to any datatype")


def from_dta_select_filter_to_df(
    file_input: Union[str, TextIOWrapper, StringIO],
    version: DtaSelectFilterVersion = None,
) -> Tuple[DtaSelectFilterVersion, List[str], List[DTAFilterResult], List[str]]:
    if type(file_input) is str:
        lines = file_input.split("\n")
    elif type(file_input) is TextIOWrapper or type(file_input) is StringIO:
        lines = file_input
    else:
        raise ValueError(f"Unsupported input type: {type(file_input)}!")

    class FileState(Enum):
        HEADER = 1
        DATA = 2
        INFO = 3

    file_state = FileState.HEADER

    h_lines, dta_filter_results, end_lines = [], [], []
    peptide_lines, protein_lines = [], []

    peptide_data = None
    protein_data = None

    current_protein_grp = 0
    peptide_line_cnt = 0

    for line in lines:
        line_elements = line.rstrip().split("\t")

        if line.startswith("Locus"):
            protein_data = {key: [] for key in line_elements}
            protein_data["protein_group"] = []
        if line.startswith("Unique"):
            peptide_data = {key: [] for key in line_elements}
            peptide_data["protein_group"] = []

        # update file state
        if len(line_elements) > 0 and line_elements[0] == "Unique":
            h_lines.append(line)
            file_state = FileState.DATA

            if version is None:
                version = determine_dta_select_filter_version(h_lines[-1])

            print(f"Version: {version}")
            continue

        if len(line_elements) > 1 and line_elements[1] == "Proteins":
            file_state = FileState.INFO

        if file_state == FileState.HEADER:
            h_lines.append(line)

        if file_state == FileState.DATA:
            if (
                line_elements[0] == ""
                or "*" in line_elements[0]
                or line_elements[0].isnumeric()
            ):
                for key, value in zip(peptide_data, line_elements):
                    peptide_data[key].append(value)
                peptide_data["protein_group"].append(current_protein_grp)

                peptide_line_cnt += 1
            else:
                if peptide_line_cnt != 0:
                    current_protein_grp += 1
                    peptide_line_cnt = 0

                for key, value in zip(protein_data, line_elements):
                    protein_data[key].append(value)
                protein_data["protein_group"].append(current_protein_grp)

        if file_state == FileState.INFO:
            end_lines.append(line)

    for k in peptide_data:
        peptide_data[k] = convert_to_best_datatype(peptide_data[k])

    for k in protein_data:
        protein_data[k] = convert_to_best_datatype(protein_data[k])

    peptide_df = pd.DataFrame(peptide_data).convert_dtypes()
    protein_df = pd.DataFrame(protein_data).convert_dtypes()

    file_name_components = [fn.split(".") for fn in peptide_df["FileName"]]

    peptide_df["file_name"] = [comp[0] for comp in file_name_components]
    peptide_df["low_scan"] = [comp[1] for comp in file_name_components]
    peptide_df["high_scan"] = [comp[2] for comp in file_name_components]
    peptide_df["charge"] = [comp[3] for comp in file_name_components]

    peptide_df.drop(["FileName"], axis=1, inplace=True)

    return version, h_lines, peptide_df, protein_df, end_lines


def to_dta_select_filter(
    version: DtaSelectFilterVersion,
    h_lines: List[str],
    dta_filter_results: List[DTAFilterResult],
    end_lines: List[str],
) -> str:
    lines = []
    for h_line in h_lines:
        if h_line.endswith("\n"):
            lines.append(h_line)
        else:
            lines.append(h_line + "\n")

    for dta_filter_result in dta_filter_results:
        lines.append(dta_filter_result.serialize(version))

    for end_line in end_lines:
        if end_line.endswith("\n"):
            lines.append(end_line)
        else:
            lines.append(end_line + "\n")

    return "".join(lines)
