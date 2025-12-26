# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='avatar',
            field=models.ImageField(blank=True, help_text='Аватар художника (если не указан, используется портрет)', null=True, upload_to='artists/avatars/', verbose_name='Аватар'),
        ),
        migrations.AddField(
            model_name='artist',
            name='has_social_networks',
            field=models.BooleanField(default=False, help_text='Отметьте, если у художника есть социальные сети', verbose_name='Есть социальные сети'),
        ),
    ]

