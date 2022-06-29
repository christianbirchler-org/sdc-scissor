# Principles

## Research
SDC-Scissor is meant to be used for research in the first place. This means that the architecture of the tool must be
highly modularized so that the development of new testing pipelines is easier and more productive.

## Best Practices
The architecture and development of SDC-Scissor should be done by applying best practices such as:
* Use of appropriate design patterns
* Extensively testing on different levels:
    * Unit
    * System
* Conducting code reviews for each pull request

## Continuous Integration
The development of SDC-Scissor integrates the code changes continuously to the `main` branch (ideally multiple times per
day). Features branched will be directly integrated into the `main` branch after approval of the code reviewer. The
merge will trigger a GitHub workflow and executes all the tests. The outcome of the test execution will be reported in
the according badge on top of the `README.md` or on top of the Documentation homepage.
