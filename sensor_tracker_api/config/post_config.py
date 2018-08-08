class PostConfig(object):
    REPLACEMENT_VARIABLE = {
        "deployment": [{"platform_name": "platform_id"}, {"power_type__name": "power_type_id"},
                       {"institution__name": "institution_id"}, {"project_name": "project_id"}]
    }

