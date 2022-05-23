#
# Copyright (c) 2017-2019 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 3 (GPLv3). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv3
# along with this software; if not, see
# https://www.gnu.org/licenses/gpl-3.0.txt.
#

"""Models system fingerprints."""

import uuid

from api.common.common_report import (REPORT_TYPE_CHOICES,
                                      REPORT_TYPE_DEPLOYMENT)

from django.db import models


class DeploymentsReport(models.Model):
    """Represents deployment report."""

    report_type = models.CharField(
        max_length=11,
        choices=REPORT_TYPE_CHOICES,
        default=REPORT_TYPE_DEPLOYMENT
    )
    report_version = models.CharField(max_length=64,
                                      null=False)
    report_platform_id = models.UUIDField(
        default=uuid.uuid4, editable=False)

    STATUS_PENDING = 'pending'
    STATUS_FAILED = 'failed'
    STATUS_COMPLETE = 'completed'
    STATUS_CHOICES = ((STATUS_PENDING, STATUS_PENDING),
                      (STATUS_FAILED, STATUS_FAILED),
                      (STATUS_COMPLETE, STATUS_COMPLETE))

    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    report_id = models.IntegerField(null=True)
    cached_fingerprints = models.TextField(null=True)
    cached_masked_fingerprints = models.TextField(null=True)
    cached_csv = models.TextField(null=True)
    cached_masked_csv = models.TextField(null=True)
    cached_insights = models.TextField(null=True)

    def __str__(self):
        """Convert to string."""
        return '{' +\
            'id:{}, report_id: {}, status:{}'.format(
                self.id,
                self.report_id,
                self.status) + '}'


class SystemFingerprint(models.Model):
    """Represents system fingerprint."""

    # Important: If you add a DATE field, add it to list
    DATE_FIELDS = ['system_last_checkin_date',
                   'system_creation_date']

    BARE_METAL = 'bare_metal'
    UNKNOWN = 'unknown'
    VIRTUALIZED = 'virtualized'
    HYPERVISOR = 'hypervisor'

    SOURCE_TYPE = (
        ('network', 'Ansible'),
        ('vcenter', 'VCenter'),
        (UNKNOWN, 'Unknown')
    )

    INFRASTRUCTURE_TYPE = (
        (BARE_METAL, 'Bare Metal'),
        (VIRTUALIZED, 'Virtualized'),
        (HYPERVISOR, 'Hypervisor'),
        (UNKNOWN, 'Unknown')
    )

    # Scan information
    deployment_report = models.ForeignKey(
        DeploymentsReport, models.CASCADE, related_name='system_fingerprints')

    # Common facts
    name = models.CharField(max_length=256, unique=False, blank=True, null=True)
    os_name = models.CharField(max_length=64, unique=False, blank=True, null=True)
    os_release = models.CharField(max_length=128, unique=False, blank=True, null=True)
    os_version = models.CharField(max_length=64, unique=False, blank=True, null=True)

    infrastructure_type = models.CharField(max_length=12, choices=INFRASTRUCTURE_TYPE)

    cloud_provider = models.CharField(
        max_length=16, unique=False, blank=True, null=True
    )

    mac_addresses = models.TextField(unique=False, blank=True, null=True)
    ip_addresses = models.TextField(unique=False, blank=True, null=True)

    cpu_count = models.PositiveIntegerField(unique=False, blank=True, null=True)

    architecture = models.CharField(max_length=64, unique=False, blank=True, null=True)

    # Network scan facts
    bios_uuid = models.CharField(max_length=36, unique=False, blank=True, null=True)
    subscription_manager_id = models.CharField(
        max_length=36, unique=False, blank=True, null=True
    )

    cpu_socket_count = models.PositiveIntegerField(unique=False, blank=True, null=True)
    cpu_core_count = models.FloatField(unique=False, blank=True, null=True)
    cpu_core_per_socket = models.PositiveIntegerField(
        unique=False, blank=True, null=True
    )
    cpu_hyperthreading = models.NullBooleanField()

    system_creation_date = models.DateField(blank=True, null=True)
    system_last_checkin_date = models.DateField(blank=True, null=True)

    system_purpose = models.TextField(unique=False, blank=True, null=True)
    system_role = models.CharField(max_length=128, unique=False, blank=True, null=True)
    system_addons = models.TextField(unique=False, blank=True, null=True)
    system_service_level_agreement = models.CharField(
        max_length=128, unique=False, blank=True, null=True
    )
    system_usage_type = models.CharField(
        max_length=128, unique=False, blank=True, null=True
    )
    insights_client_id = models.CharField(
        max_length=128, unique=False, blank=True, null=True
    )

    virtualized_type = models.CharField(
        max_length=64, unique=False, blank=True, null=True
    )
    virtual_host_name = models.CharField(
        max_length=128, unique=False, blank=True, null=True
    )
    virtual_host_uuid = models.CharField(
        max_length=36, unique=False, blank=True, null=True
    )

    system_user_count = models.PositiveIntegerField(unique=False, blank=True, null=True)
    user_login_history = models.TextField(unique=False, blank=True, null=True)

    # VCenter scan facts
    vm_state = models.CharField(max_length=24, unique=False, blank=True, null=True)
    vm_uuid = models.CharField(max_length=36, unique=False, blank=True, null=True)
    vm_dns_name = models.CharField(max_length=256, unique=False, blank=True, null=True)
    vm_host_socket_count = models.PositiveIntegerField(
        unique=False, blank=True, null=True
    )
    vm_host_core_count = models.PositiveIntegerField(
        unique=False, blank=True, null=True
    )
    vm_cluster = models.CharField(max_length=128, unique=False, blank=True, null=True)
    vm_datacenter = models.CharField(
        max_length=128, unique=False, blank=True, null=True
    )

    # Red Hat facts
    is_redhat = models.NullBooleanField()
    redhat_certs = models.TextField(unique=False, blank=True, null=True)
    # pylint: disable=invalid-name
    redhat_package_count = models.PositiveIntegerField(
        unique=False, blank=True, null=True
    )

    metadata = models.TextField(unique=False, null=False)
    sources = models.TextField(unique=False, null=False)
    etc_machine_id = models.CharField(
        max_length=48, unique=False, blank=True, null=True
    )

    def __str__(self):
        """Convert to string."""
        return '{' + 'id:{}, '\
            'deployment_report:{}, ' \
            'name:{}, '\
            'os_name:{}, '\
            'os_version:{}, '\
            'os_release:{}, '\
            'mac_addresses:{}, '\
            'ip_addresses:{}, '\
            'cpu_count:{}, '\
            'bios_uuid:{}, '\
            'subscription_manager_id:{}, '\
            'cpu_socket_count:{}, '\
            'cpu_core_count:{}, '\
            'cpu_core_per_socket:{}, '\
            'cpu_hyperthreading:{}, '\
            'system_creation_date:{}, '\
            'system_purpose:{}, '\
            'system_role:{}, '\
            'system_addons:{}, '\
            'system_service_level_agreement:{}, '\
            'system_usage_type:{}, '\
            'insights_client_id:{}, '\
            'infrastructure_type:{}, '\
            'cloud_provider:{}, '\
            'virtualized_type:{}, '\
            'vm_state:{}, '\
            'vm_uuid:{}, '\
            'vm_dns_name:{}, '\
            'virtual_host_name:{}, '\
            'virtual_host_uuid:{}, '\
            'vm_host_socket_count:{}, '\
            'vm_host_core_count:{}, '\
            'vm_datacenter:{}, '\
            'vm_cluster:{}, '\
            'is_redhat:{}, '\
            'redhat_certs:{}, '\
            'redhat_package_count:{}, '\
            'architecture:{}, '\
            'sources:{}, '\
            'system_user_count:{}, '\
            'user_login_history:{}, '\
            'metadata:{} '.format(self.id,
                                  self.deployment_report.id,
                                  self.name,
                                  self.os_name,
                                  self.os_version,
                                  self.os_release,
                                  self.mac_addresses,
                                  self.ip_addresses,
                                  self.cpu_count,
                                  self.bios_uuid,
                                  self.subscription_manager_id,
                                  self.cpu_socket_count,
                                  self.cpu_core_count,
                                  self.cpu_core_per_socket,
                                  self.cpu_hyperthreading,
                                  self.system_creation_date,
                                  self.system_purpose,
                                  self.system_role,
                                  self.system_addons,
                                  self.system_service_level_agreement,
                                  self.system_usage_type,
                                  self.insights_client_id,
                                  self.infrastructure_type,
                                  self.cloud_provider,
                                  self.virtualized_type,
                                  self.vm_state,
                                  self.vm_uuid,
                                  self.vm_dns_name,
                                  self.virtual_host_name,
                                  self.virtual_host_uuid,
                                  self.vm_host_socket_count,
                                  self.vm_host_core_count,
                                  self.vm_datacenter,
                                  self.vm_cluster,
                                  self.is_redhat,
                                  self.redhat_certs,
                                  self.redhat_package_count,
                                  self.architecture,
                                  self.sources,
                                  self.system_user_count,
                                  self.user_login_history,
                                  self.metadata) + '}'


