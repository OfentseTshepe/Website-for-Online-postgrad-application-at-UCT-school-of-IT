from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .tokens import account_activation_token
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate 
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone
from django.utils.translation import gettext as _ 
from django.core.mail import send_mail
from django.contrib.messages import constants as messages
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin

from accounts.forms import ( 
    PersonalDataForm, 
    AddressForm, DegreeForm, 
    DocumentsForm, SendEmailForm,
    ApplicationForm
)

from .models import (
    CustomUser, 
    personal, 
    residential_address,
    previous_degree, current_degree,
    documents, Application
)

from django.views.generic import (
    CreateView, DetailView,
    ListView, UpdateView,
    DeleteView, FormView,
    TemplateView
)


"""+++++++++++++++ Function Based Views ++++++++++++++++++"""

def index(request):
	return render(request, 'index.html')

def welcome(request):
    return render(request, 'Application/welcome.html')

def overview(request):
    return render(request, 'Application/Overview.html')

@login_required
def account_info(request):
    return render(request, 'accounts/account_info.html')

@login_required
def terms(request):
    return render(request, 'Application/terms.html')

@login_required
def submit(request):
    return render(request, 'Application/submit.html')

class change_password():
    pass

# SendUserEmails view class
class SendUserEmails(FormView):
    template_name = 'admin/send_email.html'
    form_class = SendEmailForm
    success_url = reverse_lazy('admin:accounts_account_changelist')

    def form_valid(self, form):
        # users = form.cleaned_data['users']
        users = form.values_list('email', flat=True) 
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, users)
        # email_users.delay(users,subject, message)
        user_message = '{0} users emailed successfully!'.format(form.cleaned_data['users'].count())
        messages.success(self.request, user_message)
        return super(SendUserEmails, self).form_valid(form)

"""+++++++++++++++++++++++++++++++++++++++++++++"""




# following CRUD - Create, Retrieve, Update, Delete using class based views




"""+++++++++++++++++++++  PERSONAL  ++++++++++++++++++++++++"""

"""create"""
class PersonalCreateView(SuccessMessageMixin, CreateView):
    model = Application
    form_class = PersonalDataForm
    template_name = "Application/CreatePersonalDetails.html"
    success_message = "submission autosaved successfully, to edit or withdraw click below."
    success_url = reverse_lazy("accounts:person-list")
    
    def get_initial(self, *args, **kwargs):
        initial = super(PersonalCreateView, self).get_initial(**kwargs)
        initial['email'] = self.request.user.email
        initial['first_Name'] = self.request.user.first_name
        initial['last_Name'] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PersonalCreateView, self).form_valid(form)

"""retrieve the object that was just created."""
class PersonalListView(SuccessMessageMixin, ListView):
    model = Application
    context_object_name = 'persons'
    template_name = 'Application/ListPersonalDetails.html'

    def get_queryset(self):
        return personal.objects.filter(user=self.request.user)


"""Update"""
class PersonalUpdateView(SuccessMessageMixin, UpdateView):
    model = Application
    form_class = PersonalDataForm
    template_name = 'Application/UpdatePersonalDetails.html'
    success_message = "application updated successfully."
    success_url = reverse_lazy("accounts:person-list")

    def get_object(self, queryset=None):
        obj = personal.objects.get(id=self.kwargs['id'])
        return obj

"""Update"""
class PersonalAddressUpdateView(SuccessMessageMixin, UpdateView):
    model = Application
    form_class = AddressForm
    template_name = "Application/UpdateAddressDetails.html"
    success_message = "application progress updated successfully."
    success_url = reverse_lazy("accounts:person-list")

    def get_object(self, queryset=None):
        obj = Application.objects.get(id=self.kwargs['id'])
        return obj


"""Delete"""
class PersonalDeleteView(SuccessMessageMixin, DeleteView):
    model = personal
    template_name = 'Application/DeletePersonalDetails.html'
    success_message = "submission withdrawn successfully."
    success_url = reverse_lazy("accounts:person-list")

    def get_object(self, queryset=None):
        obj = personal.objects.get(id=self.kwargs['id'])
        return obj


"""+++++++++++++++++++++++++++++++++++++++++++++"""


"""++++++++++++++++++++  ADDRESS  ++++++++++++++++++++++++"""

"""create"""
class AddressCreateView(CreateView):
    model = Application
    form_class = AddressForm
    template_name = 'Application/CreateAddressDetails.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddressCreateView, self).form_valid(form)


"""retrieve all person objects should set permission to only staff"""
class AddressListView(ListView):
    model = residential_address
    context_object_name = 'address'
    template_name = 'Application/ListAddressDetails.html'

    def get_queryset(self):
        return personal.objects.filter(user=self.request.user)

"""Update"""
class AddressUpdateView(SuccessMessageMixin, UpdateView):
    model = Application
    form_class = AddressForm
    template_name = 'Application/UpdateAddressDetails.html'
    success_message = "application updated successfully."
    success_url = reverse_lazy("accounts:person-list")

    def get_object(self, queryset=None):
        obj = Application.objects.get(id=2)
        return obj

"""Delete"""
class AddressDeleteView(DeleteView):
    model = residential_address
    template_name = 'Application/DeleteAddressDetails.html'

    def get_object(self):
        user = self.kwargs.get('user') 
        return get_object_or_404(residential_address, user)

    def get_success_url(self):
        return reverse('accounts:address-list')

