"""
Platform ask for Name, wmo id and serial number
"""
import os
import csv
import copy
import json
from app_common.utilities.file_prepare import check_create_dir

from tools.tools import save_instrument_and_sensor_data, take_off_instruments_from_platform, prior_post_for_instrument, \
    prior_post_for_sensors, post_for_sensors, prior_for_post_sensor_on_instrument, post_for_sensor_on_instrument, \
    save_get_to_csv


def read_from_csv_to_dict(file_path):
    with open(file_path, mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]: rows[1] for rows in reader}
    return mydict


def dict_to_csv(the_dicts, output_path):
    with open(output_path, 'w') as f:
        csvwriter = csv.writer(f)
        if the_dicts:
            csvwriter.writerow(the_dicts[0].keys())
            for x in the_dicts:
                csvwriter.writerow(x.values())


class PostPackage:
    def __init__(self, post_function, post_dict_list):
        self.post_function = post_function
        self.post_dict_list = post_dict_list
        self.post_items = []
        self.post_res_dict = []
        self.id_replacement_dict = dict()

    def generate(self):
        for x in self.post_dict_list:
            self.post_items.append(PostCell(self.post_function, x))

    def post(self):
        for x in self.post_items:
            res = x.post()
            self.post_res_dict.append(res)
        return self.post_res_dict

    def generate_id_replacement_list(self):
        for index, value in enumerate(self.post_res_dict):
            if value:
                self.id_replacement_dict[self.post_dict_list[index]["id"]] = value["id"]
        return self.id_replacement_dict


class PostCell:
    def __init__(self, post_function, post_dict):
        self.post_function = post_function
        self.post_dict = post_dict
        self.post_result = None

    def post(self):
        the_dict = copy.deepcopy(self.post_dict)
        if "id" in the_dict:
            the_dict.pop("id")
        res = self.post_function(the_dict)
        if res.status_code == 201:
            self.post_result = json.loads(res.text)
        return self.post_result


