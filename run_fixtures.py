"""Utility that runs all fixtures in parent-to-child order."""

from auth.models.fixtures import *

AdminRoleFactory.create()
SupervisorRoleFactory.create()
SupportRoleFactory.create()
DefaultAdminUserFactory.create()