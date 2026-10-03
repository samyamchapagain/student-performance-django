
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=20)),
                ('ethnicity', models.CharField(max_length=20)),
                ('parental_education', models.CharField(max_length=100)),
                ('lunch', models.CharField(max_length=30)),
                ('test_prep_course', models.CharField(max_length=30)),
                ('math_score', models.IntegerField()),
                ('reading_score', models.IntegerField()),
                ('writing_score', models.IntegerField()),
                ('predicted_grade', models.CharField(max_length=5)),
                ('predicted_level', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
