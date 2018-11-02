from django.db import models

class ipfs_details(models.Model):
    User_ID = models.CharField(max_length=250)
    File_Name = models.CharField(max_length=250)
    File_Size = models.CharField(max_length=250)
    File_Hash = models.CharField(max_length=250)
    URL = models.CharField(max_length=250)
    File_Status = models.CharField(max_length=250)
    Pin_Status = models.CharField(max_length=250)
