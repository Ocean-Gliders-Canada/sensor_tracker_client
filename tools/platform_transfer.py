import copy
from datetime import datetime
from sensor_tracker_client import sensor_tracker_client as sta

sta.basic.DEBUG = True
# Todo: format check
sta.basic.DEBUG_HOST = "http://127.0.0.1:8000/"
sta.authentication.token = "token"


def platform_transfer(target_platform_name, new_platform_name, new_serial_number, instrument_end_time=None):
    platform_obj = sta.platform.get({"name": target_platform_name})
    platform_dict = platform_obj.dict[0]
    platform_name = platform_dict["name"]
    instrument_on_platform = sta.instrument_on_platform.get({"platform_name": platform_name})
    # create new platform on server with given name
    new_platform_dict = copy.deepcopy(platform_dict)
    new_platform_dict["name"] = new_platform_name
    new_platform_dict["serial_number"] = new_serial_number
    sta.platform.post(new_platform_dict)
    the_instrument_on_platform_dict_list = instrument_on_platform.dict
    new_platform_id = sta.platform.get({"name": new_platform_name}).dict[0]["id"]
    for x in the_instrument_on_platform_dict_list:
        if x["end_time"] is None:
            sta.instrument_on_platform.patch(x["id"], {"end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            sta.instrument_on_platform.post(
                {"start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "instrument": x["instrument"],
                 "platform": new_platform_id})


if __name__ == '__main__':
    platform_transfer("otn200", "new_platform", 200)
