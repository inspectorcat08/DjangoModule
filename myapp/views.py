from datetime import timedelta, timezone
from pyexpat.errors import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from .models import MyUser, Product, Purchase, Return
from .forms import RegisterForm, AppendForm, BuyForm


class Login(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return '/profile/{}/'.format(self.request.user.id)


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/login/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.money = 10000
        obj.save()
        return super().form_valid(form=form)


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = '/login/'


class Returns(LoginRequiredMixin, CreateView):
    pk_url_kwarg = 'pk'
    login_url = "/login/"
    model = Return
    fields = []
    success_url = "/user/purchases/"
    template_name = "purchases.html"

    def form_valid(self, form):
        user = self.request.user
        obj = form.save(commit=False)
        obj.user = user
        obj.purchase = Purchase.objects.get(pk=self.kwargs["pk"])
        obj.save()
        return super().form_valid(form=form)
    # model = Return
    # form_class = PurchaseReturnForm
    # success_url = '/user/purchases/'
    # template_name = 'returns.html'
    #
    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     purchase = Purchase.objects.get(id=self.request.POST['purchase_id'])
    #     returns = Return.objects.filter(purchase=purchase)
    #     if purchase.time_of_buy + timedelta(minutes=3) < timezone.now():
    #         messages.error(self.request, 'SORRY, can be returned only 3 minutes after purchase!')
    #         return redirect('purchase')
    #     elif returns:
    #         messages.info(self.request, 'Your return request is already being processed!')
    #         return redirect('purchase')
    #     messages.info(self.request, 'Your request in work!')
    #     self.object.purchase = purchase
    #     self.object.save()
    #     return super().form_valid(form=form)


class PurchasesList(ListView):
    model = Purchase
    template_name = "purchases.html"


class Profile(LoginRequiredMixin, DetailView):
    login_url = "/login/"
    pk_url_kwarg = "pk"
    model = MyUser
    template_name = "profile.html"


class ProductListView(ListView):
    model = Product
    template_name = 'index.html'


class ProductAppend(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    form_class = AppendForm
    template_name = "add_product.html"
    success_url = '/'


class ProductUpdate(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    template_name = "change_product.html"
    model = Product
    fields = ["title", "description", "price", "quantity_in_stock", "available"]

    def get_success_url(self):
        return "/about/{}".format(self.object.pk)


class ProductAbout(DetailView):
    pk_url_kwarg = "pk"
    model = Product
    template_name = "product.html"
    extra_context = {"form": BuyForm}


class ProductBuy(LoginRequiredMixin, CreateView):
    pk_url_kwarg = "pk"
    login_url = "/login/"
    form_class = BuyForm

    def form_valid(self, form):
        product = Product.objects.get(pk=self.kwargs["pk"])
        user = self.request.user
        if product.quantity_in_stock >= form.cleaned_data["quantity"] and user.money >= (product.price*form.cleaned_data["quantity"]):
            product.quantity_in_stock -= form.cleaned_data["quantity"]
            user.money -= (product.price*form.cleaned_data["quantity"])
            purchase = form.save(commit=False)
            purchase.user = user
            purchase.product = product
            user.save()
            product.save()
            purchase.save()
            return super().form_valid(form=form)
        else:
            return redirect(f"/about/{self.kwargs['pk']}")

    def get_success_url(self):
        return "/profile/{}".format(self.request.user.id)

    def form_invalid(self, form):
        return redirect(f"/about/{self.kwargs['pk']}")

