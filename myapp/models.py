
from django.db import models
from django.db.models import Q
from django.urls.base import reverse

#Theatre


# Create your models here.
from django.contrib.auth import get_user_model
#from movie.models import Movie
from django.urls.base import reverse
User = get_user_model()

class Theatre(models.Model):
    city_choice=(
        ('DELHI','Delhi'),
        ('KOLKATA','Kolkata'),
        ('MUMBAI','Mumbai'),
        ('CHENNAI','Chennai'),
        ('BANGALORE','Bangalore'),
        ('HYDERABAD','Hyderabad')
    )
    name            =   models.CharField(max_length=50,null=False)
    city            =   models.CharField(max_length=9,choices=city_choice,null=False)
    address         =   models.CharField(max_length=30)
    no_of_screen    =   models.IntegerField()
    admin_id        =   models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name+"-"+self.address+"-"+self.city
    
    def get_absolute_url(self):
        return reverse('theatre:detail',kwargs={'theatre_id':self.pk})
    
class Show(models.Model):
    movie       =    models.ForeignKey('Movie',on_delete=models.SET_NULL,null=True,blank=True)
    theatre     =    models.ForeignKey('Theatre',on_delete=models.SET_NULL,null=True,blank=True)
    screen      =    models.IntegerField()
    date        =    models.DateField()
    time        =    models.TimeField()
    
    def __str__(self):
        return str(self.movie)+"-"+str(self.theatre)+"-"+str(self.date)+"-"+str(self.time)
    
























#home

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager




# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None,is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staffuser(self,email,password=None):
        user = self.create_user(
                email=email,
                password=password,
                is_staff = True
            )
        return user
    
    def create_superuser(self,email,password=None):
        user = self.create_user(
                email=email,
                password=password,
                is_staff=True,
                is_admin = True
            )
        return user

class User(AbstractBaseUser):
    email       =   models.EmailField(max_length=255,unique=True)
    active      =   models.BooleanField(default=True)
    staff       =   models.BooleanField(default=False)
    admin       =   models.BooleanField(default=False)
    timestamp   =   models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= []

    objects = UserManager()
    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_active(self):
        return self.active
    
    @property
    def is_admin(self):
        return self.admin

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True    















#Booking
from django.contrib.auth import get_user_model
# from theatre.models import Show
from django.urls import reverse
from django.db.models.signals import post_delete
User = get_user_model()
# Create your models here.


class Booking(models.Model):
    payment_choice = (
        ('Debit Card', 'Debit Card'),
        ('Credit Card', 'Credit Card'),
        ('Net Banking', 'Net Banking'),
        ('Wallet', 'Wallet'),
    )
    id                =     models.CharField(primary_key=True, max_length=200)
    timestamp         =     models.DateTimeField('%Y-%m-%d %H:%M:%S')
    payment_type      =     models.CharField(max_length=11, choices=payment_choice)
    paid_amount       =     models.DecimalField(max_digits=8, decimal_places=2)
    paid_by           =     models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.id)
    # def get_absolute_url(self):
    #     return reverse('booking:detail',kwargs={'btid':self.id})
    
    #def get_absolute_url(self):

class Seat(models.Model):
    seat_choice = (
        ('', 'Select'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
    )
    no              =       models.CharField(max_length=3)
    seat_type       =       models.CharField(max_length=8, choices=seat_choice, blank=False)
    show            =       models.ForeignKey(Show, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('no', 'show')

    def __str__(self):
        return self.no + str(self.show)


class BookedSeat(models.Model):
    seat            =       models.ForeignKey(Seat, on_delete=models.CASCADE)
    booking         =       models.ForeignKey(Booking, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('seat', 'booking')

    def __str__(self):
        return str(self.seat) + '|' + str(self.booking)


# def delete_reverse(sender,instance,*args,**kwargs):
#     try:
#         if instance.seat:
#             instance.seat.delete()
#     except:
#         pass

# post_delete.connect(delete_reverse,sender=BookedSeat)






























#Movie

class MovieQuerySet(models.query.QuerySet):
    def search(self,query):
        lookup = (
            Q(name__icontains=query)|
            Q(director__icontains=query)|
            Q(language__icontains=query)|
            Q(cast__icontains=query)
        )
        return self.filter(lookup).distinct()

class MovieManager(models.Manager):
    def get_queryset(self):
        return MovieQuerySet(self.model,self._db)
    def search(self,query):
        return self.get_queryset().search(query)


class Movie(models.Model):
    lang_choice=(
            ('ENGLISH','English'),
            ('BENGALI','Bengali'),
            ('HINDI','Hindi'),
            ('TAMIL','Tamil'),
            ('TELUGU','Telugu'),
            ('MALAYALAM','Malayalam'),
            ('MARATHI','Marathi'),
            ('FRENCH','French'),
        )
    rating_choice=(
            ('U','U'),
            ('UA','U/A'),
            ('A','A'),
            ('R','R'),
        )
    movie_id          =     models.IntegerField(primary_key=True)    
    name              =     models.CharField(max_length=20)
    cast              =     models.CharField(max_length=100)
    director          =     models.CharField(max_length=20)
    language          =     models.CharField(max_length=10,choices=lang_choice)
    run_length        =     models.IntegerField(help_text='Enter run length in minutes')
    certificate       =     models.CharField(max_length=2,choices=rating_choice)
    popularity_index  =     models.IntegerField(unique=True,null=True,blank=True)
    trailer           =     models.URLField(blank=True)    
    image             =     models.ImageField(blank=True, null=True,upload_to='images/')
    
    objects = MovieManager()
# Create your models here.












#mine
class user_table(models.Model):
    user_id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email =models.EmailField()
    mobile_no=models.BigIntegerField()
    password = models.CharField(max_length=50)

class feedback(models.Model):
    feed_id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email =models.EmailField()
    subject=models.CharField(max_length=50)
    message = models.CharField(max_length=150)

class admin(models.Model):
    admin_id= models.AutoField(primary_key=True)
    email =models.EmailField()
    password = models.CharField(max_length=50)



class add_movies(models.Model):  
    movie_id          =     models.IntegerField(primary_key=True)
    name              =     models.CharField(max_length=20)
    cast              =     models.CharField(max_length=100)
    director          =     models.CharField(max_length=20)
    language          =     models.CharField(max_length=10)
    run_length        =     models.IntegerField(help_text='Enter run length in minutes')
    screen_id         =     models.IntegerField(unique=True,null=True,blank=True)
    trailer           =     models.URLField(blank=True)
    image             =     models.ImageField(upload_to='images/')
    time              =     models.CharField(max_length=30)
    movie_desc        =     models.CharField(max_length=500)
    class Meta:
        unique_together = (('time', 'screen_id'),)