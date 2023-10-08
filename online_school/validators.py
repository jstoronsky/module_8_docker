from rest_framework.serializers import ValidationError


class VideoLinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link = dict(value).get(self.field)
        if link is not None and 'youtube.com' not in link:
            raise ValidationError('This link can not be used')
