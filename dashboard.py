from controlcenter import Dashboard, widgets
from .accounts.models import degree

class ModelItemList(widgets.ItemList):
    model = degree
    list_display = ('pk', 'field')

class MyDashboard(Dashboard):
    widgets = (
        ModelItemList,
    )