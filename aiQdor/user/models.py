from django.db import models

# Importação para modelo de usuário
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# ------------------------------------------------------------------------- #
                 # Classes necessárias para tratar um usuario
# ------------------------------------------------------------------------- #

class PacienteManager(BaseUserManager):
    def create_user(self, email, nome, CPF, endereco, dataNascimento, celular, password=None):    
        """
        	Cria um usuario do sistema, espeficiado como paciente
        """
        if (not email) or (not CPF)  or (not endereco) or (not dataNascimento) or (not celular):
            raise ValueError('Um Paciente precisa conter todos os campos')

        user = self.model(
            email=self.normalize_email(email),
            nome = nome,
            CPF = CPF,
            endereco = endereco,
            dataNascimento = dataNascimento,
            celular = celular
        )	

        user.set_password(password)
        user.save(using=self._db)

        return user	


    def create_superuser(self, nome, email, CPF, endereco, dataNascimento, celular, password):
        """
            Cria um superusuario
        """

        user = self.create_user(
            email,
            nome=nome,
            CPF = CPF,
            endereco = endereco,
            dataNascimento= dataNascimento,
            celular= celular,
            password=password
        )	

        user.is_admin= True
        user.save(using=self._db)

        return user

class Paciente(AbstractBaseUser):
    # dados
    email = models.EmailField(verbose_name='endreço de email', max_length=50, unique=True)
    CPF = models.CharField(max_length=14, unique=True)
    nome = models.CharField(verbose_name='Nome Completo', max_length=40)
    endereco = models.CharField(verbose_name='Endreço', max_length=40)
    celular = models.CharField(max_length=40)
    dataNascimento = models.DateField(verbose_name='Data de Nascimento')

    # necessário par ser padrão do Django
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)


    objects = PacienteManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['CPF', 'nome', 'endereco', 'dataNascimento', 'celular']

    def __str__(self):
    	return f'{self.nome}'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Este usuário é um secretario?"
        # Simplest possible answer: All admins are staff
        return self.is_admin	
