"""
CipherSim CLI - Command Line Interface

Main entry point for the CipherSim educational cybersecurity tool.
"""

import sys
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from . import ETHICAL_WARNING, __version__
from .core.hash_engine import HashEngine, HashAlgorithm
from .core.attack_simulator import AttackSimulator, AttackMode, AttackConfig, GPUSimulator
from .core.defense_simulator import DefenseSimulator, DefenseType
from .modules.password_analyzer import PasswordAnalyzer
from .modules.learning import SecurityEducation, show_learning_menu


console = Console()


def show_banner() -> None:
    """Display CipherSim banner and ethical warning"""
    banner = f"""
[bold cyan]
 ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗ ███████╗██╗███╗   ███╗
██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗██╔════╝██║████╗ ████║
██║     ██║██████╔╝███████║█████╗  ██████╔╝███████╗██║██╔████╔██║
██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗╚════██║██║██║╚██╔╝██║
╚██████╗██║██║     ██║  ██║███████╗██║  ██║███████║██║██║ ╚═╝ ██║
 ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝     ╚═╝
[/bold cyan]
[yellow]Educational Password Security Simulation Tool v{__version__}[/yellow]
[dim]For authorized security training and education only[/dim]
"""
    console.print(banner)
    console.print(ETHICAL_WARNING)


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    """
    CipherSim - Educational Password Security Simulation Tool
    
    A 2025-grade tool for learning about password security, hashing,
    and attack/defense techniques in a safe, offline environment.
    """
    pass


@cli.command()
@click.argument('password', metavar='PASSWORD')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed analysis')
def analyze(password: str, verbose: bool) -> None:
    """
    Check how strong your password is and get security recommendations.
    
    PASSWORD: The password you want to test (put it in quotes)
    
    Examples:
    
        Check a weak password:
        $ ciphersim analyze "password123"
        
        Check a strong password with detailed info:
        $ ciphersim analyze "MySecurePassphrase2025!" -v
        
        Test a passphrase:
        $ ciphersim analyze "correct horse battery staple"
    
    This tool will show you:
      • Password strength score (0-100)
      • How long it would take to crack
      • Security problems found
      • How to make it stronger
    """
    analyzer = PasswordAnalyzer()
    analyzer.analyze(password, verbose=True)


@cli.command()
@click.argument('password', metavar='PASSWORD')
@click.option('--algorithm', '-a', type=click.Choice(['argon2id', 'scrypt', 'pbkdf2_sha256', 'bcrypt']), 
              default='argon2id', help='Hashing algorithm (default: argon2id)')
def hash(password: str, algorithm: str) -> None:
    """
    Convert a password into a secure hash (one-way encryption).
    
    PASSWORD: The password to hash (put it in quotes)
    
    Examples:
    
        Hash with recommended algorithm (Argon2id):
        $ ciphersim hash "MyPassword123!"
        
        Try different algorithms:
        $ ciphersim hash "test" --algorithm bcrypt
        $ ciphersim hash "test" --algorithm scrypt
    
    Available algorithms:
      • argon2id     - Best for 2025 (slowest, most secure) ✅
      • scrypt       - Good alternative (memory-hard)
      • pbkdf2_sha256 - Industry standard (fast)
      • bcrypt       - Legacy but still secure
    
    The hash output is what gets stored in databases, never the password itself!
    """
    console.print(f"\n[cyan]Hashing password with {algorithm}...[/cyan]\n")
    
    engine = HashEngine()
    algo_map = {
        'argon2id': HashAlgorithm.ARGON2ID,
        'scrypt': HashAlgorithm.SCRYPT,
        'pbkdf2_sha256': HashAlgorithm.PBKDF2_SHA256,
        'bcrypt': HashAlgorithm.BCRYPT,
    }
    
    result = engine.hash_password(password, algo_map[algorithm])
    
    console.print(f"[green]Algorithm:[/green] {result.algorithm.value}")
    console.print(f"[green]Hash:[/green] {result.hash_value}")
    if result.salt:
        console.print(f"[green]Salt:[/green] {result.salt}")
    console.print(f"[green]Time:[/green] {result.time_ms:.2f}ms")
    console.print(f"[green]Parameters:[/green] {result.parameters}\n")


