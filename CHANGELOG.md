# Changelog

All notable changes to the HeadyConnection project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Reorganized repository structure into three main domains:
  - **HeadySystems/**: Infrastructure, backend services, and deployment configurations
  - **HeadyDirective/**: Documentation, governance policies, and compliance materials
  - **HeadyConnection/**: Community portal and frontend (planned for future development)
- Moved GitHub workflows and dependabot configuration to HeadyDirective/.github/
- Moved LICENSE, README, DELIVERY_MANIFEST, and patches.md to HeadyDirective/
- Consolidated duplicate heady_demo_kit folder into HeadySystems/
- Updated .gitignore to exclude Python artifacts and zip files

### Added
- Created mcp_config.json for Model Context Protocol configuration
- Created render.yaml for deployment on Render.com
- Created CHANGELOG.md to track project changes
- Created ARCHITECTURE.md documenting the new repository structure
- Added comprehensive root README.md

### Fixed
- Removed orphaned __pycache__ directories
- Renamed files with spaces in names (DELIVERY_MANIFEST, zip files)

## [0.1.0] - 2026-01-24

### Added
- Initial repository setup
- HeadySystems demo kit and project scaffolding
- Basic project structure with heady-fleet workspace
- execute_build.py utility for automated builds
