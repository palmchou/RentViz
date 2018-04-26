from django.db import models


class Community(models.Model):
    comm_code = models.CharField(max_length=32, db_index=True, unique=True)
    custom_name = models.CharField(max_length=32, default='')

    def __str__(self):
        if self.custom_name:
            return self.custom_name
        else:
            return self.comm_code
