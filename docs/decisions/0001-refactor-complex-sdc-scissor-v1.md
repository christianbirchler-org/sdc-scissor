# Refactor Complex SDC-Scissor v1.0
* status: accepted
* date: 2022-03-*
* deciders: Christian Birchler
* consulted: Sebastiano Panichella
* informed: Sebastiano Panichella, Alessio Gambi, Sajad Khatiri

## Context and Problem Statement
SDC-Scissor v1.0 is heavily based on the complex
[SBST tool competition platform](https://github.com/se2p/tool-competition-av). To add another simulator or other
test generators is difficult due to high coupling and high technical debt.

<!-- This is an optional element. Feel free to remove. -->
## Decision Drivers
* providing reusable code
* improve code quality

## Considered Options
1. Refactor the system and modularize the code base
2. Stick with the tool competition platform

## Decision Outcome
Chosen option: Option 1, because
it is the only option for having a sustainable platform for future research that allows to integrate easier new code
to the repository without breaking existing functionality.

<!-- This is an optional element. Feel free to remove. -->
### Positive Consequences
It improves the quality of the system and allows us to do more efficient research on SDCs.

<!-- This is an optional element. Feel free to remove. -->
### Negative Consequences
Time of 3 work weeks are required to reengineer the system and to implement and to test.
