from datetime import date
from django.db import models
from django.core.exceptions import ValidationError

class Group(models.Model):
    DAYS_OF_WEEK = [
        ('Пн', 'Понедельник'),
        ('Вт', 'Вторник'),
        ('Ср', 'Среда'),
        ('Чт', 'Четверг'),
        ('Пт', 'Пятница'),
        ('Сб', 'Суббота'),
        ('Вс', 'Воскресенье'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Название группы')
    description = models.TextField(verbose_name='Описание группы')
    weekdays = models.CharField(max_length=10, verbose_name='Дни недели', help_text='Введите дни недели через запятую (например, "Пн, Вт")')
    start_time = models.TimeField(verbose_name='Начало')
    end_time = models.TimeField(verbose_name='Конец')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    is_permanent = models.BooleanField(default=False, verbose_name='Постоянная событие')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def clean(self):
        if self.weekdays:
            days = [day.strip() for day in self.weekdays.split(',')]
            for day in days:
                if day not in dict(self.DAYS_OF_WEEK):
                    raise ValidationError(f'Неверный день недели: {day}. Допустимые: {", ".join(dict(self.DAYS_OF_WEEK).keys())}.')

            if len(days) > 2:
                raise ValidationError('Можно указать не более двух дней.')
            
        if self.start_time >= self.end_time:
            raise ValidationError('Начало события должно быть раньше конца.')

    def __str__(self):
        return f"{self.name} ({self.weekdays})"



class Customer(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')

    def calculate_age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        if 11 <= age % 100 <= 19:  # Обработка исключений для чисел от 11 до 19
            suffix = "лет"
        else:
            last_digit = age % 10
            if last_digit == 1:
                suffix = "год"
            elif 2 <= last_digit <= 4:
                suffix = "года"
            else:
                suffix = "лет"
        return f"{age} {suffix}"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Attendance(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
    date = models.DateField(verbose_name='Дата')
    is_present = models.BooleanField(default=False, verbose_name='Посещение')

    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'
        unique_together = ('customer', 'group', 'date')