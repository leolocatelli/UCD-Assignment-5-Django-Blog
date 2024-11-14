from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        # Define a altura máxima desejada
        max_height = 300
        if img.height > max_height:
            # Calcula a nova largura proporcional
            new_height = max_height
            new_width = int((max_height / img.height) * img.width)
            img = img.resize((new_width, new_height), Image.LANCZOS)
            img.save(self.image.path)
