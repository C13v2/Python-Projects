import secrets  # For cryptographic random password generation
import string   # For character sets (uppercase, lowercase, digits, symbols)
import math     # For entropy calculation

def generate_password(length=12):
    """Generates a secure password of a given length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def calculate_entropy(password):
    """Calculates entropy (bits of security) for a given password."""
    char_pool = 0
    if any(c.islower() for c in password):
        char_pool += 26  # Lowercase letters
    if any(c.isupper() for c in password):
        char_pool += 26  # Uppercase letters
    if any(c.isdigit() for c in password):
        char_pool += 10  # Digits
    if any(c in string.punctuation for c in password):
        char_pool += len(string.punctuation)  # Special characters
    
    entropy = math.log2(char_pool ** len(password))
    return entropy

if __name__ == "__main__":
    print("===== Secure Password Generator =====")
    
    while True:
        length = int(input("Enter desired password length: "))
        
        password = generate_password(length)
        entropy = calculate_entropy(password)

        print(f"\nGenerated Password: {password}")
        print(f"Password Entropy: {entropy:.2f} bits")

        if entropy < 50:
            print("⚠️ Weak password! Consider using more characters.")
        elif entropy < 80:
            print("✅ Moderate password. Could be stronger.")
        else:
            print("🔒 Strong password! Very secure.")
        
        user_choice = input("Are you happy with this password? (yes/no): ").strip().lower()
        if user_choice == 'yes':
            print("✅ Password finalized.")
            break
        else:
            print("🔄 Generating a new password...\n")