from sensor_tracker_client import sensor_tracker_client as sta


def platform_clone():
    if not sta.authentication.token:
        msg = "Please setup the user's authentication before use this funciton"
        raise msg
