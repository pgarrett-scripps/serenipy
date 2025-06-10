import unittest

from serenipy.dtaselectfilter import from_dta_select_filter, to_dta_select_filter, DTAFilterResult, PeptideLine


class TestDtaSelectFilter(unittest.TestCase):

    def test_to_from_dta_select_filter_V2_1_13(self):
        with open('data/DTASelect-filter_V2_1_13.txt', 'r') as file:
            version, head_lines, dta_select_filter_results, tail_lines = from_dta_select_filter(file)

        self.assertEqual(dta_select_filter_results[0].protein_lines[0].locus_name, 'sp|P05387|RLA2_HUMAN')
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].sequence_count, 9)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].spectrum_count, 62)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].sequence_coverage, 84.3)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].length, 115)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].molWt, 11665)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].pi, 4.5)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].validation_status, 'U')
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].nsaf, 0.0025080831)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].empai, 5.966266)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].description_name,
                         '60S acidic ribosomal protein P2 OS=Homo sapiens OX=9606 GN=RPLP2 PE=1 SV=1')

        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].unique, '*')
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].file_name,
                         '190806_300ng_180m_03_Slot2-3_1_646_nopd.357198.357198.2')
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].file_path,
                         '190806_300ng_180m_03_Slot2-3_1_646_nopd')
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].low_scan, 357198)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].high_scan, 357198)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].charge, 2)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].x_corr, 6.4774)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].delta_cn, 0.8641)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].conf, 100.0)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].mass_plus_hydrogen, 1868.9581)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].calc_mass_plus_hydrogen, 1868.9752)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].ppm, -9.1)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].total_intensity, 422160.0)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].spr, 0)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].prob_score, 63.016)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].pi, 8.64)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].ion_proportion, 95.7)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].redundancy, 9)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].measured_im_value, 1.1144)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].predicted_im_value, 1.1519999504089355)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].im_score, 0.5299)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].sequence, 'R.YVASYLLAALGGNSSPSAK.D')

        dta_select_filter_str = to_dta_select_filter(version, head_lines, dta_select_filter_results, tail_lines)
        version, head_lines, dta_select_filter_results, tail_lines = from_dta_select_filter(dta_select_filter_str)

        self.assertEqual(dta_select_filter_results[0].protein_lines[0].locus_name, 'sp|P05387|RLA2_HUMAN')
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].sequence_count, 9)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].spectrum_count, 62)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].sequence_coverage, 84.3)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].length, 115)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].molWt, 11665)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].pi, 4.5)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].validation_status, 'U')
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].nsaf, 0.0025080831)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].empai, 5.966266)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].description_name,
                         '60S acidic ribosomal protein P2 OS=Homo sapiens OX=9606 GN=RPLP2 PE=1 SV=1')

        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].unique, '*')
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].file_name,
                         '190806_300ng_180m_03_Slot2-3_1_646_nopd.357198.357198.2')
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].low_scan, 357198)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].high_scan, 357198)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].charge, 2)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].x_corr, 6.4774)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].delta_cn, 0.8641)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].conf, 100.0)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].mass_plus_hydrogen, 1868.9581)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].calc_mass_plus_hydrogen, 1868.9752)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].ppm, -9.1)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].total_intensity, 422160.0)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].spr, 0)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].prob_score, 63.016)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].pi, 8.64)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].ion_proportion, 95.7)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].redundancy, 9)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].measured_im_value, 1.1144)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].predicted_im_value, 1.1519999504089355)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].im_score, 0.5299)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].sequence, 'R.YVASYLLAALGGNSSPSAK.D')

    def test_to_from_dta_select_filter_V2_1_12(self):
        with open('data/DTASelect-filter_V2_1_12_paser.txt', 'r') as file:
            version, head_lines, dta_select_filter_results, tail_lines = from_dta_select_filter(file)
            original_text = str(file.read())

        self.assertEqual(dta_select_filter_results[0].protein_lines[0].locus_name, 'sp|P04792|HSPB1_HUMAN')
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].sequence_count, 17)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].spectrum_count, 63)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].sequence_coverage, 83.4)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].length, 205)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].molWt, 22783)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].pi, 6.4)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].validation_status, 'U')
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].nsaf, 0.0018575318)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].empai, 5.8233867)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].description_name,
                         'Heat shock protein beta-1 OS=Homo sapiens OX=9606 GN=HSPB1 PE=1 SV=2 ')
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].h_redundancy, 0)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].l_redundancy, 63)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].m_redundancy, 0)

        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].unique, '*')
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].file_name,
                         '20180819_TIMS2_12-2_AnBr_SA_200ng_HeLa_50cm_120min_100ms_11CT_2_A1_01_2768.192026.192026.2')
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].file_path,
                         '20180819_TIMS2_12-2_AnBr_SA_200ng_HeLa_50cm_120min_100ms_11CT_2_A1_01_2768')
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].low_scan, 192026)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].high_scan, 192026)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].charge, 2)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].x_corr, 1.1279)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].delta_cn, 0.3051)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].conf, 99.6)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].mass_plus_hydrogen, 831.5017)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].calc_mass_plus_hydrogen, 831.50867)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].ppm, -8.4)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].total_intensity, 24030.0)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].spr, 2)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].prob_score, 5.1368585)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].pi, 10.06)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].ion_proportion, 70.0)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].redundancy, 1)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].sequence, 'R.VPFSLLR.G')
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].ret_time, 0.7797)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].ptm_index, None)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].ptm_index_protein_list, None)

        dta_select_filter_str = to_dta_select_filter(version, head_lines, dta_select_filter_results, tail_lines)
        version, head_lines, dta_select_filter_results, tail_lines = from_dta_select_filter(dta_select_filter_str)

        self.assertEqual(dta_select_filter_results[0].protein_lines[0].locus_name, 'sp|P04792|HSPB1_HUMAN')
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].sequence_count, 17)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].spectrum_count, 63)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].sequence_coverage, 83.4)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].length, 205)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].molWt, 22783)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].pi, 6.4)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].validation_status, 'U')
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].nsaf, 0.0018575318)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].empai, 5.8233867)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].description_name,
                         'Heat shock protein beta-1 OS=Homo sapiens OX=9606 GN=HSPB1 PE=1 SV=2 ')
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].h_redundancy, 0)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].l_redundancy, 63)
        self.assertEqual(dta_select_filter_results[0].protein_lines[0].m_redundancy, 0)

        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].unique, '*')
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].file_name,
                         '20180819_TIMS2_12-2_AnBr_SA_200ng_HeLa_50cm_120min_100ms_11CT_2_A1_01_2768.192026.192026.2')
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].file_path,
                         '20180819_TIMS2_12-2_AnBr_SA_200ng_HeLa_50cm_120min_100ms_11CT_2_A1_01_2768')
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].low_scan, 192026)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].high_scan, 192026)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].charge, 2)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].x_corr, 1.1279)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].delta_cn, 0.3051)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].conf, 99.6)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].mass_plus_hydrogen, 831.5017)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].calc_mass_plus_hydrogen, 831.50867)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].ppm, -8.4)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].total_intensity, 24030.0)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].spr, 2)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].prob_score, 5.1368585)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].pi, 10.06)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].ion_proportion, 70.0)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].redundancy, 1)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].sequence, 'R.VPFSLLR.G')
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].ret_time, 0.7797)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].ptm_index, None)
        self.assertEqual(dta_select_filter_results[0].peptide_lines[0].ptm_index_protein_list, None)

    def test_dtafilter_filter(self):
        peptides_lines = [
            PeptideLine(file_name='file1.1.1.2', sequence='PEPTIDE', conf=.9, x_corr=1),
            PeptideLine(file_name='file2.1.1.2', sequence='PEPTIDE', conf=.8, x_corr=1),
            PeptideLine(file_name='file2.1.1.2', sequence='PEPTIDE', conf=.7, x_corr=1),
            PeptideLine(file_name='file4.1.1.4', sequence='PEPTIDES', conf=.7, x_corr=1),

        ]

        result = DTAFilterResult(protein_lines=None,
                                 peptide_lines=peptides_lines)

        result.filter(level=0)
        self.assertEqual(4, len(result.peptide_lines))

        result.filter(level=1) # seq, file, charge
        self.assertEqual(3, len(result.peptide_lines))

        result.filter(level=2) # seq, charge
        self.assertEqual(2, len(result.peptide_lines))