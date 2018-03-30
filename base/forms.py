from django import forms


class EffectForm(forms.Form):

    def __init__(self, *args, **kwargs):
        if kwargs.get('extra'):
            extra_fields = kwargs.pop('extra')
        else:
            extra_fields = {}
        super().__init__(*args, **kwargs)
        for key, val in extra_fields.items():
            self.fields['effect_{}'.format(key)] = forms.CharField(label=key)

    def extra_fields(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('effect_'):
                yield (self.fields[name].label, value)
