class PostConfig(object):
    REPLACEMENT_VARIABLE = {
        "deployment": {"platform_name": ("platform_id", "get_platform_id"),
                       "power_type__name": ("power_type_id", "get_power_id"),
                       "institution__name": ("institution_id", "get_institution_id"),
                       "project__name": ("project_id", "get_project_id")}
    }

    UNIQUE_VARIABLE = {
        "deployment": ["title"]
    }

    SEARCH_KEY = {
        "deployment": ["platform_name", "start_time"],
        "instrument": ["identifier"],
        "sensor": ["identifier"]
    }

    POST_VALUE_TYPE = {
        "deployment": [int, int, int, int, int, str, str, "date", "date", bool, str, str,
                       str, str, str, str, str, str, str, str, str, str, str, str,
                       float, float, float]
    }
