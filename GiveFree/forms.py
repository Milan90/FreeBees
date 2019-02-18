from django.core.validators import MinValueValidator
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from GiveFree.models import Groups


class AddAdminForm(ModelForm):
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password')
        widgets = {'password': forms.PasswordInput}

    def clean(self):
        cleaned_data = super(AddAdminForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('repeat_password')

        if password != password2:
            self.add_error('password', "Password and repeat_password must be the same!")


groups = ((g.pk, g.name) for g in Groups.objects.all())


class AddInstitutionForm(forms.Form):
    name = forms.CharField(max_length=250)
    goal = forms.CharField(max_length=200)
    city = forms.CharField(max_length=100)
    street = forms.CharField(max_length=100)
    building_number = forms.IntegerField(validators=[MinValueValidator(1)])
    flat_number = forms.IntegerField(required=False)
    zip_code = forms.CharField(max_length=6)
    groups = forms.MultipleChoiceField(choices=groups, widget=forms.CheckboxSelectMultiple)
