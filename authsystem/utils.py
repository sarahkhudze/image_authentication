from cryptography.fernet import Fernet
import hashlib
import rsa
import base64
from PIL import Image
from PIL.ExifTags import TAGS
import io

def extract_exif(image):
    """Extract EXIF metadata from image"""
    try:
        img = Image.open(image)
        exif_data = img._getexif()
        if exif_data:
            return {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
        return None
    except (AttributeError, IOError, KeyError):
        return None

def calculate_hash(image_file):
    """Calculate SHA-256 hash of an image file"""
    sha256 = hashlib.sha256()
    for chunk in image_file.chunks():
        sha256.update(chunk)
    return sha256.hexdigest()


def encrypt_image(image_file, public_key):
    """Hybrid encryption using AES for image and RSA for key"""
    try:
        # Generate a random AES key
        aes_key = Fernet.generate_key()
        cipher_suite = Fernet(aes_key)
        
        # Read image data
        image_data = b''.join([chunk for chunk in image_file.chunks()])
        
        # Encrypt image with AES
        encrypted_image = cipher_suite.encrypt(image_data)
        
        # Encrypt AES key with RSA
        encrypted_key = rsa.encrypt(aes_key, public_key)
        
        # Combine and base64 encode
        combined = encrypted_key + b'||SEP||' + encrypted_image
        return base64.b64encode(combined)
    
    except Exception as e:
        print(f"Encryption error: {str(e)}")
        raise

def decrypt_image(encrypted_data, private_key):
    """Hybrid decryption of image data"""
    try:
        # Base64 decode
        data = base64.b64decode(encrypted_data)
        
        # Split components
        encrypted_key, encrypted_image = data.split(b'||SEP||')
        
        # Decrypt AES key with RSA
        aes_key = rsa.decrypt(encrypted_key, private_key)
        
        # Decrypt image with AES
        cipher_suite = Fernet(aes_key)
        return cipher_suite.decrypt(encrypted_image)
    
    except Exception as e:
        print(f"Decryption error: {str(e)}")
        return None


#Image Verification
def verify_image(encrypted_data, original_hash, public_key):
    decrypted_data = decrypt_image(encrypted_data, public_key)
    if decrypted_data is None:
        return False
    
    sha256_hash = hashlib.sha256(decrypted_data).hexdigest()
    return sha256_hash == original_hash
