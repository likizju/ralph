# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ralph.discovery.models import Device


def get_device_components(sn=None, barcode=None):
    """Yields dicts describing all device components to be taken in assets"""
    if sn:
        try:
            ralph_device = Device.objects.get(sn=sn)
        except Device.DoesNotExist:
            raise LookupError('Device not found')
    elif barcode:
        try:
            ralph_device = Device.objects.get(barcode=barcode)
        except Device.DoesNotExist:
            raise LookupError('Device not found')
    if ralph_device:
        components = ralph_device.get_components()
        for processor in components.get('processors', []):
            yield {
                'model_proposed': processor.model.name,
            }
        for memory in components.get('memory', []):
            yield {
                'model_proposed': memory.model.name,
            }
        for storage in components.get('storages', []):
            yield {
                'model_proposed': storage.model.name,
                'sn': storage.sn,
            }
        for ethernet in components.get('ethernets', []):
            yield {
                'model_proposed': unicode(ethernet),
                'sn': ethernet.mac,
            }
        for fibrechannel in components.get('fibrechannels', []):
            yield {
                'model_proposed': fibrechannel.model.name,
            }