@cli.command()
@click.option('--mode', '-m', type=click.Choice(['dictionary', 'brute_force', 'hybrid', 'mask']),
              default='dictionary', help='Type of attack to simulate')
@click.option('--target', '-t', required=True, metavar='PASSWORD',
              help='The password to test (this is what we try to "crack")')
@click.option('--algorithm', '-a', type=click.Choice(['argon2id', 'bcrypt', 'pbkdf2_sha256']),
              default='argon2id', help='Hashing algorithm used')
@click.option('--max-attempts', default=100000, help='Stop after this many tries')
@click.option('--mask', help='Pattern for mask attack (e.g., ?u?l?l?l?d?d?d)')
def simulate(mode: str, target: str, algorithm: str, max_attempts: int, mask: str) -> None:
    """
    Simulate a password attack to see how long it takes to crack. (SAFE - OFFLINE ONLY)
    
    ⚠️  IMPORTANT: This is EDUCATIONAL simulation only. It works OFFLINE and does NOT
    attack real systems. You're testing how secure YOUR OWN passwords are.
    
    Required:
      --target, -t    The password you want to test (the one being "attacked")
                      Example: --target "mypassword123"
    
    Optional:
      --mode, -m      How to attack (default: dictionary)
                      • dictionary  - Try common passwords
                      • brute_force - Try all combinations
                      • hybrid      - Dictionary + mutations
                      • mask        - Use a pattern (needs --mask)
      
      --algorithm, -a Hash type (default: argon2id)
      --max-attempts  Stop after this many tries (default: 100,000)
      --mask          Pattern for mask mode (e.g., "?u?l?l?l?d?d?d")
                      ?u=uppercase, ?l=lowercase, ?d=digit
    
    Examples:
    
        Test how fast "password123" gets cracked:
        $ ciphersim simulate --target "password123"
        
        See if "abc" survives a brute force (it won't):
        $ ciphersim simulate --mode brute_force --target "abc"
        
        Test a pattern like "Pass123":
        $ ciphersim simulate --mode mask --target "Pass123" --mask "?u?l?l?l?d?d?d"
        
        Try with different hashing:
        $ ciphersim simulate --target "test" --algorithm bcrypt
    
    What you'll learn:
      • How many attempts it took
      • How long it took
      • Whether your password was found
      • Why certain passwords are weak
    """
    console.print("\n[bold red]⚠️  SIMULATION MODE - Educational purposes only[/bold red]\n")
    
    mode_map = {
        'dictionary': AttackMode.DICTIONARY,
        'brute_force': AttackMode.BRUTE_FORCE,
        'hybrid': AttackMode.HYBRID,
        'mask': AttackMode.MASK,
    }
    
    algo_map = {
        'argon2id': HashAlgorithm.ARGON2ID,
        'bcrypt': HashAlgorithm.BCRYPT,
        'pbkdf2_sha256': HashAlgorithm.PBKDF2_SHA256,
    }
    
    config = AttackConfig(
        mode=mode_map[mode],
        target_hash="simulated_hash",
        algorithm=algo_map[algorithm],
        max_attempts=max_attempts,
        mask=mask
    )
    
    simulator = AttackSimulator()
    result = simulator.simulate_attack(config, target)
    
    # Display results
    console.print("\n[bold cyan]📊 Simulation Results[/bold cyan]\n")
    
    if result.success:
        console.print(f"[green]✓ Password found:[/green] {result.password_found}")
    else:
        console.print(f"[red]✗ Password not found[/red]")
    
    console.print(f"[yellow]Attempts:[/yellow] {result.attempts:,}")
    console.print(f"[yellow]Time:[/yellow] {result.time_seconds:.2f} seconds")
    console.print(f"[yellow]Rate:[/yellow] {result.attempts/result.time_seconds:.0f} attempts/second")
    
    if result.stopped_by_limit:
        console.print(f"\n[yellow]⚠️  Stopped by attempt limit ({max_attempts:,})[/yellow]")
    console.print()


@cli.command()
@click.option('--defense', '-d', type=click.Choice(['rate_limiting', 'account_lockout', 
              'progressive_delay', 'ip_throttling', 'honeytoken', 'mfa']),
              default='rate_limiting', help='Type of defense to demonstrate')
