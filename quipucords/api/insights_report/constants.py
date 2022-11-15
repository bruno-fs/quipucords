# Copyright (C) 2022  Red Hat, Inc.

# This software is licensed to you under the GNU General Public License,
# version 3 (GPLv3). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv3
# along with this software; if not, see
# https://www.gnu.org/licenses/gpl-3.0.txt.

"""Insights report constants module."""

CANONICAL_FACTS = (
    "bios_uuid",
    "insights_id",
    "ip_addresses",
    "mac_addresses",
    "provider_id",
    "provider_type",
    "satellite_id",
    "subscription_manager_id",
    # the next two were added in yuptoo
    # https://github.com/RedHatInsights/yuptoo/blob/591add7518671bfaef64cb2b2afefbf908885d61/yuptoo/processor/utils.py#L27
    "etc_machine_id",
    "vm_uuid",
)
