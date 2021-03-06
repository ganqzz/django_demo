from django.contrib.auth.models import User
from django.db import models


class Thread(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)

    def get_latest_date(self):
        if self.reply_set.count() > 0:
            return self.reply_set.latest('date_created').date_created

        return self.date_created

    def __str__(self):
        return f'{self.title}'


class Reply(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateField(auto_now_add=True)
