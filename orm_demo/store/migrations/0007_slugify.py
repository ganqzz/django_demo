# Generated by Django 3.1.3 on 2021-02-28 21:29

from django.db import migrations
from django.utils.text import slugify


def slugify_product_titles(apps, schema_editor):
    Product = apps.get_model("store", "Product")

    # Better: filter(...)update(F)
    for p in Product.objects.filter(slug=""):
        p.slug = slugify(p.name)
        p.save()


def undo_slugify(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0006_auto_20210228_2041'),
    ]

    operations = [
        migrations.RunPython(slugify_product_titles, reverse_code=undo_slugify)
    ]