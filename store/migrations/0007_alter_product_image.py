# Generated by Django 4.2.16 on 2024-10-23 20:04

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='products/', verbose_name='Image'),
        ),
    ]
