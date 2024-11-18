from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    university = models.CharField(max_length=255, verbose_name="Университет")
    faculty = models.CharField(max_length=255, verbose_name="Факультет")
    specialty = models.CharField(max_length=255, verbose_name="Специальность")

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ['last_name']


class Employer(models.Model):
    company_name = models.CharField(max_length=255, verbose_name="Название компании")
    contact_person = models.CharField(max_length=255, verbose_name="Контактное лицо")
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    industry = models.CharField(max_length=255, verbose_name="Отрасль")
    location = models.CharField(max_length=255, verbose_name="Местоположение компании")

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Работодатель"
        verbose_name_plural = "Работодатели"
        ordering = ['company_name']


class Internship(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name="internships")
    position = models.CharField(max_length=255, verbose_name="Должность на стажировке")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    description = models.TextField(verbose_name="Описание стажировки")
    status = models.CharField(max_length=50, choices=[('active', 'Активная'),
                                                      ('completed', 'Завершена'),
                                                      ('cancelled', 'Отменена')],
                              default='active', verbose_name="Статус")

    def __str__(self):
        return f'{self.position} ({self.start_date} - {self.end_date})'

    class Meta:
        verbose_name = "Стажировка"
        verbose_name_plural = "Стажировки"
        ordering = ['start_date']


class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="applications")
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name="applications")
    application_date = models.DateField(verbose_name="Дата подачи заявки")
    status = models.CharField(max_length=50, choices=[('pending', 'Ожидает рассмотрения'),
                                                      ('approved', 'Одобрена'),
                                                      ('rejected', 'Отклонена')],
                              default='pending', verbose_name="Статус заявки")

    def __str__(self):
        return f'{self.student}'

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['application_date']


class Report(models.Model):
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name="reports")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="reports")
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name="reports")
    submission_date = models.DateField(verbose_name="Дата подачи отчета")
    content = models.TextField(verbose_name="Содержание отчета")
    rating = models.IntegerField(verbose_name="Оценка работодателя", choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f'{self.student}'

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"
        ordering = ['submission_date']


class Review(models.Model):
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name="reviews")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="reviews")
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(verbose_name="Оценка", choices=[(i, i) for i in range(1, 6)])
    feedback = models.TextField(verbose_name="Отзыв")

    def __str__(self):
        return f'{self.student}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['rating']


class User(models.Model):
    username = models.CharField(max_length=255, unique=True, verbose_name="Имя пользователя")
    password_hash = models.CharField(max_length=255, verbose_name="Хэш пароля")
    role = models.CharField(max_length=50, choices=[('student', 'Студент'),
                                                    ('employer', 'Работодатель'),
                                                    ('admin', 'Администратор')],
                            verbose_name="Роль")
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email")
    last_login = models.DateTimeField(auto_now=True, verbose_name="Дата последнего входа")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['username']
