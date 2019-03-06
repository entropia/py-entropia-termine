# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] 2019-03-XX
### Added
- Event class
- Date and time parsing in Event() base on the locale (default: de_DE)
- Default duration for events without end date.

### Changed
- Module now returns a list of Event classes instead of dicts

### Removed
- Unused requests import

## [1.1.0] 2019-03-05
### Added
- Module can now be used standalone
- Documentation

### Changed
- Changed internal methods and attributes to 'private'

## [1.0.0] 2019-03-04
 - Initial release
