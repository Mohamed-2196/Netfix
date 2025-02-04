# Generated by Django 5.1.5 on 2025-01-17 20:04

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_alter_service_company_alter_service_date_and_more'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_value', models.IntegerField(help_text='Rating value between 1 and 5', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('review', models.TextField(blank=True, help_text='Write an optional review', null=True)),
                ('date_rated', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_ratings', to='users.customer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_ratings', to='services.service')),
            ],
            options={
                'unique_together': {('service', 'customer')},
            },
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='rating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_requests', to='services.rating'),
        ),
    ]
