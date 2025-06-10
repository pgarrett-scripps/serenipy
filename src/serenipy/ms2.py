import multiprocessing
from dataclasses import dataclass
from enum import Enum
from io import TextIOWrapper, StringIO
from queue import Empty
from typing import Optional, Tuple, Union, List, Dict

s_line_template = "S\t{low_scan}\t{high_scan}\t{mz}\n"
i_line_template = "I\t{keyword}\t{value}\n"
z_line_template = "Z\t{charge}\t{mass}\n"
peak_line_template = "{mz} {intensity}\n"
peak_line_charged_template = "{mz} {intensity} {charge}\n"


class ILineKeywords(Enum):
    PARENT_ID_KEYWORD = "TIMSTOF_Parent_ID"
    PRECURSOR_ID_KEYWORD = "TIMSTOF_Precursor_ID"
    OOK0_KEYWORD = "Ion Mobility"
    CCS_KEYWORD = "CCS"
    RETENTION_TIME_KEYWORD = "RetTime"
    COLLISION_ENERGY_KEYWORD = "Collision_Energy"
    ISOLATION_MZ_KEYWORD = "Isolation_Mz"
    ISOLATION_WIDTH_KEYWORD = "Isolation_Width"
    SCAN_NUMBER_BEGIN_KEYWORD = "Scan_Number_Begin"
    SCAN_NUMBER_END_KEYWORD = "Scan_Number_End"
    PRECURSOR_INTENSITY_KEYWORD = "Intensity"
    OOK0_SPECTRA_KEYWORD = "OOK0_Spectra"
    CCS_SPECTRA_KEYWORD = "CCS_Spectra"
    INTENSITY_SPECTRA_KEYWORD = "Intensity_Spectra"
    MZ_SPECTRA_KEYWORD = "MZ_Spectra"


@dataclass
class Ms2Spectra:
    low_scan: int
    high_scan: int
    mz: float
    mass: float
    charge: int
    info: Dict[str, str]
    mz_spectra: List[float]
    intensity_spectra: List[float]
    charge_spectra: List[int]

    @property
    def parent_id(self) -> Union[int, None]:
        parent_id = self.info.get(ILineKeywords.PARENT_ID_KEYWORD.value)
        return int(parent_id) if parent_id else None

    @parent_id.setter
    def parent_id(self, parent_id: Union[str, int]):
        self.info[ILineKeywords.PARENT_ID_KEYWORD.value] = parent_id

    @property
    def precursor_id(self) -> Union[int, None]:
        precursor_id = self.info.get(ILineKeywords.PRECURSOR_ID_KEYWORD.value)
        return int(precursor_id) if precursor_id else None

    @precursor_id.setter
    def precursor_id(self, precursor_id: Union[str, int]):
        self.info[ILineKeywords.PRECURSOR_ID_KEYWORD.value] = precursor_id

    @property
    def ook0(self) -> Union[float, None]:
        ook0 = self.info.get(ILineKeywords.OOK0_KEYWORD.value)
        return float(ook0) if ook0 else None

    @ook0.setter
    def ook0(self, ook0: Union[str, float]):
        self.info[ILineKeywords.OOK0_KEYWORD.value] = ook0

    @property
    def ccs(self) -> Union[float, None]:
        ccs = self.info.get(ILineKeywords.CCS_KEYWORD.value)
        return float(ccs) if ccs else None

    @ccs.setter
    def ccs(self, ccs: Union[str, float]):
        self.info[ILineKeywords.CCS_KEYWORD.value] = ccs

    @property
    def rt(self) -> Union[float, None]:
        rt = self.info.get(ILineKeywords.RETENTION_TIME_KEYWORD.value)
        return float(rt) if rt else None

    @rt.setter
    def rt(self, rt: Union[str, float]):
        self.info[ILineKeywords.RETENTION_TIME_KEYWORD.value] = rt

    @property
    def ce(self) -> Union[float, None]:
        ce = self.info.get(ILineKeywords.COLLISION_ENERGY_KEYWORD.value)
        return float(ce) if ce else None

    @ce.setter
    def ce(self, ce: Union[str, float]):
        self.info[ILineKeywords.COLLISION_ENERGY_KEYWORD.value] = ce

    @property
    def iso_mz(self) -> Union[float, None]:
        iso_mz = self.info.get(ILineKeywords.ISOLATION_MZ_KEYWORD.value)
        return float(iso_mz) if iso_mz else None

    @iso_mz.setter
    def iso_mz(self, iso_mz: Union[str, float]):
        self.info[ILineKeywords.ISOLATION_MZ_KEYWORD.value] = iso_mz

    @property
    def iso_width(self) -> Union[float, None]:
        iso_width = self.info.get(ILineKeywords.ISOLATION_WIDTH_KEYWORD.value)
        return float(iso_width) if iso_width else None

    @iso_width.setter
    def iso_width(self, iso_width: Union[str, float]):
        self.info[ILineKeywords.ISOLATION_WIDTH_KEYWORD.value] = iso_width

    @property
    def scan_begin(self) -> Union[int, None]:
        scan_begin = self.info.get(ILineKeywords.SCAN_NUMBER_BEGIN_KEYWORD.value)
        return int(scan_begin) if scan_begin else None

    @scan_begin.setter
    def scan_begin(self, scan_begin: Union[str, int]):
        self.info[ILineKeywords.SCAN_NUMBER_BEGIN_KEYWORD.value] = scan_begin

    @property
    def scan_end(self) -> Union[int, None]:
        scan_end = self.info.get(ILineKeywords.SCAN_NUMBER_END_KEYWORD.value)
        return int(scan_end) if scan_end else None

    @scan_end.setter
    def scan_end(self, scan_end: Union[str, int]):
        self.info[ILineKeywords.SCAN_NUMBER_END_KEYWORD.value] = scan_end

    @property
    def prec_intensity(self) -> Union[float, None]:
        prec_intensity = self.info.get(ILineKeywords.PRECURSOR_INTENSITY_KEYWORD.value)
        return float(prec_intensity) if prec_intensity else None

    @prec_intensity.setter
    def prec_intensity(self, prec_intensity: Union[str, float]):
        self.info[ILineKeywords.PRECURSOR_INTENSITY_KEYWORD.value] = prec_intensity

    def serialize(
        self,
        mz_precision: Optional[float] = None,
        intensity_precision: Optional[float] = None,
    ) -> str:
        return _serialize_ms2_spectra(
            self, mz_precision=mz_precision, intensity_precision=intensity_precision
        )

    @staticmethod
    def deserialize(line: str) -> "Ms2Spectra":
        return _deserialize_ms2_spectra(line)