class Product(models.Model):
    """Represents a product."""

    PRESENT = 'present'
    ABSENT = 'absent'
    POTENTIAL = 'potential'
    UNKNOWN = 'unknown'
    PRESENCE_TYPE = (
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
        (POTENTIAL, 'Potential'),
        (UNKNOWN, 'Unknown')
    )

    fingerprint = models.ForeignKey(SystemFingerprint,
                                    models.CASCADE,
                                    related_name='products')
    name = models.CharField(max_length=256, unique=False, null=False)
    version = models.TextField(unique=False, null=True)
    presence = models.CharField(
        max_length=10, choices=PRESENCE_TYPE)

    metadata = models.TextField(unique=False, null=False)

    def __str__(self):
        """Convert to string."""
        return '{' + 'id:{}, '\
            'fingerprint:{}, ' \
            'name:{}, '\
            'version:{}, '\
            'presence:{}, '\
            'metadata:{} '.format(self.id,
                                  self.fingerprint.id,
                                  self.name,
                                  self.version,
                                  self.presence,
                                  self.metadata) + '}'


class Entitlement(models.Model):
    """Represents a Entitlement."""

    fingerprint = models.ForeignKey(SystemFingerprint,
                                    models.CASCADE,
                                    related_name='entitlements')
    name = models.CharField(max_length=256, unique=False, null=True)
    entitlement_id = models.CharField(max_length=256, unique=False, null=True)

    metadata = models.TextField(unique=False, null=False)

    def __str__(self):
        """Convert to string."""
        return '{' + 'id:{}, '\
            'fingerprint:{}, ' \
            'name:{}, '\
            'entitlement_id:{}, '\
            'metadata:{} '.format(self.id,
                                  self.fingerprint.id,
                                  self.name,
                                  self.entitlement_id,
                                  self.metadata) + '}'
