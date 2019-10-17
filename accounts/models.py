from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_save
from django_countries.fields import CountryField
from localflavor.za import forms
from phone_field import PhoneField
from django.conf import settings
from datetime import datetime
from filer.fields.file import FilerFileField
from django.utils.translation import ugettext_lazy as _  
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth import get_user_model
from django_fsm import FSMField, transition
from django.core.exceptions import ValidationError

"""-- choices---"""
CITIZENSHIP_CHOICES = (
    ('DEF', ''),
    ('SAC','South African Citizen'),
    ('SRP','South African Permanent Resident'),
    ('INT','International'),
)

RACE_CHOICES = (
    ('DEF', ''),
    ('BK','Black'),
    ('CO','Coloured'),
    ('IN','Indian'),
    ('WH','White'),
    ('OT','Other'),
)

TITLE_CHOICES = (
    ('DEF', ''),
    ('MR','Mr'),
    ('MRS','Mrs'),
    ('MS','Miss'),
    ('MX','Mx'),
    ('DR','Dr'),
)

DEPARTMENT_CHOICES = (
    ('CS','Department of Computer Science'),
    ('IS', 'Department of Information Systems'),
    ('IT','Department of Information Technology')
)

DEGREE_CHOICES = (
    ('DEF', ''),
    ('HONS_CS', 'Honours in Computer Science'),
    ('MIT', 'Masters in Information in Technology'),
    ('MSC_CS_CD', 'Master by Coursework ad Dissertation'),
    ('MSC_CS_D', 'Master by Dissertation'),
    ('PhD_CS', 'PhD in Computer Science'),
    ('HONS_IS', 'Honours in Information Systems'),
    ('HONS_MIS', 'Honours in Management Information Systems'),
    ('MIT', 'Masters in Information in Technology'),
    ('PSD', 'Postgraduate Diploma in Management in Information System'),
    ('MSC_IS', 'Master by Commerce in Information Systems'),
    ('PhD_IS', 'PhD in Information Systems'),
)

PREVIOUS_DEGREE_CHOICES = (
    ('DEF', ''),
    ('OTHER', 'Other'),
)

CHOICES = (
    ('DEF', ''),
    ('Y', 'Yes'),
    ('N', 'No'),
)

APPLICANT_STATUS = (
    ('AP', 'Applied'),
    ('AC', 'Accepted'),
    ('CD', 'Conditional'),
    ('DE', 'Denied'),
    ('WD', 'Withdrawn'),
)

APPLICATION_STATE = (
    ('NEW','new'),
    ('ACT','active'), 
    ('WDN','withdrawn'), 
    ('COM','complete'), 
    ('INC','incomplete'),
)
"""-- end choices---"""

"""---user profile model---"""
class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=9, 
        unique=True
    )
    
    USERNAME_FIELD = 'username'

    def __str__(self):
        # return self.email
        return self.username
    
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_application_for_new_user(sender, created, instance, **kwargs):
        if created:
            application = Application(user=instance)
            application.save()




"""Personal information Model"""
class personal(models.Model):
    # to make sure that only one row is added by a user, use one to one field.
    # user = models.OneToOneField(
    #     settings.AUTH_USER_MODEL, 
    #     on_delete=models.CASCADE, 
    #     null=True
    # )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True,
    )
    student_number = models.CharField(
        max_length=9,  
        help_text='UCT Student Number'
    )
    title = models.CharField(max_length=3, choices=TITLE_CHOICES,default='')
    first_Name = models.CharField(max_length=100, default='')
    last_Name = models.CharField(max_length=100, default='')
    email = models.EmailField(blank=True, null=False)
    phone = PhoneField(blank=True)
    citizenship = models.CharField(max_length=5, choices=CITIZENSHIP_CHOICES, default='')    
    country_of_birth = CountryField(default='', blank_label='(select country)')        
    race = models.CharField(max_length=3, choices=RACE_CHOICES, default='')    
    status = models.CharField(max_length=2, choices=APPLICANT_STATUS, default='AP')

    class Meta:
        verbose_name = _("Personal Detail")
        verbose_name_plural = _("Personal Details")

    def __str__(self):
        return self.student_number
   
    def get_delete_url(self):
        return reverse(
            'accounts:person-delete', 
            args=[str(self.id)]
        )
    
    def get_update_url(self):
        return reverse(
            'accounts:person-edit', 
            args=[str(self.id)]
        )


# current address
class residential_address(models.Model):
    address_id = models.AutoField(primary_key=True)
    address_Line_1 = models.CharField(max_length=50, default='')
    address_Line_2 = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=100, default='')
    code = models.PositiveIntegerField(default=0000)
    country_of_residence = CountryField(default=' ', blank_label='(select country)')

    class Meta:
        verbose_name = _("Residential Address")
        verbose_name_plural = _("Residential Addresses")

    def __str__(self):
        return '%s %s' % (self.city, self.code)

    def get_delete_url(self):
        return reverse(
            'accounts:address-delete', 
            args=[str(self.id)]
        )
    
    def get_update_url(self):
        return reverse(
            'accounts:address-edit', 
            args=[str(self.id)]
        )

    def save(self, *args, **kwargs):
        super(residential_address, self).save(*args,**kwargs)


