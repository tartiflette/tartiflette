# Tartiflette Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Released]

## [Unreleased]
### Fixed
- Change the way README.md is read in setup.py for long_description, now file is closed after reading.

## [0.1.7] - 2018-11-12
### Added
- (Query) Support Alias in Query and Mutation

## [0.1.6] - 2018-10-31
### Added
- (CI) Integrate missing Grammar

### Fixed
- Retrieve the appropriate operation type with operation definition.
- (SDL) Remove useless type and add Line/Col info propagation
- Add missing "UnknownDirectiveDefinition" imports

## [0.1.5] - 2018-10-11
### Added
- (CI) Integrate missing Grammar

## [0.1.4] - 2018-10-09
### Added
- (SDL / Executor) Implement declaration and execution of custom directives
- (SDL) Implement Interfaces
- (SDL) Implement Scalar Types
- (SDL) Implement directive `@Deprecated`
- (Executor) Implement Introspection and Dynamic intropection _(Documentation needed)_

### Changed
- Executor engine

## [Unreleased]

## [0.1.0] - 2018-01-26
### Added
- README.md & LICENSE
