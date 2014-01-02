from django import forms
from django.core.exceptions import ValidationError

def convert_model_field_to_for_field(f, **kwargs) :
    args = {"error_messages":f.error_messages}
    args.update(kwargs)
    return f.formfield(**args)

class AutoCreateUpdateModelForm(forms.ModelForm) :

    def save(self, commit=True):
        """
        auto update non-None Field by pk
        """
        if self.instance.pk is None:
            fail_message = 'created'
        else:
            fail_message = 'changed'
        ins = forms.save_instance(self, self.instance, self._meta.fields,
                             fail_message, False, construct=False)
        ins.save(update_fields=self.nonNoneFields)
        return ins

    def _clean_fields(self):
        nonNoneFields = set()
        for name, field in self.fields.items():
            value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
            # ignore None value field
            if None == value :
                continue

            nonNoneFields.add(name)

            try:
                if isinstance(field, forms.FileField):
                    initial = self.initial.get(name, field.initial)
                    value = field.clean(value, initial)
                else:
                    value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except ValidationError as e:
                self._errors[name] = self.error_class(e.messages)
                if name in self.cleaned_data:
                    del self.cleaned_data[name]

        self.nonNoneFields = nonNoneFields
