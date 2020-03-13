import os
import json
from tools.clone.platform_setup_clone import PlatformClone, dict_to_csv, PostPackage
from tools.tools import post_instruments, prior_post_for_instrument_on_platform, post_instrument_on_platform, \
    prior_for_post_sensor_on_instrument
from sensor_tracker_client import sensor_tracker_client as sta

# sta.basic.DEBUG_HOST = "http://localhost:8000/"
sta.authentication.token = "1537ded79296862c889ffe368b9decc3b9c2afe1"
# sta.basic.DEBUG = True

pc = PlatformClone(True, "otn200", "scotia", "/Users/xiang/project/sensor_tracker_api/test/tools/output")

pc.get_data()
instrument_dict = pc.get_data_dict["get_instrument"]

pc.create_pre_instrument_dict(pc.get_data_dict["get_instrument"], pc.get_data_dict["get_instrument_on_platform"])

dict_to_csv(pc.filtered_instrument_list, os.path.join(pc.prior_post_output_dir, "prior_instrument.csv"))

post_package_for_post_instrument = PostPackage(sta.instrument.post, pc.filtered_instrument_list)
post_package_for_post_instrument.generate()
post_package_for_post_instrument.post()
pc.instrument_id_replacement_dict = post_package_for_post_instrument.generate_id_replacement_list()

instrument_on_platform_pres = prior_post_for_instrument_on_platform(post_package_for_post_instrument.post_res_dict,
                                                                    pc.platform_id, "2010-10-01 00:00:00")

# print(instrument_on_platform_pres)
dict_to_csv(instrument_on_platform_pres, os.path.join(pc.prior_post_output_dir, "prior_instrument_on_platform.csv"))
post_instrument_on_platform_res = post_instrument_on_platform(instrument_on_platform_pres)
# print(post_instrument_on_platform_res)
# then create sensors and connect it to the

sensor_filtered_pre_post_res = pc.create_prior_post_sensor()

post_package_for_post_sensor = PostPackage(sta.sensor.post, sensor_filtered_pre_post_res)

post_package_for_post_sensor.generate()
post_package_for_post_sensor.post()
replace_id_sensor_list = post_package_for_post_sensor.generate_id_replacement_list()
# print(replace_id_sensor_list)

sensor_on_instrument_pre_post = prior_for_post_sensor_on_instrument(pc.get_data_dict["get_sensor_on_instrument"],
                                                                    replace_id_sensor_list,
                                                                    pc.instrument_id_replacement_dict)
# print(sensor_on_instrument_pre_post)

post_package_for_sensor_on_instrument = PostPackage(sta.sensor_on_instrument.post, sensor_on_instrument_pre_post)
post_package_for_sensor_on_instrument.generate()
post_package_for_sensor_on_instrument.post()
print(post_package_for_sensor_on_instrument.post_res_dict)
