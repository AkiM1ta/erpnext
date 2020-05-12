from __future__ import unicode_literals
from frappe import _

def get_data():
    return [
      {
        "label":_("General Management"),
        "icon": "octicon octicon-briefcase",
        "items": [
            {
                "type": "doctype",
                "name": "general_project",
                "description": _("Project master."),
                "onboard": 1,
            },
            {
                "type": "doctype",
                "name": "general_task",
                "route": "#List/general_task",
                "description": _("Project activity / task."),
                "onboard": 1,
            },
            {
                "type": "report",
                "route": "#List/general_task/Gantt",
                "doctype": "general_task",
                "name": "Gantt Chart",
                "description": _("Gantt chart of all tasks."),
                "onboard": 1,
            },
            {
                "type": "doctype",
                "name": "general_template",
                "description": _("Make project from a template."),
            },
          ]
      }
  ]