import copy
from datetime import datetime
from sensor_tracker_client import sensor_tracker_client as sta

sta.basic.DEBUG_HOST = "http://glidertest.ocean.dal.ca/sensor_tracker/"
sta.authentication.token = "1537ded79296862c889ffe368b9decc3b9c2afe1"
sta.basic.DEBUG = True


def take_off_instruments_from_platform(platform_name):
    """Given a platform name, then search for all instrument which currently attached to it. and then put a end time for it
    """
    # First find all instrument on the platform
    instrument_on_platform = sta.instrument_on_platform.get({"platform_name": platform_name}).dict
    # put end time for the instrument on platform

    copy_instrument_on_platform = []
    for x in instrument_on_platform:
        if x["end_time"] is None:
            copy_instrument_on_platform.append(x)
    for item in copy_instrument_on_platform:
        item["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # patch_the_new_instrument_on_platform
    for x in copy_instrument_on_platform:
        copyed_x = copy.deepcopy(x)
        the_id = copyed_x.pop("id")

        b = sta.instrument_on_platform.patch(the_id, copyed_x)


take_off_instruments_from_platform("Nemesis")
