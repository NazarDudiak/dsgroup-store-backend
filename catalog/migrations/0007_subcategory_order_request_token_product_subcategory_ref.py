from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('catalog', '0006_rename_catalog_pro_status_47b79d_idx_catalog_pro_status_168e90_idx')]

    operations = [
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seo_title', models.CharField(blank=True, max_length=60, verbose_name='SEO title')),
                ('seo_description', models.CharField(blank=True, max_length=160, verbose_name='SEO description')),
                ('name', models.CharField(max_length=100)), ('slug', models.SlugField(max_length=120)),
                ('description', models.TextField(blank=True)), ('is_active', models.BooleanField(default=True)),
                ('sort_order', models.PositiveSmallIntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='catalog.category')),
            ],
            options={'ordering': ['sort_order', 'name']},
        ),
        migrations.AddConstraint(model_name='subcategory', constraint=models.UniqueConstraint(fields=('category', 'slug'), name='unique_subcategory_per_category')),
        migrations.AddField(model_name='order', name='request_token', field=models.UUIDField(blank=True, editable=False, null=True, unique=True)),
        migrations.AddField(model_name='product', name='subcategory_ref', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='catalog.subcategory', verbose_name='subcategory')),
    ]
