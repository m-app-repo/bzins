import socket
import platform
import uuid
from hashlib import sha256
from cryptography.fernet import Fernet
from getmac import get_mac_address
from base64 import urlsafe_b64encode
import base64
import logging
import os

# Configure logging
# Create a log file path with the same name as the Python file and a .log extension
log_file_path = os.path.splitext(__file__)[0] + ".log"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(filename)s:%(lineno)s - %(funcName)20s() ] - %(levelname)s - %(message)s', filename=log_file_path)
FORMAT = " %(message)s"

# def pad_token(token):
#     if isinstance(token, str):
#         token = token.encode('utf-8')
#     return token + b'=' * (4 - len(token) % 4)

def pad_token(token):
    if isinstance(token, str):
        token = token.encode('utf-8')
    padded_token = token + b'=' * (4 - len(token) % 4)
    logging.info("Padded token: %s", padded_token)
    return padded_token

def get_system_identifier():
    # Collect system-specific informationcls
    mac_address = get_mac_address()
    system_name = platform.system()
    processor = platform.processor()
    machine_id = uuid.getnode()
    # Create a combined string of system information
    system_info = f"{mac_address}{system_name}{processor}{machine_id}"
    return system_info

def create_encryption_key(user_input):
    try:
        #print(user_input)
        # Combine system info with user input and hash them
        system_info = get_system_identifier()
        if isinstance(user_input, bytes):
            user_input = user_input.decode('utf-8')
        if system_info is None:
            system_info = ""
        if user_input is None:
            user_input = ""
        combined_info = (system_info + user_input).encode()
        hashed_info = sha256(combined_info).digest()
        # Encode the hashed info to create a valid Fernet key
        fernet_key = urlsafe_b64encode(hashed_info)
        return fernet_key
    except Exception as e:
        logging.error("Error occurred during key creation: %s", str(e), exc_info=True)
        return None

def encrypt_data(str_key, usr_slt):
    try:
        key_slt = create_encryption_key(usr_slt)
        fernet = Fernet(key_slt)
        if not isinstance(str_key, bytes):
            str_key = str_key.encode('utf-8')
        encrypted_data = fernet.encrypt(str_key)
        return encrypted_data
    except Exception as e:
        logging.error("Error occurred during encryption: %s", str(e), exc_info=True)
        return None

# def decrypt_data(str_key, usr_slt):
#     try:
#         logging.info("str_key: %s", str_key)
#         key_slt = create_encryption_key(usr_slt)
#         logging.info("key_slt: %s", key_slt) 
#         fernet = Fernet(key_slt)
#         logging.info("fernet: %s", fernet)    
#         if not isinstance(str_key, bytes):
#             byt_key = bytes(str_key, 'utf-8')
#             logging.info("str_key is not bytes - hence converting")
#         else:
#             byt_key = str_key
#             logging.info("str_key is bytes")
#         decrypted_data = None
#         try:
#             if byt_key:
#                 logging.info("byt_key: %s", byt_key)
#                 decrypted_data = fernet.decrypt(pad_token(byt_key))
#                 logging.info("decryptedstr_key: %s", decrypted_data)
#             else:
#                 logging.error("Empty or None value provided for decryption.")
#         except Exception as e:
#             logging.error("1Error occurred during decryption: %s", str(e))
#         return decrypted_data
#     except Exception as e:
#         logging.error("2Error occurred during decryption2: %s", str(e))
#         return None
    lap_key = seckey.decrypt_data(str_key=seckey.pad_token(lap_key), usr_slt=usr_slt)
def decrypt_data(str_key, usr_slt):
    try:
        logging.info("str_key: %s", str_key)
        key_slt = create_encryption_key(usr_slt)
        logging.info("key_slt: %s", key_slt) 
        fernet = Fernet(key_slt)
        logging.info("fernet: %s", fernet)    

        if not isinstance(str_key, bytes):
            byt_key = bytes(str_key, 'utf-8')
            logging.info("str_key is not bytes - hence converting")
        else:
            byt_key = str_key
            logging.info("str_key is bytes")

        decrypted_data = None
        try:
            if byt_key:
                logging.info("byt_key: %s", byt_key)
                padded_key = (byt_key)
                decrypted_data = fernet.decrypt(padded_key)
                logging.info("decryptedstr_key: %s", decrypted_data)
            else:
                logging.error("Empty or None value provided for decryption.")
        except Exception as e:
            logging.error("Error occurred during decryption: %s", str(e))
        return decrypted_data
    except Exception as e:
        logging.error("Error occurred during decryption: %s", str(e))
        return None


def setup_key():
    try:
        # Example Usage
        operation = input("Enter the operation (e for encryption or d for decryption): ")
        if operation.lower() == "e":
            user_input = input("Enter your passphrase: ")
            slt_key = create_encryption_key(user_input)
            api_key = input("Enter the API key: ")
            encrypted_api_key = encrypt_data(api_key, slt_key)
            if encrypted_api_key:
                logging.info("Encrypted API Key: %s", encrypted_api_key)
        elif operation.lower() == "d":
            user_input = input("Enter your passphrase: ")
            slt_key = create_encryption_key(user_input)
            en_api_key = input("Enter the encrypted API key: ")
            api_key = decrypt_data(en_api_key, slt_key)
            if api_key:
                logging.info("Decrypted API Key: %s", api_key)
        else:
            logging.error("Invalid operation.")
    except Exception as e:
        logging.error("Error occurred during setup: %s", str(e))
        
  

if __name__ == "__main__":
    setup_key()