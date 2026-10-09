# Changelog

## [0.12.2](https://github.com/jackrayner/ha-pypowerwall/compare/0.12.1...0.12.2) (2026-10-09)


### Bug Fixes

* point the manifest and docs at the renamed ha-pypowerwall repository ([74cf524](https://github.com/jackrayner/ha-pypowerwall/commit/74cf524b5227ce79ff281b82d8e0fa011caa6854))
* point the manifest and docs at the renamed ha-pypowerwall repository ([154f475](https://github.com/jackrayner/ha-pypowerwall/commit/154f475d23477e6bd21253ccfb86e72d0d2cf49c))

## [0.12.1](https://github.com/jackrayner/hacs-pypowerwall/compare/0.12.0...0.12.1) (2026-10-09)


### Bug Fixes

* add a tariff currency sensor for Cloud and FleetAPI modes ([f116927](https://github.com/jackrayner/hacs-pypowerwall/commit/f116927ab0cec59383d89b9c284a93007e55bacb))
* add a tariff currency sensor for Cloud and FleetAPI modes ([ae7c2c1](https://github.com/jackrayner/hacs-pypowerwall/commit/ae7c2c12b1a6289b1c1041a540905d45f3c77c43))

## [0.12.0](https://github.com/jackrayner/hacs-pypowerwall/compare/0.11.0...0.12.0) (2026-10-09)


### Features

* make the TEDAPI v1r passwords optional (at least one required) ([7e338a1](https://github.com/jackrayner/hacs-pypowerwall/commit/7e338a1d13d0277f95587ebc917718b821a0984a))

## [0.11.0](https://github.com/jackrayner/hacs-pypowerwall/compare/0.10.0...0.11.0) (2026-10-08)


### Features

* add a disabled-by-default Battery calibration binary sensor ([3e3944e](https://github.com/jackrayner/hacs-pypowerwall/commit/3e3944ed40c3f1942e03c7fd27beba44faab929e))
* add alert-backed binary sensors via a description table ([400ee2d](https://github.com/jackrayner/hacs-pypowerwall/commit/400ee2de011ad1b5325f205b5ccaada813b2b995))
* alerts reference and alert-backed binary sensors ([5f6b474](https://github.com/jackrayner/hacs-pypowerwall/commit/5f6b4749ba09660ccef1fac131932781923b9646))
* **i18n:** translate the alert binary sensor and tariff sensor names into all locales ([a867500](https://github.com/jackrayner/hacs-pypowerwall/commit/a8675000f5ae9ac6b81d7c16b411c6352e1c341d))

## [0.10.0](https://github.com/jackrayner/hacs-pypowerwall/compare/0.9.0...0.10.0) (2026-10-08)


### Features

* expose alert names as an attribute on the active alerts sensor ([8cb11dc](https://github.com/jackrayner/hacs-pypowerwall/commit/8cb11dc980424598cd2f38bc30b14dda0eb1be60))
* expose alert names as an attribute on the active alerts sensor ([fe5cad6](https://github.com/jackrayner/hacs-pypowerwall/commit/fe5cad6df6903c09aa0dae67dd370f08c6ebe16b))

## [0.9.0](https://github.com/jackrayner/hacs-pypowerwall/compare/0.8.0...0.9.0) (2026-10-08)


### Features

* add read-only tariff sensors for Cloud and FleetAPI ([7204501](https://github.com/jackrayner/hacs-pypowerwall/commit/72045014d5148f2a8675fb63786ef07d6af69927))
* add read-only tariff sensors for Cloud and FleetAPI modes ([ea44fc8](https://github.com/jackrayner/hacs-pypowerwall/commit/ea44fc8fb133468dbfc646b6157a0f1fa193c22a))
* bump pypowerwall to 0.18.2 and add Powerwall 3 fan sensors ([5ca73f1](https://github.com/jackrayner/hacs-pypowerwall/commit/5ca73f1a29c7a0b0d5e47e7bbb8ac79bb5785e97))
* bump pypowerwall to 0.18.2 and add Powerwall 3 fan sensors ([99286b4](https://github.com/jackrayner/hacs-pypowerwall/commit/99286b423f0e22a413deae3197cc31b78497c5d9))
* **i18n:** translate the fan sensor names into all locales ([5386001](https://github.com/jackrayner/hacs-pypowerwall/commit/538600123245766500db1938cec990a0771db88e))

## [0.8.0](https://github.com/jackrayner/hacs-pypowerwall/compare/0.7.0...0.8.0) (2026-09-13)


### Features

* **config_flow:** add a reconfigure flow for connection settings ([5c16e95](https://github.com/jackrayner/hacs-pypowerwall/commit/5c16e953670e7dc631e62506fe044c741e1bc20e))
* **i18n:** translate the reconfigure flow strings into all locales ([26b21bf](https://github.com/jackrayner/hacs-pypowerwall/commit/26b21bf341b621523bab55161a2a8bc7c4a09d69))

## [0.7.0](https://github.com/jackrayner/hacs-pypowerwall/compare/0.6.3...0.7.0) (2026-09-12)


### Features

* **deps:** keep manifest.json's pypowerwall pin in sync and gate v1r-only grid controls ([31f52fa](https://github.com/jackrayner/hacs-pypowerwall/commit/31f52fa685d836e672e3dbfedc36caade394ca06))
* **deps:** keep manifest.json's pypowerwall pin in sync and gate v1r-only grid controls ([de029b5](https://github.com/jackrayner/hacs-pypowerwall/commit/de029b56f697461f51733e076e4e57ccced12ed2))


### Bug Fixes

* **tests:** use async_get_device_by_identifier instead of deprecated async_get_device ([0356ebf](https://github.com/jackrayner/hacs-pypowerwall/commit/0356ebf2ab240b89de0fbf21cb4cf78d3bd36cfc))

## [0.6.3](https://github.com/jackrayner/hacs-pypowerwall/compare/0.6.2...0.6.3) (2026-09-12)


### Bug Fixes

* **deps:** bump pypowerwall from 0.16.2 to 0.17.3 ([e057533](https://github.com/jackrayner/hacs-pypowerwall/commit/e0575336e23ff841236374dd3daf689472bdcf28))
* **deps:** bump pypowerwall from 0.16.2 to 0.17.3 ([b707248](https://github.com/jackrayner/hacs-pypowerwall/commit/b70724878ee86fb02214fdbb8dd1b902753dd6cf))

## [0.6.2](https://github.com/jackrayner/hacs-pypowerwall/compare/0.6.1...0.6.2) (2026-07-13)


### Bug Fixes

* raise pypowerwall request timeout, quiet duplicate error logging ([dcc8f6b](https://github.com/jackrayner/hacs-pypowerwall/commit/dcc8f6bcaa7d3058666793873b69305242af5f2b))
* raise pypowerwall request timeout, quiet duplicate error logging ([107d24b](https://github.com/jackrayner/hacs-pypowerwall/commit/107d24bc20b44a2af0daaa1bc376c549f9ed6f90))

## [0.6.1](https://github.com/jackrayner/hacs-pypowerwall/compare/0.6.0...0.6.1) (2026-07-12)


### Bug Fixes

* address 6 code review findings in pypowerwall integration ([fa5a512](https://github.com/jackrayner/hacs-pypowerwall/commit/fa5a512ddff1a5232732f183337a9d880e256e91))
* address code review findings in pypowerwall integration ([ebffe16](https://github.com/jackrayner/hacs-pypowerwall/commit/ebffe16929abfc64e1800144caa2fbf984a9a69c))
* bump hacs.json minimum Home Assistant version to 2026.3.0 ([880c2f1](https://github.com/jackrayner/hacs-pypowerwall/commit/880c2f1de2b0ca744aa251bba001a8f149e689d2))
* bump min HA version in hacs.json; docs: License and poll-interval range ([9f74957](https://github.com/jackrayner/hacs-pypowerwall/commit/9f74957364784c2da4e53ab788a622888ebd4582))

## [0.6.0](https://github.com/jackrayner/hacs-pypowerwall/compare/0.5.1...0.6.0) (2026-07-12)


### Features

* add British English (en-GB) locale, confirm US/metropolitan French baselines ([7c7e5fa](https://github.com/jackrayner/hacs-pypowerwall/commit/7c7e5fad4e78228c0c3067e32bdaab699e7681d3))
* add French (fr) and British English (en-GB) locales ([78091f5](https://github.com/jackrayner/hacs-pypowerwall/commit/78091f58b37974d64bb8969aeb8658c132500bfd))
* add French translation ([49f5499](https://github.com/jackrayner/hacs-pypowerwall/commit/49f549953bc7af55422d30ea402af2bc1106405a))
* add translations for all Home Assistant supported languages ([ace0dda](https://github.com/jackrayner/hacs-pypowerwall/commit/ace0dda057477d9deeab64f89dfd49cb580904ca))
* add translations for all Home Assistant supported languages ([8c960dd](https://github.com/jackrayner/hacs-pypowerwall/commit/8c960dda8d38cb6498fba7364ba75ae2b0afc164))
* add translations for all Home Assistant supported languages ([69f4077](https://github.com/jackrayner/hacs-pypowerwall/commit/69f4077a358cfa3b65f4f5780209543e4992cf01))
* relax translation CI check ahead of full HA language coverage ([e61118a](https://github.com/jackrayner/hacs-pypowerwall/commit/e61118af373c974a1ab0c8a8a2eb9a675cbe7c8d))


### Bug Fixes

* remove unused strings.json ([4402c2b](https://github.com/jackrayner/hacs-pypowerwall/commit/4402c2b16bc17718110191b3c9cb25d7a992e03b))
* remove unused strings.json ([0cac5ff](https://github.com/jackrayner/hacs-pypowerwall/commit/0cac5ff729651d9d0b47e4bc511d10afe9f02462))

## [0.5.1](https://github.com/jackrayner/hacs-pypowerwall/compare/0.5.0...0.5.1) (2026-07-12)


### Bug Fixes

* remove bogus unit from uptime sensor ([b2202f8](https://github.com/jackrayner/hacs-pypowerwall/commit/b2202f86867871260fef9865d3641f2346ce32d7))

## [0.5.0](https://github.com/jackrayner/hacs-pypowerwall/compare/0.4.1...0.5.0) (2026-07-12)


### Features

* add grid import/export power sensors and estimated energy integration sensors ([d6a0797](https://github.com/jackrayner/hacs-pypowerwall/commit/d6a07977c8df86cec3ac2b84f5b91ebf7bb48ede))
* split battery power into import/export sensors ([7a720a5](https://github.com/jackrayner/hacs-pypowerwall/commit/7a720a5fabd98fd3a5699cf1782bf517c77aac9d))

## [0.4.1](https://github.com/jackrayner/hacs-pypowerwall/compare/0.4.0...0.4.1) (2026-07-11)


### Bug Fixes

* exclude CHANGELOG.md from markdownlint ([adddc64](https://github.com/jackrayner/hacs-pypowerwall/commit/adddc64f2e39ddf5072dac11670d1d642a12c8b8))

## [0.4.0](https://github.com/jackrayner/hacs-pypowerwall/compare/0.3.0...0.4.0) (2026-07-11)


### Features

* add battery energy charged/discharged sensors for the Energy dashboard ([2a67898](https://github.com/jackrayner/hacs-pypowerwall/commit/2a67898d59e3cccf24b6601b38a120d7f1f52ce5))


### Bug Fixes

* Update logos and icons ([027540e](https://github.com/jackrayner/hacs-pypowerwall/commit/027540ee4716deb424978718cf3952538f86407f))
* Update logos and icons ([9536e88](https://github.com/jackrayner/hacs-pypowerwall/commit/9536e889dce37b1dbf67cf42fb30ca5dc4a13fdf))

## [0.3.0](https://github.com/jackrayner/hacs-pypowerwall/compare/0.2.0...0.3.0) (2026-07-11)


### Features

* add remaining pypowerwall write actions ([1ffa4be](https://github.com/jackrayner/hacs-pypowerwall/commit/1ffa4beac85d7b3cf2d2065c0d5f506f33e40eae))
* add remaining pypowerwall write actions ([eee6478](https://github.com/jackrayner/hacs-pypowerwall/commit/eee647879e0a9ab7edacb1f321338d94b0cd2161))

## [0.2.0](https://github.com/jackrayner/hacs-pypowerwall/compare/0.1.0...0.2.0) (2026-07-11)


### Features

* add battery reserve and mode controls ([93d3d2f](https://github.com/jackrayner/hacs-pypowerwall/commit/93d3d2f0444e02ba07e6e103d6a858b041df14f1))
