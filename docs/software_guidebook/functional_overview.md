# Functional Overview
SDC-Scissor provides a variety of functionalities that users can leverage for their purposes. The main high-level
functionalities are described in this section. If you have questions about more the low-level functionalities then you
can also ask the community on
[Slack](https://join.slack.com/t/sdc-scissor/shared_invite/zt-1aikrj1uu-Dz0a9BE1AQ4GQp4A3Bm5og) or
[Discord](https://discord.gg/AaYnBS6s7E).

## Virtual Environments
SDC-Scissor is capabable in running the same test in different simulators. The architecture allows the use of identical
interfaces for different external simulators, e.g., [BeamNG.tech](https://beamng.tech/) and [CARLA](https://carla.org/).


## State-of-the-Art Test Generators
The use of the recent test generators from the [SBST Workshop](https://sbst22.github.io/) allows the user of SDC-Scissor
to generate diverse and meaningful tests automatically without ccreating them manually. The SBST workschop is an annual
event co-located with the
[ACM/IEEE International Conference on Software Engineering (ICSE)](https://conf.researchr.org/home/icse-2022), the top
conference in the field of academic software engineering.

## Regression Testing
The goal of regression testing is to detect faults in a software system as early as possible in the testing process
after a change was pushed to the repository. According to [1], regression testing consists of three components: (i) selection,
(ii) prioritization, and (iii) minimization.

### Test Selection
SDC-Scissor predicts the outcome of tests before executing them. This allows us in the context of regression testing to
select only those tests that are predicted to fail. By disregarding the tests that will likely fail we can speed up the
testing process as shown in [2].

### Test Prioritization
Detecting faults early in the testing process is achieved by applying a single-objective and a multi-objective genetic
algorithms as described in [3]. The goal is to find a permutation that runs first the most diverse and less costly
tests.

### Test Minimization *(not implemented)*
SDC-Scissor is able to shrink a test case only to the relevant part. The relevant part is the cause of a failure. The
goal of minimizing a test scenario is to save time in simulation by omitting the parts of a scenario that are seen as
safe for the car.

## SDC-Scissor Library
Testers of SDCs can use SDC-Scissor as a library. It supports the building process of building different testing
pipelines according to the user's needs.

## References
* [1] S. Yoo, M. Harman, "Regression testing minimization, selection and prioritization: a survey",
      *Software: Testing, Verification and Reliability*, vol. 22, no. 2, pp. 67-120, Mar. 2012, doi: 10.1002/stvr.430
* [2] C. Birchler, N. Ganz, S. Khatiri, A. Gambi, S. Panichella,
      "Cost-effective Simulation-based Test Selection in Self-driving Cars Software with SDC-Scissor",
      *2022 IEEE International Conference on Software Analysis, Evolution and Reengineering (SANER)*,
      Honolulu, HI, USA (online), Mar. 15-18 2022, pp. 164-168, doi: 10.1109/SANER53432.2022.00030
* [3] C. Birchler, S. Khatiri, P. Derakhshanfar, S. Panichella, A. Panichella,
      "Single and Multi-objective Test Cases Prioritization for Self-driving Cars in Virtual Environments",
      *ACM Transactions on Software Engineering and Methodology (TOSEM)*, Just Accepted, doi: 10.1145/3533818
