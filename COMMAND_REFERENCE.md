# CipherSim - Quick Command Reference

**Updated with clearer help text! 🎉**

## 📖 Understanding --target in simulate

The `--target` parameter is **the password you want to test**. It's what the simulation tries to "crack" (find). This is for educational testing of YOUR passwords, not attacking others!

### Example:
```bash
# Test how fast "password123" can be cracked
ciphersim simulate --target "password123"

# Test your own password
ciphersim simulate --target "MySecretPassword2025!"
```

## 🚀 Quick Examples

### Analyze a Password
```bash
# Simple check
ciphersim analyze "password123"

# Your complex password
ciphersim analyze "MySecureP@ssw0rd2025!"
```

### Simulate Attacks
```bash
# Dictionary attack - try common passwords
ciphersim simulate --target "password"

# Brute force - try all combinations (a,b,c...)
ciphersim simulate --mode brute_force --target "abc"

# Test your password
ciphersim simulate --target "YourPassword"
```

### Learn Security
```bash
# Show topics
ciphersim learn

# Learn about hashing
ciphersim learn hashing

# Understand why length matters
ciphersim learn entropy
```

### See Defenses
```bash
# Rate limiting demo
ciphersim defend --defense rate_limiting

# MFA explanation
ciphersim defend --defense mfa
```

### Easy Mode (Recommended!)
```bash
# Menu-driven interface
ciphersim interactive
```

## 💡 Pro Tips

1. **Put passwords in quotes**: `ciphersim analyze "my password"`
2. **Use --help on any command**: `ciphersim simulate --help`
3. **Start with interactive mode**: `ciphersim interactive`
4. **Learn first, simulate second**: Try `ciphersim learn` before simulations

## 🎯 What Each Command Does

| Command | What It Does | Example |
|---------|--------------|---------|
| `analyze` | Check password strength | `ciphersim analyze "test123"` |
| `hash` | Convert password to hash | `ciphersim hash "MyPass"` |
| `simulate` | Test crack time (offline) | `ciphersim simulate -t "password"` |
| `defend` | Show defense mechanisms | `ciphersim defend -d mfa` |
| `learn` | Educational tutorials | `ciphersim learn hashing` |
| `gpu` | GPU speed comparison | `ciphersim gpu` |
| `interactive` | Menu mode (easiest!) | `ciphersim interactive` |

## ❓ Common Questions

**Q: What is --target?**
A: The password you're testing. Example: `--target "mypassword123"`

**Q: Is this hacking real accounts?**
A: NO! It's offline simulation to test password strength only.

**Q: Will this crack my actual accounts?**
A: NO! This only simulates attacks on passwords YOU provide. No network activity.

**Q: Which command should I start with?**
A: Try `ciphersim interactive` for the easiest experience!

**Q: How do I see examples for a command?**
A: Run `ciphersim <command> --help`, for example: `ciphersim simulate --help`

## 🎓 Learning Path

1. **Start**: `ciphersim interactive`
2. **Learn**: `ciphersim learn hashing`
3. **Test**: `ciphersim analyze "password123"`
4. **Simulate**: `ciphersim simulate --target "password"`
5. **Defend**: `ciphersim defend --defense mfa`
6. **Master**: Try all learning topics with `ciphersim learn`

---

**Need more help?** Run: `ciphersim --help`
**Want easy mode?** Run: `ciphersim interactive`
