import datetime
from django import forms
from django.core.mail import send_mail
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Button, HTML 
from crispy_forms.bootstrap import FormActions
from django.utils.translation import gettext as _ 
from allauth.account.forms import SignupForm

from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm
) 

from .models import(
    CustomUser, 
    personal, 
    residential_address,
    previous_degree, current_degree,
    documents, Application
)


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user 

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'email')


class PersonalDataForm(forms.ModelForm):
    
    class Meta:
        model = Application
        fields = (
            'title',
            'first_Name',
            'last_Name',
            'student_number',
            'email',
            'phone',
            'citizenship',
            'race', 
            'country_of_birth',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper
        self.helper.form_method = 'post'
        # Layout formats how the form is rendered
        self.helper.form_class 
        self.helper.layout = Layout (
            Fieldset("Personal Information",
                'title',
                'first_Name',
                'last_Name',
                'student_number',                
                'email',
                'phone',
                HTML("""<h4>Demography</h4>"""),
                'citizenship',
                'race', 
                'country_of_birth'
            ), Submit('Submit', 'Save', css_class='btn primary'),
        )


class AddressForm(forms.ModelForm):
    
    class Meta:
        model = Application
        fields = (
            'address_Line_1',
            'address_Line_2',
            'city',
            'code',
            'country_of_residence',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'
        # Layout formats how the form is rendered
        self.helper.layout = Layout (
            'address_Line_1',
            'address_Line_2',
            'city',
            'code',
            'country_of_residence',
            Submit('submit','Save', css_class='btn success')
        )    


class DegreeForm(forms.ModelForm):
    
    class Meta:
        model = previous_degree
        fields = (
            'previous_degree',
            'NQF_equivalent',
            'years',
            'previous_university',
            'country_obtained',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'
        # Layout formats how the form is rendered
        self.helper.layout = Layout (
            'previous_university',
            'previous_degree',
            'NQF_equivalent',
            'years',
            'country_obtained',
            Submit('submit','Save', css_class='btn success')
        )

class DocumentsForm(forms.ModelForm):
    
    class Meta:
        model = documents
        fields = (
            'curriculum_vitae',
            'cover_letter',
            'transcript',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'
        # Layout formats how the form is rendered
        self.helper.layout = Layout (
            'curriculum_vitae',
            'cover_letter',
            'transcript',
            Submit('submit','Upload', css_class='btn success')
        )


class SendEmailForm(forms.Form):
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('Subject')}))
    message = forms.CharField(widget=forms.Textarea)
    users = forms.ModelMultipleChoiceField(
        label="To",
        queryset=CustomUser.objects.all(),
        widget=forms.SelectMultiple()
    )

class ApplicationForm(PersonalDataForm, AddressForm, DegreeForm, DocumentsForm):
    
    class Meta:
        model = Application
        fields = (
            # personal details
            'title',
            'first_Name',
            'last_Name',
            'student_number',
            'email',
            'phone',
            'citizenship',
            'race',
            'country_of_birth',
            # address
            'address_Line_1',
            'address_Line_2',
            'city',
            'code',
            'country_of_residence',
            # Previous qualifications
            'previous_degree',
            'NQF_equivalent',
            'years',
            'previous_university',
            'country_obtained',
            # Study Choices
            # to be added by xhanti

            # Documents
            'curriculum_vitae',
            'cover_letter',
            'transcript',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper
        self.helper.form_method = 'post'
        # Layout formats how the form is rendered
        self.helper.form_class 
        self.helper.layout = Layout (
            Fieldset("Update Application",
                HTML("""<h4><strong>Personal Details</strong></h4>"""),
                'title',
                'first_Name',
                'last_Name',
                'student_number',                
                'email',
                'phone',
                HTML("""<h4><strong>Demography</strong></h4>"""),
                'citizenship',
                'race', 
                'country_of_birth',
                HTML("""<h4><strong>Address</strong></h4>"""),
                'address_Line_1',
                'address_Line_2',
                'city',
                'code',
                'country_of_residence',
                HTML("""<h4><strong>Previous Qualifications</strong></h4>"""),
                'previous_degree',
                'NQF_equivalent',
                'years',
                'previous_university',
                'country_obtained',
                # HTML("""<h4>Study Choices</h4>"""),
                HTML("""<h4><strong>Documents Uploaded</strong></h4>"""),
                'curriculum_vitae',
                'cover_letter',
                'transcript'
            ), FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel')
            ),
        )