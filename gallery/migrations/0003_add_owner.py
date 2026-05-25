from django.db import migrations, models
import django.conf


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_alter_recipephoto_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipephoto',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE, related_name='photos', to=django.conf.settings.AUTH_USER_MODEL),
        ),
    ]
