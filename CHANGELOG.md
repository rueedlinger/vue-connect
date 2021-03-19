# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added multiple connect clusters support ([#5][i5])
- Added JSON editor to improve user experience ([#37][i37])

[i5]: https://github.com/rueedlinger/vue-connect/issues/5
[i37]: https://github.com/rueedlinger/vue-connect/issues/37

### Changed

- Store shared state ([#32][i32], [#49][i49])
  - replaced SQLite with Redis
  - connect cluster state
  - error message
  - downtime of the failed connector

[i32]: https://github.com/rueedlinger/vue-connect/issues/32
[i49]: https://github.com/rueedlinger/vue-connect/issues/32

## [0.4.0] - 2021-02-23

### Added

- Support front-end filtering ([#11][i11])

### Changed

- Display style of the reload button ([#33][i33])
- Support custom polling time ([#13][i13])
- Handle Kafka Connect API downtime ([#4][i4])

[i4]: https://github.com/rueedlinger/vue-connect/issues/4
[i11]: https://github.com/rueedlinger/vue-connect/issues/11
[i13]: https://github.com/rueedlinger/vue-connect/issues/13
[i33]: https://github.com/rueedlinger/vue-connect/issues/33

### Fixed

- Removed tooltips to fix loading animation for the cluster operations.

## [0.3.0] - 2021-02-05

### Added

- When a connector or task has the state FAILURE show details on the main page ([#25][i25])
- Added a container image of the latest version of the master branch ([#9][i9])

[i9]: https://github.com/rueedlinger/vue-connect/issues/9
[i25]: https://github.com/rueedlinger/vue-connect/issues/25

### Changed

- Optimize list sort and display abnormal connectors first ([#10][i10])
- Supports icon state switching after clicking ([#12][i12])
- Changed frontend polling interval to 1 minute and catch errors.

[i10]: https://github.com/rueedlinger/vue-connect/issues/10
[i12]: https://github.com/rueedlinger/vue-connect/issues/12
[i15]: https://github.com/rueedlinger/vue-connect/issues/15

### Fixed

- Optimize the implementation of obtaining the status of connectors ([#3][i3])
- Added request timeout to 5 sec in backend to fix requests accumulate when the network connection times out ([#15][i15])

[i3]: https://github.com/rueedlinger/vue-connect/issues/3

## [0.2.0] - 2021-02-02

### Changed

- Replaced Pure CSS with Bulma

## [0.1.0] - 2020-10-09

### Added

- First version of the Docker Image with
  - _vue-connect-ui_ - Fontend with Vue.js.
  - _vue-connect-api_ - Backend API in Python.
- This CHANGELOG file to hopefully serve as an evolving example of a
  standardized open source project CHANGELOG.
