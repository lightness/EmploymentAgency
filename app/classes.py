from django.core.urlresolvers import reverse, reverse_lazy


ALERT_TYPES = ("alert-success", "alert-info", "alert-warning", "alert-danger",)
BUTTON_TYPES = ("btn-default", "btn-primary", "btn-success", "btn-warning", "btn-danger", "btn-info", "btn-link",)
DEFAULT_ALERT_TYPE = ALERT_TYPES[0]
DEFAULT_BUTTON_TYPE = BUTTON_TYPES[0]


class Alert(object):
    alert_class = None
    text = None
    button_class = None
    button_text = None
    button_redirect_url = None

    def __init__(self, text, **kwargs):
        # text
        self.text = text
        # alert class
        alert_class = kwargs.get('alert_class', DEFAULT_ALERT_TYPE)
        if alert_class in ALERT_TYPES:
            self.alert_class = alert_class
        else:
            self.alert_class = DEFAULT_ALERT_TYPE
        # button class
        button_class = kwargs.get('button_class', DEFAULT_BUTTON_TYPE)
        if button_class in BUTTON_TYPES:
            self.button_class = button_class
        else:
            self.button_class = DEFAULT_BUTTON_TYPE
        # button text
        self.button_text = kwargs.get('button_text', None)
        # button redirect view
        self.button_redirect_url = reverse(kwargs.get('button_redirect_url','Home'))