# Generated by Django 5.0.2 on 2024-08-26 11:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images')),
                ('details', models.TextField()),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Instructors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=80, unique=True)),
                ('instructor_first_name', models.CharField(max_length=200)),
                ('instructor_last_name', models.CharField(max_length=200)),
                ('courses_assigned', models.IntegerField(blank=True, null=True)),
                ('number_of_students', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='instructor_images')),
                ('instructor_id', models.CharField(blank=True, max_length=8, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Instructor',
                'verbose_name_plural': 'Instructors',
            },
        ),
        migrations.CreateModel(
            name='MainCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'MainCategory',
                'verbose_name_plural': 'MainCategories',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('details', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('course_code', models.CharField(max_length=25)),
                ('course_status', models.CharField(choices=[('qualifications', 'Qualifications'), ('courses', 'Courses')], max_length=14)),
                ('course_type', models.CharField(choices=[('online', 'Online'), ('on demand', 'On Demand'), ('class room', 'Class Room')], max_length=10)),
                ('duration', models.CharField(max_length=45)),
                ('days_per_week', models.PositiveIntegerField()),
                ('enrolled_courses', models.BooleanField(default=False)),
                ('number_of_students', models.IntegerField(blank=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='courses.category')),
                ('instructor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='courses.instructors')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='mainCategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='courses.maincategory'),
        ),
    ]