"""Detail"""
class AddressDetailView(DetailView):
    model = residential_address
    form_class = AddressForm # check the form classes for problems
    template_name = 'Application/ShowAddressDetails.html'

    def get_object(self):
        id_ = self.kwargs.get('id') 
        return get_object_or_404(residential_address, id=id_)

    def get_context_data(self, **kwargs):
        context = super(AddressDetailView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        # context['form'] = AddressDetailView()
        return context

"""+++++++++++++++++++++++++++++++++++++++++++++"""








"""+++++++++++++++++++++   DEGREE   ++++++++++++++++++++++++"""

"""create"""
class DegreeCreateView(CreateView):
    model = previous_degree
    form_class = DegreeForm
    template_name = 'Application/CreateDegreeDetails.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(DegreeCreateView, self).form_valid(form)

"""retrieve"""
class DegreeListView(ListView):
    model = previous_degree
    queryset = previous_degree.objects.all()
    template_name = 'Application/ListDegreeDetails.html'

"""Update"""
class DegreeUpdateView(UpdateView):
    model = previous_degree
    form_class = DegreeForm
    template_name = 'Application/UpdateDegreeDetails.html'

    def get_object(self):
        user = self.kwargs.get('user') 
        return get_object_or_404(previous_degree, user)

"""Delete"""
class DegreeDeleteView(DeleteView):
    model = previous_degree
    template_name = 'Application/DeleteDegreeDetails.html'

    def get_object(self):
        user = self.kwargs.get('user') 
        return get_object_or_404(previous_degree, user)

    def get_success_url(self):
        return reverse('accounts:degree-list')

"""Detail"""
class DegreeDetailView(DetailView):
    model = previous_degree
    form_class = DegreeForm
    template_name = 'Application/ShowDegreeDetails.html'

    def get_object(self):
        id_ = self.kwargs.get('id') 
        return get_object_or_404(previous_degree, id=id_)

    def get_context_data(self, **kwargs):
        context = super(DegreeDetailView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        # context['form'] = PersonalDetailView()
        return context

"""+++++++++++++++++++++++++++++++++++++++++++++"""








"""+++++++++++++++++++++   DOCUMENTS   ++++++++++++++++++++++++"""

"""create"""
class DocumentCreateView(CreateView):
    model = documents
    form_class = DocumentsForm
    template_name = 'Application/CreateDocumentDetails.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(DocumentDetailView, self).form_valid(form)

"""retrieve"""
class DocumentListView(ListView):
    model = documents
    queryset = documents.objects.all()
    template_name = 'Application/ListDocumentDetails.html'

"""Update"""
class DocumentUpdateView(UpdateView):
    model = documents
    form_class = DocumentsForm
    template_name = 'Application/UpdateDocumentDetails.html'

    def get_object(self):
        user = self.kwargs.get('user') 
        return get_object_or_404(documents, user)

"""Delete"""
class DocumentDeleteView(DeleteView):
    model = documents
    template_name = 'Application/DeleteDocumentDetails.html'

    def get_object(self):
        user = self.kwargs.get('user') 
        return get_object_or_404(documents, user)

    def get_success_url(self):
        return reverse('accounts:document-list')

"""Detail"""
class DocumentDetailView(DetailView):
    model = documents
    form_class = DocumentsForm
    template_name = 'Application/ShowDocumentDetails.html'

    def get_object(self):
        id_ = self.kwargs.get('id') 
        return get_object_or_404(documents, id=id_)

    def get_context_data(self, **kwargs):
        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        # context['form'] = PersonalDetailView()
        return context

"""+++++++++++++++++++++++++++++++++++++++++++++"""







"""+++++++++++++++++ APPLICATION +++++++++++++++++++++++"""
# should probably use formview here because after submitting i need to validate and then maybe send notification

"""create"""
class ApplicationCreateView(SuccessMessageMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = "Application/CreateApplicationDetails.html"
    success_message = "submission autosaved successfully, to edit or withdraw click on overview."
    success_url = reverse_lazy("accounts:application-list")
    
    def get_initial(self, *args, **kwargs):
        initial = super(ApplicationCreateView, self).get_initial(**kwargs)
        initial['email'] = self.request.user.email
        initial['first_Name'] = self.request.user.first_name
        initial['last_Name'] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ApplicationCreateView, self).form_valid(form)

"""retrieve the object that was just created."""
class ApplicationListView(SuccessMessageMixin, ListView):
    model = Application
    context_object_name = 'My_Application'
    template_name = 'Application/ListApplicationDetails.html'

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)


"""Update"""
class ApplicationUpdateView(SuccessMessageMixin, UpdateView):
    model = Application
    form_class = ApplicationForm
    template_name = "Application/UpdateApplicationDetails.html"
    success_message = "application updated successfully."
    success_url = reverse_lazy("accounts:list-application")

    def get_object(self, queryset=None):
        obj = Application.objects.get(id=self.kwargs['id'])
        return obj


"""Delete"""
class ApplicationDeleteView(SuccessMessageMixin, DeleteView):
    model = personal
    template_name = 'Application/DeletePersonalDetails.html'
    success_message = "submission withdrawn successfully."
    success_url = reverse_lazy("accounts:list-application")

    def get_object(self, queryset=None):
        obj = personal.objects.get(id=self.kwargs['id'])
        return obj
"""+++++++++++++++++++++++++++++++++++++++++++++"""




