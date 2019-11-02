from django.db import models
from django.conf import settings

# Create your models here.
class Message(models.Model):
	author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	content=models.TextField()
	timestamp=models.DateTimeField(auto_now_add=True)


	def last_10_messages(self):
		return Message.objects.order_by('-timestamp').all()[:10]