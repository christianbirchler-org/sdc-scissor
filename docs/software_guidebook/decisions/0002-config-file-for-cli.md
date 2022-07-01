# Config File for CLI
* status: accepted
* date: 2022-07-01
* deciders: Christian Birchler
* consulted: -
* informed: -

## Context and Problem Statement
The configuration of SDC-Scissor was mainly done over the CLI. Since the tool has many various commands and options it
is not very user-friendly to type all the configs in the console.

## Decision Drivers
* Usability

## Considered Options
* Use a separate configuration file
* The user configures SDC-Scissor with environment variables

## Decision Outcome

Chosen option: "Use a separate configuration file", because
this enables the possibility to easily share the same setup via one config file that is useful for reproduce experiments.
