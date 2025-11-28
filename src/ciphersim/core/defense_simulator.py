"""
Defense Simulator - Demonstrates Security Defenses Against Password Attacks

Educational module showing how various defense mechanisms protect against attacks.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import time
from datetime import datetime, timedelta
from collections import defaultdict

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn


class DefenseType(Enum):
    """Types of defense mechanisms"""
    RATE_LIMITING = "rate_limiting"
    ACCOUNT_LOCKOUT = "account_lockout"
    PROGRESSIVE_DELAY = "progressive_delay"
    IP_THROTTLING = "ip_throttling"
    HONEYTOKEN = "honeytoken"
    MFA = "mfa"
    CAPTCHA = "captcha"


@dataclass
class LoginAttempt:
    """Represents a login attempt"""
    timestamp: datetime
    ip_address: str
    username: str
    password: str
    success: bool


@dataclass
class DefenseConfig:
    """Configuration for defense mechanisms"""
    # Rate limiting
    max_attempts_per_minute: int = 5
    max_attempts_per_hour: int = 20
    
    # Account lockout
    lockout_threshold: int = 5
    lockout_duration_minutes: int = 15
    
    # Progressive delay
    enable_progressive_delay: bool = True
    base_delay_ms: int = 500
    
    # IP throttling
    enable_ip_throttling: bool = True
    ip_max_attempts: int = 10
    
    # Honeytoken
    honeytoken_passwords: List[str] = None
    
    # MFA
    require_mfa: bool = True


class DefenseSimulator:
    """
    Simulates various defense mechanisms against password attacks.
    
    Educational demonstration of how security controls protect accounts:
    - Rate limiting
    - Account lockout
    - Progressive delays
    - IP throttling
    - Honeytoken passwords
    - Multi-factor authentication (MFA)
    """
    
    def __init__(self, config: Optional[DefenseConfig] = None) -> None:
        self.config = config or DefenseConfig()
        self.attempt_history: List[LoginAttempt] = []
        self.failed_attempts: Dict[str, int] = defaultdict(int)
        self.locked_accounts: Dict[str, datetime] = {}
        self.ip_attempts: Dict[str, List[datetime]] = defaultdict(list)
        self.console = Console()
        
        # Initialize honeytoken passwords
        if self.config.honeytoken_passwords is None:
            self.config.honeytoken_passwords = [
                "admin", "password", "123456", "root", "admin123"
            ]
    
    def simulate_defense(
        self, 
        defense_type: DefenseType,
        attack_attempts: int = 100,
        attack_rate: int = 10  # Attempts per second
    ) -> None:
        """
        Simulate a defense mechanism against an attack.
        
        Args:
            defense_type: Type of defense to demonstrate
            attack_attempts: Number of attack attempts to simulate
            attack_rate: Rate of attack (attempts/second)
        """
        self.console.print(f"\n[bold cyan]🛡️  Simulating {defense_type.value.replace('_', ' ').title()}[/bold cyan]\n")
        
        if defense_type == DefenseType.RATE_LIMITING:
            self._demo_rate_limiting(attack_attempts, attack_rate)
        elif defense_type == DefenseType.ACCOUNT_LOCKOUT:
            self._demo_account_lockout(attack_attempts)
        elif defense_type == DefenseType.PROGRESSIVE_DELAY:
            self._demo_progressive_delay(attack_attempts)
        elif defense_type == DefenseType.IP_THROTTLING:
            self._demo_ip_throttling(attack_attempts)
        elif defense_type == DefenseType.HONEYTOKEN:
            self._demo_honeytoken()
        elif defense_type == DefenseType.MFA:
            self._demo_mfa()
        else:
            self.console.print(f"[yellow]Defense type {defense_type} not yet implemented[/yellow]")
    
    def _demo_rate_limiting(self, attempts: int, rate: int) -> None:
        """Demonstrate rate limiting defense"""
        blocked = 0
        allowed = 0
        
        self.console.print(
            f"[yellow]⚙️  Rate Limit: {self.config.max_attempts_per_minute} attempts/minute[/yellow]\n"
        )
        
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task("[cyan]Attack simulation...", total=attempts)
            
            minute_attempts = 0
            minute_start = datetime.now()
            
            for i in range(attempts):
                current_time = datetime.now()
                
                # Reset counter every minute
                if (current_time - minute_start).seconds >= 60:
                    minute_attempts = 0
                    minute_start = current_time
                
                # Check rate limit
                if minute_attempts < self.config.max_attempts_per_minute:
                    allowed += 1
                    minute_attempts += 1
                else:
                    blocked += 1
                
                progress.update(task, advance=1)
                time.sleep(1.0 / rate)  # Simulate attack rate
        
        # Display results
        self._display_defense_results(
            "Rate Limiting",
            allowed,
            blocked,
            f"{self.config.max_attempts_per_minute} attempts/minute limit"
        )
    
    def _demo_account_lockout(self, attempts: int) -> None:
        """Demonstrate account lockout after failed attempts"""
        blocked = 0
        allowed = 0
        failed_count = 0
        locked = False
        
        self.console.print(
            f"[yellow]⚙️  Lockout after {self.config.lockout_threshold} failed attempts "
            f"for {self.config.lockout_duration_minutes} minutes[/yellow]\n"
        )
        
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task("[cyan]Attack simulation...", total=attempts)
            
            for i in range(attempts):
                if locked:
                    blocked += 1
                elif failed_count < self.config.lockout_threshold:
                    allowed += 1
                    failed_count += 1
                else:
                    # Account locked!
                    locked = True
                    blocked += 1
                    self.console.print(
                        f"\n[red]🔒 Account locked after {failed_count} failed attempts![/red]\n"
                    )
                
                progress.update(task, advance=1)
                time.sleep(0.01)
        
        self._display_defense_results(
            "Account Lockout",
            allowed,
            blocked,
            f"Locked after {self.config.lockout_threshold} failures"
        )
    
    def _demo_progressive_delay(self, attempts: int) -> None:
        """Demonstrate progressive delay (exponential backoff)"""
        blocked = 0
        total_delay = 0.0
        
        self.console.print(
            "[yellow]⚙️  Progressive delay increases with each failed attempt[/yellow]\n"
        )
        
        delays = []
        for i in range(min(attempts, 10)):
            delay = self.config.base_delay_ms * (2 ** i) / 1000.0  # Exponential backoff
            delays.append(delay)
            total_delay += delay
        
        # Display delay progression table
        table = Table(title="Progressive Delay Schedule")
        table.add_column("Attempt #", style="cyan")
        table.add_column("Delay", style="yellow")
        table.add_column("Cumulative", style="green")
        
        cumulative = 0.0
        for i, delay in enumerate(delays[:10], 1):
            cumulative += delay
            table.add_row(
                str(i),
                f"{delay:.2f}s",
                f"{cumulative:.2f}s"
            )
        
        self.console.print(table)
        self.console.print(
            f"\n[green]✓ After 10 attempts, attacker has wasted {cumulative:.2f} seconds[/green]"
        )
        self.console.print(
            f"[green]✓ Attack becomes impractical due to exponential time cost[/green]\n"
        )
    
    def _demo_ip_throttling(self, attempts: int) -> None:
        """Demonstrate IP-based throttling"""
        blocked = 0
        allowed = 0
        
        self.console.print(
            f"[yellow]⚙️  IP Throttling: Max {self.config.ip_max_attempts} "
            f"attempts per IP[/yellow]\n"
        )
        
        # Simulate attacks from multiple IPs
        ips = [f"192.168.1.{i}" for i in range(1, 6)]
        ip_counts = {ip: 0 for ip in ips}
        
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task("[cyan]Multi-IP attack...", total=attempts)
            
            for i in range(attempts):
                ip = ips[i % len(ips)]
                
                if ip_counts[ip] < self.config.ip_max_attempts:
                    allowed += 1
                    ip_counts[ip] += 1
                else:
                    blocked += 1
                
                progress.update(task, advance=1)
                time.sleep(0.01)
        
        self._display_defense_results(
            "IP Throttling",
            allowed,
            blocked,
            f"{self.config.ip_max_attempts} attempts per IP"
        )
    
    def _demo_honeytoken(self) -> None:
        """Demonstrate honeytoken password trap"""
        self.console.print(
            Panel(
                "[bold yellow]🍯 Honeytoken Password Trap[/bold yellow]\n\n"
                "Honeytoken passwords are fake, obvious passwords that trigger alerts.\n"
                "When an attacker tries these, security teams are immediately notified.\n\n"
                "[cyan]Example Honeytokens:[/cyan]\n"
                + "\n".join(f"  • {pwd}" for pwd in self.config.honeytoken_passwords[:5]) +
                "\n\n[red]⚠️  Using a honeytoken triggers:[/red]\n"
                "  • Immediate security alert\n"
                "  • IP address blocking\n"
                "  • Incident response activation\n"
                "  • Account flagged for review",
                title="Honeytoken Defense",
                border_style="yellow"
            )
        )
    
    def _demo_mfa(self) -> None:
        """Demonstrate how MFA defeats password attacks"""
        self.console.print(
            Panel(
                "[bold green]🔐 Multi-Factor Authentication (MFA)[/bold green]\n\n"
                "MFA requires TWO or more verification factors:\n"
                "  1️⃣  Something you KNOW (password)\n"
                "  2️⃣  Something you HAVE (phone, security key)\n"
                "  3️⃣  Something you ARE (biometric)\n\n"
                "[yellow]Why MFA defeats password attacks:[/yellow]\n"
                "  ✓ Attacker needs BOTH password AND second factor\n"
                "  ✓ Second factor is time-limited (e.g., 30-second TOTP)\n"
                "  ✓ Physical possession required (can't steal remotely)\n"
                "  ✓ Phishing-resistant options (FIDO2, WebAuthn)\n\n"
                "[green]Even if password is compromised, account stays secure! 🛡️[/green]",
                title="MFA Protection",
                border_style="green"
            )
        )
    
    def _display_defense_results(
        self, 
        defense_name: str,
        allowed: int,
        blocked: int,
        config_summary: str
    ) -> None:
        """Display defense simulation results"""
        total = allowed + blocked
        block_rate = (blocked / total * 100) if total > 0 else 0
        
        table = Table(title=f"\n{defense_name} Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="yellow")
        
        table.add_row("Total Attempts", str(total))
        table.add_row("Allowed", f"[green]{allowed}[/green]")
        table.add_row("Blocked", f"[red]{blocked}[/red]")
        table.add_row("Block Rate", f"[bold]{block_rate:.1f}%[/bold]")
        table.add_row("Configuration", config_summary)
        
        self.console.print(table)
        self.console.print(
            f"\n[green]✓ Defense successfully blocked {blocked}/{total} "
            f"({block_rate:.1f}%) malicious attempts[/green]\n"
        )
