"""
Attack Simulator - Safe Offline Password Attack Simulation

WARNING: This module is for EDUCATIONAL PURPOSES ONLY.
All simulations are performed offline with no network activity.
"""

from typing import Iterator, Optional, List, Tuple, Dict
from enum import Enum
from dataclasses import dataclass
import itertools
import string
import time
from pathlib import Path

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from .hash_engine import HashEngine, HashAlgorithm


class AttackMode(Enum):
    """Supported attack simulation modes"""
    DICTIONARY = "dictionary"
    BRUTE_FORCE = "brute_force"
    HYBRID = "hybrid"
    MASK = "mask"
    CREDENTIAL_STUFFING = "credential_stuffing"


@dataclass
class AttackConfig:
    """Configuration for attack simulation"""
    mode: AttackMode
    target_hash: str
    algorithm: HashAlgorithm
    max_attempts: int = 1_000_000
    speed_limit: int = 10_000  # Attempts per second (realistic simulation)
    charset: str = string.ascii_lowercase + string.digits
    min_length: int = 1
    max_length: int = 8
    wordlist_path: Optional[Path] = None
    mask: Optional[str] = None  # e.g., "?u?l?l?l?d?d?d?d"


@dataclass
class AttackResult:
    """Result of attack simulation"""
    success: bool
    password_found: Optional[str]
    attempts: int
    time_seconds: float
    mode: AttackMode
    stopped_by_limit: bool


