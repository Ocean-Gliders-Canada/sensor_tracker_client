import copy
import json
import time
from datetime import datetime
from sensor_tracker_client import sensor_tracker_client as sta


def instrument_transfer(from_platform_name, to_platform_name, new_platform_serial_number=None,
                        instrument_end_time=None):
    """
    Transfer instruments from one platform to another platform

    :param from_platform_name:
    :param to_platform_name:
    :param new_platform_serial_number:
    :param instrument_end_time:
    :return:
    """
    if not sta.authentication.token:
        msg = "You must set sta authentication before use this function"
        raise msg
    from_platform_obj = sta.platform.get({"name": from_platform_name})
    platform_dict = from_platform_obj.dict[0]
    platform_name = platform_dict["name"]

    # create new platform on server with given name if the platform is not exist
    to_platform_obj = sta.platform.get({"name": to_platform_name})
    if to_platform_obj.dict:
        to_platform_id = to_platform_obj.dict[0]["id"]
    else:
        new_platform_dict = copy.deepcopy(platform_dict)
        new_platform_dict["name"] = to_platform_name
        if new_platform_serial_number:
            new_platform_dict["serial_number"] = new_platform_serial_number
        else:
            msg = "Platform {} is not exist. Serial Number is required for create a new platform number"
            raise msg
        res = sta.platform.post(new_platform_dict)
        if res.status_code == 201:
            ret_dict = json.dumps(res.text)
            to_platform_id = ret_dict["id"]
        else:
            msg = "Failed to create an new platform\n {}".format(res.text)
            raise msg

    if instrument_end_time:
        try:
            time.strptime(instrument_end_time, "%Y-%m-%d %H:%M:%S")
        except:
            msg = "instrument_end_time {} doesn't match the time format \"%Y-%m-%d %H:%M:%S\""
            raise msg


    instrument_on_platform = sta.instrument_on_platform.get({"platform_name": platform_name})
    the_instrument_on_platform_dict_list = instrument_on_platform.dict
    for x in the_instrument_on_platform_dict_list:
        if x["end_time"] is None:
            if instrument_end_time:
                sta.instrument_on_platform.patch(x["id"], {"end_time": instrument_end_time})
            else:
                sta.instrument_on_platform.patch(x["id"], {"end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            sta.instrument_on_platform.post(
                {"start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "instrument": x["instrument"],
                 "platform": to_platform_id})