# degree information    
class previous_degree(models.Model):
    previous_id = models.AutoField(primary_key=True)
    NQF_equivalent = models.CharField(max_length=100, default='')
    years = models.PositiveIntegerField(default=0000)
    other_degree = models.CharField(max_length=100, default='')
    degree_standard = models.CharField(max_length=100, default='')
    previous_university = models.CharField(max_length=100, default='')
    country_obtained = CountryField(default='', blank_label='(select country)')
    previous_degree = models.CharField(max_length=12, choices=PREVIOUS_DEGREE_CHOICES, default='BSC')
    
    class Meta:
        verbose_name = _("Previous Qualification")
        verbose_name_plural = _("Previous Qualifications")

    def __str__(self):
        return self.previous_degree
    
    def get_absolute_url(self):
        return reverse('accounts:previous-detail', args=[str(self.id)])


class current_degree(models.Model):
    current_id = models.AutoField(primary_key=True)
    degree = models.CharField(max_length=14, choices=DEGREE_CHOICES, default=' ')
    department = models.CharField(max_length=4, choices=DEPARTMENT_CHOICES, default='CS') 
    # MIT Degree fields
    number_of_years_prior_to_IT_experience = models.PositiveIntegerField(default=0000)

    level_0_of_undergraduate_mathematics =  models.PositiveIntegerField(default=0000)
    level_0_math_average = models.PositiveIntegerField(default=0000)

    level_1_of_undergraduate_mathematics =  models.PositiveIntegerField(default=0000)
    level_1_math_average = models.PositiveIntegerField(default=0000)

    level_2_of_undergraduate_mathematics =  models.PositiveIntegerField(default=0000)
    level_2_math_average = models.PositiveIntegerField(default=0000)

    level_3_of_undergraduate_mathematics =  models.PositiveIntegerField(default=0000)
    level_3_math_average = models.PositiveIntegerField(default=0000)

    project_component = models.CharField(max_length=2, choices=CHOICES, default=' ')

    description = models.TextField(max_length=500, default='')

    class Meta:
        verbose_name = _("Degree Choice")
        verbose_name_plural = _("Degree Choices")

    def __str__(self):
        return self.current_degree
    
    def get_absolute_url(self):
        return reverse('accounts:current-detail', args=[str(self.id)])


class documents(models.Model):
    doc_id = models.AutoField(primary_key=True)
    curriculum_vitae = models.FileField(upload_to='documents/')
    cover_letter = models.FileField(upload_to='documents/')
    transcript = models.FileField(upload_to='documents/')
    
    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
    
    def __str__(self):
        return '%s' % (self.doc_id)

    def get_absolute_url(self):
        return reverse('accounts:document-detail', args=[str(self.id)])


"""the application inherits from the other models instead of referencing them."""
# `Surname`,`Name`,`Title`,`Student Number`,`Email`,`Status` `Degree`
# class Application(models.Model):    
#     personal = models.ForeignKey(
#         personal, 
#         on_delete=models.CASCADE, 
#     )
#     residential = models.ForeignKey(
#         residential_address, 
#         on_delete=models.CASCADE, 
#     )
#     current_degree = models.ForeignKey(
#         current_degree, 
#         on_delete=models.CASCADE, 
#     )
#     documents = models.ForeignKey(
#         documents, 
#         on_delete=models.CASCADE, 
#     )

class Application(personal, residential_address, documents, current_degree, previous_degree): 
    creation = models.DateTimeField(auto_now_add=True, blank=True) # date the application was created
    state = FSMField(default='new')

    class Meta:
        verbose_name = _("Application")
        verbose_name_plural = _("Applications")
        ordering = ("creation",)


    def get_absolute_url(self):
        return reverse('accounts:person-list', args=[str(self.id)])
    
    @property
    def name(personal):
        return personal.first_Name
    
    @property
    def surname(personal):
        return personal.last_Name
    
    def degree(current_degree):
        return current_degree.degree
    
    def title(personal):
        return personal.title

    def email(personal):
        return personal.email

    def status(personal):
        return personal.status
    
    def student_number(personal):
        return personal.student_number

    def get_delete_url(self):
        return reverse(
            'accounts:delete-application', 
            args=[str(self.id)]
        )
    
    def get_update_url(self):
        return reverse(
            'accounts:edit-application', 
            args=[str(self.id)]
        )
    
    # @receiver(pre_save, sender=settings.AUTH_USER_MODEL)
    # def check_no_conflicting_application(sender, instance, *args, **kwargs):
    #     # If another JuicerBaseSettings object exists a ValidationError will be raised
    #     if Application.objects.exclude(pk=instance.pk).exists():
    #         raise ValidationError('Application with this ID number already exists, click modify or withdraw then proceed.')