# Generated by Django 5.2.4 on 2025-07-09 07:16

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('html', models.TextField(verbose_name='Question Text')),
                ('is_published', models.BooleanField(default=False, verbose_name='Has been published?')),
                ('maximum_marks', models.DecimalField(decimal_places=2, default=4, max_digits=6, verbose_name='Maximum Marks')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Is this answer correct?')),
                ('html', models.TextField(verbose_name='Choice Text')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='quizapp.question')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuizProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('total_score', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total Score')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AttemptedQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Was this attempt correct?')),
                ('marks_obtained', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Marks Obtained')),
                ('selected_choice', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quizapp.choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.question')),
                ('quiz_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='quizapp.quizprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
