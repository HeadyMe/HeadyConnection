# HeadyConnection Repository

Official repository for HeadySystems Inc. and HeadyConnection Inc. - A comprehensive ecosystem for building secure, scalable, and compliant systems.

## 📁 Repository Structure

This repository is organized into three main domains:

### **HeadySystems/** - Infrastructure & Backend
The core infrastructure, backend services, and deployment configurations.

- **heady-fleet/**: Multi-project workspace containing:
  - `auth-service`: Authentication and identity management (auth.heady.io)
  - `guardian-gateway`: Security services and gateway
  - `home-hub-beta`: Home automation hardware integration
  - `symphony-node-01`: Symphony orchestration node
  - `heady-bank-core`: Financial services core
  
- **heady_project/**: Core project modules and services
  - `src/`: Source code for various Heady components
  - `config/`: Project configuration files

- **execute_build.py**: Automated build utility for cloning repos, extracting packages, and running build scripts
- **run_demo.py**: Demo runner for the Heady ecosystem
- **projects.json**: Workspace configuration defining all projects

### **HeadyDirective/** - Documentation & Governance
Documentation, governance policies, security, and compliance materials.

- **README.md**: Ecosystem overview
- **LICENSE**: Project license
- **DELIVERY_MANIFEST.md**: Release artifacts and checksums
- **patches.md**: Comprehensive patch history and changes
- **.github/**: GitHub workflows and automation
  - `workflows/codeql.yml`: Code security scanning
  - `dependabot.yml`: Dependency management

### **HeadyConnection/** - Community & Frontend *(Planned)*
Future home for community portal, frontend applications, and event management.

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Git

### Running the Demo

```bash
# Clone the repository
git clone https://github.com/HeadyMe/HeadyConnection.git
cd HeadyConnection

# Run the demo
python3 HeadySystems/run_demo.py
```

### Building Projects

Use the `execute_build.py` utility to automate repository cloning, package extraction, and builds:

```bash
python3 HeadySystems/execute_build.py \
    --repo-url https://github.com/HeadyConnection/Heady.git \
    --zip-file /path/to/HeadySystems_package_v1_0_0.zip \
    --build-script Heady_Golden_Master_Builder_v_1_0_0.py \
    --work-dir /tmp/heady_build \
    --output-dir /tmp/heady_package
```

## 📋 Project Configuration

The repository uses two main configuration files:

### **mcp_config.json**
Model Context Protocol configuration for the Heady ecosystem, defining server configurations and workspace structure.

### **render.yaml**
Deployment configuration for Render.com, including:
- Demo web service
- Documentation static site

## 🏗️ Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed information about:
- System design and components
- Trust domains and security boundaries
- Data isolation principles
- Deployment architecture

## 🔒 Security & Compliance

- **Data Isolation**: Strict isolation between verticals is mandatory
- **Trust Domains**: Each vertical operates within its own compliance boundary
- **Zero Cross-Vertical Sharing**: No database sharing or data replication between verticals
- **Metadata-Only Exchange**: Shared services may only exchange non-sensitive routing metadata

## 📚 Documentation

- [HeadyDirective README](HeadyDirective/README.md) - Official ecosystem documentation
- [Delivery Manifest](HeadyDirective/DELIVERY_MANIFEST.md) - Release artifacts and checksums
- [Patches](HeadyDirective/patches.md) - Comprehensive patch history
- [Demo Guide](HeadySystems/DEMO_README.md) - Demo execution instructions

## 🤝 Contributing

This repository follows strict governance and compliance requirements. All changes must:
- Respect data isolation boundaries
- Maintain security and compliance standards
- Follow the architectural principles outlined in ARCHITECTURE.md

## 📄 License

See [LICENSE](HeadyDirective/LICENSE) for details.

## 🔗 Links

- **Organization**: HeadySystems Inc. & HeadyConnection Inc.
- **Repository**: https://github.com/HeadyMe/HeadyConnection

---

*For questions or support, please open an issue in this repository.*
