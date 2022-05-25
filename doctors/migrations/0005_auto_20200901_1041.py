# Generated by Django 3.0.7 on 2020-09-01 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0004_speciality_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialityCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.CharField(blank=True, max_length=225, null=True)),
                ('image_url', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Speciality Type',
                'verbose_name_plural': 'Speciality Types',
            },
        ),
        migrations.AlterModelOptions(
            name='speciality',
            options={'verbose_name': 'speciality', 'verbose_name_plural': 'specialities'},
        ),
        migrations.RemoveField(
            model_name='speciality',
            name='description',
        ),
        migrations.AddField(
            model_name='speciality',
            name='speciality_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='doctors.SpecialityCategory'),
        ),
    ]