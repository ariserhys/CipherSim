# Security Policy and Compliance

## Overview

CipherSim is an **educational cybersecurity tool** designed to teach password security concepts through safe, offline simulations. This document outlines our security model, compliance standards, and responsible disclosure policy.

## ⚖️ Legal and Ethical Framework

### Authorized Use Only

CipherSim is designed exclusively for:

✅ **Educational purposes** in academic settings
✅ **Authorized security testing** with explicit permission  
✅ **Professional training** in cybersecurity programs
✅ **Red-team exercises** in controlled environments
✅ **Personal learning** about password security

❌ **Unauthorized use** against real systems or accounts is **STRICTLY PROHIBITED**

### Compliance Standards

CipherSim aligns with industry security standards:

#### OWASP ASVS 5.1 (Application Security Verification Standard)

- **V2.1**: Password Security Requirements
  - Uses memory-hard algorithms (Argon2id)
  - Implements proper salting
  - Supports adequate password length
  - Prevents common passwords

- **V8.2**: Client-side Data Protection
  - No credential transmission
  - Offline-only operation
  - No persistent credential storage

#### NIST SP 800-63B (Digital Identity Guidelines)

- **Section 5.1.1**: Memorized Secret Verifiers
  - Minimum 8 characters (recommends 12+)
  - Allows all ASCII characters
  - No complexity requirements forcing
  - Salt minimum 32 bits (we use 128 bits)

- **Section 5.1.1.2**: Salt and Iteration Count
  - Unique salt per credential
  - PBKDF2: minimum 10,000 iterations (we use 600,000)
  - bcrypt: minimum work factor 10 (we use 12)

#### MITRE ATT&CK Framework

- **T1110**: Brute Force (Simulation only)
  - Password Guessing (Educational demonstration)
  - Password Cracking (Offline simulation)
  - Credential Stuffing (Demo data only)

**Important**: All MITRE ATT&CK techniques are **simulated for education**, not performed against live systems.

## 🛡️ Threat Model

### What We Protect Against

1. **Misuse Prevention**
   - No network capabilities (prevents remote attacks)
   - Demo data only (prevents real credential exposure)
   - Rate limiting in simulations (prevents resource exhaustion)

2. **Data Protection**
   - No real credential storage
   - No persistent password storage
   - No credential transmission
   - No logging of sensitive data

### Security Controls

#### Offline-Only Operation

```python
# Hard-coded safety constraint
OFFLINE_ONLY = True  # Cannot be disabled

# No network imports or capabilities
# No socket operations
# No HTTP/HTTPS requests
# No DNS lookups
```

#### Demo Data Only

All attack simulations use:
- Hardcoded test passwords
- Public domain wordlists
- Synthetic credential pairs
- **NEVER** real user data

#### Ethical Warnings

Users see ethical warnings:
- On first launch
- Before attack simulations
- In all documentation
- In source code comments

## 🔒 Cryptographic Implementation

### Hashing Algorithm Security

#### Argon2id (Recommended)

```yaml
Parameters:
  Memory Cost: 64 MB (65536 KB)
  Time Cost: 3 iterations
  Parallelism: 4 threads
  Salt Length: 16 bytes (128 bits)
  Hash Length: 32 bytes (256 bits)

Security Properties:
  - Memory-hard (GPU-resistant)
  - Side-channel resistant
  - Configurable difficulty
  - Winner of Password Hashing Competition 2015
```

#### scrypt

```yaml
Parameters:
  N: 16384 (2^14) - CPU/memory cost
  r: 8 - Block size
  p: 1 - Parallelization
  Salt Length: 16 bytes
  Hash Length: 32 bytes

Security Properties:
  - Memory-hard
  - GPU-resistant
  - Widely supported
```

#### PBKDF2

```yaml
Parameters:
  Iterations: 600,000 (OWASP 2023)
  Hash: SHA256 or SHA512
  Salt Length: 16 bytes
  Hash Length: 32 bytes

Security Properties:
  - Industry standard
  - FIPS 140-2 approved
  - Widely compatible
```

#### bcrypt

```yaml
Parameters:
  Rounds: 12 (work factor)
  
Security Properties:
  - Time-tested (1999)
  - Moderate GPU resistance
  - Legacy compatibility
```

