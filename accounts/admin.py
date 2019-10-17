from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import CustomUserChangeForm, SendEmailForm
from django.shortcuts import render

from accounts.models import (
    CustomUser, 
    Application, 
    personal, documents,
    residential_address, 
    current_degree, previous_degree
)

User = get_user_model()

"""---Admin sit customization---"""
admin.site.site_title = "SITPG Administration"
admin.site.site_header = "SITPG Administration"
admin.site.index_title = "SITPG"
"""---End Admin sit customization---"""

"""Mixin for marking application status"""
class MarkStatus:
    def mark_status_accepted(self, request, queryset):
        for stat in queryset:
            stat.status = 'AC'
            stat.save()
            if queryset.count() == 1:
                message_bit = "1 Applicant was"
            else:
                message_bit = "%s Applicants were" % queryset.count()
        self.message_user(request, "%s successfully marked as accepted." % message_bit, level=messages.SUCCESS)

    def mark_status_denied(self, request, queryset):
        for stat in queryset:
            stat.status = 'DE'
            stat.save()
            if queryset.count() == 1:
                message_bit = "1 Applicant was"
            else:
                message_bit = "%s Applicants were" % queryset.count()
        self.message_user(request, "%s successfully marked as denied." % message_bit, level=messages.SUCCESS)


    def mark_status_conditional(self, request, queryset):
        for stat in queryset:
            stat.status = 'CD'
            stat.save()
            if queryset.count() == 1:
                message_bit = "1 Applicant was"
            else:
                message_bit = "%s Applicants were" % queryset.count()
        self.message_user(request, "%s successfully marked as conditionally accepted." % message_bit, level=messages.SUCCESS)

    def mark_status_withdrawn(self, request, queryset):
        for stat in queryset:
            stat.status = 'WD'
            stat.save()
            if queryset.count() == 1:
                message_bit = "1 Applicant was"
            else:
                message_bit = "%s Applicants were" % queryset.count()
        self.message_user(request, "%s successfully marked as withdrawn." % message_bit, level=messages.SUCCESS)

    def reset_status(self, request, queryset):
        for stat in queryset:
            stat.status = 'AP'
            stat.save()
            if queryset.count() == 1:
                message_bit = "1 Applicant was"
            else:
                message_bit = "%s Applicants were" % queryset.count()
        self.message_user(request, " %s status successfully reset." % message_bit, level=messages.SUCCESS)        
"""End Mixin for marking application status"""


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChangeForm
    list_display = ['username', 'email',]

admin.site.register(CustomUser, CustomUserAdmin)

"""---Personal Details Model---"""
class PersonalResource(resources.ModelResource):
    
    class Meta:
        model = personal
        fields = (
            'first_Name',
            'last_Name',
            'title',
            'status',
        )

class PersonalAdmin(ImportExportModelAdmin, MarkStatus):
    resource_class = PersonalResource
    list_display = (
        'user_id',
        'student_number', 
        'first_Name', 
        'last_Name', 
        'title', 
        'status'
    )
    list_filter = (
        'status',
    )
    search_fields = (
        'first_Name',
        'last_Name'
    )
    actions = [
        "mark_status_accepted", 
        "mark_status_denied", 
        "mark_status_conditional", 
        "mark_status_withdrawn",
        "reset_status",
    ]

admin.site.register(personal, PersonalAdmin)
"""---End Personal Details Model---"""

# needed for exporting data
class ApplicationResource(resources.ModelResource):
    
    class Meta:
        model = Application
        fields = (
            'student_number', 
            'first_Name', 
            'last_Name',
            'email',
            'title',
            'degree',
            'status',
        )

# `Surname`,`Name`,`Title`,`Student Number`,`Email`,`Status` `Degree`
class ApplicationAdmin(PersonalAdmin):
    resource_class = ApplicationResource
    list_display = (
        'email',
        'id',
        'student_number',
        'title',
        'surname',
        'name',
        'degree',
        'status'
    )
    
    list_filter = (
        'status',
        'degree',
    )
    
    search_fields = (
        'name',
        'surname'
        'current_degree'
    )
    
    actions = [
        "mark_status_accepted", 
        "mark_status_denied", 
        "mark_status_conditional", 
        "mark_status_withdrawn",
        "reset_status",
        "send_email",
    ]
    

    def send_email(self, request, queryset):
        form = SendEmailForm(initial={'users': queryset})
        return render(request, 'admin/send_email.html', {'form': form})

admin.site.register(Application, ApplicationAdmin)


admin.site.register(previous_degree)
admin.site.register(current_degree)
admin.site.register(documents)
admin.site.register(residential_address)