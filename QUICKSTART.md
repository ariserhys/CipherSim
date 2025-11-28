# CipherSim - Quick Start Guide

Get started with CipherSim in 5 minutes! 🚀

## Installation

### Step 1: Install Python 3.12+

Make sure you have Python 3.12 or newer:

```bash
python --version
```

If needed, download from: https://www.python.org/downloads/

### Step 2: Install CipherSim

```bash
# Navigate to CipherSim directory
cd CipherSim

# Install dependencies
pip install -r requirements.txt

# Install CipherSim
pip install -e .
```

### Step 3: Verify Installation

```bash
ciphersim --version
```

You should see: `CipherSim version 1.0.0`

## Your First 5 Minutes

### 1. Analyze a Password (30 seconds)

```bash
ciphersim analyze "password123"
```

See how weak this common password is! ❌

Now try a strong one:

```bash
ciphersim analyze "MySecurePassphrase2025!"
```

Much better! ✅

### 2. Learn About Hashing (1 minute)

```bash
ciphersim learn hashing
```

Read the beautiful explanation of how password hashing works.

### 3. Hash a Password (30 seconds)

```bash
ciphersim hash "MyPassword123!"
```

See Argon2id in action! Notice how fast it is despite being secure.

### 4. Simulate an Attack (2 minutes)

```bash
ciphersim simulate --mode dictionary --target "password"
```

Watch the dictionary attack find "password" quickly. This is why common passwords are dangerous!

### 5. See Defense Mechanisms (1 minute)

```bash
ciphersim defend --defense rate_limiting
```

Learn how rate limiting stops attackers!

## Interactive Mode (Easiest!)

Don't like command-line? Try interactive mode:

```bash
ciphersim interactive
```

You'll get a menu where you can explore everything with simple number choices.

## Recommended Learning Path

### Week 1: Basics
- Day 1: Password analysis (`analyze` command)
- Day 2: Learn hashing (`learn hashing`)
- Day 3: Learn entropy (`learn entropy`)
- Day 4: Learn salting (`learn salt`)
- Day 5: Compare algorithms (`learn algorithms`)

### Week 2: Attacks
- Day 1: Dictionary attacks (`simulate --mode dictionary`)
- Day 2: Brute force (`simulate --mode brute_force`)
- Day 3: Hybrid attacks (`simulate --mode hybrid`)
- Day 4: Learn all attack types (`learn attacks`)
- Day 5: GPU comparison (`gpu`)

### Week 3: Defenses
- Day 1: Rate limiting (`defend --defense rate_limiting`)
- Day 2: Account lockout (`defend --defense account_lockout`)
- Day 3: Progressive delay (`defend --defense progressive_delay`)
- Day 4: MFA (`defend --defense mfa`)
- Day 5: Best practices (`learn best_practices`)

## Common Use Cases

### "I want to check if my password is strong"

```bash
ciphersim analyze "YourPasswordHere" --verbose
```

### "I want to understand why Argon2id is recommended"

```bash
ciphersim learn algorithms
```

### "I want to see how long it takes to crack my password"

```bash
ciphersim analyze "YourPasswordHere"
# Look at the "Time to Crack" table
```

### "I want to demonstrate attacks to my team"

```bash
# Show weak password
ciphersim simulate --mode dictionary --target "password123"

# Show strong password resistance
ciphersim simulate --mode brute_force --target "XyZ!@#789abc" --max-attempts 1000000
```

### "I want to teach password security to students"

Use interactive mode for live demos:

```bash
ciphersim interactive
```

Then walk through:
1. Analyze weak vs strong passwords
2. Explain hashing concepts
3. Demonstrate attacks
4. Show defenses

## Pro Tips

### Generate Strong Passphrases

CipherSim teaches you that **length > complexity**. Try:

```bash
ciphersim analyze "horse battery staple correct"
```

Even with just spaces and lowercase, it's extremely strong!

### Compare Algorithms

Want to see why Argon2id beats bcrypt?

```bash
ciphersim gpu
```

Notice how Argon2id is much slower on GPU due to memory-hardness.

### Test Your Password Policy

If you're setting password requirements:

```bash
# Test minimum: 8 chars, mixed case, number
ciphersim analyze "Pass123!"

# Test recommended: 12+ chars
ciphersim analyze "MyLongPass2025"
```

## Troubleshooting

### "Command not found: ciphersim"

Solution:

```bash
# Make sure you installed it
pip install -e .

# If still not working, use Python module syntax
python -m ciphersim analyze "test"
```

### "ModuleNotFoundError: No module named 'argon2'"

Solution:

```bash
# Install dependencies
pip install -r requirements.txt
```

### "Permission denied"

Solution:

```bash
# Use --user flag
pip install --user -e .
```

## Getting Help

### In-app Help

```bash
# General help
ciphersim --help

# Command-specific help
ciphersim analyze --help
ciphersim simulate --help
ciphersim defend --help
```

### Available Topics

```bash
# List all learning topics
ciphersim learn
```

### Show All Commands

```bash
ciphersism --help
```

You'll see:
- `analyze` - Password strength analysis
- `hash` - Hash passwords
- `simulate` - Attack simulations
- `defend` - Defense demonstrations
- `learn` - Educational content
- `gpu` - Performance comparison
- `interactive` - Menu mode

## Next Steps

Once you're comfortable with the basics:

1. **Read SECURITY.md** - Understand compliance and ethics
2. **Explore all learning modules** - `ciphersim learn <topic>`
3. **Try different attack modes** - Dictionary, brute force, hybrid, mask
4. **Test all defenses** - See how each one protects accounts
5. **Share with others** - Teach your team about password security

## Remember

🔒 **Use strong, unique passwords**
🔑 **Use a password manager**
🛡️ **Enable MFA everywhere**
📚 **Keep learning about security**
⚖️ **Use this tool ethically**

---

**Ready to dive deeper?** Check out the full [README.md](README.md) for advanced features!

**Have questions?** See the [SECURITY.md](SECURITY.md) for compliance info.

**Want to contribute?** See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Happy learning! 🎓
