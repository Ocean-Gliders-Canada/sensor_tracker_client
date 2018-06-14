class Config(object):
    FORMAT = {
        "deployment_format": [("wmo_id",), ("deployment_number",), ("platform_name",), ("power_type", "name"),
                              ("title",),
                              ("start_time",), ("end_time",), ("testing_mission",), ("comment",), ("acknowledgement",),
                              ("contributor_name",),
                              ("creator_name",), ("contributor_role",), ("creator_email",), ("creator_name",),
                              ("creator_url",),
                              ("institution", "name"), ("project", "name"),
                              ("data_repository_link",), ("publisher_email",),
                              ("publisher_name",), ("publisher_url",), ("metadata_link",), ("references",),
                              ("sea_name",),
                              ("latitude",), ("longitude",), ("depth",)],
        "platform_format": [
            ("name",), ("institution", "name"),
            ("platform_type", "model"), ("purchase_date",), ("wmo_id",), ("serial_number",)
        ],
        "sensor_format": [
            ("identifier",), ("long_name",), ("standard_name",), ("accuracy",), ("resolution",), ("valid_min",),
            ("valid_max",), ("instrument", "short_name"),
            ("include_in_output",), ("display_in_web_interface",), ("comment",)
        ],
        "instrument_format": [
            ("id",), ("identifier",), ("short_name",), ("long_name",), ("manufacturer", "name"), ("manufacturer_id",),
            ("serial",),
            ("comment",)
        ],
        "platform_instrument_format": [
            ("instrument", "identifier"), ("instrument", "id"), ("platform", "name"), ("platform", "id"),
            ("start_time",),
            ("end_time",), ("comment",)
        ],
        "platform_type_format": [
            ("id",), ("model",), ("manufacturer", "name"), ("manufacturer", "id")
        ],
        "manufacturer": [
            ("province",), ("city",), ("name",), ("country",), ("street",), ("postal_code",), ("contact_email",),
            ("contact_name",), ("contact_phone",), ("id",)
        ]
    }

    SENSOR_TRACKER_CONNECTOR = 'http://bugs.ocean.dal.ca/sensor_tracker/api/'
    SENSOR_TRACKER_LOCAL_URL = "http://127.0.0.1:8000/api/"
    GLIDER_TYPE = ["Wave", "Slocum"]
