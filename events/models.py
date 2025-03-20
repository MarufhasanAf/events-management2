from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name    
    
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    LOCATION_CHOICES = [
        ('DHAKA', 'Dhaka'),
        ('CHITTAGONG', 'Chittagong'),
        ('KHULNA', 'Khulna'),
        ('RAJSHAHI', 'Rajshahi'),
        ('BARISAL', 'Barisal'),
        ('SYLHET', 'Sylhet'),
        ('RANGPUR', 'Rangpur'),
        ('MYMENSINGH', 'Mymensingh'),
    ]
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.name
    
class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    events = models.ManyToManyField(Event, related_name='participants')

    def __str__(self):
        return self.name

