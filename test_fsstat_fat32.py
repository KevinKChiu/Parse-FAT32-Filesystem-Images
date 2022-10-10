import logging
import unittest
from subprocess import run

from gradescope_utils.autograder_utils.decorators import partial_credit, weight

import fsstat

FILENAME = "fsstat.py"


class TestFormatting(unittest.TestCase):
    @weight(5)
    def test_part0_black(self):
        p = run(["black", "--quiet", "--check", FILENAME])
        self.assertEqual(
            p.returncode, 0, f"Black return code of {p.returncode} indicates a problem."
        )

    @weight(5)
    def test_part0_isort(self):
        p = run(
            [
                "isort",
                "--profile",
                "black",
                "--quiet",
                "--check-only",
                FILENAME,
            ]
        )
        self.assertEqual(
            p.returncode, 0, f"isort return code of {p.returncode} indicates a problem."
        )

    @weight(5)
    def test_part0_flake8(self):
        p = run(
            [
                "flake8",
                "--max-line-length=110",
                "--ignore=E203,W503",
                "--quiet",
                "--quiet",
                "--select=F,N",
                FILENAME,
            ]
        )
        self.assertEqual(
            p.returncode,
            0,
            f"flake8 return code of {p.returncode} indicates a problem.",
        )


class TestParseReservedPartition(unittest.TestCase):
    @partial_credit(60.0)
    def test_parse_part1_reserved_partition(self, set_score=None):
        fs = fsstat.Fat("./fat32-1.empty.dd")
        expected = {
            "bytes_per_sector": 512,
            "sectors_per_cluster": 2,
            "reserved_sectors": 414,
            "number_of_fats": 2,
            "total_sectors": 2060288,
            "sectors_per_fat": 7985,
            "root_dir_first_cluster": 2,
            "bytes_per_cluster": 1024,
            "fat0_sector_start": 414,
            "fat0_sector_end": 8398,
            "data_start": 16384,
            "data_end": 2060287,
        }
        score = 0
        incorrect = []
        for key in expected:
            if key in fs.boot:
                if fs.boot[key] == expected[key]:
                    score += 5
                else:
                    incorrect.append(key)
        # score must be set ahead of the assert
        set_score(score)
        msg = f"The following boot sector keys are incorrect: {incorrect}"
        self.assertEqual(fs.boot, expected, msg=msg)


