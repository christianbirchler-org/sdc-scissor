#
# This illustrates how the code_pipeline can be used to run the sample test generator
#
import unittest
from click.testing import CliRunner


class RunOneGeneratorTest(unittest.TestCase):

    def test_code_pipeline(self):

        BEAMNG_HOME="C://BeamNG.tech.v0.23.5.1"
        BEAMNG_USER="C://BeamNG.tech.v0.23.5.1_userpath"

        from competition import generate
        runner = CliRunner()
        result = runner.invoke(generate, ['--visualize-tests',
                                          '--time-budget', '10'
                                          '--executor', 'beamng',
                                          '--beamng-home', BEAMNG_HOME,
                                          '--beamng-user', BEAMNG_USER,
                                          '--map-size', '200',
                                          '--module-name', 'sample_test_generators.one_test_generator',
                                          '--class-name OneTestGenerator'])
        assert result.exit_code == 0


if __name__ == '__main__':
    unittest.main()