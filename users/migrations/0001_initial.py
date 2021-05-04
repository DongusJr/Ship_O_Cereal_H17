# Generated by Django 3.2 on 2021-05-04 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0003_auto_20210504_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PreviousOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_purchases', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ZipCodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip', models.IntegerField()),
                ('city_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.IntegerField()),
                ('username', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=256, unique=True)),
                ('address', models.CharField(max_length=128)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.previousorders')),
                ('zip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.zipcodes')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='prev',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.previousorders'),
        ),
    ]
