# -*- coding: utf-8 -*-
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Div, Field, HTML
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from users.models import UserProfile


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    Div(
                        Field('username', ),
                        css_class='col-lg-4 col-md-4 col-sm-8'
                    ),
                    css_class='row justify-content-center'
                ),
                Div(
                    Div(
                        Field('pwd', ),
                        css_class='col-lg-4 col-md-4 col-sm-8'
                    ),
                    css_class='row justify-content-center'
                ),
                Div(
                    Div(
                        Field(HTML(_(u'¿No te acuerdas? Hazlo <a href="/reset_password">aqu&iacute;</a>')), ),
                        css_class='col-lg-4 col-md-4 col-sm-8'
                    ),
                    css_class='row justify-content-center'
                ),

                FormActions(
                    Div(
                        Div(
                            Div(
                                Submit('submit', _(u"Iniciar sesión"), css_class='btn btn-primary mr-3'),
                                css_class='row justify-content-end'
                            ),
                            css_class='col-lg-4 col-md-4 col-sm-8'
                        ),
                        css_class='row justify-content-center'
                    )
                )
            )
        )

    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', _(u'Only alphanumeric characters are allowed.'))

    username = forms.CharField(label=_(u"Nombre de usuario"), help_text='', validators=[alphanumeric])
    pwd = forms.CharField(label=_(u"Contraseña"), widget=forms.PasswordInput())


class SignupForm(ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Fieldset(
            '',
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ),
        FormActions(Div(
                        Div(
                            Submit('submit', _(u"Registrarse"), css_class='btn btn-primary'),
                        css_class='col-lg-12 col-md-12 col-sm-12 col-xs-12 mx-auto'),
                    css_class='row')
        )
    )

    username = forms.RegexField(label=_("Username"), max_length=30,
                                regex=r'^[0-9a-zA-Z]*$',
                                help_text=_(u"Requerido. Menos de 30 caracteres. Letras y números"),
                                error_messages={
                                    'invalid': _(u"Este campo solo puede contener letras y números")})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        labels = {
            'first_name': _(u'Nombre'),
            'last_name': _(u'Apellido'),
            'username': _(u'Nombre de usuario'),
            'email': _(u'Correo electrónico'),
            'password': _(u'Contraseña'),
        }
        email = {
            'required': True
        }
        widgets = {
            'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class UserModelForm(ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Fieldset(
            '',
            Div(
                Div(
                    Field('first_name',),
                    css_class='col-lg-6 col-md-6 col-sm-10'
                ),
                css_class='row justify-content-center'
            ),
            Div(
                Div(
                    Field('last_name',),
                    css_class='col-lg-6 col-md-6 col-sm-10'
                ),
                css_class='row justify-content-center'
            ),
            Div(
                Div(
                    Field('email',),
                    css_class='col-lg-6 col-md-6 col-sm-10'
                ),
                css_class='row justify-content-center'
            ),
        )
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': _(u'Nombre'),
            'last_name': _(u'Apellido'),
            'email': _(u'Correo electrónico'),
        }
        email = {
            'required': True
        }

    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class UserProfileModelForm(ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Fieldset(
            '',
            Div(
                Div(
                    Field('bio', ),
                    css_class='col-lg-6 col-md-6 col-sm-10'
                ),
                css_class='row justify-content-center'
            ),
            Div(
                Div(
                    Field('photo', ),
                    css_class='col-lg-6 col-md-6 col-sm-10'
                ),
                css_class='row justify-content-center'
            ),
        ),
        FormActions(
            Div(
                Div(
                    Div(
                        Submit('submit', _(u"Actualizar"), css_class='btn btn-warning'),
                        css_class='row justify-content-end'
                    ),
                    css_class='col-lg-6 col-md-6 col-sm-10'
                ),
                css_class='row justify-content-center'
            )
        )
    )

    class Meta:
        model = UserProfile
        fields = ['bio', 'photo']


class PasswordResetRequestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PasswordResetRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    Div(
                        Field('email_or_username', ),
                        css_class='col-lg-4 col-md-4 col-sm-8'
                    ),
                    css_class='row justify-content-center'
                ),
                FormActions(
                    Div(
                        Div(
                            Div(
                                Submit('submit', _(u"Recuperar"), css_class='btn btn-primary mr-3'),
                                css_class='row justify-content-end'
                            ),
                            css_class='col-lg-4 col-md-4 col-sm-8'
                        ),
                        css_class='row justify-content-center'
                    )
                )
            )
        )

    email_or_username = forms.CharField(label=_(u"Email Or Username"), max_length=254)


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    Div(
                        Field('new_password1', ),
                        css_class='col-lg-4 col-md-4 col-sm-8'
                    ),
                    css_class='row justify-content-center'
                ),
                Div(
                    Div(
                        Field('new_password2', ),
                        css_class='col-lg-4 col-md-4 col-sm-8'
                    ),
                    css_class='row justify-content-center'
                ),
                FormActions(
                    Div(
                        Div(
                            Div(
                                Submit('submit', _(u"Guardar"), css_class='btn btn-primary'),
                                css_class='row justify-content-end'
                            ),
                            css_class='col-lg-4 col-md-4 col-sm-8'
                        ),
                        css_class='row justify-content-center'
                    )
                )
            )
        )

    error_messages = {
        'password_mismatch': _(u"The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=_(u"New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_(u"New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2
