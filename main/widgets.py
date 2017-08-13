from django import forms
from django.template.loader import render_to_string


class GoogleMapPointWidget(forms.TextInput):
    def render(self, name, value, attrs):
        lat, lng = 35, 127

        if value:
            lng, lat = value.split(',')

        html = super().render(name, value, attrs)
        rendered = render_to_string('google_map_point_widget.html', {
            'lat': lat,
            'lng': lng,
        })
        return html + rendered

