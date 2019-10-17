from django.db import models

class Person(models.Model):
    TESTER = 'tester'
    DEVELOPER = 'developer'
    CTO = 'CTO'

    POSITIONS_CHOICES = (
        (TESTER, 'Тестировщик'),
        (DEVELOPER, 'Разработчик'),
        (CTO, 'CTO'),
    )

    name = models.CharField(max_length=30)
    city = models.ForeignKey(
        'City',
        on_delete=models.CASCADE,
    )
    position = models.CharField(max_length=15,
                                choices=POSITIONS_CHOICES,
                                default=CTO)
    supervisor = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        db_table = "person"


class City(models.Model):
    name = models.CharField(max_length=40)
    population = models.IntegerField()

    class Meta:
        db_table = "city"


class JobInfo(models.Model):
    director = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
        null=False
    )
    activity_field = models.CharField(max_length=100)

    class Meta:
        db_table = "job_info"
