from django.db import models
from accounts.models import TimeStamp
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Tawjihi(models.Model):
    COURSE_CATEGORY_CHOICES = (
        ('Bac', 'Bac'),
        ('Jihawi', 'Jihawi'),
        ('Tawjih', 'Tawjih'),
        ('Concours', 'Concours')
    )
    
    course_categroy = models.CharField(choices=COURSE_CATEGORY_CHOICES, max_length=20, null=True, blank=True)
    title = models.CharField(max_length=50)
    price = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.title} ({self.price}) dhs'

    
class Reservation(TimeStamp):
    STATUS = (
        ('Paid', _('Paid')),
        ('Canceled',_('Canceled')),
        ('Waiting', _('Waiting'))
    )

    name = models.CharField(max_length=220)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    field_of_Study = models.CharField(max_length=100)
    tawgihi = models.ForeignKey(Tawjihi, on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=STATUS, default='Waiting')
    contacted = models.BooleanField(default=False)
    