import unittest

from serenipy.ms2 import to_ms2, from_ms2


class TestMs2(unittest.TestCase):

    def test_load_ms2_from_file(self):

        with open('data/sample.ms2', 'r') as file:
            header, ms2_spectras = from_ms2(file)

        self.assertEqual(len(ms2_spectras), 3)
        self.assertEqual(len(header), 15)
        self.assertEqual(ms2_spectras[0].low_scan, 2)
        self.assertEqual(ms2_spectras[0].high_scan, 2)
        self.assertEqual(ms2_spectras[0].mz, 514.8916)
        self.assertEqual(ms2_spectras[0].mass, 514.8916)
        self.assertEqual(ms2_spectras[0].charge, 1)
        self.assertEqual(ms2_spectras[0].info['TIMSTOF_Parent_ID'], '1')
        self.assertEqual(ms2_spectras[0].info['RetTime'], '0.6534')

        ms2_str = to_ms2(header, ms2_spectras)
        header, ms2_spectras = from_ms2(ms2_str)

        self.assertEqual(len(ms2_spectras), 3)
        self.assertEqual(len(header), 15)
        self.assertEqual(ms2_spectras[0].low_scan, 2)
        self.assertEqual(ms2_spectras[0].high_scan, 2)
        self.assertEqual(ms2_spectras[0].mz, 514.8916)
        self.assertEqual(ms2_spectras[0].mass, 514.8916)
        self.assertEqual(ms2_spectras[0].charge, 1)
        self.assertEqual(ms2_spectras[0].info['TIMSTOF_Parent_ID'], '1')
        self.assertEqual(ms2_spectras[0].info['RetTime'], '0.6534')
