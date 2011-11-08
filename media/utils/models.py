from django.db import models
import forms

class CNPJField(models.CharField):
    """
    """
    empty_strings_allowed = False
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 18
        models.CharField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        from django.contrib.localflavor.br.forms import BRCNPJField
        defaults = {'form_class': BRCNPJField}
        defaults.update(kwargs)
        return super(models.CharField, self).formfield(**defaults)


class NARADateField(models.DateField):
    """
    """
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.NARADateField}
        defaults.update(kwargs)
        return super(NARADateField, self).formfield(**defaults)

    def value_to_string(self, obj):
        val = self._get_val_from_obj(obj)
        if val is None:
            data = ''
        else:
            data = datetime_safe.new_date(val).strftime("%d/%m/%Y")
        return data

