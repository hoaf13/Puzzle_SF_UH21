from django.db import models

# Create your models here.

class IntentAction(models.Model):
    session_id = models.TextField(max_length=100)
    room_id = models.TextField(max_length=100)
    at_time = models.DateTimeField(auto_created=True)    
    intent = models.TextField(max_length=100)
    action = models.TextField(max_length=100)
    bot_message = models.TextField(max_length=1000)
    client_message = models.TextField(max_length=1000)  
    
    