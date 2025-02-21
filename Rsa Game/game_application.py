import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
import random
import time
import json
from os import path
from frames import PrimeFrame, KeyFrame, EncryptFrame, DecryptFrame

class RSAGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA Cryptography Game")
        self.root.geometry("1000x700")
        
        # Game state variables
        self.player_name = ""
        self.difficulty = 1  # Default: Medium
        self.p = 0
        self.q = 0
        self.n = 0
        self.phi = 0
        self.e = 0
        self.d = 0
        self.encrypted = []
        self.start_time = 0
        self.total_time = 0
        self.stage_times = []  # Track time for each stage

        # Create main paned window
        self.main_pane = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)
        
        # Create frames
        self.content_frame = ttk.Frame(self.main_pane)
        self.notes_frame = ttk.Frame(self.main_pane)
        self.main_pane.add(self.content_frame, weight=3)
        self.main_pane.add(self.notes_frame, weight=1)
        
        # Initialize notes section first
        self.create_notes_section()
        
        # Initialize game frames
        self.frames = {}
        from frames import StartFrame, PrimeFrame, KeyFrame, EncryptFrame, DecryptFrame, LeaderboardFrame
        for F in (StartFrame, PrimeFrame, KeyFrame, EncryptFrame, DecryptFrame, LeaderboardFrame):
            frame = F(self.content_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartFrame)

    def create_notes_section(self):
        """Create the persistent notes panel."""
        notes_header = ttk.Label(self.notes_frame, text="Instructions & Examples", 
                               font=("Helvetica", 12, "bold"))
        notes_header.pack(pady=10)
        
        self.notes_text = scrolledtext.ScrolledText(self.notes_frame, 
                                                  wrap=tk.WORD,
                                                  width=30,
                                                  height=30,
                                                  font=("Helvetica", 10))
        self.notes_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.notes_text.config(state=tk.DISABLED)  
        
    def update_notes(self, content):
        """Update the notes panel with new content."""
        self.notes_text.config(state=tk.NORMAL)
        self.notes_text.delete(1.0, tk.END)
        self.notes_text.insert(tk.INSERT, content)
        self.notes_text.config(state=tk.DISABLED)
        
    def show_frame(self, cont):
        """Show the specified frame."""
        frame = self.frames[cont]
        frame.tkraise()
        frame.update_notes()

    def start_game(self):
        """Start the game and initialize timers."""
        if not self.player_name:
            messagebox.showerror("Error", "Please enter your name!")
            return
            
        self.start_time = time.time()
        self.total_time = 0
        self.stage_times = []
        self.show_frame(PrimeFrame)

    def validate_primes(self, p, q):
        """Validate the prime numbers entered by the user."""
        # Check if the numbers are prime
        if not (self.is_prime(p) and self.is_prime(q)):
            messagebox.showerror("Error", "Invalid prime numbers!")
            return False

        # Check if the primes match the selected difficulty level
        if self.difficulty == 1:  # Easy (2-digit primes)
            if not (10 <= p <= 99 and 10 <= q <= 99):
                messagebox.showerror("Error", "For Easy difficulty, both primes must be 2-digit numbers!")
                return False
        elif self.difficulty == 2:  # Medium (3-digit primes)
            if not (100 <= p <= 999 and 100 <= q <= 999):
                messagebox.showerror("Error", "For Medium difficulty, both primes must be 3-digit numbers!")
                return False
        elif self.difficulty == 3:  # Hard (4-digit primes)
            if not (1000 <= p <= 9999 and 1000 <= q <= 9999):
                messagebox.showerror("Error", "For Hard difficulty, both primes must be 4-digit numbers!")
                return False

        # If validation passes, proceed with the game
        self.stage_times.append(time.time() - self.start_time)
        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (p-1) * (q-1)
        self.start_time = time.time()
        self.show_frame(KeyFrame)
        return True

    def generate_keys(self, e):
        """Generate the public and private keys."""
        if math.gcd(e, self.phi) != 1:
            messagebox.showerror("Error", "Invalid public exponent!")
            return False
            
        self.stage_times.append(time.time() - self.start_time)
        self.e = e
        self.d = self.mod_inverse(e, self.phi)
        self.start_time = time.time()
        self.show_frame(EncryptFrame)
        return True

    def encrypt_message(self, message):
        """Encrypt the message using the public key."""
        try:
            self.encrypted = [pow(ord(c), self.e, self.n) for c in message]
            self.stage_times.append(time.time() - self.start_time)
            self.start_time = time.time()
            self.show_frame(DecryptFrame)
            return True
        except:
            messagebox.showerror("Error", "Encryption failed!")
            return False

    def decrypt_message(self, d):
        """Decrypt the message using the private key."""
        try:
            decrypted = ''.join([chr(pow(c, d, self.n)) for c in self.encrypted])
            self.stage_times.append(time.time() - self.start_time)
            self.total_time = sum(self.stage_times)
            return decrypted
        except:
            return False

    def save_to_leaderboard(self):
        """Save the player's score to the leaderboard."""
        leaderboard = self.load_leaderboard()
        leaderboard.append({
            "name": self.player_name,
            "time": self.total_time,
            "difficulty": ["Easy", "Medium", "Hard"][self.difficulty - 1]
        })
        leaderboard.sort(key=lambda x: x["time"])
        """Change according to your own directory"""
        with open("C:/Users/user/Downloads/Rsa Game/JSON file/leaderboard.json", "w") as f:
            json.dump(leaderboard[:10], f)

    def load_leaderboard(self):
        """Load the leaderboard from a JSON file."""
        if not path.exists("C:/Users/user/Downloads/Rsa Game/JSON file/leaderboard.json"):
             return []  # Return an empty list if the file doesn't exist
    
        try:
            with open("C:/Users/user/Downloads/Rsa Game/JSON file/leaderboard.json", "r") as f:
                leaderboard = json.load(f)
            # Ensure the leaderboard is a list and has the correct structure
            if not isinstance(leaderboard, list):
                return []  # Return an empty list if the file is corrupted
            return leaderboard
        except (json.JSONDecodeError, FileNotFoundError):
            return []  # Return an empty list if the file is corrupted or can't be read

    # Core RSA functions
    def is_prime(self, num, k=5):
        """Miller-Rabin primality test."""
        if num < 2:
            return False
        for prime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
            if num % prime == 0:
                return num == prime
        d = num - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        for _ in range(k):
            a = random.randint(2, min(num - 2, 1 << 20))
            x = pow(a, d, num)
            if x == 1 or x == num - 1:
                continue
            for __ in range(s - 1):
                x = pow(x, 2, num)
                if x == num - 1:
                    break
            else:
                return False
        return True

    def mod_inverse(self, e, phi):
        """Extended Euclidean Algorithm for modular inverse."""
        g, x, _ = self.extended_gcd(e, phi)
        if g != 1:
            return None
        else:
            return x % phi

    def extended_gcd(self, a, b):
        """Extended Euclidean Algorithm."""
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.extended_gcd(b % a, a)
            return (g, x - (b // a) * y, y)