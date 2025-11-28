<div align="center">

# 🔐 CipherSim

### Educational Password Security Simulation Tool

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/CipherSim)
[![Python](https://img.shields.io/badge/python-3.12+-green.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Security](https://img.shields.io/badge/security-OWASP%20ASVS%205.1-red.svg)](SECURITY.md)
[![Educational](https://img.shields.io/badge/use-educational%20only-yellow.svg)](#ethical-use)

**A 2025-grade cybersecurity education platform featuring modern password hashing, safe offline attack simulations, interactive defense demonstrations, and comprehensive security learning modules.**

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Documentation](#-documentation) • [Learning Path](#-learning-path)

---

</div>

## ⚠️ Educational Use Only

> **IMPORTANT**: This tool is designed exclusively for **authorized security training**, **cybersecurity education**, and **professional red-team exercises**. Any malicious use is strictly prohibited and may violate applicable laws.

**CipherSim operates:**
- ✅ **Offline only** - No network connectivity
- ✅ **Demo data only** - No real credentials
- ✅ **Safe simulations** - Educational demonstrations
- ✅ **Ethical framework** - Strong compliance standards

---

## 📑 Table of Contents

- [Features](#-features)
  - [Password Analysis](#password-analysis)
  - [Modern Hashing](#modern-hashing)
  - [Attack Simulations](#attack-simulations)
  - [Defense Mechanisms](#defense-mechanisms)
  - [Educational Modules](#educational-modules)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage Examples](#-usage-examples)
- [Learning Path](#-learning-path)
- [Documentation](#-documentation)
- [Technology Stack](#-technology-stack)
- [Security & Compliance](#-security--compliance)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🔍 Password Analysis

Advanced password security analysis with comprehensive metrics:

- **Entropy Calculation** - Shannon entropy in bits
- **Pattern Detection** - Keyboard patterns, sequences, dates, repetition
- **Dictionary Checking** - Common password identification
- **Strength Scoring** - 0-100 score with 5 strength categories
- **Crack Time Estimates** - Real-world time-to-crack calculations
- **Smart Recommendations** - Context-specific security advice

```bash
$ ciphersim analyze "MyPassword123!"
```

### 🔒 Modern Hashing

2025 industry-standard password hashing algorithms:

| Algorithm | Year | Security | 2025 Status |
|-----------|------|----------|-------------|
| **Argon2id** | 2015 | ⭐⭐⭐⭐⭐ | ✅ **RECOMMENDED** |
| **scrypt** | 2009 | ⭐⭐⭐⭐ | ✅ Good |
| **bcrypt** | 1999 | ⭐⭐⭐ | ⚠️ Legacy (Still OK) |
| **PBKDF2** | 2000 | ⭐⭐⭐ | ⚠️ Acceptable |

- ✅ Memory-hard algorithms (GPU-resistant)
- ✅ Configurable parameters
- ✅ Time-to-crack estimation
- ✅ Compliance with NIST SP 800-63B

```bash
$ ciphersim hash "MySecurePassword2025!"
```

### ⚔️ Attack Simulations

**Safe, offline-only** password attack demonstrations:

| Attack Mode | Description | Use Case |
|-------------|-------------|----------|
| 🔤 **Dictionary** | Try common passwords | Test against known weak passwords |
| 🔢 **Brute Force** | All combinations | See exponential difficulty |
| 🔀 **Hybrid** | Dictionary + mutations | Test l33t speak resistance |
| 🎭 **Mask** | Pattern-based | Test structured passwords |
| 🎯 **Credential Stuffing** | Demo mode only | Understand breach risks |

**Safety Features:**
- Rate limiting (realistic ~10K attempts/sec)
- Maximum attempt limits
- Offline-only operation
- Demo data exclusively

```bash
$ ciphersim simulate --target "password123"
```

### 🛡️ Defense Mechanisms

Interactive demonstrations of security controls:

- **Rate Limiting** - Throttle login attempts
- **Account Lockout** - Auto-lock after failures
- **Progressive Delay** - Exponential backoff
- **IP Throttling** - Per-IP address limits
- **Honeytoken Passwords** - Trap password alerts
- **Multi-Factor Authentication (MFA)** - Why MFA defeats attacks

```bash
$ ciphersim defend --defense mfa
```

### 📚 Educational Modules

Comprehensive cybersecurity learning content:

| Topic | What You'll Learn |
|-------|-------------------|
| 🔐 **Hashing** | How password hashing works, one-way functions |
| 📊 **Entropy** | Why longer passwords are stronger |
| 🧂 **Salting** | How salts prevent rainbow tables |
| 🌈 **Rainbow Tables** | Attack mechanism and prevention |
| 🔬 **Algorithms** | Argon2id vs bcrypt vs PBKDF2 comparison |
| ✅ **Best Practices** | NIST SP 800-63B & OWASP guidelines |
| ⚔️ **Attack Methods** | All common attack vectors explained |

```bash
$ ciphersim learn hashing
```

---

## 🚀 Quick Start

### One-Minute Demo

```bash
# 1. Analyze a password (see how weak "password123" is!)
ciphersim analyze "password123"

# 2. Learn about password security
ciphersim learn hashing

# 3. Try interactive mode (easiest way to explore)
ciphersim interactive
```

### First Attack Simulation

```bash
# See how fast a dictionary attack finds "password"
ciphersim simulate --target "password"

# Test your own password
ciphersim simulate --target "YourPasswordHere"
```

### See Defenses in Action

```bash
# Watch rate limiting block 95% of attacks
ciphersim defend --defense rate_limiting

# Learn why MFA is critical
ciphersim defend --defense mfa
```

---

## 📦 Installation

### Prerequisites

- **Python 3.12+** ([Download](https://www.python.org/downloads/))
- pip package manager

### Install Steps

```bash
# 1. Navigate to CipherSim directory
cd CipherSim

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install CipherSim
pip install -e .

# 4. Verify installation
ciphersim --version
```

**Expected output:** `ciphersim, version 1.0.0`

### Troubleshooting

<details>
<summary>❌ "Command not found: ciphersim"</summary>

**Solution:**
```bash
# Try with Python module syntax
python -m ciphersim --help

# Or reinstall with --user flag
pip install --user -e .
```
</details>

<details>
<summary>❌ "ModuleNotFoundError: No module named 'argon2'"</summary>

**Solution:**
```bash
# Install dependencies first
pip install -r requirements.txt
```
</details>

---

## 💻 Usage Examples

### Password Analysis

<details open>
<summary><b>Click to see examples</b></summary>

```bash
# Check a weak password
$ ciphersim analyze "password123"

# Analyze a strong passphrase
$ ciphersim analyze "correct horse battery staple"

# Get detailed recommendations
$ ciphersim analyze "MyP@ssw0rd" --verbose
```

**Sample Output:**
```
🔍 Password Security Analysis

Metrics
┌──────────────────────┬────────────────┐
│ Property             │ Value          │
├──────────────────────┼────────────────┤
│ Length               │ 15             │
│ Character Set Size   │ 72             │
│ Entropy              │ 94.02 bits     │
│ Score                │ 85/100         │
│ Strength             │ VERY STRONG    │
└──────────────────────┴────────────────┘
```
</details>

### Attack Simulations

<details>
<summary><b>Click to see examples</b></summary>

```bash
# Dictionary attack (default mode)
$ ciphersim simulate --target "password"

# Brute force attack
$ ciphersim simulate --mode brute_force --target "abc"

# Hybrid attack with mutations
$ ciphersim simulate --mode hybrid --target "Welcome2024"

# Mask-based attack (e.g., Pass + 3 digits)
$ ciphersim simulate --mode mask --target "Pass123" --mask "?u?l?l?l?d?d?d"
```
</details>

### Defense Demonstrations

<details>
<summary><b>Click to see examples</b></summary>

```bash
# Rate limiting demo
$ ciphersim defend --defense rate_limiting

# Account lockout simulation
$ ciphersim defend --defense account_lockout

# Progressive delay visualization
$ ciphersim defend --defense progressive_delay

# MFA explanation
$ ciphersim defend --defense mfa
```
</details>

### Learning Modules

<details>
<summary><b>Click to see examples</b></summary>

```bash
# List all topics
$ ciphersim learn

# Learn about password hashing
$ ciphersim learn hashing

# Understand entropy (password strength)
$ ciphersim learn entropy

# Compare algorithms
$ ciphersim learn algorithms

# Security best practices
$ ciphersim learn best_practices
```
</details>

### Interactive Mode

```bash
# Launch menu-driven interface (easiest!)
$ ciphersim interactive
```

**Menu Options:**
1. Analyze Password
2. Hash Password
3. Simulate Attack
4. Demonstrate Defense
5. Learn Security Concepts
6. GPU Performance Comparison
7. Exit

---

## 🎓 Learning Path

### 🟢 Beginner Track (Week 1)

**Goal:** Understand password security basics

1. **Day 1**: `ciphersim learn hashing` - How hashing works
2. **Day 2**: `ciphersim analyze` - Test various passwords
3. **Day 3**: `ciphersim learn entropy` - Why length matters
4. **Day 4**: `ciphersim learn salt` - Salt and pepper concepts  
5. **Day 5**: `ciphersim defend --defense mfa` - Best defense

### 🟡 Intermediate Track (Week 2)

**Goal:** Learn attack techniques and defenses

1. **Day 1**: `ciphersim learn rainbow_tables` - Classic attack
2. **Day 2**: `ciphersim simulate` - Try dictionary attacks
3. **Day 3**: `ciphersim simulate --mode brute_force` - Exponential difficulty
4. **Day 4**: `ciphersim defend` - All defense types
5. **Day 5**: `ciphersim learn algorithms` - Algorithm comparison

### 🔴 Advanced Track (Week 3)

**Goal:** Master implementation and best practices

1. **Day 1**: `ciphersim learn attacks` - All attack vectors
2. **Day 2**: `ciphersim learn best_practices` - NIST/OWASP guidelines
3. **Day 3**: `ciphersim gpu` - GPU performance analysis
4. **Day 4**: Build password policies using insights
5. **Day 5**: Review `SECURITY.md` for compliance

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| **[README.md](README.md)** | This file - Complete user guide |
| **[QUICKSTART.md](QUICKSTART.md)** | 5-minute getting started tutorial |
| **[COMMAND_REFERENCE.md](COMMAND_REFERENCE.md)** | Quick command cheat sheet |
| **[SECURITY.md](SECURITY.md)** | Security policy & compliance (OWASP, NIST) |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Technical overview & architecture |
| **[LICENSE](LICENSE)** | MIT License with ethical use clause |

### Command Help

All commands have detailed help:

```bash
ciphersim --help              # Show all commands
ciphersim analyze --help      # Analyze command help
ciphersim simulate --help     # Simulate command help
ciphersim defend --help       # Defend command help
ciphersim learn --help        # Learn command help
```

---

## 🛠️ Technology Stack

### Core Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Core language | 3.12+ |
| **argon2-cffi** | Argon2id hashing | 23.1.0+ |
| **cryptography** | scrypt, PBKDF2 | 42.0.0+ |
| **bcrypt** | bcrypt hashing | 4.1.2+ |
| **rich** | Beautiful CLI | 13.7.0+ |
| **click** | CLI framework | 8.1.7+ |
| **PyYAML** | Configuration | 6.0.1+ |

### Standards Compliance

- ✅ **OWASP ASVS 5.1** - Application Security Verification Standard
- ✅ **NIST SP 800-63B** - Digital Identity Guidelines
- ✅ **MITRE ATT&CK** - Adversarial simulation rules
- ✅ **RFC 9106** - Argon2 specification

---

## 🔒 Security & Compliance

### Safety Guarantees

| Feature | Status |
|---------|--------|
| Offline-only operation | ✅ Enforced |
| No real credentials | ✅ Demo data only |
| No network requests | ✅ No network code |
| Ethical warnings | ✅ Prominent everywhere |
| Rate limiting | ✅ Built-in |

### Compliance Standards

**OWASP ASVS 5.1:**
- V2.1: Password Security Requirements ✅
- V8.2: Client-side Data Protection ✅

**NIST SP 800-63B:**
- Section 5.1.1: Memorized Secret Verifiers ✅
- Section 5.1.1.2: Salt and Iteration Count ✅

**MITRE ATT&CK:**
- T1110: Brute Force (Simulation only) ✅

[📄 Read full security policy](SECURITY.md)

---

## 📂 Project Structure

```
CipherSim/
├── 📄 README.md                    ← You are here
├── 📄 QUICKSTART.md                ← 5-minute tutorial
├── 📄 SECURITY.md                  ← Security & compliance
├── 📄 LICENSE                      ← MIT + ethical clause
├── 📄 requirements.txt             ← Dependencies
├── 📄 pyproject.toml               ← Project config
│
├── 📁 src/ciphersim/              ← Source code
│   ├── cli.py                      ← CLI interface
│   ├── core/
│   │   ├── hash_engine.py          ← Hashing algorithms
│   │   ├── attack_simulator.py     ← Attack simulations
│   │   └── defense_simulator.py    ← Defense demos
│   └── modules/
│       ├── password_analyzer.py    ← Strength analysis
│       └── learning.py             ← Educational content
│
├── 📁 config/                     ← Configuration
│   └── simulation_config.yaml      ← Settings
│
└── 📁 data/                       ← Educational datasets
    ├── common_passwords.txt        ← 100 common passwords
    └── wordlist_subset.txt         ← 200 word dictionary
```

---

## 🎯 Use Cases

### 👨‍🎓 For Students

- Learn cryptography fundamentals
- Understand password security
- Hands-on cybersecurity practice
- Project for security courses

### 👨‍💻 For Developers

- Implement secure authentication
- Choose correct hashing algorithm
- Test password policies
- Security training workshops

### 👨‍🏫 For Instructors

- Live attack/defense demos
- Interactive security lessons
- Assessment material
- Compliance training

### 🏢 For Organizations

- Security awareness training
- Developer education
- Red team exercises
- Policy development

---

## 🌟 Key Improvements Over DevBrute

| Aspect | DevBrute (2023) | CipherSim (2025) |
|--------|-----------------|------------------|
| **Python Version** | 3.7-3.9 | 3.12+ |
| **Primary Hash** | MD5, SHA1 | Argon2id ✅ |
| **UI** | Basic print | Rich library 🎨 |
| **CLI Framework** | argparse | Click ⚡ |
| **Educational** | None | 7 modules 📚 |
| **Defenses** | None | 6 mechanisms 🛡️ |
| **Documentation** | 1 README | 6 documents 📖 |
| **Compliance** | None | OWASP + NIST ✅ |

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Important**: All contributions must maintain the educational focus and ethical standards of this project.

### Areas for Contribution

- 🌐 Web UI (Next.js + WebAssembly)
- 📊 HTML report generation
- 🔌 Have I Been Pwned integration
- 🌍 Internationalization (i18n)
- 📝 Additional learning modules
- 🧪 Comprehensive test suite

---

## 📄 License

MIT License with Ethical Use Clause

Copyright (c) 2025 CipherSim Team

**See [LICENSE](LICENSE) for full text.**

**By using this software, you agree to:**
- Use only for educational/authorized purposes
- Comply with all applicable laws
- Never attack unauthorized systems
- Accept full responsibility for your actions

---

## 🙏 Acknowledgments

- **Argon2** - Password Hashing Competition winners
- **OWASP** - Security standards and best practices
- **NIST** - Password security guidelines (SP 800-63B)
- **zxcvbn** - Password strength estimation inspiration
- **Rich** - Beautiful terminal UI library

---

## 📞 Support & Community

### Getting Help

- 📖 **Documentation**: [View all docs](/)
- 💬 **Issues**: [GitHub Issues](https://github.com/yourusername/CipherSim/issues)
- 🗣️ **Discussions**: [GitHub Discussions](https://github.com/yourusername/CipherSim/discussions)
- 📧 **Email**: support@ciphersim.example

### Quick Links

- [Installation Guide](#-installation)
- [Usage Examples](#-usage-examples)
- [Learning Path](#-learning-path)
- [Security Policy](SECURITY.md)
- [Command Reference](COMMAND_REFERENCE.md)

---

<div align="center">

## 🎉 Ready to Learn Password Security?

```bash
# Start with interactive mode (easiest!)
ciphersim interactive

# Or jump right in
ciphersim analyze "password123"
```

### Built with ❤️ for cybersecurity education

**Use knowledge to BUILD, not to BREAK. Stay ethical. 🛡️**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/yourusername/CipherSim)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Security](https://img.shields.io/badge/Security-Education-red?style=for-the-badge)](SECURITY.md)

---

**⭐ Star this repo** if you find it useful! | **🐛 Found a bug?** [Report it](https://github.com/yourusername/CipherSim/issues)

</div>
