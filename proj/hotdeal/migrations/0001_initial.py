# Generated by Django 5.0.4 on 2024-04-19 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ScrappingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('price', models.CharField(max_length=20)),
                ('category', models.CharField(max_length=20)),
                ('shop', models.CharField(max_length=20)),
                ('delivery_fee', models.CharField(max_length=20)),
                ('url', models.CharField(max_length=100)),
            ],
        ),
    ]
