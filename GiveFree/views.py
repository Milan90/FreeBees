from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
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


class AddInstitutionView(View):

    def get(self, request):
        form = AddInstitutionForm()
        return render(request, "GiveFree/add_institution.html", {"form": form})

    def post(self, request):
        form = AddInstitutionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            goal = form.cleaned_data["goal"]
            city = form.cleaned_data["city"]
            street = form.cleaned_data["street"]
            building_number = form.cleaned_data["building_number"]
            try:
                flat_number = form.cleaned_data["flat_number"]
            except ValueError:
                flat_number = None

            zip_code = form.cleaned_data["zip_code"]
            groups_id = form.cleaned_data["groups"]

            address = InstitutionAddress.objects.create(city=city,
                                                        street=street,
                                                        building_number=building_number,
                                                        flat_number=flat_number,
                                                        zip_code=zip_code)
            institution = Institution.objects.create(name=name, goal=goal, address=address)

            for group in groups_id:
                institution.groups.add(Groups.objects.get(pk=group))
                institution.save()

            return redirect("/institutions")
        else:
            return render(request, "GiveFree/add_institution.html", {"form": form})


class InstitutionListView(View):

    def get(self, request):
        institutions = Institution.objects.all()
        inst_group = {}

        for institution in institutions:
            inst_group.setdefault(institution.name, [institution.groups.all()])
            for groups in inst_group[institution.name]:
                g = []
                for group in groups:
                    g.append(group.name)
                inst_group[institution.name] = g

        ctx = {"institutions": institutions,
               "inst_group": inst_group}

        return render(request, "GiveFree/institution_list.html", ctx)


class EditInstitutionView(View):
    def get(self, request, id):
        institution = Institution.objects.get(pk=id)
        institution_groups = institution.groups.all()
        groups_id = []
        for group in institution_groups:
            groups_id.append(group.id)

        form_values = {'name': institution.name,
                       'goal': institution.goal,
                       'city': institution.address.city,
                       'street': institution.address.street,
                       'building_number': institution.address.building_number,
                       'flat_number': institution.address.flat_number,
                       'zip_code': institution.address.zip_code,
                       'groups': groups_id}

        form = AddInstitutionForm(initial=form_values)

        return render(request, "GiveFree/edit_institution.html", {"form": form})

    def post(self, request, id):
        form = AddInstitutionForm(request.POST)
        if form.is_valid():
            institution = Institution.objects.get(pk=id)
            institution.name = form.cleaned_data["name"]
            institution.goal = form.cleaned_data["goal"]
            institution.address.city = form.cleaned_data["city"]
            institution.address.street = form.cleaned_data["street"]
            institution.address.building_number = form.cleaned_data["building_number"]
            institution.address.flat_number = form.cleaned_data["flat_number"]

            groups_id = []
            for group in institution.groups.all():
                groups_id.append(str(group.id))

            updated_groups_id = form.cleaned_data["groups"]

            if updated_groups_id == groups_id:
                institution.address.save()
                institution.save()
                return redirect("institutions")
            else:
                institution.groups.clear()
                for id in updated_groups_id:
                    institution.groups.add(Groups.objects.get(pk=id))

                institution.address.save()
                institution.save()
                return redirect("institutions")


class DeleteInstitutionView(DeleteView):
    model = Institution
    template_name = "GiveFree/delete_institution.html"
    success_url = reverse_lazy("institutions")
