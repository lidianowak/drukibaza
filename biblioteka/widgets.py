from django.forms.widgets import SelectMultiple
from django.urls import reverse
from django.utils.safestring import mark_safe


class SelectMultipleWithAddButton(SelectMultiple):
    add_url_name = None

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)

        if not self.add_url_name:
            return html

        url = reverse(self.add_url_name)

        return mark_safe(
            html +
            f'''
            <div style="margin-top:4px;">
                <a href="{url}" target="_blank" class="button">
                    ➕ Dodaj nowy obiekt
                </a>
            </div>
            '''
        )