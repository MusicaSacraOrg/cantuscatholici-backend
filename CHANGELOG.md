# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Refresh token functionality for extended user sessions
  - Added `RefreshToken` database model with revocation support
  - Updated login and register endpoints to return both access and refresh tokens
  - Added `/user/refresh` endpoint to exchange refresh tokens for new access tokens
  - Implemented refresh token lifecycle management (create, verify, revoke)
  - Implemented token rotation: old refresh tokens are automatically revoked when new tokens are issued
  - Added `InvalidRefreshTokenException` for handling invalid refresh tokens
  - Added `AUTH_REFRESH_TOKEN_EXPIRE_DAYS` configuration (default: 7 days)
  - Created database migration for `refresh_tokens` table

### Changed

- Token response schema now includes `refresh_token` field alongside `access_token`
- Access tokens expire in 30 minutes, refresh tokens in 7 days
- Improved transaction handling in refresh endpoint to prevent race conditions and ensure atomic operations
- Fixed timezone issue in token expiration checks by using UTC-aware timestamps
- Fixed `RefreshTokenRequest` schema alias configuration to accept camelCase input (`refreshToken` instead of `refresh_token`)
- Added database commit in `create_refresh_token_for_user` to ensure tokens are persisted

### Testing

- Added 7 comprehensive tests for refresh token functionality:
  - `test_user_register_returns_refresh_token` - Verifies register endpoint returns refreshToken
  - `test_user_login_returns_refresh_token` - Verifies login endpoint returns refreshToken
  - `test_user_refresh_token_success` - Tests full refresh flow and token exchange
  - `test_user_refresh_token_rotation_prevents_reuse` - Verifies token rotation security
  - `test_user_refresh_token_invalid_token` - Tests rejection of invalid tokens
  - `test_user_refresh_token_empty_token` - Tests rejection of empty tokens
- All 13 tests passing (including 6 existing user authentication tests)
- Added `conftest.py` to Docker image for proper test fixture discovery
