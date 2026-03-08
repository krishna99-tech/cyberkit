from zxcvbn import zxcvbn
from getpass import getpass
import bcrypt


def check_strength(password):
    result = zxcvbn(password)
    score = result['score']
    if score == 3:
        response = "Your password is strong."
    elif score == 4:
        response = "Your password is very strong."
    else:
        feedback = result.get('feedback', {})
        warning = feedback.get('warning', 'Your password is weak.')
        suggestions = feedback.get('suggestions', [])
        response = f"{warning} Suggestions: {' '.join(suggestions)}"
        response += " Consider using a mix of uppercase letters, lowercase letters, numbers, and special characters."
        for suggestion in suggestions:
            response += " " + suggestion
    return response

def hash_pw(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def verify_password(password, hashed):
    if bcrypt.checkpw(password.encode(), hashed):
       return "Password is correct. Access granted."
    else:
         return "Password is incorrect. Access denied."



if __name__ == "__main__":
    while True:
        password1 = getpass("Enter your password: ")
        print(check_strength(password1))
        if check_strength(password1).startswith("Weak"):
            print("Please choose a stronger password.")
        else:
            break
    hash_password = hash_pw(password1)
    print(f"Hashed password: {hash_password}")
    attempt = getpass("Re-enter your password to verify: ")
    print(verify_password(attempt, hash_password))