def _serialize_ms2_spectra(
    ms2_spectra: Ms2Spectra,
    mz_precision: Optional[float] = None,
    intensity_precision: Optional[float] = None,
) -> str:

    s_line = s_line_template.format(
        low_scan=ms2_spectra.low_scan,
        high_scan=ms2_spectra.high_scan,
        mz=ms2_spectra.mz,
    )
    i_lines = [
        i_line_template.format(keyword=k, value=v) for k, v in ms2_spectra.info.items()
    ]
    z_line = z_line_template.format(charge=ms2_spectra.charge, mass=ms2_spectra.mass)

    if ms2_spectra.charge_spectra:
        peak_lines = [
            peak_line_charged_template.format(
                mz=m if mz_precision is None else round(m, mz_precision),
                intensity=(
                    i if intensity_precision is None else round(i, intensity_precision)
                ),
                charge=int(c),
            )
            for m, i, c in zip(
                ms2_spectra.mz_spectra,
                ms2_spectra.intensity_spectra,
                ms2_spectra.charge_spectra,
            )
        ]
    else:
        peak_lines = [
            peak_line_template.format(
                mz=m if mz_precision is None else round(m, mz_precision),
                intensity=(
                    i if intensity_precision is None else round(i, intensity_precision)
                ),
            )
            for m, i in zip(ms2_spectra.mz_spectra, ms2_spectra.intensity_spectra)
        ]

    return "".join([s_line] + i_lines + [z_line] + peak_lines)


