from django.db             import models
from persons.models        import Person
from socialnetworks.models import Socialnetwork

# Create your models here.

class Client(Person):
    gender = models.CharField("Gênero", max_length = 1, choices = [
        ("M", "Masculino"),
        ("F", "Feminino"),
        ("O", "Outro"),
    ])
    socialnetwork = models.ManyToManyField(Socialnetwork, verbose_name = "Redes Sociais")

    class Meta:
        verbose_name        = "Cliente"
        verbose_name_plural = "Clientes"
        ordering            = [ "id" ]

    def __str__(self):
        return super().__str__()
