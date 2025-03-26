from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import rsa
import base64
from django.contrib.auth.hashers import make_password



#User creation
class CustomUser(AbstractUser):
    telephone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        unique=True
    )
    id_number = models.CharField(max_length=20, unique=True)
    public_key = models.TextField(blank=True, null=True)
    private_key = models.TextField(blank=True, null=True)
    camera_make = models.CharField(max_length=100, blank=True, null=True)
    camera_model = models.CharField(max_length=100, blank=True, null=True)

    def generate_keys(self):
        """Generate RSA key pair and save as strings"""
        (pubkey, privkey) = rsa.newkeys(2048)  # Using 2048-bit keys now
        self.public_key = pubkey.save_pkcs1().decode('utf-8')
        self.private_key = privkey.save_pkcs1().decode('utf-8')
        self.save()

    def get_public_key(self):
        """Convert stored public key string back to RSA key object"""
        if not self.public_key:
            raise ValueError("No public key exists for this user")
        return rsa.PublicKey.load_pkcs1(self.public_key.encode('utf-8'))

    def get_private_key(self):
        """Convert stored private key string back to RSA key object"""
        if not self.private_key:
            raise ValueError("No private key exists for this user")
        return rsa.PrivateKey.load_pkcs1(self.private_key.encode('utf-8'))

    def save(self, *args, **kwargs):
        """Ensure keys are generated when new user is created"""
        if not self.pk and not self.public_key:  # New user
            self.generate_keys()
        super().save(*args, **kwargs)
        
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()
    
    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)


#User uploaded images
class UserImage(models.Model):
    VERIFICATION_CHOICES = [
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/')
    encrypted_image = models.BinaryField(blank=True, null=True)
    image_hash = models.CharField(max_length=64, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    camera_make = models.CharField(max_length=100, blank=True, null=True)
    camera_model = models.CharField(max_length=100, blank=True, null=True)
    verification_status = models.CharField(
        max_length=10,
        choices=VERIFICATION_CHOICES,
        default='pending'
    )
    verification_notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('user', 'image_hash')
    
    def get_decrypted_image(self):
        """Helper method to decrypt the image"""
        from .utils import decrypt_image
        if not self.encrypted_image or not self.user.private_key:
            return None
        return decrypt_image(self.encrypted_image, self.user.get_private_key())
