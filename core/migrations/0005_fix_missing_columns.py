from django.db import migrations, connection

def add_missing_columns(apps, schema_editor):
    cursor = connection.cursor()

    # Verifica colunas da tabela requisition
    cursor.execute("PRAGMA table_info(core_requisition);")
    columns = [col[1] for col in cursor.fetchall()]

    # Se icon_url não existir, cria
    if "icon_url" not in columns:
        cursor.execute("ALTER TABLE core_requisition ADD COLUMN icon_url varchar(255);")

    # Verifica colunas da tabela product
    cursor.execute("PRAGMA table_info(core_product);")
    columns = [col[1] for col in cursor.fetchall()]

    # Se image_url não existir, cria
    if "image_url" not in columns:
        cursor.execute("ALTER TABLE core_product ADD COLUMN image_url varchar(255);")


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_order_options_remove_product_image_and_more'),
    ]

    operations = [
        migrations.RunPython(add_missing_columns),
    ]
