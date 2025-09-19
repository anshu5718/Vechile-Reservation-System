from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random

class User_profile(AbstractUser):
    USER_TYPE = [
        ('customer', 'customer'),
        ('driver', 'driver'),
        ('admin', 'admin')
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE, default='customer')

    def __str__(self):
        return self.username


class OTP(models.Model):
    user = models.ForeignKey(User_profile, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'otp')

    @staticmethod
    def otp_generator(email, length=6):
        user = User_profile.objects.filter(email=email).first()
        if user is None:
            raise Exception("User doesn’t exist")
        
        for _ in range(3):
            otp = "".join([str(random.randint(0, 9)) for _ in range(length)])
            if not OTP.objects.filter(otp=otp).exists():
                break
        
        # Delete old OTPs
        OTP.objects.filter(user=user).delete()

        new_otp = OTP(user=user, otp=otp)
        new_otp.save()
        return new_otp

    def is_expired(self):
        now = timezone.now()
        return now - self.created_at > datetime.timedelta(minutes=5)

    @staticmethod
    def check_otp(otp):
        otp_record = OTP.objects.filter(otp=otp).first()
        if otp_record and not otp_record.is_expired():
            user_id = otp_record.user.id
            otp_record.delete()
            return user_id
        return None

    def __str__(self):
        return self.otp
