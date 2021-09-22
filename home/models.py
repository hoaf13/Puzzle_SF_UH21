from django.db import models

# Create your models here.

class Conversation(models.Model):
    _id = models.CharField(max_length=100)
    create_time = models.CharField(max_length=100)
    booking_status = models.CharField(max_length=100)
    """
    :success: đặt lịch thành công  
    :foward: chuyển máy tới nhân viên 
    :error: cuộc gọi bị lỗi (server lỗi)
    :abort: khách hàng bỏ dở giữa chừng
    """
    end_time = models.CharField(max_length=100)
    

class QApair(models.Model):
    create_time_bot_message = models.CharField(max_length=100, null=True)
    create_time_client_message = models.CharField(max_length=100, null=True)
    action = models.TextField(max_length=100)
    bot_message = models.TextField(max_length=1000)
    intent = models.TextField(max_length=100)
    client_message = models.TextField(max_length=1000)  
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)


    