class TestClusterChain(unittest.TestCase):
    @partial_credit(20.0)
    def test_part2_cluster_chain(self, set_score=None):
        self.maxDiff = None
        total_points = 0
        all_expected = {
            1: [
                ("./fat32-1.empty.dd", 2, [16384, 16385]),
                ("./fat32-1.empty.dd", 4, [16388, 16389]),
            ],
            2: [
                ("./fat32-4.non-empty.dd", 4, [16388, 16389]),
                ("./fat32-4.non-empty.dd", 7, [16394, 16395]),
            ],
            # fmt: off
            3: [("./fat32-5.add-images.dd", 550, [17480, 17481, 17482, 17483, 17484, 17485, 17486, 17487, 17488, 17489, 17490, 17491, 17492, 17493, 17494, 17495, 17496, 17497, 17498, 17499, 17500, 17501, 17502, 17503, 17504, 17505, 17506, 17507, 17508, 17509, 17510, 17511, 17512, 17513, 17514, 17515, 17516, 17517, 17518, 17519, 17520, 17521, 17522, 17523, 17524, 17525, 17526, 17527, 17528, 17529, 17530, 17531, 17532, 17533, 17534, 17535, 17536, 17537, 17538, 17539, 17540, 17541, 17542, 17543, 17544, 17545, 17546, 17547, 17548, 17549, 17550, 17551, 17552, 17553, 17554, 17555, 17556, 17557, 17558, 17559, 17560, 17561, 17562, 17563, 17564, 17565, 17566, 17567, 17568, 17569, 17570, 17571, 17572, 17573, 17574, 17575, 17576, 17577, 17578, 17579, 17580, 17581, 17582, 17583, 17584, 17585, 17586, 17587, 17588, 17589, 17590, 17591, 17592, 17593, 17594, 17595, 17596, 17597, 17598, 17599, 17600, 17601, 17602, 17603, 17604, 17605, 17606, 17607, 17608, 17609, 17610, 17611, 17612, 17613, 17614, 17615, 17616, 17617, 17618, 17619, 17620, 17621, 17622, 17623, 17624, 17625, 17626, 17627, 17628, 17629, 17630, 17631, 17632, 17633, 17634, 17635, 17636, 17637, 17638, 17639, 17640, 17641, 17642, 17643, 17644, 17645])], 
            4: [("./fat32-5.add-images.dd", 9, [16398, 16399, 16400, 16401, 16402, 16403, 16404, 16405, 16406, 16407, 16408, 16409, 16410, 16411, 16412, 16413, 16414, 16415, 16416, 16417, 16418, 16419, 16420, 16421, 16422, 16423, 16424, 16425, 16426, 16427, 16428, 16429, 16430, 16431, 16432, 16433, 16434, 16435, 16436, 16437, 16438, 16439, 16440, 16441, 16442, 16443, 16444, 16445, 16446, 16447, 16448, 16449, 16450, 16451, 16452, 16453, 16454, 16455, 16456, 16457, 16458, 16459, 16460, 16461, 16462, 16463, 16464, 16465, 16466, 16467, 16468, 16469, 16470, 16471, 16472, 16473, 16474, 16475, 16476, 16477, 16478, 16479, 16480, 16481, 16482, 16483, 16484, 16485, 16486, 16487, 16488, 16489, 16490, 16491, 16492, 16493, 16494, 16495, 16496, 16497, 16498, 16499, 16500, 16501, 16502, 16503, 16504, 16505, 16506, 16507, 16508, 16509, 16510, 16511, 16512, 16513, 16514, 16515, 16516, 16517, 16518, 16519, 16520, 16521, 16522, 16523, 16524, 16525, 16526, 16527, 16528, 16529, 16530, 16531, 16532, 16533, 16534, 16535, 16536, 16537, 16538, 16539, 16540, 16541, 16542, 16543, 16544, 16545, 16546, 16547, 16548, 16549, 16550, 16551, 16552, 16553, 16554, 16555, 16556, 16557, 16558, 16559, 16560, 16561, 16562, 16563, 16564, 16565, 16566, 16567, 16568, 16569, 16570, 16571, 16572, 16573, 16574, 16575, 16576, 16577, 16578, 16579, 16580, 16581, 16582, 16583, 16584, 16585, 16586, 16587, 16588, 16589, 16590, 16591, 16592, 16593, 16594, 16595, 16596, 16597, 16598, 16599, 16600, 16601, 16602, 16603, 16604, 16605, 16606, 16607, 16608, 16609, 16610, 16611, 16612, 16613, 16614, 16615, 16616, 16617, 16618, 16619, 16620, 16621, 16622, 16623, 16624, 16625, 16626, 16627, 16628, 16629, 16630, 16631, 16632, 16633, 16634, 16635, 16636, 16637, 16638, 16639, 16640, 16641, 16642, 16643, 16644, 16645, 16646, 16647, 16648, 16649, 16650, 16651, 16652, 16653, 16654, 16655, 16656, 16657, 16658, 16659, 16660, 16661, 16662, 16663, 16664, 16665, 16666, 16667, 16668, 16669, 16670, 16671, 16672, 16673, 16674, 16675, 16676, 16677, 16678, 16679, 16680, 16681, 16682, 16683, 16684, 16685, 16686, 16687, 16688, 16689, 16690, 16691, 16692, 16693, 16694, 16695, 16696, 16697, 16698, 16699, 16700, 16701, 16702, 16703, 16704, 16705, 16706, 16707, 16708, 16709, 16710, 16711, 16712, 16713, 16714, 16715, 16716, 16717, 16718, 16719, 16720, 16721, 16722, 16723, 16724, 16725, 16726, 16727, 16728, 16729, 16730, 16731, 16732, 16733, 16734, 16735, 16736, 16737, 16738, 16739, 16740, 16741, 16742, 16743, 16744, 16745, 16746, 16747, 16748, 16749, 16750, 16751, 16752, 16753, 16754, 16755, 16756, 16757, 16758, 16759, 16760, 16761, 16762, 16763, 16764, 16765, 16766, 16767, 16768, 16769, 16770, 16771, 16772, 16773, 16774, 16775, 16776, 16777, 16778, 16779, 16780, 16781, 16782, 16783, 16784, 16785, 16786, 16787, 16788, 16789, 16790, 16791, 16792, 16793, 16794, 16795, 16796, 16797, 16798, 16799, 16800, 16801, 16802, 16803, 16804, 16805, 16806, 16807, 16808, 16809, 16810, 16811, 16812, 16813, 16814, 16815, 16816, 16817, 16818, 16819, 16820, 16821, 16822, 16823, 16824, 16825, 16826, 16827, 16828, 16829, 16830, 16831, 16832, 16833, 16834, 16835, 16836, 16837, 16838, 16839, 16840, 16841, 16842, 16843, 16844, 16845, 16846, 16847, 16848, 16849, 16850, 16851, 16852, 16853, 16854, 16855, 16856, 16857, 16858, 16859, 16860, 16861, 16862, 16863, 16864, 16865, 16866, 16867, 16868, 16869, 16870, 16871, 16872, 16873, 16874, 16875, 16876, 16877, 16878, 16879, 16880, 16881, 16882, 16883, 16884, 16885, 16886, 16887, 16888, 16889, 16890, 16891, 16892, 16893, 16894, 16895, 16896, 16897, 16898, 16899, 16900, 16901, 16902, 16903, 16904, 16905, 16906, 16907, 16908, 16909, 16910, 16911, 16912, 16913, 16914, 16915, 16916, 16917, 16918, 16919, 16920, 16921, 16922, 16923, 16924, 16925, 16926, 16927, 16928, 16929, 16930, 16931, 16932, 16933, 16934, 16935, 16936, 16937, 16938, 16939, 16940, 16941, 16942, 16943, 16944, 16945, 16946, 16947, 16948, 16949, 16950, 16951, 16952, 16953, 16954, 16955, 16956, 16957, 16958, 16959, 16960, 16961, 16962, 16963, 16964, 16965, 16966, 16967, 16968, 16969, 16970, 16971, 16972, 16973, 16974, 16975, 16976, 16977, 16978, 16979, 16980, 16981, 16982, 16983, 16984, 16985, 16986, 16987, 16988, 16989, 16990, 16991, 16992, 16993, 16994, 16995, 16996, 16997, 16998, 16999, 17000, 17001, 17002, 17003, 17004, 17005, 17006, 17007, 17008, 17009, 17010, 17011, 17012, 17013, 17014, 17015, 17016, 17017, 17018, 17019, 17020, 17021, 17022, 17023, 17024, 17025, 17026, 17027, 17028, 17029, 17030, 17031, 17032, 17033, 17034, 17035, 17036, 17037, 17038, 17039, 17040, 17041, 17042, 17043, 17044, 17045, 17046, 17047, 17048, 17049, 17050, 17051, 17052, 17053, 17054, 17055, 17056, 17057, 17058, 17059, 17060, 17061, 17062, 17063, 17064, 17065, 17066, 17067, 17068, 17069, 17070, 17071, 17072, 17073, 17074, 17075, 17076, 17077, 17078, 17079, 17080, 17081, 17082, 17083, 17084, 17085, 17086, 17087, 17088, 17089, 17090, 17091, 17092, 17093, 17094, 17095, 17096, 17097, 17098, 17099, 17100, 17101, 17102, 17103, 17104, 17105, 17106, 17107, 17108, 17109, 17110, 17111, 17112, 17113, 17114, 17115, 17116, 17117, 17118, 17119, 17120, 17121, 17122, 17123, 17124, 17125, 17126, 17127, 17128, 17129, 17130, 17131, 17132, 17133, 17134, 17135, 17136, 17137, 17138, 17139, 17140, 17141, 17142, 17143, 17144, 17145, 17146, 17147, 17148, 17149, 17150, 17151, 17152, 17153, 17154, 17155, 17156, 17157, 17158, 17159, 17160, 17161, 17162, 17163, 17164, 17165, 17166, 17167, 17168, 17169, 17170, 17171, 17172, 17173, 17174, 17175, 17176, 17177, 17178, 17179, 17180, 17181, 17182, 17183, 17184, 17185, 17186, 17187, 17188, 17189, 17190, 17191, 17192, 17193, 17194, 17195, 17196, 17197, 17198, 17199, 17200, 17201, 17202, 17203, 17204, 17205, 17206, 17207, 17208, 17209, 17210, 17211, 17212, 17213, 17214, 17215, 17216, 17217, 17218, 17219, 17220, 17221, 17222, 17223, 17224, 17225, 17226, 17227, 17228, 17229, 17230, 17231, 17232, 17233, 17234, 17235, 17236, 17237, 17238, 17239, 17240, 17241, 17242, 17243, 17244, 17245, 17246, 17247, 17248, 17249, 17250, 17251, 17252, 17253, 17254, 17255, 17256, 17257, 17258, 17259, 17260, 17261, 17262, 17263, 17264, 17265, 17266, 17267, 17268, 17269, 17270, 17271, 17272, 17273, 17274, 17275, 17276, 17277, 17278, 17279, 17280, 17281, 17282, 17283, 17284, 17285, 17286, 17287, 17288, 17289, 17290, 17291, 17292, 17293, 17294, 17295, 17296, 17297, 17298, 17299, 17300, 17301, 17302, 17303, 17304, 17305, 17306, 17307, 17308, 17309, 17310, 17311, 17312, 17313, 17314, 17315, 17316, 17317, 17318, 17319, 17320, 17321, 17322, 17323, 17324, 17325, 17326, 17327, 17328, 17329, 17330, 17331, 17332, 17333, 17334, 17335, 17336, 17337, 17338, 17339, 17340, 17341, 17342, 17343, 17344, 17345, 17346, 17347, 17348, 17349, 17350, 17351, 17352, 17353, 17354, 17355, 17356, 17357, 17358, 17359, 17360, 17361, 17362, 17363, 17364, 17365, 17366, 17367, 17368, 17369, 17370, 17371, 17372, 17373, 17374, 17375, 17376, 17377, 17378, 17379, 17380, 17381, 17382, 17383, 17384, 17385, 17386, 17387, 17388, 17389, 17390, 17391, 17392, 17393, 17394, 17395, 17396, 17397, 17398, 17399, 17400, 17401, 17402, 17403, 17404, 17405, 17406, 17407, 17408, 17409, 17410, 17411, 17412, 17413, 17414, 17415, 17416, 17417, 17418, 17419, 17420, 17421, 17422, 17423, 17424, 17425, 17426, 17427, 17428, 17429, 17430, 17431, 17432, 17433, 17434, 17435, 17436, 17437, 17438, 17439, 17440, 17441, 17442, 17443, 17444, 17445, 17446, 17447, 17448, 17449, 17450, 17451, 17452, 17453, 17454, 17455, 17456, 17457, 17458, 17459, 17460, 17461, 17462, 17463, 17464, 17465, 17466, 17467, 17468, 17469, 17470, 17471, 17472, 17473, 17474, 17475, 17476, 17477, 17478, 17479])]
            # fmt: on
        }
        all_results = {}
        for test_num in all_expected:
            score = 5
            results = list()
            for filename, cluster, expected in all_expected[test_num]:
                fs = fsstat.Fat(filename)
                results.append((filename, cluster, fs._get_sectors(cluster)))
                if fs._get_sectors(cluster) != expected:
                    score = 0
            total_points += score
            all_results[test_num] = results
        set_score(total_points)
        logging.debug(f"all_expected: {all_expected}")
        self.assertEqual(
            all_results,
            all_expected,
            msg="                               "
            f"Your results: {all_results}                                                         "
            f"Expected resulted:\n{all_expected}",
        )


