### **README File Explanation for Non-Technical Users**

Welcome to the **RSA Cryptography Game**! This game is designed to help you learn and understand how the RSA encryption algorithm works in a fun and interactive way. Below is a step-by-step guide on how to use the game.

---

### **1. What is the RSA Cryptography Game?**
The RSA Cryptography Game simulates the process of generating encryption keys, encrypting messages, and decrypting them using the RSA algorithm. You will:
- Choose two prime numbers.
- Generate public and private keys.
- Encrypt a message using the public key.
- Decrypt the message using the private key.

The game also tracks your performance and displays a leaderboard with the fastest completion times.

---

### **2. How to Play**

#### **Step 1: Download and Install**
1. Download the game files to your computer.
2. Ensure you have Python installed. If not, download and install Python from [python.org](https://www.python.org/).

#### **Step 2: Run the Game**
1. Open the folder where you downloaded the game files.
2. Double-click the file named `game_application.py` to start the game.

#### **Step 3: Enter Your Name**
- When the game starts, you will see a screen asking for your name.
- Type your name in the box and click **Start Game**.

#### **Step 4: Select Difficulty**
- Choose a difficulty level:
  - **Easy**: Use 2-digit prime numbers (e.g., 11, 13).
  - **Medium**: Use 3-digit prime numbers (e.g., 101, 103).
  - **Hard**: Use 4-digit prime numbers (e.g., 1009, 1013).

#### **Step 5: Enter Prime Numbers**
- Enter two prime numbers (`p` and `q`) based on the difficulty level you selected.
- Click **Validate Primes** to proceed.

#### **Step 6: Generate Keys**
- The game will compute values for `n` and `φ(n)`.
- Select a public exponent (`e`) from the dropdown menu and click **Generate Keys**.

#### **Step 7: Encrypt a Message**
- Type a message (e.g., "HELLO") in the text box.
- Click **Encrypt** to encrypt the message using the public key.

#### **Step 8: Decrypt the Message**
- Enter the private key (`d`) provided by the game.
- Click **Decrypt** to reveal the original message.

#### **Step 9: View Leaderboard**
- After decrypting the message, your score (time taken) will be saved.
- Click **View Leaderboard** to see the top 10 scores.

---

### **3. Directory for JSON File**
The leaderboard data is stored in a JSON file. If you need to change the directory where this file is saved, follow these steps:

1. Open the file named `game_application.py` in a text editor (e.g., Notepad).
2. Look for the following line in the code:
   ```python
   with open("C:/Users/user/Downloads/Rsa Game/JSON file/leaderboard.json", "w") as f:
   ```
3. Replace the path `"C:/Users/user/Downloads/Rsa Game/JSON file/leaderboard.json"` with the directory where you want to save the file. For example:
   ```python
   with open("C:/Your/Desired/Path/leaderboard.json", "w") as f:
   ```
4. Save the file and restart the game.
