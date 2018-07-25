# -*- coding: utf-8 -*-
import datetime

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, Field
from django.utils.translation import ugettext as _
from articles.models import Article
from django import forms


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class ArticleForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Fieldset(
            '',
            Div(
                Div(
                    Field('title', ),
                    css_class='col-lg-6 col-md-6 col-sm-10'
                ),
                css_class='row justify-content-center'
            ),
            Div(
                Div(
                    Field('media', ),
                    css_class='col-lg-6 col-md-6 col-sm-10'
                ),
                css_class='row justify-content-center'
            ),
            Div(
                Div(
                    Field('introduction', ),
                    css_class='col-lg-6 col-md-6 col-sm-10'
                ),
                css_class='row justify-content-center'
            ),
            Div(
                Div(
                    Field('text', ),
                    css_class='col-lg-6 col-md-6 col-sm-10'
                ),
                css_class='row justify-content-center'
            ),
            Div(
                Div(
                    Field('categories', ),
                    css_class='col-lg-6 col-md-6 col-sm-10'
                ),
                css_class='row justify-content-center'
            ),
            Div(
                Div(
                    Field('publication_date', ),
                    css_class='col-lg-6 col-md-6 col-sm-10'
                ),
                css_class='row justify-content-center'
            ),
            FormActions(
                Div(
                    Div(
                        Div(
                            Submit('submit', _(u"Guardar artículo"), css_class='btn btn-primary'),
                            css_class='row justify-content-end'
                        ),
                        css_class='col-lg-6 col-md-6 col-sm-10'
                    ),
                    css_class='row justify-content-center'
                )
            )
        )
    )

    publication_date = forms.DateTimeField(label=_(u"Fecha de publicación"), required=True, widget=DateTimeInput,
                                           input_formats=['%Y-%m-%dT%H:%M'], initial=datetime.date.today())

    class Meta:
        model = Article
        exclude = ['user', 'article_answered']