class PlatformClone:
    def __init__(self, new_platform: bool, platform_name, target_platform_name, output_dir, serial_number=None,
                 wmo_id=None):
        """

        :param new_platform:
        :param platform_name:
        :param target_platform_name:
        :param output_dir:
        :param serial_number:
        :param wmo_id:
        """
        self.new_platform = new_platform
        self.platform_name = platform_name
        self.target_platform_name = target_platform_name
        self.serial_number = serial_number
        self.wmo_id = wmo_id
        self.output_dir = os.path.join(output_dir, platform_name)
        check_create_dir(self.output_dir)
        self.get_output_dir = os.path.join(self.output_dir, "get")
        check_create_dir(self.get_output_dir)
        self.prior_post_output_dir = os.path.join(self.output_dir, "prior_post")
        check_create_dir(self.prior_post_output_dir)
        self.post_output_dir = os.path.join(self.output_dir, "post")
        check_create_dir(self.post_output_dir)
        self.get_data_dict = dict()
        self.prior_data_dict = dict()
        self.post_data_dict = dict()
        self.post_package_dict = dict()
        self.platform_id = None
        self.get_platform_dict = None
        self.get_instrument_dict = None
        self.get_instrument_on_platform_dict = None
        self.get_sensor_dict = None
        self.get_sensor_on_instrument_dict = None
        self.instrument_id_list = None
        self.employed_sensor_id_list = None
        self.filtered_instrument_list = None
        self.post_instrument_list = None
        self.instrument_id_replacement_dict = dict()
        self.sensor_id_replacement_dict = dict()
        self.filtered_sensor_list = None

    def clone(self):
        # get all necessary
        get_file_prefix = "get"
        platform_res, instrument_res, instrument_on_platform_res, sensor_res, sensor_on_instrument_res \
            = save_instrument_and_sensor_data(
            self.platform_name, self.output_dir, get_file_prefix)
        if self.new_platform:
            """If the target platform doesn't not exist
            create the platform first"""
            ...
        else:
            """Take the instruments off from the target platform"""
            take_off_instruments_from_platform(self.platform_name)

    def get_data(self):
        target_platform_res, instrument_res, instrument_on_platform_res, sensor_res, sensor_on_instrument_res \
            = save_instrument_and_sensor_data(
            self.target_platform_name, self.get_output_dir, "get")

        platform_res = save_get_to_csv("platform", {"name": self.platform_name}, self.get_output_dir, "get_to")
        self.get_data_dict["get_platform"] = platform_res.dict
        self.get_data_dict["get_target_platform"] = target_platform_res.dict
        self.get_data_dict["get_instrument"] = instrument_res.dict
        self.get_data_dict["get_instrument_on_platform"] = instrument_on_platform_res.dict
        self.get_data_dict["get_sensor"] = sensor_res.dict
        self.get_data_dict["get_sensor_on_instrument"] = sensor_on_instrument_res.dict
        self.platform_id = self.get_data_dict["get_platform"][0]["id"]

    # if previous step was finished, start to create instruments
    def create_pre_instrument_dict(self, get_instrument_dict, instrument_on_platform_res):
        instrument_id_list = []
        for res in instrument_on_platform_res:
            if res["end_time"] is None:
                instrument_id_list.append(res["instrument"])
        self.instrument_id_list = instrument_id_list
        filtered_instrument_list = prior_post_for_instrument(get_instrument_dict, instrument_id_list)
        self.filtered_instrument_list = filtered_instrument_list
        return self.filtered_instrument_list

    def create_instrument_id_replacement_dict(self):

        if len(self.post_instrument_list) != len(self.filtered_instrument_list):
            raise AttributeError
        else:
            for index, post_instrument in enumerate(self.post_instrument_list):
                self.instrument_id_replacement_dict[post_instrument["id"]] = self.filtered_instrument_list[index]["id"]

    def create_sensor_id_replacement_dict(self):
        if len(self.post_sensor_list) != len(self.filtered_sensor_list):
            raise AttributeError
        else:
            for index, post_sensor in enumerate(self.post_sensor_list):
                self.sensor_id_replacement_dict[self.filtered_sensor_list["id"]] = \
                    self.filtered_instrument_list[index]["id"]

    def create_sensor(self):
        res = None
        if True:
            # this place is for taking data from csv or from the original step
            res = self.create_prior_post_sensor()

        post_res = post_for_sensors(res)

        prior_post_sensor_on_instrument = []
        for x in self.get_sensor_on_instrument_dict:
            if not x["end_time"]:
                prior_post_sensor_on_instrument.append(copy.deepcopy(x))

        prior_for_post_sensor_on_instrument_res = prior_for_post_sensor_on_instrument(
            self.get_sensor_on_instrument_dict, self.sensor_id_replacement_dict,
            self.instrument_id_replacement_dict)

        dict_to_csv(prior_for_post_sensor_on_instrument_res,
                    os.path.join(self.prior_post_output_dir, "prior_post_for_sensor_on_instrument.csv"))
        if True:
            post_for_sensor_on_instrument(prior_for_post_sensor_on_instrument_res)

    def create_prior_post_sensor(self):
        instrument_ids = []
        for instrument in self.get_data_dict["get_instrument"]:
            if instrument["identifier"] == "m" or instrument["identifier"] == "c":
                instrument_ids.append((instrument["id"]))

        self.employed_sensor_id_list = []
        for sensor_on_instrument in self.get_data_dict["get_sensor_on_instrument"]:
            if not sensor_on_instrument["end_time"]:
                if sensor_on_instrument["instrument"] in instrument_ids:
                    self.employed_sensor_id_list.append(sensor_on_instrument["sensor"])

        res = prior_post_for_sensors(self.get_data_dict["get_sensor"], self.employed_sensor_id_list)
        dict_to_csv(res, os.path.join(self.prior_post_output_dir, "prior_post_for_sensor.csv"))
        self.filtered_sensor_list = res
        return res
