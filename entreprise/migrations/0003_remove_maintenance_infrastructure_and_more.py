# Generated by Django 4.2.1 on 2023-06-05 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entreprise', '0002_employe_structure_alter_infrastructure_responsable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintenance',
            name='infrastructure',
        ),
        migrations.AddField(
            model_name='maintenance',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='maintenance',
            name='machine',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='entreprise.machine'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='date_maintenance',
            field=models.DateField(auto_now=True),
        ),
    ]
