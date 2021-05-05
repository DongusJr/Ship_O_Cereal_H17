# Generated by Django 3.2 on 2021-05-04 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_products_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listedas',
            old_name='name',
            new_name='tag',
        ),
        migrations.AddField(
            model_name='products',
            name='in_stock',
            field=models.IntegerField(default=1),
        ),
    ]