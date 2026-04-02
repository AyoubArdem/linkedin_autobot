import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0002_update_accounts_models"),
    ]

    operations = [
        migrations.CreateModel(
            name="Leads",
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
                ("full_name", models.CharField(max_length=255)),
                ("url", models.URLField()),
                ("title", models.CharField(blank=True, max_length=255)),
                ("location", models.CharField(blank=True, max_length=255)),
                ("experience", models.TextField(blank=True)),
                ("about", models.TextField(blank=True)),
                ("score", models.FloatField(default=0)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "NEW"),
                            ("contacted", "CONTACTED"),
                            ("converted", "CONVERTED"),
                        ],
                        default="new",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="leads",
                        to="accounts.workspace",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="LeadInteraction",
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
                ("message", models.TextField(blank=True, null=True)),
                ("sent_at", models.DateTimeField(auto_now_add=True)),
                ("response", models.TextField(blank=True, null=True)),
                ("response_at", models.DateTimeField(blank=True, null=True)),
                (
                    "lead",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interactions",
                        to="automation.leads",
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interactions",
                        to="accounts.workspace",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LeadTAG",
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
                ("name", models.CharField(max_length=50)),
                (
                    "leads",
                    models.ManyToManyField(
                        blank=True,
                        related_name="tags",
                        to="automation.leads",
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lead_tags",
                        to="accounts.workspace",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="leads",
            constraint=models.UniqueConstraint(
                fields=("workspace", "url"),
                name="unique_lead_url_per_workspace",
            ),
        ),
        migrations.AddConstraint(
            model_name="leadtag",
            constraint=models.UniqueConstraint(
                fields=("workspace", "name"),
                name="unique_tag_name_per_workspace",
            ),
        ),
    ]
