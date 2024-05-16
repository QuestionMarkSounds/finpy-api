from cryptography.fernet import Fernet

def annoyingBug(roach, mode, config):
    majorRoach = ""

    if mode == 1:
        majorRoach = config["ROACH_PRINCE"]
    elif mode == 2:
        majorRoach = config["ROACH_QUEEN"]
    elif mode == 3:
        majorRoach = config["ROACH_KING"]
    
    fernet = Fernet(config["YABADABADOO"])
    annoyingBug = roach + majorRoach
    encrypted = fernet.encrypt(annoyingBug)
    
    return encrypted

def bugSpray(annoyingRoach, mode, config):
    majorRoach = ""

    if mode == 1:
        majorRoach = config["ROACH_PRINCE"]
    elif mode == 2:
        majorRoach = config["ROACH_QUEEN"]
    elif mode == 3:
        majorRoach = config["ROACH_KING"]
    
    fernet = Fernet(config["YABADABADOO"])
    decrypted = fernet.decrypt(annoyingRoach).decode()
    decrypted.replace(majorRoach, "")

    return decrypted