### Key Derivation Security

All implementations use:
- **Cryptographically secure RNG** for salt generation
- **Constant-time comparison** (where applicable)
- **No hardcoded secrets** (except demo passwords)

## 🚨 Vulnerability Reporting

### Responsible Disclosure

If you discover a security vulnerability in CipherSim:

#### ⚠️ DO NOT:
- Exploit the vulnerability
- Publicly disclose before patch
- Test against production systems

#### ✅ DO:
1. **Report privately** to [@ariserhys]
2. **Provide details**:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (optional)
3. **Allow response time**: 90 days before public disclosure

### Security Issue Classification

#### Critical
- Enables unauthorized system access
- Exposes real credentials
- Bypasses ethical safeguards

**Response Time**: 24 hours acknowledgment, 7 days patch

#### High
- Significant privacy violation
- Cryptographic weakness
- Data exposure

**Response Time**: 48 hours acknowledgment, 14 days patch

#### Medium
- Denial of service
- Information disclosure
- Configuration weakness

**Response Time**: 7 days acknowledgment, 30 days patch

#### Low
- Documentation issues
- Minor bugs
- Cosmetic problems

**Response Time**: 14 days acknowledgment, 60 days patch

## 🔐 Security Hardening

### Deployment Recommendations

#### For Educational Institutions

```bash
# Run in isolated container
docker run --rm --network none ciphersim

# Limit resource usage
docker run --memory=1g --cpus=1 ciphersim

# Read-only filesystem
docker run --read-only ciphersim
```

#### For Corporate Training

- Deploy in **air-gapped network**
- Use **dedicated training environment**
- Enable **audit logging** (optional)
- Restrict to **authorized personnel**

#### For Individual Learning

- Run in **virtual machine**
- Use **separate user account**
- Keep **updated** to latest version

### Security Checklist

Before deploying CipherSim:

- [ ] Verify no real credentials in system
- [ ] Confirm network is disabled/firewalled
- [ ] Review ethical guidelines with users
- [ ] Obtain management approval (if corporate)
- [ ] Document authorized use
- [ ] Set up monitoring (if required)
- [ ] Plan incident response
- [ ] Define acceptable use policy

## 📋 Audit and Compliance

### Logging (Optional)

CipherSim does **not log by default**, but can be configured:

```yaml
# config/simulation_config.yaml
safety:
  log_all_operations: true  # Disabled by default
```

If enabled, logs contain:
- Command executed
- Timestamp
- Analysis results (non-sensitive)
- **NEVER passwords or hashes**

### Compliance Verification

To verify CipherSim compliance:

```bash
# Check configuration
cat config/simulation_config.yaml

# Verify offline mode
grep -r "requests\|urllib\|socket" src/  # Should find nothing

# Verify no credential storage
grep -r "password.*=" src/ | grep -v "demo\|test\|example"

# Check ethical warnings
grep -r "ETHICAL\|WARNING" src/
```

## 🔍 Security Audit History

### Version 1.0.0 (2025-11-28)

**Audit**: Initial security review
**Findings**: None
**Status**: ✅ Approved for educational use

**Reviewed**:
- Offline-only operation ✅
- No credential storage ✅
- Ethical warnings present ✅
- Cryptographic implementation ✅
- Demo data only ✅

## 📚 References

### Standards and Guidelines

- **OWASP ASVS 5.1**: https://owasp.org/www-project-application-security-verification-standard/
- **NIST SP 800-63B**: https://pages.nist.gov/800-63-3/sp800-63b.html
- **MITRE ATT&CK**: https://attack.mitre.org/
- **CWE-916**: Use of Password Hash With Insufficient Computational Effort
- **Argon2 RFC 9106**: https://datatracker.ietf.org/doc/html/rfc9106

### Security Resources

- **OWASP Password Storage Cheat Sheet**
- **OWASP Authentication Cheat Sheet**
- **Have I Been Pwned**: Password breach checking
- **Password Hashing Competition**: https://www.password-hashing.net/

---

**Last Updated**: 2025-11-28
**Next Review**: 2026-05-28 (6 months)

For security concerns, contact: security@ciphersim.example
