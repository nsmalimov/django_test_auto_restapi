# Generated by Django 2.2.6 on 2019-10-17 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('population', models.IntegerField()),
            ],
            options={
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('position', models.CharField(choices=[('tester', 'Тестировщик'), ('developer', 'Разработчик'), ('CTO', 'CTO')], default='CTO', max_length=15)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.City')),
                ('supervisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.Person')),
            ],
            options={
                'db_table': 'person',
            },
        ),
        migrations.CreateModel(
            name='JobInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_field', models.CharField(max_length=100)),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Person')),
            ],
            options={
                'db_table': 'job_info',
            },
        ),
    ]
