# Generated for Практическая работа № 11.
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes_app', '0002_alter_route_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='routes/',
                verbose_name='Изображение',
            ),
        ),
    ]
