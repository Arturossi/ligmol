from django.db import models

# Create your models here.

class Complex(models.Model):
    length = 200

    # Fields
    id = models.IntegerField(primary_key=True)
    Complex = models.CharField(max_length=length, blank=False, null=False, default='unknown')
    host = models.CharField(max_length=length, blank=False, null=False, default='unknown')
    guest = models.CharField(max_length=length, blank=False, null=False, default='unknown')
    gbmodel = models.IntegerField()
    intdiel = models.IntegerField()
    saltcom = models.FloatField()
    average = models.CharField(max_length=length, blank=False, null=False, default='unknown')
    mmgbsa = models.FloatField()
    nma = models.FloatField()
    deltag = models.FloatField()
    exp = models.FloatField()
    challenge = models.CharField(max_length=length, blank=False, null=False, default='unknown')
  
    # Metadata
    class Meta:
        ordering = ('id', 'Complex', 'host', 'guest', 'gbmodel',
         'intdiel', 'saltcom', 'average', 'mmgbsa', 'nma', 'deltag', 'exp', 'challenge' ) 
         # helps in alphabetical listing. Sould be a tuple

    def __str__(self):
        # It is not a nice print but it is sort of readable (SORT OF)
        return ', '.join('{}{}'.format(key, val) for key, val in self.__dict__.items())