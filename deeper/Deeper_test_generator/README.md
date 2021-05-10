# Deeper_Generator_ADAS_ToolCompetition

**Deeper** is a simulation-based test generator using an evolutionary process (i.e., mainly NSGAII) for testing a DNN-based function, i.e., lane keeping system, in automotive domain. It has been mainly developed based on DeepJanus Test input generator (https://github.com/testingautomated-usi/DeepJanus/tree/master/DeepJanus-BNG), which is to explore the Frontier of Behaviours for Deep Learning System Testing and is shared under the MIT license.
The current test generator has been customized for <a href="https://sbst21.github.io/tools/">Cyber-Physical Systems Testing Competition</a> in <a href="https://sbst21.github.io/">SBST 2021</a>. It uses the provided code pipelines by the <a href="https://github.com/se2p/tool-competition-av">competition repository</a>.  

**Installation:**

For the installation of *BeamNG simulator*, please read the <a href="https://github.com/se2p/tool-competition-av/blob/main/documentation/INSTALL.md">installation guide</a> at the Cyber-Physical Systems Testing Competition repository.  

*Python:*

This code has been tested with Python 3.7.

*Other Libraries:*

To easily install the other dependencies with rely on pip, we suggest to create a dedicated virtual environment (we tested venv), activate and run the following command:

pip install -r requirements.txt

Then, please install the additional librararies, stated in "additional-requirements.txt", using the following command:

pip install -r additional-requirements.txt

*Shapely:*

You should download the wheel file matching you Python version, i.e. download the file with cp37 in the name if you use Python 3.7. The wheel file should also match the architecture of your machine, i.e., you should install the file with either win32 or win_amd64 in the name.

**Deeper_Test_Generator:**

The proposed generator has been placed in folder "Deeper Test Generators" and can be exeuted using a script like the following one:

python competition.py --time-budget INTEGER --executor beamng --beamng-home PATH --map-size INTEGER --oob-tolerance FLOAT --module-name Deeper_test_generators.deeper_test_generator --class-name DeeperTestGenerator

(P.S., It uses a set of initial seed population in folder "data -> member_seeds -> Seed_Population". Please do not remove the folder data and note that Deeper does not work with "mock" executor.)

**References:**

[1]. Riccio, V., & Tonella, P. (2020, November). Model-based exploration of the frontier of behaviours for deep learning system testing. In Proceedings of the 28th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering (pp. 876-888).
