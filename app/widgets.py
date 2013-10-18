#coding: utf-8
from django import forms
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput, CheckboxInput
import string


class BootstrapMixin(object):
    bootstrap_class_1 = 'form-control'
    bootstrap_class_2 = 'input-sm'

    def add_bootstrap_class(self, class_name, attrs=None):
        if attrs is not None:
            sCssClasses = attrs.pop('class', '')
            aCssClasses = string.split(sCssClasses, ' ')
            if class_name not in aCssClasses:
                sCssClasses += ' %s' % class_name
                attrs['class'] = sCssClasses
        else:
            attrs = {'class': class_name}
        return attrs

    def __init__(self, attrs=None):
        attrs = self.add_bootstrap_class(self.bootstrap_class_1, attrs)
        attrs = self.add_bootstrap_class(self.bootstrap_class_2, attrs)
        super(BootstrapMixin, self).__init__(attrs)


class BootstrapTextInput(BootstrapMixin, forms.TextInput):
    pass


class BootstrapSelect(BootstrapMixin, forms.Select):
    pass


class BootstrapDateInput(BootstrapMixin, forms.DateInput):
    pass


class BootstrapNumberInput(BootstrapMixin, forms.NumberInput):
    pass


class BootstrapTextarea(BootstrapMixin, forms.Textarea):
    pass


class BootstrapImage(forms.ClearableFileInput):
    initial_text = ''
    input_text = ''
    clear_checkbox_label = ''

    def __init__(self, *args, **kwargs):

        self.url_length = kwargs.pop('url_length',30)
        self.preview = kwargs.pop('preview',True)
        self.image_width = kwargs.pop('image_width',200)
        super(BootstrapImage, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None,):

        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'

        substitutions['input'] = super(forms.ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):

            template = self.template_with_initial
            if self.preview:
                substitutions['initial'] = (u'<br>\
                <a href="{0}" target="_blank"><img src="{0}" width="{2}"></a><br>'.format
                    (escape(value.url),'...'+escape(force_unicode(value))[-self.url_length:],
                     self.image_width))
            else:
                substitutions['initial'] = (u'<a href="{0}">{1}</a>'.format
                    (escape(value.url),'...'+escape(force_unicode(value))[-self.url_length:]))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)

