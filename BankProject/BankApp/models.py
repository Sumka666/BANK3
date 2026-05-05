from django.db import models


class User(models.Model):
    account_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    passwordhash = models.CharField(max_length=64)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.email})"