@click.option('--attempts', default=100, help='Number of attacks to simulate')
def defend(defense: str, attempts: int) -> None:
    """
    See how security defenses protect against password attacks.
    
    This shows you HOW to defend against the attacks, not just how to attack!
    
    Options:
      --defense, -d   Which defense to demo (default: rate_limiting)
                      • rate_limiting    - Limit login attempts per minute
                      • account_lockout  - Lock account after failures
                      • progressive_delay - Slow down attackers over time
                      • ip_throttling    - Block suspicious IP addresses
                      • honeytoken       - Trap passwords that alert admins
                      • mfa              - Multi-Factor Authentication
      
      --attempts      How many attacks to simulate (default: 100)
    
    Examples:
    
        See how rate limiting blocks attackers:
        $ ciphersim defend --defense rate_limiting
        
        Learn about Multi-Factor Authentication:
        $ ciphersim defend --defense mfa
        
        Simulate 200 attacks against account lockout:
        $ ciphersim defend --defense account_lockout --attempts 200
    
    You'll see:
      • How many attacks were blocked
      • Why the defense works
      • Real-world effectiveness
    """
    defense_map = {
        'rate_limiting': DefenseType.RATE_LIMITING,
        'account_lockout': DefenseType.ACCOUNT_LOCKOUT,
        'progressive_delay': DefenseType.PROGRESSIVE_DELAY,
        'ip_throttling': DefenseType.IP_THROTTLING,
        'honeytoken': DefenseType.HONEYTOKEN,
        'mfa': DefenseType.MFA,
    }
    
    simulator = DefenseSimulator()
    simulator.simulate_defense(defense_map[defense], attack_attempts=attempts)


@cli.command()
@click.argument('topic', required=False, metavar='[TOPIC]')
def learn(topic: str) -> None:
    """
    Learn about password security - like a mini cybersecurity course!
    
    TOPIC: What you want to learn about (optional - shows menu if omitted)
    
    Available Topics:
      • hashing        - How password hashing works
      • entropy        - Why longer passwords are stronger
      • salt           - What salts are and why they matter
      • rainbow_tables - How rainbow table attacks work
      • algorithms     - Compare Argon2id vs bcrypt vs PBKDF2
      • best_practices - Security tips for 2025
      • attacks        - Common attack methods explained
    
    Examples:
    
        Show all available topics:
        $ ciphersim learn
        
        Learn how password hashing works:
        $ ciphersim learn hashing
        
        Understand password strength (entropy):
        $ ciphersim learn entropy
        
        See which algorithm is best:
        $ ciphersim learn algorithms
    
    Perfect for:
      • Students learning cybersecurity
      • Developers building secure apps
      • Anyone who wants to understand password security
    """
    educator = SecurityEducation()
    
    if topic:
        educator.teach_topic(topic)
    else:
        show_learning_menu()
        console.print("\n[dim]Usage: ciphersim learn <topic>[/dim]\n")


@cli.command()
def gpu() -> None:
    """
    Compare how fast different GPUs can crack passwords.
    
    Shows you why some algorithms (like Argon2id) are more secure than others
    because they're harder to crack even with powerful GPUs.
    
    Example:
        $ ciphersim gpu
    
    You'll see a table comparing:
      • RTX 4090 (high-end GPU)
      • RTX 3080 (mid-range GPU)  
      • CPU only (no GPU)
    
    And how many passwords/second each can try for different algorithms.
    """
    console.print("\n[bold cyan]🖥️  GPU Performance Comparison[/bold cyan]\n")
    
    comparison = GPUSimulator.get_performance_comparison()
    
    from rich.table import Table
    table = Table(title="Simulated Hash/Second Performance")
    table.add_column("GPU Tier", style="cyan")
    table.add_column("Argon2id", style="green")
    table.add_column("scrypt", style="yellow")
    table.add_column("PBKDF2-SHA256", style="orange1")
    table.add_column("bcrypt", style="magenta")
    
    for tier, perf in comparison.items():
        table.add_row(
            tier.replace('_', ' '),
            f"{perf.get(HashAlgorithm.ARGON2ID, 0):,}",
            f"{perf.get(HashAlgorithm.SCRYPT, 0):,}",
            f"{perf.get(HashAlgorithm.PBKDF2_SHA256, 0):,}",
            f"{perf.get(HashAlgorithm.BCRYPT, 0):,}",
        )
    
    console.print(table)
    console.print("\n[green]💡 Notice how Argon2id is much slower on GPU (memory-hard)[/green]")
    console.print("[green]   This is why it's the recommended algorithm for 2025![/green]\n")