class TestGetContent(unittest.TestCase):
    @weight(20.0)
    def test_part3_1_get_content(self):
        fs = fsstat.Fat("./fat32-4.non-empty.dd")
        results = fs._retrieve_data(7)
        expected = b"This is non-unicode content in a file. \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        self.assertEqual(results, expected)


class TestParseDir(unittest.TestCase):
    @partial_credit(30)
    def test_part3_2_parse_dir(self, set_score=None):
        fs = fsstat.Fat("./fat32-4.non-empty.dd")
        self.assertIn("root_dir_first_cluster", fs.boot)
        all_files = fs.parse_dir(fs.boot["root_dir_first_cluster"])
        root_entry_0 = {
            "parent": "",
            "dir_cluster": 2,
            "entry_num": 0,
            "dir_sectors": [16384, 16385],
            "entry_type": "vol",
            "name": "ASSIGN4",
            "deleted": False,
        }
        root_entry_1 = {
            "parent": "",
            "dir_cluster": 2,
            "entry_num": 1,
            "dir_sectors": [16384, 16385],
            "entry_type": "lfn",
            "name": " Information",
            "deleted": False,
        }

        root_entry_3 = {
            "parent": "",
            "dir_cluster": 2,
            "entry_num": 3,
            "dir_sectors": [16384, 16385],
            "entry_type": "dir",
            "name": "SYSTEM~1",
            "deleted": False,
        }
        root_entry_4 = {
            "parent": "",
            "dir_cluster": 2,
            "entry_num": 4,
            "dir_sectors": [16384, 16385],
            "entry_type": "0x20",
            "name": "EMPTY.TXT",
            "deleted": False,
        }
        root_entry_6 = {
            "parent": "",
            "dir_cluster": 2,
            "entry_num": 6,
            "dir_sectors": [16384, 16385],
            "entry_type": "0x20",
            "name": "_SCII.TXT",
            "deleted": True,
        }
        score = 0.0
        correct_entries = list()
        for entry in [
            root_entry_0,
            root_entry_1,
            root_entry_3,
            root_entry_4,
            root_entry_6,
        ]:
            for result in all_files:
                if (
                    entry["parent"] == result["parent"]
                    and entry["name"] == result["name"]
                    and entry["entry_num"] == result["entry_num"]
                    and entry["dir_cluster"] == result["dir_cluster"]
                    and entry["entry_type"] == result["entry_type"]
                    and entry["deleted"] == result["deleted"]
                ):
                    score += 6
                    correct_entries.append(entry)
        set_score(score)
        self.assertEqual(
            correct_entries,
            [
                root_entry_0,
                root_entry_1,
                root_entry_3,
                root_entry_4,
                root_entry_6,
            ],
            (
                f"Expected {correct_entries} to be "
                f"{[root_entry_0, root_entry_1, root_entry_3, root_entry_4,root_entry_6]}"
            ),
        )

    @partial_credit(20)
    def test_part3_3_parse_dir_recursively(self, set_score=None):
        fs = fsstat.Fat("./fat32-4.non-empty.dd")
        self.assertIn("root_dir_first_cluster", fs.boot)
        all_files = fs.parse_dir(fs.boot["root_dir_first_cluster"])

        subdir_entry_0 = {
            "parent": "/SYSTEM~1",
            "dir_cluster": 3,
            "entry_num": 0,
            "dir_sectors": [16386, 16387],
            "entry_type": "dir",
            "name": ".",
            "deleted": False,
        }
        subdir_entry_1 = {
            "parent": "/SYSTEM~1",
            "dir_cluster": 3,
            "entry_num": 1,
            "dir_sectors": [16386, 16387],
            "entry_type": "dir",
            "name": "..",
            "deleted": False,
        }
        subdir_entry_3 = {
            "parent": "/SYSTEM~1",
            "dir_cluster": 3,
            "entry_num": 3,
            "dir_sectors": [16386, 16387],
            "entry_type": "lfn",
            "name": "WPSettings.da",
            "deleted": False,
        }
        subdir_entry_4 = {
            "parent": "/SYSTEM~1",
            "dir_cluster": 3,
            "entry_num": 4,
            "dir_sectors": [16386, 16387],
            "entry_type": "0x20",
            "name": "WPSETT~1.DAT",
            "deleted": False,
            "content_cluster": 4,
        }
        score = 0.0
        correct_entries = list()
        for entry in [subdir_entry_0, subdir_entry_1, subdir_entry_3, subdir_entry_4]:
            for result in all_files:
                if (
                    entry["parent"] == result["parent"]
                    and entry["name"] == result["name"]
                    and entry["entry_num"] == result["entry_num"]
                    and entry["dir_cluster"] == result["dir_cluster"]
                    and entry["entry_type"] == result["entry_type"]
                    and entry["deleted"] == result["deleted"]
                    and (
                        entry["content_cluster"] == result["content_cluster"]
                        if "content_cluster" in result
                        else True
                    )
                ):
                    score += 5
                    correct_entries.append(entry)

        set_score(score)
        self.assertEqual(
            correct_entries,
            [
                subdir_entry_0,
                subdir_entry_1,
                subdir_entry_3,
                subdir_entry_4,
            ],
            (
                f"Expected {correct_entries} to be "
                f"{[subdir_entry_0, subdir_entry_1, subdir_entry_3, subdir_entry_4]}"
            ),
        )

    @weight(7.5)
    def test_part3_4_get_content_1(self):
        fs = fsstat.Fat("./fat32-5.add-images.dd")
        self.assertIn("root_dir_first_cluster", fs.boot)
        all_files = fs.parse_dir(fs.boot["root_dir_first_cluster"])

        ascii_text = {
            "parent": "",
            "dir_cluster": 2,
            "entry_num": 7,
            "dir_sectors": [16384, 16385],
            "entry_type": "0x20",
            "name": "ASCII.TXT",
            "deleted": False,
            "content_cluster": 7,
            "filesize": 39,
            "content_sectors": [16394, 16395],
            "content": "b'This is non-unicode content in a file. '",
            "slack": "b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'",
        }
        self.assertIn(ascii_text, all_files)

    @weight(7.5)
    def test_part3_4_get_content_2(self):
        fs = fsstat.Fat("./fat32-7.delete-all.dd")
        self.assertIn("root_dir_first_cluster", fs.boot)
        all_files = fs.parse_dir(fs.boot["root_dir_first_cluster"])
        deleted_file_1 = {
            "parent": "",
            "dir_cluster": 2,
            "entry_num": 7,
            "dir_sectors": [16384, 16385],
            "entry_type": "0x20",
            "name": "_SCII.TXT",
            "deleted": True,
            "content_cluster": 7,
            "filesize": 39,
            "content_sectors": [],
            "content": "b'This is non-unicode content in a file. '",
            "slack": None,
        }
        self.assertIn(deleted_file_1, all_files)

    @weight(7.5)
    def test_part3_4_get_content_3(self):
        fs = fsstat.Fat("./fat32-7.delete-all.dd")
        self.assertIn("root_dir_first_cluster", fs.boot)
        all_files = fs.parse_dir(fs.boot["root_dir_first_cluster"])
        deleted_file_2 = {
            "parent": "",
            "dir_cluster": 2,
            "entry_num": 5,
            "dir_sectors": [16384, 16385],
            "entry_type": "0x20",
            "name": "_ONEMPTY.TXT",
            "deleted": True,
            "content_cluster": 6,
            "filesize": 68,
            "content_sectors": [],
            "content": "b'\\xff\\xfeT\\x00h\\x00i\\x00s\\x00 \\x00f\\x00i\\x00l\\x00e\\x00 \\x00c\\x00o\\x00n\\x00t\\x00e\\x00n\\x00t\\x00 \\x00i\\x00s\\x00 \\x00n\\x00o\\x00t\\x00 \\x00e\\x00m\\x00p\\x00t\\x00y\\x00.\\x00\\r\\x00\\n\\x00'",
            "slack": None,
        }
        self.assertIn(deleted_file_2, all_files)

    @weight(7.5)
    def test_part3_4_get_slack(self):
        fs = fsstat.Fat("./fat32-7.delete-all.dd")
        self.assertIn("root_dir_first_cluster", fs.boot)
        all_files = fs.parse_dir(fs.boot["root_dir_first_cluster"])
        slack_file = {
            "parent": "",
            "dir_cluster": 2,
            "entry_num": 14,
            "dir_sectors": [16384, 16385],
            "entry_type": "0x20",
            "name": "SLACK.TXT",
            "deleted": False,
            "content_cluster": 5,
            "filesize": 36,
            "content_sectors": [16390, 16391],
            "content": "b'This file has slack data available. '",
            "slack": "b'The butler did it!\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'",
        }
        self.assertIn(slack_file, all_files)


if __name__ == "__main__":
    unittest.main()
