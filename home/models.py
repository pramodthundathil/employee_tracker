from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Email field must be set')
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='email address')
    username = models.CharField(max_length=30, unique=True,verbose_name='username')
    first_name = models.CharField(max_length=30, blank=True, verbose_name='first name')
    last_name = models.CharField(max_length=30, blank=True, verbose_name='last name')
    phone = models.CharField(max_length=15, blank=True, verbose_name='phone number')
    address = models.TextField(blank=True, verbose_name='address')
    is_active = models.BooleanField(default=True, verbose_name='active')
    is_staff = models.BooleanField(default=False, verbose_name='staff status')
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    job_title = models.CharField(max_length=50, blank=True, verbose_name='job title', choices=(
                                                                                            ("Developer", "Developer"),
                                                                                            ("Designer", "Designer"),
                                                                                            ("Analyst", "Analyst"),
                                                                                            ("Tester", "Tester"),
                                                                                            ("Support", "Support"),
                                                                                            ("Manager", "Manager"),
                                                                                            ("Executive", "Executive"),
                                                                                            ("Senior Executive", "Senior Executive"),
                                                                                            ("Lead Developer", "Lead Developer"),
                                                                                            ("Junior Developer", "Junior Developer"),
                                                                                            ("Senior Developer", "Senior Developer"),
                                                                                            ("Intern", "Intern")))
    department = models.CharField(max_length=50, blank=True, verbose_name='department', choices=(
                                                                                            
                                                                                            ("HR", "Human Resources"),
                                                                                            ("IT", "Information Technology"),
                                                                                            ("FIN", "Finance"),
                                                                                            ("MKT", "Marketing"),
                                                                                            ("SALES", "Sales"),
                                                                                            ("ENG", "Engineering"),
                                                                                            ("ADMIN", "Administration"),
                                                                                        ))
    role = models.CharField(max_length=20, 
                            choices=(
                                ("employee","employee"),
                                ("manager","manager"),
                                ("admin","admin"),

                            ),
                            default='user'
                            )
    
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined')
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

        
    def __str__(self):
        return str(self.first_name + " " + self.last_name)
    


class Attendance(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="attendance")
    attendance_marked = models.BooleanField(default=False)
    attendance = models.CharField(max_length=20, choices=(("Present","Present"),("Absent","Absent")),null=True, blank=True)
    attendance_status = models.BooleanField(null=True, blank=True)
    in_date_time = models.DateTimeField(auto_now_add=True)
    out_date_time = models.DateTimeField(auto_now_add=True)
    approve = models.BooleanField(default=False)

class Messages_to_employees(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="messages")
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    approve = models.BooleanField(default=False)

class PublicMessages(models.Model):
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    approve = models.BooleanField(default=False)


class FeedBack(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="feedback")
    feedback = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    approve = models.BooleanField(default=False)

class Salaries(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="salaries")
    salary = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    month = models.CharField(max_length=20, choices=(("January","January"),("February","February"),("March","March"),("April","April"),("May","May"),("June","June"),("July","July"),("August","August"),("September","September"),("October","October"),("November","November"),("December","December")))
    year = models.IntegerField()


class Leave(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="leaves")
    leave_type = models.CharField(max_length=20, choices=(
        ("Sick Leave", "Sick Leave"),
        ("Casual Leave", "Casual Leave"),
        ("Maternity Leave", "Maternity Leave"),
        ("Paternity Leave", "Paternity Leave"),
        ("Bereavement Leave", "Bereavement Leave"),
        ("Unpaid Leave", "Unpaid Leave"),
    ))
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=(
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ), default="Pending")
    applied_on = models.DateTimeField(auto_now_add=True)
    approved_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} ({self.start_date} to {self.end_date})"