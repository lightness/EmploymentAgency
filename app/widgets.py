#coding: utf-8
from django import forms
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