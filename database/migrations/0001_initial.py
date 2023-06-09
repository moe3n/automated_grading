# Generated by Django 4.0 on 2023-05-24 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='question',
            fields=[
                ('question_id', models.BigAutoField(db_column='question_id', primary_key=True, serialize=False)),
                ('question_number', models.BigIntegerField(db_column='question_number')),
                ('question_text', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='subject',
            fields=[
                ('subject_name', models.CharField(max_length=30)),
                ('subject_id', models.BigAutoField(db_column='subject_id', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('user_id', models.BigAutoField(db_column='user_id', primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='score',
            fields=[
                ('score_id', models.BigAutoField(db_column='score_id', primary_key=True, serialize=False)),
                ('score', models.FloatField()),
                ('response_text', models.CharField(max_length=3000)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.question')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.user')),
            ],
        ),
        migrations.CreateModel(
            name='response',
            fields=[
                ('response_id', models.BigAutoField(db_column='response_id', primary_key=True, serialize=False)),
                ('response_text', models.CharField(max_length=3000)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.question')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.user')),
            ],
        ),
        migrations.CreateModel(
            name='question_set',
            fields=[
                ('set_id', models.BigAutoField(db_column='set_id', primary_key=True, serialize=False)),
                ('set_number', models.IntegerField(db_column='set_number')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.subject')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='set_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.question_set'),
        ),
        migrations.CreateModel(
            name='answer',
            fields=[
                ('answer_id', models.BigAutoField(db_column='answer_id', primary_key=True, serialize=False)),
                ('answer_text', models.CharField(max_length=3000)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.question')),
            ],
        ),
    ]
