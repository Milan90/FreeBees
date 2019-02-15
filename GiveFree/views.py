from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView
from GiveFree.models import *
from GiveFree.forms import *


class LandingPageView(View):

    def get(self, request):
        return render(request, "GiveFree/index.html")

    def post(self, request):
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        message = request.POST.get("message")
        if name and surname and message:
            ContactMessage.objects.create(name=name, surname=surname, message=message)
            ctx = {"message": "Wiadomość wysłana poprawnie"}
            return render(request, "GiveFree/index.html", ctx)
        else:
            ctx = {"message": "Wypełnij poprawnie wyszystkie pola!"}
            return render(request, "GiveFree/index.html", ctx)


class MainPageView(LoginRequiredMixin, View):
    login_url = "accounts/login"
    redirect_field_name = "next"

    def get(self, request):
        if request.user.is_staff:
            return render(request, "GiveFree/administrator.html")

        else:
            return render(request, "GiveFree/form.html")

    def post(self, request):
        if request.is_ajax():
            pass


class AdminsList(View):

    def get(self, request):
        if request.user.is_staff:
            admins = User.objects.all().filter(is_staff=True)
            return render(request, "GiveFree/admins_list.html", {"admins": admins})


class AddAdmin(View):

    def get(self, request):
        form = AddAdminForm()
        return render(request, "GiveFree/add_admin.html", {"form": form})

    def post(self, request):
        form = AddAdminForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            User.objects.create_user(username=username, first_name=first_name,
                                     email=email, password=password, is_staff=True)

            return redirect("/admins")


class EditAdminView(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'GiveFree/edit_admin.html'
    success_url = reverse_lazy('admins')


class DeleteAdminView(DeleteView):
    model = User
    template_name = 'GiveFree/delete_admin.html'
    success_url = reverse_lazy('admins')
