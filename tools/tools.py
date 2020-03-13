import copy
import os
from datetime import datetime
from sensor_tracker_client import sensor_tracker_client as sta


# sta.basic.DEBUG_HOST = "http://localhost:8000/"
# sta.authentication.token = "1537ded79296862c889ffe368b9decc3b9c2afe1"
# sta.basic.DEBUG = True



def take_off_instruments_from_platform(platform_name, end_time=None):
    """Given a platform name, then search for all instrument which currently attached to it. and then put a end time for it
    """
    # First find all instrument on the platform
    instrument_on_platform_rb = sta.instrument_on_platform.get({"platform_name": platform_name})
    instrument_on_platform = instrument_on_platform_rb.dict
    # put end time for the instrument on platform
    copy_instrument_on_platform = []
    for x in instrument_on_platform:
        if x["end_time"] is None:
            copy_instrument_on_platform.append(x)
    for item in copy_instrument_on_platform:
        if end_time:
            item["end_time"] = end_time
        else:
            item["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # patch_the_new_instrument_on_platform
    for x in copy_instrument_on_platform:
        copyed_x = copy.deepcopy(x)
        the_id = copyed_x.pop("id")

        b = sta.instrument_on_platform.patch(the_id, copyed_x)


def save_get_to_csv(get_function_name, get_input, output_dir, file_name_prefix):
    get_function = getattr(sta, get_function_name).get
    output_file_name = file_name_prefix + "_" + get_function_name + ".csv"
    output_file_path = os.path.join(output_dir, output_file_name)
    r_o = get_function(get_input)
    r_o.to_csv(output_file_path)
    return r_o


def save_instrument_and_sensor_data(platform_name, output_dir, file_name_prefix):
    platform_res = save_get_to_csv("platform", {"name": platform_name}, output_dir, file_name_prefix)
    instrument_res = save_get_to_csv("instrument", {"platform_name": platform_name}, output_dir, file_name_prefix)
    instrument_on_platform_res = save_get_to_csv("instrument_on_platform", {"platform_name": platform_name},
                                                 output_dir, file_name_prefix)
    sensor_res = save_get_to_csv("sensor", {"platform_name": platform_name}, output_dir, file_name_prefix)
    sensor_on_instrument_res = save_get_to_csv("sensor_on_instrument", {"platform_name": platform_name},
                                               output_dir, file_name_prefix)
    return platform_res, instrument_res, instrument_on_platform_res, sensor_res, sensor_on_instrument_res


def clean_post_element(instrument_data):
    new_instrument_data = copy.deepcopy(instrument_data)
    # new_instrument_data.pop("modified_date")
    # new_instrument_data.pop("created_date")
    new_instrument_data.pop("comment")
    return new_instrument_data


def prior_post_for_instrument(instrument_dict, instrument_id_list):
    filtered_instrument_list = []
    for instrument in instrument_dict:
        the_id = instrument["id"]
        if the_id in instrument_id_list:
            if instrument["identifier"] == "m" or instrument["identifier"] == "c":
                filtered_instrument_list.append(clean_post_element(instrument))
    return filtered_instrument_list


def post_instruments(filtered_instrument_list):
    res_list = []
    for instrument in filtered_instrument_list:
        res = sta.instrument.post(instrument)
        res_list.append(res)
    return res_list


def prior_post_for_instrument_on_platform(instrument_dicts, platform_id, instrument_start_time=None):
    if not instrument_start_time:
        instrument_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    instrument_on_platform_post_format = {
        "start_time": instrument_start_time,
    }
    instrument_on_platform_post_list = []
    for instrument in instrument_dicts:
        instrument_on_platform_post_item = copy.deepcopy(instrument_on_platform_post_format)
        instrument_on_platform_post_item["instrument"] = instrument["id"]
        instrument_on_platform_post_item["platform"] = platform_id
        instrument_on_platform_post_list.append(instrument_on_platform_post_item)
    return instrument_on_platform_post_list


def post_instrument_on_platform(post_instrument_on_platform_dicts):
    res_list = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for item in post_instrument_on_platform_dicts:
        if "id" in item:
            item.pop("id")
        res = sta.instrument_on_platform.post(item)
        res_list.append(res)
    return res_list


def prior_post_for_sensors(sensor_dicts, sensor_id_list):
    filtered_sensor_list = []
    for sensor in sensor_dicts:
        if sensor["id"] in sensor_id_list:
            filtered_sensor_list.append(clean_post_element(sensor))
    return filtered_sensor_list


def post_for_sensors(sensor_dicts):
    sensor_post_res_list = []
    for sensor in sensor_dicts:
        sensor_post_res_list.append(sta.sensor.post(sensor))
    return sensor_post_res_list


def prior_for_post_sensor_on_instrument(get_sensor_on_instrument_dicts, sensor_id_replace_dict,
                                        instrument_id_replacement_dict):
    filtered_sensor_on_instrument_list = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for sensor_on_instrument in get_sensor_on_instrument_dicts:
        if not sensor_on_instrument["end_time"]:
            sensor_on_instrument["start_time"] = now
            new_sensor_on_instrument = clean_post_element(sensor_on_instrument)
            sensor_id = new_sensor_on_instrument["sensor"]
            instrument_id = new_sensor_on_instrument["instrument"]
            if sensor_id in sensor_id_replace_dict and instrument_id in instrument_id_replacement_dict:
                new_sensor_on_instrument["sensor"] = sensor_id_replace_dict[sensor_id]
                new_sensor_on_instrument["instrument"] = instrument_id_replacement_dict[instrument_id]
                filtered_sensor_on_instrument_list.append(new_sensor_on_instrument)
    return filtered_sensor_on_instrument_list


def post_for_sensor_on_instrument(filtered_sensor_on_instrument_list):
    res_list = []
    for sensor_on_instrument in filtered_sensor_on_instrument_list:
        res_list.append(sta.sensor_on_instrument.post(sensor_on_instrument))
    return res_list

# save_instrument_and_sensor_data("scotia", "/Users/xiang/project/sensor_tracker_api/tools/scotia/", "get")
