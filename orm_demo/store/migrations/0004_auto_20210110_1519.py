# Generated by Django 3.1.3 on 2021-01-20 22:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0003_add_product_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock_count',
            field=models.IntegerField(help_text='How many items are currently in stock.'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              to='store.product')),
            ],
        ),
    ]
