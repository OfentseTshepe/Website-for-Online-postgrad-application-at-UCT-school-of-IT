from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from accounts.forms import SendEmailForm
from django.core import mail
from django.core.mail import send_mail
from django.contrib.messages import constants as messages
from django.views.generic import FormView

def home_redirect(requests):
    return redirect('/accounts/index')

# SendUserEmails view class
class SendUserEmails(FormView):
    template_name = 'admin/send_email.html'
    form_class = SendEmailForm
    success_url = reverse_lazy('admin:accounts_account_changelist')

    def form_valid(self, form):
        users = form.cleaned_data['users']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        # send_mail(subject, message, users)
        # email_users.delay(users,subject, message)
        user_message = '{0} users emailed successfully!'.format(form.cleaned_data['users'].count())
        messages.success(self.request, user_message)
        return super(SendUserEmails, self).form_valid(form)