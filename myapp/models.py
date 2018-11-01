from django.db import models

# Create your models here.

class ledger(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.IntegerField();
	file_name  = models.CharField(max_length=50) 
	file_extension = models.CharField(max_length=50)
	file_type = models.CharField(max_length=50)
	file_hash = models.CharField(max_length=150)
	url = models.CharField(max_length=150)
	file_status = models.BooleanField()
	pin_status = models.BooleanField()

