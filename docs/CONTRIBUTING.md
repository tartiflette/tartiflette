# Contributing to Tartiflette

:tada: Thanks for being here :tada:

- [Contributing to Tartiflette](#contributing-to-tartiflette)
  - [Code of conduct](#code-of-conduct)
  - [How can I contribute?](#how-can-i-contribute)
    - [Reporting bugs](#reporting-bugs)
    - [Suggesting enhancements](#suggesting-enhancements)
    - [Pull Requests](#pull-requests)
  - [Changelog](#changelog)

## Code of conduct

We expect from each contributor to respect for the [Code of Conduct](./CODE-OF-CONDUCT.md) which governs the **Tartiflette** project.

## How can I contribute?

### Reporting bugs

To report a bug, please [create an issue on github](https://github.com/dailymotion/tartiflette/issues/new) and follow the guidelines below.

Please provide the steps to reproduce your problem and, if possible, a full reproducible environment. **As we are working directly with containers, please provide the Dockerfile sample or the Docker image name**

* [ ] **Explain with a simple sentence the expected behavior**
* [ ] **Tartiflette version:** _e.g 0.1.0_
* [ ] **Python version:** _e.g 3.6_
* [ ] **Executed in docker:** _Yes|No_
* [ ] **Dockerfile sample:** _Link of sample_
* [ ] **GraphQL Schema & Query:** _e.g gist, pastebin or directly the query_
* [ ] **Is it a regression from a previous versions?** _e.g Yes|No_
* [ ] **Stack trace**

### Suggesting enhancements

* A feature is missing from the GraphQL Specification?
* A hook is missing in the API to plug your code?
* A part of the project could be improved?

Don't hesitate to ask a new feature or join in and send us a pull request with your own feature!

Before coding anything, make sure to:

* **Stage 1 - Proposal:** Propose your changes/ideas through an issue _(optional)_
* **Stage 2 - Draft:** Push your code & create a pull-request with the `WHY` of your work.
* **Stage 3 - Candidate:** Stable code, tested & documented.
* **Stage 4 - :tada:** Your code is merged and available.

### Pull Requests

Before submitting your pull-request, make sure the following is done.

* [ ] Fork [the repository](https://github.com/dailymotion/tartiflette) and create your branch from `master` so that it can be merged easily.
* [ ] Update CHANGELOG.md with your change (include reference to the issue & this PR).
* [ ] Make sure all of the significant new logic is covered by tests.
* [ ] Make sure all quality checks are green _[(Gazr specification)](https://gazr.io)_.

## Changelog

All notable changes to this project will be documented in the [CHANGELOG.md](https://github.com/dailymotion/tartiflette/blob/master/CHANGELOG.md) file.
