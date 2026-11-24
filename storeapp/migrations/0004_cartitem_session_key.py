from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("storeapp", "0003_cart_item"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart_item",
            name="session_key",
            field=models.CharField(blank=True, db_index=True, default="", max_length=40),
        ),
    ]
