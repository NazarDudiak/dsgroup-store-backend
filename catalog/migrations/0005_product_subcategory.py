from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('catalog', '0004_brand_attributedefinition_product_brand_and_more')]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.SlugField(blank=True, db_index=True, help_text='For example: powerbanks or over-ear-headphones.', max_length=80),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['status', 'subcategory'], name='catalog_pro_status_47b79d_idx'),
        ),
    ]
