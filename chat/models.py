from django.db import models
from django.conf import settings

# Create your models here.
class Message(models.Model):
	author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	content=models.TextField()
	timestamp=models.DateTimeField(auto_now_add=True)


	def last_10_messages(self):
		return Message.objects.order_by('-timestamp').all()[:10]


class Contact(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username



class Chat(models.Model):
    participants = models.ManyToManyField(
        Contact, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return "{}".format(self.pk)