"""
Learning Module - Educational Content on Password Security

Interactive educational content explaining cryptographic concepts, hashing,
and password security best practices.
"""

from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich import box


class SecurityEducation:
    """Educational content module for password security concepts"""
    
    def __init__(self) -> None:
        self.console = Console()
    
    def teach_topic(self, topic: str) -> None:
        """
        Teach a specific security topic.
        
        Available topics:
        - hashing
        - entropy
        - salt
        - rainbow_tables
        - algorithms
        - best_practices
        - attacks
        """
        topic_map = {
            'hashing': self._teach_hashing,
            'entropy': self._teach_entropy,
            'salt': self._teach_salt,
            'rainbow_tables': self._teach_rainbow_tables,
            'algorithms': self._teach_algorithms,
            'best_practices': self._teach_best_practices,
            'attacks': self._teach_attacks,
        }
        
        teacher = topic_map.get(topic.lower())
        if teacher:
            teacher()
        else:
            self.console.print(
                f"[yellow]Topic '{topic}' not found. Available topics:[/yellow]\n"
                + "\n".join(f"  • {t}" for t in topic_map.keys())
            )
    
    def _teach_hashing(self) -> None:
        """Explain password hashing"""
        content = """
# 🔐 Password Hashing Explained

## What is Password Hashing?

Password hashing is a **one-way mathematical function** that transforms a password 
into a fixed-size string of characters (the "hash"). It's designed to be:

- **One-way**: You can't reverse a hash to get the original password
- **Deterministic**: Same password always produces the same hash
- **Fast to compute**: Quick to verify passwords
- **Avalanche effect**: Tiny password change = completely different hash

## Why Hash Passwords?

**NEVER store passwords in plain text!**

If stored in plain text:
❌ Database breach = all passwords exposed
❌ Admins can see user passwords
❌ Massive security liability

With hashing:
✅ Database stores only hashes
✅ Even admins can't see passwords
✅ Breach exposes hashes (still bad, but much better)

## How Hashing Works

```
User Password: "MyPassword123!"
        ↓
Hash Function (e.g., Argon2id)
        ↓
Hash: $argon2id$v=19$m=65536,t=3,p=4$abc123...
```

During login:
1. User enters password
2. System hashes it
3. Compares hash with stored hash
4. Match = correct password ✓

## Modern Hashing (2025)

**Recommended:** Argon2id
- Memory-hard (resists GPU attacks)
- Configurable difficulty
- Side-channel resistant

**Also Good:** scrypt, bcrypt
**Avoid:** MD5, SHA1, plain SHA256 (too fast!)
"""
        self.console.print(Panel(Markdown(content), title="Password Hashing", border_style="cyan"))
    
    def _teach_entropy(self) -> None:
        """Explain password entropy"""
        content = """
# 📊 Password Entropy

## What is Entropy?

Entropy measures password **randomness** and **unpredictability** in bits.
Higher entropy = harder to crack.

**Formula:** Entropy = log₂(charset_size ^ length)

## Entropy Examples

| Password | Length | Charset | Entropy | Strength |
|----------|--------|---------|---------|----------|
| `abc`     | 3      | 26      | 14 bits | ❌ Very Weak |
| `password` | 8     | 26      | 38 bits | ❌ Weak |
| `P@ssw0rd` | 8     | 72      | 51 bits | ⚠️ Moderate |
| `MyP@ss123!` | 10  | 72      | 64 bits | ✅ Good |
| `Correct-Horse-Battery-Staple` | 28 | 27 | 132 bits | ✅✅ Excellent |

## Key Insights

**Length > Complexity**
- `correcthorsebatterystaple` (25 chars lowercase) = 117 bits
- `P@s5!` (5 chars complex) = 32 bits

**Each bit doubles difficulty:**
- 40 bits = 1 trillion combinations
- 50 bits = 1 quadrillion combinations  
- 60 bits = 1 quintillion combinations
- 128 bits = practically unbreakable

## 2025 Recommendations

✅ Minimum 60 bits for regular accounts
✅ Minimum 80 bits for sensitive accounts
✅ 128+ bits for cryptographic keys

**Pro tip:** Use passphrases (4-5 random words) for high entropy + memorability!
"""
        self.console.print(Panel(Markdown(content), title="Entropy", border_style="green"))
    
    def _teach_salt(self) -> None:
        """Explain password salting"""
        content = """
# 🧂 Password Salting

## What is a Salt?

A **salt** is a random value added to a password before hashing.

```
Password: "password123"
Salt: "a8f3c9e2d1b7"
        ↓
Hash(password + salt) = final hash
```

## Why Use Salt?

### Without Salt ❌
```
User1: "password123" → hash_abc123
User2: "password123" → hash_abc123  (same hash!)
```
- Identical passwords = identical hashes
- Enables rainbow table attacks
- Reveals password reuse

### With Salt ✅
```
User1: "password123" + salt1 → hash_xyz789
User2: "password123" + salt2 → hash_def456  (different!)
```
- Same password = different hashes
- Each password needs separate attack
- Rainbow tables useless!

## Salt Best Practices

✅ **Unique per password** - Every password gets own salt
✅ **Random** - Use cryptographically secure RNG
✅ **Long enough** - At least 16 bytes (128 bits)
✅ **Not secret** - Can be stored alongside hash

❌ **Never reuse** salts across passwords
❌ **Never use** predictable values (userIDs, timestamps)

## Pepper (Bonus)

A **pepper** is like a salt, but:
- Same for all passwords
- Stored separately from database (e.g., in code/config)
- Provides defense if database is stolen

```
Hash(password + salt + pepper)
```

## Modern Practice

Good password hashing algorithms (Argon2id, bcrypt) 
**automatically handle salting** for you! 🎉
"""
        self.console.print(Panel(Markdown(content), title="Salting", border_style="yellow"))
    
    def _teach_rainbow_tables(self) -> None:
        """Explain rainbow tables"""
        content = """
# 🌈 Rainbow Tables

## What is a Rainbow Table?

A **precomputed table** of password hashes.

```
Password     →  Hash
───────────────────────────────
password     →  5f4dcc3b...
123456       →  e10adc39...
qwerty       →  d8578edf...
... (millions more)
```

## How Rainbow Tables Work

**Traditional Attack:**
1. Get stolen hash
2. Try each possible password
3. Hash it
4. Compare with stolen hash
5. Repeat until match

⏱️ **Very slow** - must calculate each hash

**Rainbow Table Attack:**
1. Get stolen hash
2. Look it up in precomputed table
3. Instant match!

⚡ **Very fast** - no calculation needed

## Rainbow Table Trade-off

**Time-Memory Trade-off:**
- Pre-computation takes **lots of time** (months)
- Stored tables require **lots of space** (terabytes)
- Attack itself is **very fast** (seconds)

## Defense Against Rainbow Tables

### 1. Salting 🧂
Adding unique salt makes rainbow tables useless:
- Rainbow table has: `hash("password")`
- Your hash is: `hash("password" + "a8f3c9e2")`
- **No match!** Attacker needs new table for each salt

### 2. Slow Hash Functions
- Argon2id, bcrypt, scrypt
- Too slow to precompute billions of hashes
- Makes table generation impractical

### 3. Long Passwords
- More possible combinations
- Larger tables required
- Eventually becomes impossible to store

## Real-World Impact

**Without Salt (2012 LinkedIn breach):**
- 6.5M password hashes stolen
- No salt used
- Millions cracked in days using rainbow tables

**With Salt (Modern systems):**
- Rainbow tables ineffective
- Each password requires individual brute force
- Takes years instead of days

## Conclusion

Rainbow tables were a serious threat **before 2010**.

Modern password hashing (with salts) has made them **obsolete**. 

✅ Always use salted hashes!
"""
        self.console.print(Panel(Markdown(content), title="Rainbow Tables", border_style="magenta"))
    
    def _teach_algorithms(self) -> None:
        """Compare hashing algorithms"""
        self.console.print("\n[bold cyan]🔬 Password Hashing Algorithms Comparison[/bold cyan]\n")
        
        # Algorithm comparison table
        table = Table(title="2025 Hashing Algorithm Guide", box=box.ROUNDED)
        table.add_column("Algorithm", style="cyan")
        table.add_column("Year", style="yellow")
        table.add_column("Type", style="green")
        table.add_column("Security", style="magenta")
        table.add_column("2025 Status", style="white")
        
        table.add_row(
            "Argon2id",
            "2015",
            "Memory-hard",
            "⭐⭐⭐⭐⭐",
            "[green]✅ RECOMMENDED[/green]"
        )
        table.add_row(
            "scrypt",
            "2009",
            "Memory-hard",
            "⭐⭐⭐⭐",
            "[green]✅ Good[/green]"
        )
        table.add_row(
            "bcrypt",
            "1999",
            "CPU-hard",
            "⭐⭐⭐",
            "[yellow]⚠️ Legacy (Still OK)[/yellow]"
        )
        table.add_row(
            "PBKDF2",
            "2000",
            "CPU-hard",
            "⭐⭐⭐",
            "[yellow]⚠️ Acceptable[/yellow]"
        )
        table.add_row(
            "SHA256",
            "2001",
            "Fast hash",
            "⭐",
            "[red]❌ Too Fast[/red]"
        )
        table.add_row(
            "MD5",
            "1992",
            "Fast hash",
            "",
            "[red]❌ BROKEN[/red]"
        )
        
        self.console.print(table)
        
        # Detailed comparison
        details = """
## Why Argon2id is Best for 2025

**Memory-Hard:**
- Requires significant RAM (e.g., 64 MB)
- GPUs have limited memory bandwidth
- Resists parallel attacks

**Side-Channel Resistant:**
- Protected against timing attacks
- Safe on modern processors

**Configurable:**
- Adjust time cost (iterations)
- Adjust memory cost  
- Adjust parallelism
- Future-proof: increase as hardware improves

**Winner:** Password Hashing Competition 2015

## Algorithm Details

### Argon2id (2025 Standard)
```
Time cost: 3 iterations
Memory: 64 MB  
Parallelism: 4 threads
Hash time: ~100ms
GPU speedup: 2-5x (memory bottleneck)
```

### scrypt
```
Memory: 16-32 MB
Hash time: ~100ms
GPU speedup: 5-10x
```

### bcrypt  
```
Rounds: 12-14
Hash time: ~250ms
GPU speedup: 50-100x
```

### PBKDF2-SHA256
```
Iterations: 600,000+
Hash time: ~100ms  
GPU speedup: 1000x+ (vulnerable!)
```

## Migration Guide

**Currently using MD5/SHA1?**
→ Migrate to Argon2id immediately!

**Currently using PBKDF2?**
→ Increase iterations, plan Argon2id migration

**Currently using bcrypt?**
→ System is secure, but consider Argon2id for new projects

**Starting new project?**
→ Use Argon2id, no question!
"""
        self.console.print(Panel(Markdown(details), border_style="cyan"))
    
    def _teach_best_practices(self) -> None:
        """Teach password security best practices"""
        content = """
# 🛡️ Password Security Best Practices (2025)

## For Users

### ✅ DO:
1. **Use unique passwords** for every account
2. **Use a password manager** (1Password, Bitwarden, etc.)
3. **Enable MFA** everywhere possible
4. **Use passphrases** (4-5 random words) when memorizing
5. **Make it long** (16+ characters recommended)
6. **Update** passwords if service is breached

### ❌ DON'T:
1. **Reuse passwords** across sites
2. **Use personal info** (name, birthday, pet names)
3. **Use common passwords** (password123, qwerty)
4. **Share passwords** via email/text
5. **Write passwords** on sticky notes
6. **Use simple patterns** (abc123, qwerty)

## For Developers

### Password Storage:
```python
✅ DO: Use Argon2id with proper parameters
❌ DON'T: Store passwords in plain text
❌ DON'T: Use fast hashes (MD5, SHA256)
❌ DON'T: Implement your own crypto
```

### Password Policies:
```
✅ DO: Require 12+ characters
✅ DO: Check against breached password lists
✅ DO: Allow long passwords (64+ chars)
✅ DO: Allow all characters (including spaces)

❌ DON'T: Enforce complex rules (1 upper, 1 digit...)
❌ DON'T: Force periodic password changes
❌ DON'T: Limit password length unnecessarily
```

### Defense in Depth:
1. **Rate limiting** - Max 5 attempts/minute
2. **Account lockout** - Lock after 5 failures
3. **Progressive delays** - Exponential backoff
4. **MFA requirement** - Required for sensitive accounts
5. **Breach detection** - Monitor for credential stuffing
6. **Security headers** - CSP, HSTS, etc.

## Recommended Resources

**NIST SP 800-63B** (2025)
- Modern password guidelines
- No more complex requirements
- Length > complexity

**OWASP ASVS**
- Application security standards
- Password storage requirements
- Authentication best practices

**Have I Been Pwned**
- Check if passwords are compromised
- API for breach detection
- Integrate into registration flows

## Common Myths

❌ **Myth:** Complex rules make strong passwords
✅ **Reality:** Length matters more than complexity

❌ **Myth:** Change passwords every 90 days
✅ **Reality:** Only change if compromised

❌ **Myth:** Security questions add security
✅ **Reality:** They're often guessable, use MFA instead

❌ **Myth:** Password managers are risky
✅ **Reality:** More secure than reusing passwords

## The Bottom Line

**For Users:** Password Manager + MFA = 99% protected

**For Developers:** Argon2id + Rate Limiting + MFA = Secure system
"""
        self.console.print(Panel(Markdown(content), title="Best Practices", border_style="green"))
    
    def _teach_attacks(self) -> None:
        """Explain common password attack methods"""
        content = """
# ⚔️ Common Password Attack Methods

## 1. Brute Force Attack

**What:** Try every possible password combination

**How:**
```
Try: a
Try: b
Try: c
...
Try: zzz
Try: aaaa
...
```

**Defense:**
- Long passwords (exponential difficulty)
- Slow hashing (Argon2id)
- Rate limiting

**Real-world:** Ineffective against strong passwords

---

## 2. Dictionary Attack

**What:** Try common words from a dictionary

**How:**
```
Try: password
Try: admin
Try: welcome
Try: monkey
Try: dragon
...
```

**Defense:**
- Avoid common passwords
- Check against breach lists
- Add random characters

**Real-world:** Very effective against weak passwords

---

## 3. Credential Stuffing

**What:** Use stolen username/password pairs from other breaches

**How:**
```
Try: user@email.com:Password123 (from LinkedIn breach)
Try: user@email.com:Welcome2024 (from Yahoo breach)
...
```

**Defense:**
- Unique passwords per site (!!)
- Rate limiting
- Breach detection
- MFA

**Real-world:** Extremely common, often successful

---

## 4. Rainbow Table Attack

**What:** Use precomputed hash tables

**How:**
```
Stolen hash: 5f4dcc3b...
Lookup in table: 5f4dcc3b... = "password"
```

**Defense:**
- Salting (makes tables useless)
- Slow hashing

**Real-world:** Obsolete against modern systems

---

## 5. Phishing

**What:** Trick user into revealing password

**How:**
```
Fake email/site that looks legitimate
User enters credentials
Attacker captures them
```

**Defense:**
- User education
- MFA (limits damage)
- Password managers (detect fake sites)

**Real-world:** Most successful attack method

---

## 6. Keylogging

**What:** Record user keystrokes

**How:**
```
Malware on user's computer
Records every keystroke
Sends to attacker
```

**Defense:**
- Antivirus/EDR
- MFA
- Virtual keyboards
- Regular security scans

**Real-world:** Targets high-value individuals

---

## Attack Speed Comparison

**8-character password (lowercase + digits)**

| Attack Method | Time to Crack |
|--------------|---------------|
| GPU Brute Force (Argon2id) | ~3 years |
| GPU Brute Force (PBKDF2) | ~2 weeks |
| GPU Brute Force (no hash) | ~30 seconds |
| Dictionary Attack | Seconds (if in list) |
| Rainbow Table (no salt) | Instant |
| Credential Stuffing | Instant (if reused) |
| Phishing | Depends on user |

## Defense Priority

1. **MFA** - Defeats most attacks even if password stolen
2. **Unique passwords** - Prevents credential stuffing
3. **Long passwords** - Makes brute force impractical  
4. **Rate limiting** - Slows all automated attacks
5. **Argon2id hashing** - Makes cracking very expensive

## Remember

🎯 **Attackers choose the easiest method.**

If you have:
- Strong unique password + MFA → Attackers move to easier target
- Weak/reused password → You're the easy target
"""
        self.console.print(Panel(Markdown(content), title="Attack Methods", border_style="red"))


# Helper function for CLI
def show_learning_menu() -> None:
    """Display learning module menu"""
    console = Console()
    
    console.print("\n[bold cyan]📚 Password Security Education[/bold cyan]\n")
    console.print("Available topics:\n")
    console.print("  1. [cyan]hashing[/cyan] - How password hashing works")
    console.print("  2. [green]entropy[/green] - Password randomness and strength")
    console.print(" 3. [yellow]salt[/yellow] - Salting and peppering")
    console.print("  4. [magenta]rainbow_tables[/magenta] - Rainbow table attacks")
    console.print("  5. [cyan]algorithms[/cyan] - Hashing algorithm comparison")
    console.print("  6. [green]best_practices[/green] - Security best practices")
    console.print("  7. [red]attacks[/red] - Common attack methods\n")
