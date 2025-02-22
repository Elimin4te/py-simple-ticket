"""Utility that runs all fixtures in parent-to-child order."""

from auth.models.fixtures.roles import *
from auth.models.fixtures.users import *

from tickets.models.fixtures.incidences import *
from tickets.models.fixtures.categories import *

# -------- Roles
AdminRoleFactory.create()
SupervisorRoleFactory.create()
SupportRoleFactory.create()

# -------- Users
DefaultAdminUserFactory.create()
AnalistUserFactory.create_batch(3)

# -------- Incidences
IncidenceFactory.create_batch(8)

# -------- Categories
AppCategoryFactory.create()
GmailCategoryFactory.create()
ExcelCategoryFactory.create()
GmailCategoryFactory.create()
HWCategoryFactory.create()
PrinterCategoryFactory.create()
ATSPrinterCategoryFactory.create()

