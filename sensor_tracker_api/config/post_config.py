class PostConfig(object):
    REPLACEMENT_VARIABLE = {
        "deployment": [{"platform_name": ("platform_id", "get_platform_id")},
                       {"power_type__name": ("power_type_id", "get_power_id")},
                       {"institution__name": ("institution_id", "get_institution_id")},
                       {"project_name": ("project_id",)}]
    }

    UNIQUE_VARIABLE = {
        "deployment": ["title"]
    }

    SEARCH_KEY = {
        "deployment": ["platform_name", "start_time"],
        "instrument": ["identifier"],
        "sensor": ["identifier"]
    }
