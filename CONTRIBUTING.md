# Contributing
## Feature Request
When contributing to this repository, please first discuss the change you wish to make on our
[GitHub Discussions](https://github.com/ChristianBirchler/sdc-scissor/discussions).
If the feature request is approved then a new issue is opened to keep track
of the development of the feature. The issue should follow the provided `Feature` issue template.
In case you want to implement the feature by yourself then you can do it by forking the repository
and create a pull request to the `main` branch. A pull request is only accepted if it adheres to
the pull request process and all checks of the CI pipeline have passed.

In case you are a direct contributor with access to this repository please note that we follow a
[Scaled Trunk-Based Development](https://trunkbaseddevelopment.com/#scaled-trunk-based-development)
branching strategy. Rather having dedicated release branches we tag the releases directly on the
trunk (`main` branch). By tagging a release a dedicated CD pipeline is triggered that publishes
the release automatically on PyPI.

### Pull Request Process
1. Fork the SDC-Scissor repository
2. Implement your feature (**NOTE**: Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) commit message style!)
3. Provide test implementations
   - Unit tests
   - Integration tests
   - System tests
4. Format your code with `poetry run black -C -l 120 .` command
5. Open a pull request to SDC-Scissor's `main` branch
6. Follow the instructions of the code reviewer

## Bug Report
In case you want to report a bug then open directly a new issue with the `Bug` issue template.
Please fill all the sections in the provided template so that the resolvement of the bug can be
done as efficient as possible.

Please note we have a [Code of Conduct](https://github.com/ChristianBirchler/sdc-scissor/blob/main/CODE_OF_CONDUCT.md),
please follow it in all your interactions with the project.
