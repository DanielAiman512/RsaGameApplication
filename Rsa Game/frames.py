import tkinter as tk
from tkinter import ttk, messagebox
import math

class StartFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="RSA Cryptography Game", font=("Helvetica", 18))
        label.pack(pady=20)
        
        # Name entry
        name_frame = ttk.Frame(self)
        name_frame.pack(pady=10)
        ttk.Label(name_frame, text="Enter your name:").pack(side=tk.LEFT)
        self.name_entry = ttk.Entry(name_frame)
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        # Difficulty selection
        difficulty_frame = ttk.LabelFrame(self, text="Select Difficulty")
        difficulty_frame.pack(pady=10)
        
        self.difficulty = tk.IntVar(value=0)
        ttk.Radiobutton(difficulty_frame, text="Easy (2-digit primes: 10-99)", 
                       variable=self.difficulty, value=1).pack(anchor=tk.W)
        ttk.Radiobutton(difficulty_frame, text="Medium (3-digit primes: 100-999)", 
                       variable=self.difficulty, value=2).pack(anchor=tk.W)
        ttk.Radiobutton(difficulty_frame, text="Hard (4-digit primes: 1000-9999)", 
                       variable=self.difficulty, value=3).pack(anchor=tk.W)
        
        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Start Game", command=self.start_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="View Leaderboard", command=self.show_leaderboard).pack(side=tk.LEFT, padx=5)

    def start_game(self):
        """Start the game after validating the name."""
        self.controller.player_name = self.name_entry.get()
        if not self.controller.player_name:
            messagebox.showerror("Error", "Please enter your name!")
            return
        self.controller.difficulty = self.difficulty.get()
        self.controller.start_game()

    def show_leaderboard(self):
        """Navigate to the leaderboard."""
        self.controller.show_frame(LeaderboardFrame)

    def update_notes(self):
        """Update the notes panel with instructions and RSA explanation."""
        notes = """=== RSA Cryptography Basics ===

    RSA is a public-key cryptosystem used for secure data transmission. It involves:
    1. Key Generation:
    - Choose two large prime numbers, p and q.
    - Compute n = p × q and φ(n) = (p-1)(q-1).
    - Choose public exponent e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1.
    - Compute private exponent d as the modular inverse of e modulo φ(n).

    2. Encryption:
    - Convert message to numbers (e.g., ASCII).
    - Encrypt: c = m^e mod n.

    3. Decryption:
    - Decrypt: m = c^d mod n.

    === Game Instructions ===
    1. Enter your name.
    2. Select difficulty level.
    3. Click Start Game to begin.
    4. View leaderboard anytime."""
        self.controller.update_notes(notes)

class PrimeFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Prime Number Selection", font=("Helvetica", 14))
        label.pack(pady=10)
        
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=20)
        
        ttk.Label(input_frame, text="Enter prime p:").grid(row=0, column=0, padx=5)
        self.p_entry = ttk.Entry(input_frame)
        self.p_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Enter prime q:").grid(row=1, column=0, padx=5)
        self.q_entry = ttk.Entry(input_frame)
        self.q_entry.grid(row=1, column=1, padx=5)
        
        validate_btn = ttk.Button(self, text="Validate Primes", command=self.validate)
        validate_btn.pack(pady=10)

    def validate(self):
        """Validate the prime numbers entered by the user."""
        try:
            p = int(self.p_entry.get())
            q = int(self.q_entry.get())
            if self.controller.validate_primes(p, q):
                messagebox.showinfo("Success", "Valid primes!")
        except:
            messagebox.showerror("Error", "Invalid input!")

    def update_notes(self):
        """Update the notes panel with prime selection instructions and RSA explanation."""
        notes = """=== Prime Selection ===

    RSA relies on two large prime numbers, p and q:
    - Primes must be:
    - Whole numbers >1.
    - Divisible only by 1 and themselves.

    === Example ===
    Let p = 3 and q = 11:
    - n = p × q = 3 × 11 = 33.
    - φ(n) = (p-1)(q-1) = 2 × 10 = 20.

    === Why Primes? ===
    - Primes ensure n is hard to factorize.
    - Larger primes increase security."""
        self.controller.update_notes(notes)

class KeyFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Key Generation", font=("Helvetica", 14))
        label.pack(pady=10)
        
        self.info_frame = ttk.Frame(self)
        self.info_frame.pack(pady=10)
        
        # Labels to display n and phi(n)
        self.n_label = ttk.Label(self.info_frame, text="")
        self.n_label.pack()
        
        self.phi_label = ttk.Label(self.info_frame, text="")
        self.phi_label.pack()
        
        e_frame = ttk.Frame(self)
        e_frame.pack(pady=10)
        
        ttk.Label(e_frame, text="Select public exponent e:").pack()
        self.e_var = tk.IntVar()
        self.e_menu = ttk.Combobox(e_frame, textvariable=self.e_var)
        self.e_menu.pack()
        
        generate_btn = ttk.Button(self, text="Generate Keys", command=self.generate)
        generate_btn.pack(pady=10)

    def update_display(self):
        """Update the display with the current values of p, q, n, and phi."""
        self.n_label.config(text=f"n = {self.controller.p} × {self.controller.q} = {self.controller.n}")
        self.phi_label.config(text=f"φ(n) = ({self.controller.p}-1)({self.controller.q}-1) = {self.controller.phi}")

    def generate(self):
        """Generate the public and private keys."""
        if self.controller.generate_keys(self.e_var.get()):
            messagebox.showinfo("Success", f"Private key d = {self.controller.d}")

    def update_notes(self):
        """Update the notes panel with key generation instructions and RSA explanation."""
        # Update the display with the current values of p, q, n, and phi
        self.update_display()
        
        # Populate the dropdown with valid e values
        valid_e = [e for e in [3, 5, 7, 11, 17, 257, 65537] if math.gcd(e, self.controller.phi) == 1]
        self.e_menu['values'] = valid_e
        if valid_e:
            self.e_menu.current(0)  # Set the first valid e as the default selection
        else:
            messagebox.showerror("Error", "No valid e found!")

        # Update the notes panel
        notes = """=== Key Generation ===

    1. Compute n = p × q.
    2. Compute φ(n) = (p-1)(q-1).
    3. Choose public exponent e:
    - Must be coprime with φ(n).
    - Common choices: 3, 5, 17, 65537.
    4. Compute private key d:
    - d = e⁻¹ mod φ(n).

    === Example ===
    If p = 3, q = 11:
    - n = 3 × 11 = 33.
    - φ(n) = 2 × 10 = 20.
    - Choose e = 3 (valid since gcd(3, 20) = 1, Otherwise invalid 1 < value & value > 1).
    - Compute d = 7 (since 3 × 7 mod 20 = 1).

    === Options ===
    • Select e from dropdown.
    • Click Generate to continue."""
        self.controller.update_notes(notes)

class EncryptFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Message Encryption", font=("Helvetica", 14))
        label.pack(pady=10)
        
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Enter message:").pack()
        self.message_entry = ttk.Entry(input_frame, width=40)
        self.message_entry.pack()
        
        encrypt_btn = ttk.Button(self, text="Encrypt", command=self.encrypt)
        encrypt_btn.pack(pady=10)

    def encrypt(self):
        """Encrypt the message using the public key."""
        message = self.message_entry.get()

        if message:
            if self.controller.encrypt_message(message):
                messagebox.showinfo("Encrypted", f"Encrypted message: {' '.join(map(str, self.controller.encrypted))}")

    def update_notes(self):
        """Update the notes panel with encryption instructions and RSA explanation."""
        notes = """=== Encryption ===

    1. Convert message to numbers (e.g., ASCII).
    2. Encrypt each number: c = m^e mod n.

    === Example ===
    If e = 3, n = 33:
    - Message "A" → ASCII 65.
    - Encrypted: 65³ mod 33 = 32.

    === Why Modular Arithmetic? ===
    - Keeps numbers manageable.
    - Ensures reversibility with private key.

    === Options ===
    • Enter text to encrypt.
    • Click Encrypt when ready."""
        self.controller.update_notes(notes)

class DecryptFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Message Decryption", font=("Helvetica", 14))
        label.pack(pady=10)
        
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Enter private key d:").pack()
        self.d_entry = ttk.Entry(input_frame)
        self.d_entry.pack()
        
        decrypt_btn = ttk.Button(self, text="Decrypt", command=self.decrypt)
        decrypt_btn.pack(pady=10)

    def decrypt(self):
        """Decrypt the message using the private key."""
        try:
            d = int(self.d_entry.get())
            decrypted = self.controller.decrypt_message(d)
            if decrypted:
                messagebox.showinfo("Decrypted", f"Decrypted message: {decrypted}")
                self.controller.save_to_leaderboard()
                self.controller.show_frame(LeaderboardFrame)
        except:
            messagebox.showerror("Error", "Invalid decryption!")

    def update_notes(self):
        """Update the notes panel with decryption instructions and RSA explanation."""
        notes = """=== Decryption ===

    1. Decrypt each number: m = c^d mod n.
    2. Convert numbers back to text (e.g., ASCII).

    === Example ===
    If d = 7, n = 33:
    - Encrypted: 32.
    - Decrypted: 32⁷ mod 33 = 65 → "A".

    === Why Does It Work? ===
    - Euler's theorem ensures m^(e×d) ≡ m mod n.
    - Private key d reverses the encryption.

    === Options ===
    • Enter private key d.
    • Click Decrypt to verify."""
        self.controller.update_notes(notes)

class LeaderboardFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Leaderboard", font=("Helvetica", 14))
        label.pack(pady=10)
        
        self.leaderboard_text = tk.Text(self, height=10, width=50)
        self.leaderboard_text.pack(pady=10)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Play Again", 
                 command=lambda: controller.show_frame(StartFrame)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Main Menu", 
                 command=lambda: controller.show_frame(StartFrame)).pack(side=tk.LEFT, padx=5)
        
        self.load_leaderboard()
        self.start_periodic_refresh()
        
    def load_leaderboard(self):
        """Load and display leaderboard entries."""
        try:
            leaderboard = self.controller.load_leaderboard()
            self.leaderboard_text.delete(1.0, tk.END)
            
            if not leaderboard:
                self.leaderboard_text.insert(tk.END, "No scores yet. Play a game to see your score here!")
            else:
                for idx, entry in enumerate(leaderboard[:10], 1):
                    # Handle missing 'difficulty' key
                    difficulty = entry.get("difficulty", "Unknown")
                    self.leaderboard_text.insert(tk.END, 
                        f"{idx}. {entry['name']}: {entry['time']:.2f}s ({difficulty})\n")
        except Exception as e:
            messagebox.showerror("Error", f"Leaderboard error: {str(e)}")

    def start_periodic_refresh(self):
        """Start periodic refresh of the leaderboard."""
        self.load_leaderboard()
        self.after(3000, self.start_periodic_refresh)  # Refresh every 3 seconds

    def update_notes(self):
        """Update notes panel with leaderboard help and RSA summary."""
        notes = """=== RSA Summary ===

    1. Key Generation:
    - Choose primes p and q.
    - Compute n = p × q and φ(n) = (p-1)(q-1).
    - Choose e and compute d = e⁻¹ mod φ(n).

    2. Encryption:
    - c = m^e mod n.

    3. Decryption:
    - m = c^d mod n.

    === Leaderboard ===
    Scores sorted by:
    1. Completion time.
    2. Difficulty level.

    === Options ===
    • Play Again: Restart game.
    • Main Menu: Return to start."""
        self.controller.update_notes(notes)