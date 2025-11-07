from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from ipam.models import IPAddress, Prefix
from .models import GeoIP

MONITORED_MODELS = [IPAddress, Prefix]


@receiver(post_delete)
def delete_related_object(sender, instance, **kwargs):
    if sender not in MONITORED_MODELS:
        return
    content_type = ContentType.objects.get_for_model(sender)
    GeoIP.objects.filter(object_type=content_type, object_id=instance.pk).delete()


@receiver(post_save)
def create_or_update_related_object(sender, instance, **kwargs):
    if sender not in MONITORED_MODELS:
        return
    content_type = ContentType.objects.get_for_model(sender)
    if instance.custom_field_data['geoip_feed']:
        obj, created = GeoIP.objects.get_or_create(object_type=content_type, object_id=instance.pk)
        if not created:
            obj.save()
    else:
        GeoIP.objects.filter(object_type=content_type, object_id=instance.pk).delete()