@cli.command()
def interactive() -> None:
    """
    Start easy-to-use menu mode (best for beginners!).
    
    Instead of typing commands, you'll get a numbered menu where you just
    pick options. Perfect if you're new to command-line tools!
    
    Example:
        $ ciphersim interactive
    
    Then just follow the prompts:
      1. Analyze Password
      2. Hash Password
      3. Simulate Attack
      4. Demonstrate Defense
      5. Learn Security Concepts
      6. GPU Performance Comparison
      7. Exit
    
    Recommended if you're just starting out or want to explore features!
    """
    show_banner()
    
    while True:
        console.print("\n[bold cyan]Main Menu[/bold cyan]\n")
        console.print("  1. Analyze Password")
        console.print("  2. Hash Password")
        console.print("  3. Simulate Attack")
        console.print("  4. Demonstrate Defense")
        console.print("  5. Learn Security Concepts")
        console.print("  6. GPU Performance Comparison")
        console.print("  7. Exit\n")
        
        choice = console.input("[cyan]Select option (1-7):[/cyan] ")
        
        if choice == '1':
            password = console.input("\n[yellow]Enter password to analyze:[/yellow] ")
            analyzer = PasswordAnalyzer()
            analyzer.analyze(password, verbose=True)
        
        elif choice == '2':
            password = console.input("\n[yellow]Enter password to hash:[/yellow] ")
            algo = console.input("[yellow]Algorithm (argon2id/bcrypt/scrypt):[/yellow] ") or 'argon2id'
            ctx = click.Context(hash)
            ctx.invoke(hash, password=password, algorithm=algo)
        
        elif choice == '3':
            console.print("\n[yellow]Attack simulation options:[/yellow]")
            console.print("  1. Dictionary Attack")
            console.print("  2. Brute Force Attack")
            console.print("  3. Hybrid Attack")
            mode_choice = console.input("[cyan]Select mode (1-3):[/cyan] ")
            mode_map = {'1': 'dictionary', '2': 'brute_force', '3': 'hybrid'}
            mode = mode_map.get(mode_choice, 'dictionary')
            
            target = console.input("[yellow]Target password:[/yellow] ")
            ctx = click.Context(simulate)
            ctx.invoke(simulate, mode=mode, target=target, algorithm='argon2id', 
                      max_attempts=100000, mask=None)
        
        elif choice == '4':
            console.print("\n[yellow]Defense mechanisms:[/yellow]")
            console.print("  1. Rate Limiting")
            console.print("  2. Account Lockout")
            console.print("  3. Progressive Delay")
            console.print("  4. IP Throttling")
            console.print("  5. Honeytoken")
            console.print("  6. MFA")
            def_choice = console.input("[cyan]Select defense (1-6):[/cyan] ")
            def_map = {'1': 'rate_limiting', '2': 'account_lockout', '3': 'progressive_delay',
                      '4': 'ip_throttling', '5': 'honeytoken', '6': 'mfa'}
            defense = def_map.get(def_choice, 'rate_limiting')
            
            ctx = click.Context(defend)
            ctx.invoke(defend, defense=defense, attempts=100)
        
        elif choice == '5':
            show_learning_menu()
            topic = console.input("\n[cyan]Enter topic name:[/cyan] ")
            educator = SecurityEducation()
            educator.teach_topic(topic)
        
        elif choice == '6':
            ctx = click.Context(gpu)
            ctx.invoke(gpu)
        
        elif choice == '7':
            console.print("\n[green]Thank you for using CipherSim! Stay secure! 🔐[/green]\n")
            break
        
        else:
            console.print("[red]Invalid option. Please try again.[/red]")


def main() -> None:
    """Main entry point"""
    # Show banner if no arguments provided
    if len(sys.argv) == 1:
        show_banner()
        console.print("\n[yellow]Use 'ciphersim --help' for command list or 'ciphersim interactive' for menu mode[/yellow]\n")
    
    cli()


if __name__ == '__main__':
    main()
