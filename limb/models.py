import uuid
import pytz

from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.base_user import AbstractBaseUser

from .validators import (JsonValidator, schema_emails,
                         schema_phone_numbers, schema_social_networks)


TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class NaturalPerson(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True, editable=False)
    uid = models.UUIDField(unique=True, editable=False,
                           default='', verbose_name='Идентификационный номер')
    phone_number = models.CharField(
        max_length=16, unique=True,
        validators=[RegexValidator(regex=r'^\+\d{9,15}$')],
        verbose_name='Номер телефона',
        help_text='Пример заполнения: +79012314483'
    )
    additional_phone_numbers = models.JSONField(
        default=list, blank=True,
        validators=[JsonValidator(limit_value=schema_phone_numbers)],
        verbose_name='Дополнительные номера',
        help_text='Пример заполнения: ["+79012314483", "+79012314483"]'
    )

    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество')

    creation_date = models.DateTimeField(auto_now_add=True,
                                         verbose_name='Дата создания')
    change_date = models.DateTimeField(auto_now=True,
                                       verbose_name='Дата изменения')
    status_change_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата изменения статуса'
    )

    status = models.CharField(max_length=10,
                              choices=[('active', 'Активен'),
                                       ('not_active', 'Не активен')],
                              default='active', verbose_name='Статус')
    client_type = models.CharField(max_length=8,
                                   choices=[('primary', 'Первичный'),
                                            ('repeated', 'Повторный'),
                                            ('external', 'Внешний'),
                                            ('indirect', 'Косвенный')],
                                   default='primary', verbose_name='Тип')
    email = models.JSONField(
        default=list, blank=True,
        validators=[JsonValidator(limit_value=schema_emails)],
        verbose_name='E-mail (почта)',
        help_text='Пример заполнения: ["n@mail.ru", "n@mail.ru"]'
    )
    gender = models.CharField(max_length=10,
                              choices=[('male', 'Мужской'),
                                       ('female', 'Женский'),
                                       ('unknown', 'Неизвестно')],
                              default='unknown', verbose_name='Пол')
    time_zone = models.CharField(max_length=32, choices=TIMEZONES,
                                 default='Europe/Moscow',
                                 verbose_name='Часовой пояс')
    social_networks = models.JSONField(
        default=dict, blank=True,
        validators=[JsonValidator(limit_value=schema_social_networks)],
        verbose_name='Социальные сети',
        help_text='Пример заполнения: {<br>\
            "VK": ["https://vk.com/"],<br>\
            "FB": ["https://ru-ru.facebook.com/"],<br>\
            "ОК": "https://ru-ru.facebook.com/",<br>\
            "Instagram": "https://ru-ru.facebook.com/",<br>\
            "Telegram": "https://ru-ru.facebook.com/",<br>\
            "WhatsApp": "https://ru-ru.facebook.com/",<br>\
            "Viber": "https://ru-ru.facebook.com/"<br>\
        }'
    )

    password = None
    last_login = None
    username = ''
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'Физическое лицо (клиент)'
        verbose_name_plural = 'Физические лица (клиенты)'

    def __str__(self):
        return self.phone_number

    # Реализация отслеживания даты изменения статуса.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.snapshot_status = self.status

    def save(self, *args, **kwargs):
        self.uid = uuid.uuid1(node=1)

        if self.snapshot_status != self.status:
            self.status_change_date = timezone.now()
        return super().save(*args, **kwargs)


class LegalEntity(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    uid = models.UUIDField(unique=True, editable=False,
                           default='', verbose_name='Идентификационный номер')

    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )
    change_date = models.DateTimeField(auto_now=True,
                                       verbose_name='Дата изменения')

    name = models.CharField(max_length=255, verbose_name='Полное название')
    abbreviation = models.CharField(max_length=100,
                                    verbose_name='Сокращенное название')

    inn = models.PositiveBigIntegerField(verbose_name='ИНН', unique=True)
    kpp = models.PositiveBigIntegerField(verbose_name='КПП')

    class Meta:
        verbose_name = 'Юридическое лицо'
        verbose_name_plural = 'Юридические лица'

    def __str__(self):
        return str(self.inn)

    def save(self, *args, **kwargs):
        self.uid = uuid.uuid1(node=2)
        return super().save(*args, **kwargs)


class Department(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    uid = models.UUIDField(unique=True, editable=False,
                           default='', verbose_name='Идентификационный номер')
    name = models.CharField(max_length=255, unique=True,
                            verbose_name='Название')
    legal_entity = models.ManyToManyField(
        'LegalEntity', blank=True, related_name='departments', default=None,
        verbose_name='Юридическое лицо'
    )
    natural_person = models.ManyToManyField(
        'NaturalPerson', blank=True, related_name='departments', default=None,
        verbose_name='Физическое лицо (клиент)',
        through='DepartmentNaturalPerson',
        through_fields=('department_id', 'naturalperson_id')
    )

    parent_department = models.ForeignKey(
        'self', null=True, blank=True, related_name='children_departments',
        default=None, on_delete=models.CASCADE,
        verbose_name='Вышестоящий департамент'
    )
    nesting_level = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.uid = uuid.uuid1(node=3)

        if self.parent_department:
            if self.parent_department.nesting_level == 6:
                raise ValidationError('Достигнута максимальная вложенность!')
            else:
                self.nesting_level = self.parent_department.nesting_level + 1
        return super().save(*args, **kwargs)


class DepartmentNaturalPerson(models.Model):
    department_id = models.ForeignKey('Department', on_delete=models.CASCADE)
    naturalperson_id = models.ForeignKey(
        'NaturalPerson', on_delete=models.CASCADE,
        verbose_name='Физическое лицо (клиент)'
    )
    date_added = models.DateTimeField(
        verbose_name='Дата добавления клиента в департамент',
        blank=True, null=True, auto_now_add=True
    )

    class Meta:
        verbose_name = 'Физическое лицо (клиент)'
        verbose_name_plural = 'Физические лица (клиенты)'
        auto_created = True
