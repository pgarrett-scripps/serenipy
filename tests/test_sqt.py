import unittest


from serenipy.sqt import from_sqt, to_sqt


class TestSqt(unittest.TestCase):

    def test_load_sqt_v1_4_0(self):

        with open('data/sqt_V1_4_0.sqt', 'r') as file:
            sqt_version, h_lines, s_lines = from_sqt(file)

        self.assertEqual(len(s_lines), 4)
        self.assertEqual(len(h_lines), 25)

        self.assertEqual(s_lines[0].low_scan, 21)
        self.assertEqual(s_lines[0].high_scan, 21)
        self.assertEqual(s_lines[0].charge, 2)
        self.assertEqual(s_lines[0].process_time, 586)
        self.assertEqual(s_lines[0].server, 'nodeb0227_Thread-1')
        self.assertEqual(s_lines[0].experimental_mass, 1122.40845)
        self.assertEqual(s_lines[0].total_ion_intensity, 12230.00)
        self.assertEqual(s_lines[0].lowest_sp, 0.0086)
        self.assertEqual(s_lines[0].number_matches, 7)

        self.assertEqual(s_lines[0].m_lines[0].xcorr_rank, 1)
        self.assertEqual(s_lines[0].m_lines[0].sp_rank, 1)
        self.assertEqual(s_lines[0].m_lines[0].calculated_mass, 1122.42037)
        self.assertEqual(s_lines[0].m_lines[0].delta_cn, 0.0000)
        self.assertEqual(s_lines[0].m_lines[0].xcorr, 0.0000)
        self.assertEqual(s_lines[0].m_lines[0].sp, 9.999999747378752E-6)
        self.assertEqual(s_lines[0].m_lines[0].matched_ions, 4)
        self.assertEqual(s_lines[0].m_lines[0].expected_ions, 16)
        self.assertEqual(s_lines[0].m_lines[0].sequence, 'K.CFHDCGGNR.T')
        self.assertEqual(s_lines[0].m_lines[0].validation_status, 'U')

        self.assertEqual(s_lines[0].m_lines[0].l_lines[0].locus_name, 'Reverse_sp|Q9NQ36|SCUB2_HUMAN')
        self.assertEqual(s_lines[0].m_lines[0].l_lines[0].peptide_index_in_protein_sequence, 661)
        self.assertEqual(s_lines[0].m_lines[0].l_lines[0].peptide_sequence, 'INK.CFHDCGGNR.TQC')

        sqt_str = to_sqt(sqt_version, h_lines, s_lines)
        sqt_version, header, s_lines = from_sqt(sqt_str)

        self.assertEqual(len(s_lines), 4)
        self.assertEqual(len(header), 25)

        self.assertEqual(s_lines[0].low_scan, 21)
        self.assertEqual(s_lines[0].high_scan, 21)
        self.assertEqual(s_lines[0].charge, 2)
        self.assertEqual(s_lines[0].process_time, 586)
        self.assertEqual(s_lines[0].server, 'nodeb0227_Thread-1')
        self.assertEqual(s_lines[0].experimental_mass, 1122.40845)
        self.assertEqual(s_lines[0].total_ion_intensity, 12230.00)
        self.assertEqual(s_lines[0].lowest_sp, 0.0086)
        self.assertEqual(s_lines[0].number_matches, 7)

        self.assertEqual(s_lines[0].m_lines[0].xcorr_rank, 1)
        self.assertEqual(s_lines[0].m_lines[0].sp_rank, 1)
        self.assertEqual(s_lines[0].m_lines[0].calculated_mass, 1122.42037)
        self.assertEqual(s_lines[0].m_lines[0].delta_cn, 0.0000)
        self.assertEqual(s_lines[0].m_lines[0].xcorr, 0.0000)
        self.assertEqual(s_lines[0].m_lines[0].sp, 9.999999747378752E-6)
        self.assertEqual(s_lines[0].m_lines[0].matched_ions, 4)
        self.assertEqual(s_lines[0].m_lines[0].expected_ions, 16)
        self.assertEqual(s_lines[0].m_lines[0].sequence, 'K.CFHDCGGNR.T')
        self.assertEqual(s_lines[0].m_lines[0].validation_status, 'U')

        self.assertEqual(s_lines[0].m_lines[0].l_lines[0].locus_name, 'Reverse_sp|Q9NQ36|SCUB2_HUMAN')
        self.assertEqual(s_lines[0].m_lines[0].l_lines[0].peptide_index_in_protein_sequence, 661)
        self.assertEqual(s_lines[0].m_lines[0].l_lines[0].peptide_sequence, 'INK.CFHDCGGNR.TQC')

    def test_load_sqt_v2_1_0(self):

        with open('data/sqt_V2_1_0.sqt', 'r') as file:
            sqt_version, h_lines, s_lines = from_sqt(file)

        self.assertEqual(len(s_lines), 3)
        self.assertEqual(len(h_lines), 20)

        self.assertEqual(s_lines[0].low_scan, 194118)
        self.assertEqual(s_lines[0].high_scan, 194118)
        self.assertEqual(s_lines[0].charge, 3)
        self.assertEqual(s_lines[0].process_time, 18)
        self.assertEqual(s_lines[0].server, 'paser_Thread-195379')
        self.assertEqual(s_lines[0].experimental_mass, 3136.39819)
        self.assertEqual(s_lines[0].total_ion_intensity, 43217.00)
        self.assertEqual(s_lines[0].lowest_sp, 0.0131)
        self.assertEqual(s_lines[0].number_matches, 0)
        self.assertEqual(s_lines[0].experimental_ook0, 1.0633)

        self.assertEqual(s_lines[0].m_lines[0].xcorr_rank, 1)
        self.assertEqual(s_lines[0].m_lines[0].sp_rank, 0)
        self.assertEqual(s_lines[0].m_lines[0].calculated_mass, 3136.43097)
        self.assertEqual(s_lines[0].m_lines[0].delta_cn, 0.0000)
        self.assertEqual(s_lines[0].m_lines[0].xcorr, 0.9294)
        self.assertEqual(s_lines[0].m_lines[0].sp, 499.000)
        self.assertEqual(s_lines[0].m_lines[0].matched_ions, 13)
        self.assertEqual(s_lines[0].m_lines[0].expected_ions, 77)
        self.assertEqual(s_lines[0].m_lines[0].sequence, 'R.TALLESDEHTCPTCHQNDVSPDALIANK.F')
        self.assertEqual(s_lines[0].m_lines[0].validation_status, 'U')
        self.assertEqual(s_lines[0].m_lines[0].predicted_ook0, 1.0606)
        self.assertEqual(s_lines[0].m_lines[0].tims_score, 0.9078)

        self.assertEqual(s_lines[0].m_lines[0].l_lines[0].locus_name, 'sp|Q7Z6E9|RBBP6_HUMAN')
        self.assertEqual(s_lines[0].m_lines[0].l_lines[0].peptide_index_in_protein_sequence, 285)
        self.assertEqual(s_lines[0].m_lines[0].l_lines[0].peptide_sequence, 'CIR.TALLESDEHTCPTCHQNDVSPDALIANK.FLR')

        self.assertEqual(s_lines[0].m_lines[2].predicted_ook0, None)
        self.assertEqual(s_lines[0].m_lines[2].tims_score, None)

        sqt_str = to_sqt(sqt_version, h_lines, s_lines)
        sqt_version, h_lines, s_lines = from_sqt(sqt_str)

        self.assertEqual(len(s_lines), 3)
        self.assertEqual(len(h_lines), 20)

        self.assertEqual(s_lines[0].low_scan, 194118)
        self.assertEqual(s_lines[0].high_scan, 194118)
        self.assertEqual(s_lines[0].charge, 3)
        self.assertEqual(s_lines[0].process_time, 18)
        self.assertEqual(s_lines[0].server, 'paser_Thread-195379')
        self.assertEqual(s_lines[0].experimental_mass, 3136.39819)
        self.assertEqual(s_lines[0].total_ion_intensity, 43217.00)
        self.assertEqual(s_lines[0].lowest_sp, 0.0131)
        self.assertEqual(s_lines[0].number_matches, 0)
        self.assertEqual(s_lines[0].experimental_ook0, 1.0633)

        self.assertEqual(s_lines[0].m_lines[0].xcorr_rank, 1)
        self.assertEqual(s_lines[0].m_lines[0].sp_rank, 0)
        self.assertEqual(s_lines[0].m_lines[0].calculated_mass, 3136.43097)
        self.assertEqual(s_lines[0].m_lines[0].delta_cn, 0.0000)
        self.assertEqual(s_lines[0].m_lines[0].xcorr, 0.9294)
        self.assertEqual(s_lines[0].m_lines[0].sp, 499.000)
        self.assertEqual(s_lines[0].m_lines[0].matched_ions, 13)
        self.assertEqual(s_lines[0].m_lines[0].expected_ions, 77)
        self.assertEqual(s_lines[0].m_lines[0].sequence, 'R.TALLESDEHTCPTCHQNDVSPDALIANK.F')
        self.assertEqual(s_lines[0].m_lines[0].validation_status, 'U')
        self.assertEqual(s_lines[0].m_lines[0].predicted_ook0, 1.0606)
        self.assertEqual(s_lines[0].m_lines[0].tims_score, 0.9078)

        self.assertEqual(s_lines[0].m_lines[0].l_lines[0].locus_name, 'sp|Q7Z6E9|RBBP6_HUMAN')
        self.assertEqual(s_lines[0].m_lines[0].l_lines[0].peptide_index_in_protein_sequence, 285)
        self.assertEqual(s_lines[0].m_lines[0].l_lines[0].peptide_sequence, 'CIR.TALLESDEHTCPTCHQNDVSPDALIANK.FLR')

        self.assertEqual(s_lines[0].m_lines[2].predicted_ook0, None)
        self.assertEqual(s_lines[0].m_lines[2].tims_score, None)

    def test_load_sqt_v2_1_0_ext(self):

        with open('data/sqt_V2_1_0_ext.sqt', 'r') as file:
            sqt_version, h_lines, s_lines = from_sqt(file)

        sqt_str = to_sqt(sqt_version, h_lines, s_lines)
        sqt_version, h_lines, s_lines = from_sqt(sqt_str)
