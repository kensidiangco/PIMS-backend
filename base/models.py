from django.db import models

class Pouch(models.Model):
    
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]

    size = models.CharField(max_length=10, choices=SIZE_CHOICES, unique=True)
    quantity = models.IntegerField(default=0)
    date_updated = models.DateTimeField(auto_now=True)

class Pouch_In(models.Model):
    pouch = models.ForeignKey(Pouch, verbose_name=("pouch"), on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class Pouch_Out(models.Model):
    pouch = models.ForeignKey(Pouch, verbose_name=(""), on_delete=models.CASCADE)
    getter = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0, blank=True)
    purpose = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="Free")
    given = models.CharField(max_length=100)
    date_created = models.DateField()
    date_updated = models.DateTimeField(auto_now=True)