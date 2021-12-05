import jsonschema

from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError


schema_emails = {
    "type": "array",
    "items": {
        "type": "string",
        "format": "email"
    }
}

schema_phone_numbers = {
    "type": "array",
    "items": {
        "type": "string",
        "pattern": "^\+\d{9,15}$"
    }
}

schema_social_networks = {
    "type": "object",
    "properties": {
        "VK": {
            "type": "array",
            "items": {
                "format": "uri"
            }
        },
        "FB": {
            "type": "array",
            "items": {
                "format": "uri"
            },
        },
        "ОК": {
            "type": "string",
            "format": "uri"
        },
        "Instagram": {
            "type": "string",
            "format": "uri"
        },
        "Telegram": {
            "type": "string",
            "format": "uri"
        },
        "WhatsApp": {
            "type": "string",
            "format": "uri"
        },
        "Viber": {
            "type": "string",
            "format": "uri"
        },
    }
}


class JsonValidator(BaseValidator):
    def compare(self, value, schema):
        try:
            jsonschema.validate(
                value, schema,
                format_checker=jsonschema.draft7_format_checker
            )
        except jsonschema.exceptions.ValidationError:
            raise ValidationError(
                '%(value)s ошибка валидации, введите данные по примеру!',
                params={'value': value}
            )
