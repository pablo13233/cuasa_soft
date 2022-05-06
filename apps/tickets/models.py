from django.db import models

# Create your models here.

def format_time_spent(time_spent):
    if time_spent:
        time_spent = "{0:02d}h:{1:02d}m".format(
            time_spent.seconds // 3600,
            time_spent.seconds % 3600 // 60
        )
    else:
        time_spent = ""
    return time_spent

class Cola(models.Model):
    titulo = models.CharField(max_length=100)
    