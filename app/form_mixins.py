#coding: utf-8
from django.template.defaultfilters import filesizeformat
from EmploymentAgency.settings import *
from django import forms


class ImageFormMixin(object):
    def clean_image(self, image_name):
        file = self.cleaned_data[image_name]
        if hasattr(file, 'content_type'):
            file_type = file.content_type.split('/')[0]
            if file_type in IMAGE_CONTENT_TYPES:
                if file._size > MAX_UPLOAD_SIZE:
                    raise forms.ValidationError(u'Размер изображения должен быть в пределах %s. Размер загружаемого фото: %s' % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(file._size)))
            else:
                raise forms.ValidationError(u'Неподдерживаемый формат изображений')
            return file
        else:
            return file