class AttackSimulator:
    """
    Safe offline attack simulator for educational purposes.
    
    Simulates common password attack techniques:
    - Dictionary attacks
    - Brute force attacks
    - Hybrid attacks (dictionary + mutations)
    - Mask-based attacks
    - Credential stuffing (demo only)
    
    All simulations are offline and rate-limited for realistic demonstration.
    """
    
    def __init__(self, hash_engine: Optional[HashEngine] = None) -> None:
        self.hash_engine = hash_engine or HashEngine()
        self._stop_requested = False
    
    def simulate_attack(self, config: AttackConfig, target_password: str) -> AttackResult:
        """
        Simulate a password attack (EDUCATIONAL ONLY).
        
        Args:
            config: Attack configuration
            target_password: The password to find (for simulation)
            
        Returns:
            AttackResult with success status and statistics
        """
        print(f"\n🎯 Starting {config.mode.value} attack simulation...")
        print(f"⚠️  SIMULATION ONLY - No real attacks are being performed\n")
        
        start_time = time.time()
        attempts = 0
        found = False
        stopped_by_limit = False
        
        # Generate password candidates based on mode
        if config.mode == AttackMode.DICTIONARY:
            candidates = self._dictionary_generator(config)
        elif config.mode == AttackMode.BRUTE_FORCE:
            candidates = self._brute_force_generator(config)
        elif config.mode == AttackMode.HYBRID:
            candidates = self._hybrid_generator(config)
        elif config.mode == AttackMode.MASK:
            candidates = self._mask_generator(config)
        elif config.mode == AttackMode.CREDENTIAL_STUFFING:
            candidates = self._credential_stuffing_generator(config)
        else:
            raise ValueError(f"Unsupported attack mode: {config.mode}")
        
        # Simulate attack with progress bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
        ) as progress:
            task = progress.add_task(
                f"[cyan]Testing passwords...", 
                total=min(config.max_attempts, 100000)
            )
            
            for candidate in candidates:
                # Rate limiting for realistic simulation
                if attempts > 0 and attempts % config.speed_limit == 0:
                    time.sleep(1.0)
                
                # Check if password matches
                if candidate == target_password:
                    found = True
                    break
                
                attempts += 1
                progress.update(task, advance=1)
                
                # Check limits
                if attempts >= config.max_attempts:
                    stopped_by_limit = True
                    break
                
                if self._stop_requested:
                    break
        
        elapsed = time.time() - start_time
        
        return AttackResult(
            success=found,
            password_found=target_password if found else None,
            attempts=attempts,
            time_seconds=elapsed,
            mode=config.mode,
            stopped_by_limit=stopped_by_limit
        )
    
    def stop(self) -> None:
        """Request simulation to stop"""
        self._stop_requested = True
    
    # Generator methods for different attack modes
    
    def _dictionary_generator(self, config: AttackConfig) -> Iterator[str]:
        """Generate passwords from a dictionary wordlist"""
        if not config.wordlist_path or not config.wordlist_path.exists():
            # Use default common passwords
            yield from self._default_wordlist()
        else:
            with open(config.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    password = line.strip()
                    if password:
                        yield password
    
    def _brute_force_generator(self, config: AttackConfig) -> Iterator[str]:
        """Generate all possible passwords in charset within length range"""
        for length in range(config.min_length, config.max_length + 1):
            for combo in itertools.product(config.charset, repeat=length):
                yield ''.join(combo)
    
    def _hybrid_generator(self, config: AttackConfig) -> Iterator[str]:
        """
        Generate passwords using dictionary + mutations.
        Combines wordlist with common mutations (l33t speak, appending numbers, etc.)
        """
        # First try dictionary as-is
        for word in self._dictionary_generator(config):
            yield word
            
            # Common mutations
            yield word.capitalize()
            yield word.upper()
            yield word.lower()
            
            # Append common numbers
            for num in ['1', '123', '2024', '2025', '!']:
                yield word + num
                yield word.capitalize() + num
            
            # L33t speak substitutions
            leet_map = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
            leet_word = ''.join(leet_map.get(c.lower(), c) for c in word)
            if leet_word != word:
                yield leet_word
    
    def _mask_generator(self, config: AttackConfig) -> Iterator[str]:
        """
        Generate passwords based on a mask pattern.
        
        Mask syntax:
        ?l = lowercase letter
        ?u = uppercase letter
        ?d = digit
        ?s = special character
        ?a = any (all charset)
        
        Example: "?u?l?l?l?d?d?d?d" = Aaaa1234
        """
        if not config.mask:
            yield from self._brute_force_generator(config)
            return
        
        # Parse mask into character sets
        charsets = []
        mask = config.mask
        i = 0
        
        while i < len(mask):
            if mask[i] == '?' and i + 1 < len(mask):
                placeholder = mask[i+1]
                if placeholder == 'l':
                    charsets.append(string.ascii_lowercase)
                elif placeholder == 'u':
                    charsets.append(string.ascii_uppercase)
                elif placeholder == 'd':
                    charsets.append(string.digits)
                elif placeholder == 's':
                    charsets.append('!@#$%^&*()_+-=[]{}|;:,.<>?')
                elif placeholder == 'a':
                    charsets.append(string.ascii_letters + string.digits + string.punctuation)
                i += 2
            else:
                # Literal character
                charsets.append([mask[i]])
                i += 1
        
        # Generate all combinations
        for combo in itertools.product(*charsets):
            yield ''.join(combo)
    
    def _credential_stuffing_generator(self, config: AttackConfig) -> Iterator[str]:
        """
        Simulate credential stuffing attack (DEMO ONLY).
        Uses fake credential pairs for educational demonstration.
        """
        # DEMO credentials only - NOT REAL
        demo_credentials = [
            ("user1@example.com", "Password123!"),
            ("testuser@demo.com", "Welcome2024"),
            ("admin@test.local", "Admin@123"),
            ("demo@email.com", "Summer2024!"),
        ]
        
        for email, password in demo_credentials:
            yield password
    
    @staticmethod
    def _default_wordlist() -> List[str]:
        """Default common passwords for simulation"""
        return [
            "password", "123456", "12345678", "qwerty", "abc123",
            "password123", "admin", "letmein", "welcome", "monkey",
            "dragon", "master", "sunshine", "princess", "football",
            "iloveyou", "shadow", "michael", "superman", "trustno1",
        ]


class GPUSimulator:
    """
    Simulates GPU-accelerated password cracking performance.
    
    Provides realistic performance estimates without actual GPU usage.
    Educational demonstration of why GPU cracking is effective.
    """
    
    # Simulated performance for different GPU tiers (hashes/second)
    GPU_TIERS = {
        "RTX_4090": {
            HashAlgorithm.ARGON2ID: 50_000,
            HashAlgorithm.SCRYPT: 100_000,
            HashAlgorithm.PBKDF2_SHA256: 10_000_000,
            HashAlgorithm.BCRYPT: 500_000,
        },
        "RTX_3080": {
            HashAlgorithm.ARGON2ID: 30_000,
            HashAlgorithm.SCRYPT: 60_000,
            HashAlgorithm.PBKDF2_SHA256: 6_000_000,
            HashAlgorithm.BCRYPT: 300_000,
        },
        "CPU_ONLY": {
            HashAlgorithm.ARGON2ID: 1_000,
            HashAlgorithm.SCRYPT: 2_000,
            HashAlgorithm.PBKDF2_SHA256: 100_000,
            HashAlgorithm.BCRYPT: 10_000,
        }
    }
    
    @classmethod
    def estimate_performance(
        cls, 
        algorithm: HashAlgorithm,
        gpu_tier: str = "RTX_4090"
    ) -> int:
        """
        Estimate hash calculation performance.
        
        Args:
            algorithm: Hashing algorithm
            gpu_tier: GPU tier (RTX_4090, RTX_3080, CPU_ONLY)
            
        Returns:
            Estimated hashes per second
        """
        return cls.GPU_TIERS.get(gpu_tier, cls.GPU_TIERS["CPU_ONLY"]).get(
            algorithm, 1000
        )
    
    @classmethod
    def get_performance_comparison(cls) -> Dict[str, Dict[HashAlgorithm, int]]:
        """Get full performance comparison across all GPU tiers"""
        return cls.GPU_TIERS