def _deserialize_ms2_spectra(
    spectra_str: Union[str, List[str]], include_spectra=True
) -> Ms2Spectra:
    if isinstance(spectra_str, str):
        lines = spectra_str.split("\n")
    elif isinstance(spectra_str, list):
        lines = spectra_str
    else:
        raise ValueError(f"Unsupported spectra_str type: {type(spectra_str)}!")

    low_scan, high_scan, mz, mass, charge = None, None, None, None, None
    info, mz_spectra, intensity_spectra, charge_spectra = {}, [], [], []

    for line in lines:
        if line.startswith("S"):
            line_elems = line.strip().split("\t")
            low_scan = int(line_elems[1])
            high_scan = int(line_elems[2])
            mz = float(line_elems[3])
        elif line.startswith("Z"):
            line_elems = line.strip().split("\t")
            charge = int(line_elems[1])
            mass = float(line_elems[2])
        elif line.startswith("I"):
            line_elems = line.strip().split("\t")
            info[line_elems[1]] = "\t".join(line_elems[2:])
        elif line[0].isnumeric() and include_spectra:
            line_elems = line.strip().split(" ")
            mz_spectra.append(float(line_elems[0]))
            intensity_spectra.append(float(line_elems[1]))
            if len(line_elems) == 3:
                charge_spectra.append(float(line_elems[2]))

    return Ms2Spectra(
        low_scan=low_scan,
        high_scan=high_scan,
        mz=mz,
        mass=mass,
        charge=charge,
        info=info,
        mz_spectra=mz_spectra,
        intensity_spectra=intensity_spectra,
        charge_spectra=charge_spectra,
    )


def ms2_spectra_consumer(queue: multiprocessing.Queue, return_dict: Dict):
    print("Consumer: Running", flush=True)
    # consume work
    while True:
        try:
            tmp_spectra_lines = queue.get(timeout=1)
        except Empty:
            break
        ms2_spectra = _deserialize_ms2_spectra(tmp_spectra_lines)
        return_dict[ms2_spectra.low_scan] = ms2_spectra

    print("Consumer: Stopping")


def get_header(ms2_input: Union[str, TextIOWrapper, StringIO]):
    if type(ms2_input) is str:
        lines = ms2_input.split("\n")
    elif type(ms2_input) is TextIOWrapper or type(ms2_input) is StringIO:
        lines = ms2_input
    else:
        raise ValueError(f"Unsupported input type: {type(ms2_input)}!")

    header_lines = []

    for line in lines:
        if line.startswith("H"):
            header_lines.append(line)
        else:
            break

    return header_lines


def get_spectra(ms2_input: Union[str, TextIOWrapper, StringIO], include_spectra=True):
    if type(ms2_input) is str:
        lines = ms2_input.split("\n")
    elif type(ms2_input) is TextIOWrapper or type(ms2_input) is StringIO:
        lines = ms2_input
    else:
        raise ValueError(f"Unsupported input type: {type(ms2_input)}!")

    tmp_spectra_lines = []

    for line in lines:

        if line.startswith("H"):
            continue

        elif line.startswith("S"):
            if tmp_spectra_lines:
                spectra = _deserialize_ms2_spectra(tmp_spectra_lines, include_spectra)
                yield spectra
                tmp_spectra_lines = []

        if line:
            tmp_spectra_lines.append(line)

    spectra = _deserialize_ms2_spectra(tmp_spectra_lines, include_spectra)
    yield spectra


def from_ms2(
    ms2_input: Union[str, TextIOWrapper, StringIO], include_spectra=True
) -> Tuple[List[str], List[Ms2Spectra]]:
    if type(ms2_input) is str:
        lines = ms2_input.split("\n")
    elif type(ms2_input) is TextIOWrapper or type(ms2_input) is StringIO:
        lines = ms2_input
    else:
        raise ValueError(f"Unsupported input type: {type(ms2_input)}!")

    header_lines = []
    spectra = []
    tmp_spectra_lines = []

    for line in lines:

        if line.startswith("H"):
            header_lines.append(line)
            continue

        elif line.startswith("S"):
            if tmp_spectra_lines:
                spectra.append(
                    _deserialize_ms2_spectra(tmp_spectra_lines, include_spectra)
                )
                tmp_spectra_lines = []

        if line:
            tmp_spectra_lines.append(line)

    spectra.append(_deserialize_ms2_spectra(tmp_spectra_lines, include_spectra))

    return header_lines, spectra


def to_ms2(h_lines: List[str], ms2_spectras: List[Ms2Spectra]) -> str:
    lines = []
    for h_line in h_lines:
        if h_line.endswith("\n"):
            lines.append(h_line)
        else:
            lines.append(h_line + "\n")

    for ms2_spectra in ms2_spectras:
        lines.append(_serialize_ms2_spectra(ms2_spectra))

    return "".join(lines)
