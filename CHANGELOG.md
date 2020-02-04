# Changelog

## [Unreleased]

### Added

- nothing added

### Changed

- nothing changed

### Removed

- nothing removed

## [2.15.0]

### Added

- added parameter `use_tls`. It allows to activate or not the tls use within smtp connection. Default value is `True` for backward compatibility.
- added the check to ensure the SMTP server supports the auth extension before login

### Changed

- change function `get_connection` badly named `sender_email` parameter
- change the sender while sending over SMTP

### Removed

- removed unnecessary class EmailToConsole, since standard `smtpd` python module make the job.

## [2.14.0]

### Changed

- changed project configuration and documentation

## [2.13.0]

### Added

- first public release
