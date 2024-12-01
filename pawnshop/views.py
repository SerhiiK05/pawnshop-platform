from django.views import generic


# Create your views here.
def index():
    pass


class UserListView(generic.ListView):
    pass


class UserDetailView(generic.DetailView):
    pass


class UserCreateView(generic.CreateView):
    pass


class UserUpdateView(generic.UpdateView):
    pass


class UserDeleteView(generic.DeleteView):
    pass


class ItemListView(generic.ListView):
    pass


class ItemDetailView(generic.DetailView):
    pass


class ItemCreateView(generic.CreateView):
    pass


class ItemUpdateView(generic.UpdateView):
    pass


class ItemDeleteView(generic.DeleteView):
    pass


class LoanListView(generic.ListView):
    pass


class LoanDetailView(generic.DetailView):
    pass


class LoanCreateView(generic.CreateView):
    pass


class LoanUpdateView(generic.UpdateView):
    pass


class LoanDeleteView(generic.DeleteView):
    pass


class PaymentListView(generic.ListView):
    pass


class PaymentDetailView(generic.DetailView):
    pass


class PaymentCreateView(generic.CreateView):
    pass


class PaymentUpdateView(generic.UpdateView):
    pass


class PaymentDeleteView(generic.DeleteView):
    pass


class ReferralBonusListView(generic.ListView):
    pass


class ReferralBonusDetailView(generic.DetailView):
    pass


class ReferralBonusCreateView(generic.CreateView):
    pass


class ReferralBonusUpdateView(generic.UpdateView):
    pass


class ReferralBonusDeleteView(generic.DeleteView):
    pass