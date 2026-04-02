import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0002_update_accounts_models"),
        ("automation", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LLM",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.FloatField(default=0)),
                ("insights_strategic", models.TextField(blank=True, null=True)),
                ("recommended_outreach_ways", models.TextField(blank=True, null=True)),
                ("decision_maker_level", models.CharField(blank=True, max_length=100, null=True)),
                ("prompt", models.TextField(blank=True, null=True)),
                ("raw_response", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "lead",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="analyses",
                        to="automation.leads",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lead_analyses",
                        to="accounts.user",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="llm",
            constraint=models.UniqueConstraint(
                fields=("user", "lead"),
                name="unique_analysis_per_user_and_lead",
            ),
        ),
    ]
