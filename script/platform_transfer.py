import copy

from sensor_tracker_api import sensor_tracker_api as sta

sta.basic.DEBUG = True
# Todo: format check
sta.basic.DEBUG_HOST = "http://glidertest.ocean.dal.ca:8001/"
sta.authentication.token = "1537ded79296862c889ffe368b9decc3b9c2afe1"


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
    print(instrument_on_platform.dict)


if __name__ == '__main__':
    platform_transfer("otn200", "new_platform", 200)
