from django import forms


class ActionForm(forms.Form):
    def __init__(self, *args, obj=None, queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = obj
        self.queryset = queryset

    def get_context(self):
        return {}

    def form_action(self, obj, user):
        raise NotImplementedError()

    def save(self, obj=None, user=None):
        try:
            return self.form_action(obj, user)
        except Exception as e:
            print(e)
            error_message = str(e)
            self.add_error(None, error_message)
            raise