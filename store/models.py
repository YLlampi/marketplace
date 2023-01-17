from django.db import models
from django.contrib.auth.models import User
from django.core.files import File

from io import BytesIO
from PIL import Image

from userprofile.models import UserProfile, Department


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    DEPARTAMENTOS_CHOICES = (
        ('AMAZONAS', 'Amazonas'),
        ('ANCASH', 'Áncash'),
        ('APURIMAC', 'Apurímac'),
        ('AREQUIPA', 'Arequipa'),
        ('AYACUCHO', 'Ayacucho'),
        ('CAJAMARCA', 'Cajamarca'),
        ('CALLAO', 'Callao'),
        ('CUSCO', 'Cusco'),
        ('HUANCAVELICA', 'Huancavelica'),
        ('HUANUCO', 'Huánuco'),
        ('ICA', 'Ica'),
        ('JUNIN', 'Junín'),
        ('LA_LIBERTAD', 'La Libertad'),
        ('LAMBAYEQUE', 'Lambayeque'),
        ('LIMA', 'Lima'),
        ('LORETO', 'Loreto'),
        ('MADRE_DE_DIOS', 'Madre de Dios'),
        ('MOQUEGUA', 'Moquegua'),
        ('PASCO', 'Pasco'),
        ('PIURA', 'Piura'),
        ('PUNO', 'Puno'),
        ('SAN_MARTIN', 'San Martín'),
        ('TACNA', 'Tacna'),
        ('TUMBES', 'Tumbes'),
        ('UCAYALI', 'Ucayali')
    )

    DISPONIBLE = 'disponible'
    AGOTADO = 'agotado'

    STATUS_CHOICES = (
        (DISPONIBLE, 'Disponible'),
        (AGOTADO, 'Agotado'),
    )

    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    departamento = models.CharField('Departamento', max_length=15, choices=DEPARTAMENTOS_CHOICES, default='AREQUIPA',
                                    null=True)
    # departamento = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    title = models.CharField('Nombre', max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField('Descripción', blank=True)
    price = models.DecimalField('Precio', max_digits=6, decimal_places=2)
    quantity = models.IntegerField('Cantidad', null=True)
    is_new = models.BooleanField('Es nuevo?', default=True, null=True)

    image = models.ImageField('Imagen 1', upload_to='uploads/product_images/%Y/%m/%d/', blank=True, null=True)
    image_two = models.ImageField('Imagen 2', upload_to='uploads/product_images/%Y/%m/%d/', blank=True, null=True)
    image_three = models.ImageField('Imagen 3', upload_to='uploads/product_images/%Y/%m/%d/', blank=True, null=True)

    thumbnail = models.ImageField(upload_to='uploads/product_images/thumbnail/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=DISPONIBLE)

    class Meta:
        ordering = ('-created_at',)

    def get_display_price(self):
        temp_price = str(self.price).replace(',', '.')
        return temp_price

    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        name = image.name.replace('uploads/product_images/', '')

        thumbnail = File(thumb_io, name=name)

        return thumbnail

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'

    def get_image_url(self):
        if self.image:
            return self.image.url
        else:
            return 'https://via.placeholder.com/240x240x.jpg'

    def get_image_two_url(self):
        if self.image_two:
            return self.image_two.url
        else:
            return 'https://via.placeholder.com/240x240x.jpg'

    def get_image_three_url(self):
        if self.image_three:
            return self.image_three.url
        else:
            return 'https://via.placeholder.com/240x240x.jpg'

    def __str__(self):
        return self.title


class Order(models.Model):
    first_name = models.CharField('Nombre', max_length=255)
    last_name = models.CharField('Apellido', max_length=255)
    address = models.CharField('Direccion', max_length=255)
    zipcode = models.CharField('Código postal', max_length=255, blank=True, null=True)
    city = models.CharField('Ciudad', max_length=255)
    paid_amount = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    merchant_id = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)

    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def get_display_price(self):
        return self.price / 100

    def __str__(self):
        return f'Orden {self.order.id} - {self.product.title}'
