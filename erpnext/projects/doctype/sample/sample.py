from __future__ import unicode_literals
import frappe

from frappe.model.document import Document
import random


class Sample(Document):
    def after_insert(self):
        if self.sample_no:
            frappe.db.set_value("Sample", self.name, "sample_number",
                                self.sample_no + "-" + str(random.randint(999, 9999)))
