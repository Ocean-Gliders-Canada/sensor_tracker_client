import json
import pandas as pd

deployment_format = [("wmo_id",), ("deployment_number",), ("platform_name",), ("power_type", "name"), ("title",),
                     ("start_time",), ("end_time",), ("testing_mission",), ("comment",), ("acknowledgement",),
                     ("contributor_name",),
                     ("creator_name",), ("contributor_role",), ("creator_email",), ("creator_name",),
                     ("creator_url",),
                     ("data_repository_link",), ("publisher_email",),
                     ("publisher_name",), ("publisher_url",), ("metadata_link",), ("references",), ("sea_name",),
                     ("latitude",), ("longitude",), ("depth",)]

platform_format = [
    ("name",), ("institution", "name"),
    ("platform_type", "model"), ("purchase_date",), ("wmo_id",), ("serial_number",)
]

sensor_format = [
    ("identifier",), ("long_name",), ("accuracy",), ("resolution",), ("valid_min",), ("valid_max",),
    ("include_in_output",), ("display_in_web_interface",), ("comment",)
]

instrument_format = [
    ("")
]


def parser(content, format):
    table_rows = []
    for item in content:
        row = row_parser(format, item)
        table_rows.append(row)
    return table_rows


def row_parser(format, item):
    row = []
    for i in format:
        res = get_content(i, item)
        row.append(res)

    return row


def get_content(format, item):
    res = None
    for x in format:
        if item and x in item:
            res = item[x]
        item = res

    return res


def create_pandas_header(format):
    header = []
    for x in format:
        name = get_name(x)
        header.append(name)
    return header


def get_name(item):
    name = ""
    for x in item:
        name = name + x
    return name


def create_pandas(header, content):
    df = pd.DataFrame(content, columns=header)
    return df


from sensor_tracker_api.api_old import AccessApi

api = AccessApi(debug=True)
# b = api.get_platform_deployment("Fundy", "2018-05-17 16:02:26")
b = api.get_deployments("Slocum")

content = parser(b, deployment_format)
header = create_pandas_header(deployment_format)
df = create_pandas(header, content)
print(df)
