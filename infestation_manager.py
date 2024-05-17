from cryptography.fernet import Fernet
import base64
from aes import AESCipher

def annoyingBug(roach, mode, config):
    majorRoach = ""

    if mode == 1:
        majorRoach = config["ROACH_PRINCE"]
    elif mode == 2:
        majorRoach = config["ROACH_QUEEN"]
    elif mode == 3:
        majorRoach = config["ROACH_KING"]
    
    # fernet = Fernet(base64.urlsafe_b64encode(config["YABADABADOO"].encode('utf-8')))
    aes = AESCipher(config["YABADABADOO"], config["MUTATION"])
    
    annoyingBug = roach + majorRoach
    print(annoyingBug.encode())
    encrypted = aes.encrypt(annoyingBug.encode())
    
    return encrypted

def bugSpray(annoyingRoach, mode, config):
    majorRoach = ""

    if mode == 1:
        majorRoach = config["ROACH_PRINCE"]
    elif mode == 2:
        majorRoach = config["ROACH_QUEEN"]
    elif mode == 3:
        majorRoach = config["ROACH_KING"]
    
    aes = AESCipher(config["YABADABADOO"], config["MUTATION"])
    decrypted = aes.decrypt(annoyingRoach)
    decrypted.replace(majorRoach, "")

    return decrypted