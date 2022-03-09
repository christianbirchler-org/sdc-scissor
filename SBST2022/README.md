# Cyber-Physical Systems Testing Competition #

The [SBST Workshop](https://sbst22.github.io/) offers a challenge for software testers who want to work with self-driving cars in the context of the usual [tool competition](https://sbst22.github.io/tools/).

## Important Dates

The deadline to submit your tool is: **January 21st 2022**

The results of the evaluation will be communicated to participants on: **February 25th 2022**

The camera-ready paper describing your tool is due to: **Sunday March 18th 2020**

## Goal ##
The competitors should generate virtual roads to test a lane keeping assist system using the provided code_pipeline.

The generated roads are evaluated in the [**BeamNG.tech**](https://www.beamng.tech/) driving simulator.
This simulator is ideal for researchers due to its state-of-the-art soft-body physics simulation, ease of access to sensory data, and a Python API to control the simulation.

[![Video by BeamNg GmbH](https://github.com/BeamNG/BeamNGpy/raw/master/media/steering.gif)](https://github.com/BeamNG/BeamNGpy/raw/master/media/steering.gif)

>Note: BeamNG GmbH, the company developing the simulator, kindly offers it for free for researcher purposes upon registration (see [Installation](documentation/INSTALL.md)).

## Comparing the Test Generators ##

Deciding which test generator is the best is far from trivial and, currently, remains an open challenge. In this competition, we rank test generators by considering various metrics of effectiveness and efficiency that characterize the generated tests but also the process of generating them, i.e., test generation. We believe that our approach to compare test generators is objective and fair, and it can provide a compact metric to rank them.

### Ranking Formula

The formula to rank test generators is the following weighted sum:

```
rank = a * OOB_Coverage + b * test_generation_efficiency + c *  test_generation_effectiveness
```

where:

- `OOB_Coverage` captures the effectiveness of the generated tests that must expose as many failures as possible (i.e., Out Of Bound episodes) but also as many different failures as possible. We compute this metric by extending the approach adopted in the previous edition of the competition with our recent work on [Illumination Search](https://dl.acm.org/doi/10.1145/3460319.3464811). As an example, our novel approach has been already adopted for the generation of relevant test cases from existing maps (see [SALVO](https://ieeexplore.ieee.org/document/9564107)). Therefore, we identify tests' portion relevant to the OOBs, extract their structural and behavioral features, and populate feature maps of a predefined size (i.e., 25x25 cells). Finally, we define `OOB_Coverage` by counting the cells in the map covered by the exposed OOBs. **Larger values of `OOB_Coverage` identify better test generators.**

- `test_generation_efficiency` captures the efficiency in generating, but not executing, the tests. We measure it as the inverse of the average time it takes for the generators to create the tests normalized using the following (standard) formula: 

    ``` norm(x) = (x - min) / (max - min)```

    Where `min` and `max` are values empirically found during the benchmarking as the minimum and maximum average times for generating test across all the competitors.

- `test_generation_effectiveness` captures the ability of the test generator to create valid tests; therefore, we compute it as the ratio of valid tests over all the generated tests.


### Setting the Weights

We set the values of the in the ranking formula's weights (i.e., `a`, `b`, and `c`) to rank higher the test generators that trigger many and different failures; test generation efficiency and effectiveness are given equal but secondary importance. The motivation behind this choice is that test generators' main goal is to trigger failures, while being efficient and effective in generating the tests is of second order importance.

The following table summarizes the proposed weight assignment:

| a | b | c |
|---|---|---|
|0.6|0.2|0.2|



## Implement Your Test Generator ##
We make available a [code pipeline](code_pipeline) that will integrate your test generator with the simulator by validating, executing and evaluating your test cases. Moreover, we offer some [sample test generators](sample_test_generators/README.md) to show how to use our code pipeline.

## Information About the Competition ##
More information can be found on the SBST tool competition website: [https://sbst22.github.io/tools/](https://sbst22.github.io/tools/)

## Repository Structure ##
[Code pipeline](code_pipeline): code that integrates your test generator with the simulator

[Self driving car testing library](self_driving): library that helps the integration of the test input generators, our code pipeline, and the BeamNG simulator

[Scenario template](levels_template/tig): basic scenario used in this competition

[Documentation](documentation/README.md): contains the installation guide, detailed rules of the competition, and the frequently asked questions

[Sample test generators](sample_test_generators/README.md): sample test generators already integrated with the code pipeline for illustrative purposes 

[Requirements](requirements.txt): contains the list of the required packages.


## License ##
The software we developed is distributed under GNU GPL license. See the [LICENSE.md](LICENSE.md) file.

## Contacts ##

Dr. Alessio Gambi  - Passau University, Germany - alessio.gambi@uni-passau.de

Dr. Vincenzo Riccio  - Universita' della Svizzera Italiana, Lugano, Switzerland - vincenzo.riccio@usi.ch
