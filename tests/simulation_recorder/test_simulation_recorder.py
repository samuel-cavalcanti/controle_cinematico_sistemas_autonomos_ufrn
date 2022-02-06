import unittest
import tempfile
from src.modules.simulation_recorder import SimulationRecorder, SimulationCSVRecorder


class SimulationTestCase(unittest.TestCase):

    def test_simulation_csv_recorder(self):

        headers = ['x', 'y', 'z']

        recorder: SimulationRecorder = SimulationCSVRecorder(headers)

        with self.assertRaises(AssertionError):
            recorder.add_sample([1, 2])

        recorder.add_sample([1, 2, 3])

        read_and_write_mode = 'r+'

        temp_file = tempfile.NamedTemporaryFile(mode=read_and_write_mode)

        recorder.save(temp_file.name)

        expected_content = 'x,y,z\n1,2,3\n'

        with open(temp_file.name) as csv_file:
            content = csv_file.read()
            self.assertEqual(content, expected_content)
