# Contributing
## Feature Request
When contributing to this repository, please first discuss the change you wish to make in our Slack
or Discord channels. If the feature request is approved then a new issue is oppened to keep track
of the development of the featue. The issue should follow the provided `Feature` issue template.
In case you want to implement the feature by yourself then you can do it by forking the repository
and create a pull request to the `main` branch. A pull request is only accepted if it adheres to
the pull request process and all checks of the CI pipeline have passed.

In case you are a direct contributor with access to this repository please not that we follow a
[Scaled Trunk-Based Development](https://trunkbaseddevelopment.com/#scaled-trunk-based-development)
branching strategy. Rather having dedicated release branches we tag the releases directly on the
trunk (`main` branch). By tagging a release a dedicated CD piipeline is triggered that publishes
the release automatically on PyPI.

### Pull Request Process
1. Fork the SDC-Scissor repository
2. Implement your feature
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

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Code of Conduct
### Our Pledge
In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, gender identity and expression, level of experience,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

### Our Standards
Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

### Our Responsibilities
Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

### Scope
This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

### Enforcement
Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team at [birchler.chr@gmail.com](mailto:birchler.chr@gmail.com). All
complaints will be reviewed and investigated and will result in a response that
is deemed necessary and appropriate to the circumstances. The project team is
obligated to maintain confidentiality with regard to the reporter of an incident.
Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.

### Attribution
This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at [http://contributor-covenant.org/version/1/4][version]

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/
