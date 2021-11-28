from django.views import generic
from .models import Transaction


class TransactionListView(generic.ListView):
    model = Transaction
    context_object_name = "transactions"
    template_name = "transactions/transaction_list.html"
