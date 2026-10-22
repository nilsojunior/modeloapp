from django.db         import models
from categories.models import Category

# Create your models here.
class Product(models.Model):
    id               = models.BigAutoField(primary_key = True)
    name             = models.CharField("Nome", max_length = 50)
    description      = models.TextField("Descrição", max_length = 200)
    fabrication_date = models.DateField("Data Fabricação", auto_now = False, auto_now_add = False)
    isactive         = models.BooleanField("Ativo", default = False)
    price            = models.DecimalField("Preço", max_digits = 10, decimal_places = 2, default = 0)
    photo            = models.ImageField("Foto", upload_to = "photos")
    doc              = models.FileField("Documentos", upload_to = "docs")
    category         = models.ForeignKey(Category, on_delete = models.CASCADE)

    class Meta:
        verbose_name        = "Produto"
        verbose_name_plural = "Produtos"
        ordering            = [ "id" ]

    def __str__(self):
        return f"{self.name}"
