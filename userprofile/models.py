from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Department(models.Model):
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
        ('LA LIBERTAD', 'La Libertad'),
        ('LAMBAYEQUE', 'Lambayeque'),
        ('LIMA', 'Lima'),
        ('LORETO', 'Loreto'),
        ('MADRE DE DIOS', 'Madre de Dios'),
        ('MOQUEGUA', 'Moquegua'),
        ('PASCO', 'Pasco'),
        ('PIURA', 'Piura'),
        ('PUNO', 'Puno'),
        ('SAN MARTIN', 'San Martín'),
        ('TACNA', 'Tacna'),
        ('TUMBES', 'Tumbes'),
        ('UCAYALI', 'Ucayali')
    )
    title = models.CharField('', max_length=50, choices=DEPARTAMENTOS_CHOICES, null=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
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
        ('LA LIBERTAD', 'La Libertad'),
        ('LAMBAYEQUE', 'Lambayeque'),
        ('LIMA', 'Lima'),
        ('LORETO', 'Loreto'),
        ('MADRE DE DIOS', 'Madre de Dios'),
        ('MOQUEGUA', 'Moquegua'),
        ('PASCO', 'Pasco'),
        ('PIURA', 'Piura'),
        ('PUNO', 'Puno'),
        ('SAN MARTIN', 'San Martín'),
        ('TACNA', 'Tacna'),
        ('TUMBES', 'Tumbes'),
        ('UCAYALI', 'Ucayali')
    )

    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    first_name = models.CharField('Nombres', max_length=150, null=True)
    last_name = models.CharField('Apellidos', max_length=150, null=True)
    num_whatsapp = models.CharField('WhatsApp', max_length=9, null=True)

    departamento = models.CharField('Departamento', max_length=15, choices=DEPARTAMENTOS_CHOICES, default='AREQUIPA', null=True)
    #departamento = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)


    is_vendor = models.BooleanField('Es vendedor?', default=False)


    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.user.username
