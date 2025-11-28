"""
Password Analyzer - Advanced Password Strength Analysis

Provides comprehensive password security analysis including:
- Entropy calculation
- Pattern detection
- Dictionary checking
- Crack time estimation
- Security recommendations
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import re
import math
import string

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from ..core.hash_engine import HashEngine, HashAlgorithm


class PasswordStrength(Enum):
    """Password strength categories"""
    VERY_WEAK = "very_weak"
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    VERY_STRONG = "very_strong"


@dataclass
class PatternMatch:
    """Detected pattern in password"""
    pattern_type: str
    description: str
    severity: str  # low, medium, high
    position: Tuple[int, int]


@dataclass
class PasswordAnalysis:
    """Complete password security analysis"""
    password: str
    length: int
    charset_size: int
    entropy_bits: float
    strength: PasswordStrength
    patterns: List[PatternMatch]
    crack_time_estimates: Dict[str, str]
    score: int  # 0-100
    recommendations: List[str]


class PasswordAnalyzer:
    """
    Advanced password strength analyzer using multiple techniques.
    
    Based on zxcvbn-style analysis with modern 2025 standards:
    - Shannon entropy calculation
    - Pattern recognition (keyboard patterns, dates, names)
    - Dictionary word detection
    - Crack time estimation across algorithm types
    - Actionable improvement recommendations
    """
    
    # Common keyboard patterns
    KEYBOARD_PATTERNS = [
        'qwerty', 'asdfgh', 'zxcvbn', '12345', 'qwertyuiop',
        'asdfghjkl', 'zxcvbnm', 'qazwsx', '1qaz2wsx',
    ]
    
    # Common sequences
    SEQUENCES = [
        'abc', '123', 'xyz', 'rst',
    ]
    
    # Common years (for date detection)
    YEAR_PATTERN = re.compile(r'(19|20)\d{2}')
    
    def __init__(self, hash_engine: Optional[HashEngine] = None) -> None:
        self.hash_engine = hash_engine or HashEngine()
        self.console = Console()
        
        # Load common passwords (in real implementation, load from file)
        self.common_passwords = self._load_common_passwords()
    
    def analyze(self, password: str, verbose: bool = True) -> PasswordAnalysis:
        """
        Perform comprehensive password analysis.
        
        Args:
            password: Password to analyze
            verbose: Whether to display detailed output
            
        Returns:
            PasswordAnalysis with complete security assessment
        """
        # Calculate basic metrics
        length = len(password)
        charset_size = self._calculate_charset_size(password)
        entropy = self._calculate_entropy(password, charset_size)
        
        # Detect patterns
        patterns = self._detect_patterns(password)
        
        # Estimate crack times
        crack_times = self._estimate_crack_times(password, length, charset_size)
        
        # Calculate score (0-100)
        score = self._calculate_score(password, entropy, patterns)
        
        # Determine strength category
        strength = self._categorize_strength(score, entropy)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            password, length, charset_size, patterns, strength
        )
        
        analysis = PasswordAnalysis(
            password=password,
            length=length,
            charset_size=charset_size,
            entropy_bits=entropy,
            strength=strength,
            patterns=patterns,
            crack_time_estimates=crack_times,
            score=score,
            recommendations=recommendations
        )
        
        if verbose:
            self.display_analysis(analysis)
        
        return analysis
    
    def display_analysis(self, analysis: PasswordAnalysis) -> None:
        """Display formatted analysis results"""
        # Strength indicator with color
        strength_colors = {
            PasswordStrength.VERY_WEAK: "red",
            PasswordStrength.WEAK: "orange1",
            PasswordStrength.MODERATE: "yellow",
            PasswordStrength.STRONG: "green",
            PasswordStrength.VERY_STRONG: "bold green",
        }
        
        strength_color = strength_colors.get(analysis.strength, "white")
        
        # Header
        self.console.print(f"\n[bold cyan]🔍 Password Security Analysis[/bold cyan]\n")
        
        # Basic metrics table
        metrics_table = Table(title="Metrics", box=box.ROUNDED)
        metrics_table.add_column("Property", style="cyan")
        metrics_table.add_column("Value", style="yellow")
        
        metrics_table.add_row("Length", str(analysis.length))
        metrics_table.add_row("Character Set Size", str(analysis.charset_size))
        metrics_table.add_row("Entropy", f"{analysis.entropy_bits:.2f} bits")
        metrics_table.add_row("Score", f"{analysis.score}/100")
        metrics_table.add_row(
            "Strength", 
            f"[{strength_color}]{analysis.strength.value.upper().replace('_', ' ')}[/{strength_color}]"
        )
        
        self.console.print(metrics_table)
        
        # Crack time estimates
        if analysis.crack_time_estimates:
            self.console.print("\n[bold]⏱️  Time to Crack Estimates (Brute Force)[/bold]\n")
            
            crack_table = Table(box=box.SIMPLE)
            crack_table.add_column("Algorithm", style="cyan")
            crack_table.add_column("CPU", style="yellow")
            crack_table.add_column("GPU (RTX 4090)", style="red")
            
            for algo_name, times in analysis.crack_time_estimates.items():
                crack_table.add_row(algo_name, times['cpu'], times['gpu'])
            
            self.console.print(crack_table)
        
        # Patterns detected
        if analysis.patterns:
            self.console.print("\n[bold yellow]⚠️  Patterns Detected[/bold yellow]\n")
            
            for pattern in analysis.patterns:
                severity_color = {
                    'low': 'yellow',
                    'medium': 'orange1',
                    'high': 'red'
                }.get(pattern.severity, 'white')
                
                self.console.print(
                    f"  [{severity_color}]•[/{severity_color}] "
                    f"{pattern.pattern_type}: {pattern.description}"
                )
        
        # Recommendations
        if analysis.recommendations:
            self.console.print("\n[bold green]💡 Recommendations[/bold green]\n")
            for i, rec in enumerate(analysis.recommendations, 1):
                self.console.print(f"  {i}. {rec}")
        
        self.console.print()
    
    # Analysis methods
    
    def _calculate_charset_size(self, password: str) -> int:
        """Calculate the character set size used in password"""
        has_lowercase = any(c in string.ascii_lowercase for c in password)
        has_uppercase = any(c in string.ascii_uppercase for c in password)
        has_digits = any(c in string.digits for c in password)
        has_special = any(c in string.punctuation for c in password)
        has_space = ' ' in password
        
        size = 0
        if has_lowercase:
            size += 26
        if has_uppercase:
            size += 26
        if has_digits:
            size += 10
        if has_special:
            size += 32
        if has_space:
            size += 1
        
        return size if size > 0 else 1
    
    def _calculate_entropy(self, password: str, charset_size: int) -> float:
        """
        Calculate Shannon entropy of password.
        
        Entropy (bits) = log2(charset_size ^ length)
        """
        if len(password) == 0 or charset_size == 0:
            return 0.0
        
        return math.log2(charset_size ** len(password))
    
    def _detect_patterns(self, password: str) -> List[PatternMatch]:
        """Detect common patterns that weaken passwords"""
        patterns = []
        password_lower = password.lower()
        
        # Check if it's a common password
        if password_lower in self.common_passwords:
            patterns.append(PatternMatch(
                pattern_type="Common Password",
                description="This is a commonly used password",
                severity="high",
                position=(0, len(password))
            ))
        
        # Check for keyboard patterns
        for pattern in self.KEYBOARD_PATTERNS:
            if pattern in password_lower:
                patterns.append(PatternMatch(
                    pattern_type="Keyboard Pattern",
                    description=f"Contains keyboard pattern: {pattern}",
                    severity="high",
                    position=(password_lower.index(pattern), password_lower.index(pattern) + len(pattern))
                ))
        
        # Check for sequences
        for seq in self.SEQUENCES:
            if seq in password_lower:
                patterns.append(PatternMatch(
                    pattern_type="Character Sequence",
                    description=f"Contains character sequence: {seq}",
                    severity="medium",
                    position=(password_lower.index(seq), password_lower.index(seq) + len(seq))
                ))
        
        # Check for repeated characters
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                patterns.append(PatternMatch(
                    pattern_type="Character Repetition",
                    description=f"Repeated character: {password[i]}",
                    severity="medium",
                    position=(i, i+3)
                ))
                break
        
        # Check for dates/years
        year_match = self.YEAR_PATTERN.search(password)
        if year_match:
            patterns.append(PatternMatch(
                pattern_type="Date/Year",
                description=f"Contains year: {year_match.group()}",
                severity="medium",
                position=year_match.span()
            ))
        
        # Check for common substitutions (l33t speak)
        leet_patterns = {'@': 'a', '3': 'e', '1': 'i', '0': 'o', '$': 's', '7': 't'}
        leet_found = any(char in password for char in leet_patterns.keys())
        if leet_found:
            patterns.append(PatternMatch(
                pattern_type="L33t Speak",
                description="Uses common character substitutions (easily defeated)",
                severity="low",
                position=(0, len(password))
            ))
        
        return patterns
    
    def _estimate_crack_times(
        self, 
        password: str, 
        length: int, 
        charset_size: int
    ) -> Dict[str, Dict[str, str]]:
        """Estimate time to crack password with different algorithms"""
        estimates = {}
        
        algorithms = [
            (HashAlgorithm.ARGON2ID, "Argon2id (2025 Recommended)"),
            (HashAlgorithm.BCRYPT, "bcrypt"),
            (HashAlgorithm.PBKDF2_SHA256, "PBKDF2-SHA256"),
        ]
        
        for algo, display_name in algorithms:
            # CPU estimate
            cpu_estimate = self.hash_engine.estimate_crack_time(
                length, charset_size, algo, use_gpu=False
            )
            
            # GPU estimate
            gpu_estimate = self.hash_engine.estimate_crack_time(
                length, charset_size, algo, use_gpu=True
            )
            
            estimates[display_name] = {
                'cpu': cpu_estimate.human_readable,
                'gpu': gpu_estimate.human_readable
            }
        
        return estimates
    
    def _calculate_score(
        self, 
        password: str, 
        entropy: float, 
        patterns: List[PatternMatch]
    ) -> int:
        """Calculate password score (0-100)"""
        # Start with entropy-based score
        # 128 bits = perfect score
        score = min(100, int(entropy / 128 * 100))
        
        # Deduct points for patterns
        for pattern in patterns:
            if pattern.severity == 'high':
                score -= 25
            elif pattern.severity == 'medium':
                score -= 15
            elif pattern.severity == 'low':
                score -= 5
        
        # Bonus for length
        if len(password) >= 16:
            score += 10
        elif len(password) >= 12:
            score += 5
        
        # Ensure score is in valid range
        return max(0, min(100, score))
    
    def _categorize_strength(self, score: int, entropy: float) -> PasswordStrength:
        """Categorize password strength based on score and entropy"""
        if score >= 80 and entropy >= 80:
            return PasswordStrength.VERY_STRONG
        elif score >= 60 and entropy >= 60:
            return PasswordStrength.STRONG
        elif score >= 40 and entropy >= 40:
            return PasswordStrength.MODERATE
        elif score >= 20:
            return PasswordStrength.WEAK
        else:
            return PasswordStrength.VERY_WEAK
    
    def _generate_recommendations(
        self, 
        password: str, 
        length: int, 
        charset_size: int,
        patterns: List[PatternMatch],
        strength: PasswordStrength
    ) -> List[str]:
        """Generate actionable security recommendations"""
        recommendations = []
        
        # Length recommendations
        if length < 12:
            recommendations.append(
                f"Increase length to at least 12 characters (current: {length}). "
                "Each additional character exponentially increases security."
            )
        elif length < 16:
            recommendations.append(
                "Consider using 16+ characters for maximum security in 2025."
            )
        
        # Character set recommendations
        if charset_size < 62:  # Not using both upper and lower
            recommendations.append(
                "Use a mix of uppercase, lowercase, numbers, and special characters."
            )
        
        # Pattern-specific recommendations
        if any(p.pattern_type == "Common Password" for p in patterns):
            recommendations.append(
                "CRITICAL: This is a commonly used password. Change it immediately!"
            )
        
        if any(p.pattern_type == "Keyboard Pattern" for p in patterns):
            recommendations.append(
                "Avoid keyboard patterns (qwerty, asdf, etc.). Use random characters instead."
            )
        
        if any(p.pattern_type == "Date/Year" for p in patterns):
            recommendations.append(
                "Avoid using dates or years. This information can be easily guessed."
            )
        
        # General recommendations
        if strength in [PasswordStrength.VERY_WEAK, PasswordStrength.WEAK]:
            recommendations.append(
                "Use a password manager to generate and store strong, unique passwords."
            )
            recommendations.append(
                "Enable Multi-Factor Authentication (MFA) for critical accounts."
            )
        
        if not recommendations:
            recommendations.append(
                "✓ Password is strong! Remember to use unique passwords for each account."
            )
            recommendations.append(
                "✓ Enable MFA for additional security layer."
            )
        
        return recommendations
    
    @staticmethod
    def _load_common_passwords() -> set:
        """Load common passwords (simplified for demo)"""
        return {
            'password', '123456', '12345678', 'qwerty', 'abc123',
            'password123', 'admin', 'letmein', 'welcome', 'monkey',
            'dragon', 'master', 'sunshine', 'princess', 'football',
            'iloveyou', 'shadow', 'michael', 'superman', 'trustno1',
            'passw0rd', 'admin123', 'root', 'toor', 'password1',
        }
