# Generated by Django 4.2.7 on 2025-07-17 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_media_alter_postlike_options_remove_post_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='posts.postcomment', verbose_name='Commentaire parent'),
        ),
    ]
