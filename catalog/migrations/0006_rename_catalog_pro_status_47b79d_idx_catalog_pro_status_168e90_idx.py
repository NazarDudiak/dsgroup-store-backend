from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [('catalog', '0005_product_subcategory')]

    operations = [
        migrations.RenameIndex(
            model_name='product',
            new_name='catalog_pro_status_168e90_idx',
            old_name='catalog_pro_status_47b79d_idx',
        ),
    ]
