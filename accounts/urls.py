from . import views
from django.conf.urls import url
from django.urls import include, path
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .views import (
    PersonalListView, PersonalCreateView,
    PersonalUpdateView, PersonalDeleteView, 
    PersonalAddressUpdateView,
    
    AddressListView, AddressCreateView,
    AddressUpdateView, AddressDeleteView,
    
    DegreeListView, DegreeCreateView,
    DegreeUpdateView, DegreeDeleteView,
    DegreeDetailView,

    DocumentListView, DocumentCreateView,
    DocumentUpdateView, DocumentDeleteView,
    DocumentDetailView,

    ApplicationListView, ApplicationCreateView,
    ApplicationUpdateView, ApplicationDeleteView,
)

app_name = 'accounts' # namespace for urls

urlpatterns = [
    # Navbar urls
    path('', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),  
    url(r'^welcome/$', views.welcome, name='welcome'),    
    url(r'^account-info/$', views.account_info, name='account_info'),   
    
    # personal views CRUD urls
    path('add-person/', login_required(PersonalCreateView.as_view()), name='person-add'),
    path('list-person/', PersonalListView.as_view(), name='person-list'),
    path('<int:id>/edit-person/', login_required(PersonalUpdateView.as_view()), name='person-edit'),
    path('<int:id>/delete-person/', login_required(PersonalDeleteView.as_view()), name='person-delete'),

    # address views CRUD urls
    path('add-address/', login_required(AddressCreateView.as_view()), name='address-add'),
    path('list-address/', login_required(AddressListView.as_view()), name='address-list'),
    path('<int:id>/edit-address/', login_required(AddressUpdateView.as_view()), name='address-edit'),
    path('<int:id>/delete-address/', login_required(AddressDeleteView.as_view()), name='address-delete'),
        
    # Current_Degree views CRUD urls
    path('add-current/', login_required(DegreeCreateView.as_view()), name='degree-add'),
    path('edit-current/', login_required(DegreeUpdateView.as_view()), name='degree-edit'),
    path('list-current/', login_required(DegreeListView.as_view()), name='degree-list'),
    path('<int:id>/detail-current/', login_required(DegreeDetailView.as_view()), name='degree-detail'),
    path('<int:id>/delete-current/', login_required(DegreeDeleteView.as_view()), name='degree-delete'),

    # # Previous_Degree views CRUD urls
    # path('add-previous/', login_required(AddressCreateView.as_view()), name='address-add'),
    # path('edit-previous/', login_required(AddressUpdateView.as_view()), name='address-detail'),
    # path('list-previous/', login_required(AddressListView.as_view()), name='address-list'),
    # path('<int:id>/detail-previous/', login_required(AddressDetailView.as_view()), name='address-detail'),
    # path('<int:id>/delete-previous/', login_required(AddressDeleteView.as_view()), name='address-delete'),      
    
    # document views CRUD urls    
    url(r'^documents/$', views.documents, name='documents'),
    path('add-document/', login_required(DocumentCreateView.as_view()), name='document-add'),
    path('edit-document/', login_required(DocumentUpdateView.as_view()), name='document-edit'),
    path('list-document/', login_required(DocumentListView.as_view()), name='document-list'),
    path('<int:id>/detail-document/', login_required(DocumentDetailView.as_view()), name='document-detail'),
    path('<int:id>/delete-document/', login_required(DocumentDeleteView.as_view()), name='document-delete'),   
    
    # Complete ApplicationView urls
    path('add-application/', login_required(ApplicationCreateView.as_view()), name='add-application'),
    path('list-application/', login_required(ApplicationListView.as_view()), name='list-application'),
    path('<int:id>/edit-application/', login_required(ApplicationUpdateView.as_view()), name='edit-application'),
    path('<int:id>/delete-application/', login_required(ApplicationDeleteView.as_view()), name='delete-application'),
    
    # refactor to flat pages (if time allows)
    url(r'^terms/$', views.terms, name='terms'),
    url(r'^submit/$', views.submit, name='submit'),
    url(
        regex=r'^email-users/$', 
        view=views.SendUserEmails.as_view(), 
        name='email'
    ), 

]
