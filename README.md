
Sensor Tracker Api Library
=============

This library provides a pure Python interface for the Sensor Tracker Api


Installing
----------

Install through pip:

    pip install git+https://gitlab.oceantrack.org/ceotr/metadata-tracker/tracker_api.git


Usage Examples
--------------
 
The API is exposed via the ``sensor_tracker_api``  class.

For starters, the library is using singleton pattern. The object will be instantiated as soon as you import the class.

    >>> from sensor_tracker_api import sensor_tracker_api as sta

Make sure to set up the basic configurations before using the other functions. It only needs to be configured once at the beginning of the script.

    >>> # Basic setup
    >>> sta.basic.DEBUG = True # Turn on the debug mode, the default is False
    >>> # When debug mode is on, the HOST link will point to DEBUG HOST.
    >>> sta.basic.DEBUG_HOST = 'http://127.0.0.1:8000/' # Default DEBUG HOST is "http://127.0.0.1:8000/"

**NOTE**: As the debug mode is off, ``sensor_tracker_api`` is pointed to the CEOTR [Sensor Tracker API server](http://bugs.ocean.dal.ca/sensor_tracker/)


The sensor tracker api requires the use of token or username and password for POST and PUT operations. GET doesn't require authentication.

    >>> sta.authentication.token = "your_token"
    >>> # or
    >>> sta.authentication.username = "your_username"
    >>> sta.authentication.password = "your_password"

To see if your credentials are successful:

    >>>


### GET Operations

The usage format of get operation:

    # For full list
    response_data = sta.target_model.get()
    # For filter
    response_data = sta.target_model.get({"filter name":"filter value"})

##### Institutions

To fetch full list of institutions

    >>> institution_res = sta.institution.get()

To fetch institutions with name OTN

    >>> institution_res2 = sta.institution.get({"name": "OTN"})


##### Response data

All GET operations will return a ``response_data`` object, which contains results and can be converted into
different format such as dictionary

    >>> institution_res_dict = institution_res.dict

##### Project

To fetch full list of project

    >>> project_res = sta.project.get()

To fetch project with name "Gulf of St. Lawrence Animal Tracking for OTN"

    >>> project_res2 = sta.project.get({"name": "Gulf of St. Lawrence Animal Tracking for OTN"})

##### Manufacturer

To fetch full list of manufacturers

    >>> manufacturer_res = sta.manufacturer.get()

To fetch manufacturer with name "Teledyne Webb"

    >>> manufacturer_res2 = sta.manufacturer.get({"name": "Teledyne Webb"})

##### Instrument

To fetch full list of instruments

    >>> instrument_res = sta.instrument.get()

To fetch instrument with identifier "c"

    >>> instrument_res2 = sta.instrument.get({"identifier": "c"})

To fetch instrument on a platform

    >>> instrument_res3 = sta.instrument.get({"platform_name": "otn200"})

To fetch instrument by deployment

    >>> instrument_res4 = sta.instrument.get({"platform_name": "otn200", "start_time": "2017-08-02 19:37:38"})
    >>> instrument_res5 = sta.instrument.get({"platform_name": "otn200", "start_time": "2017-08-02"})

##### Instrument_on_platform

To fetch full list of instrument on platform

    >>> instrument_on_platform_res = sta.instrument_on_platform.get()

To fetch instrument on platform by platform name

    >>> instrument_on_platform_res2 = sta.instrument_on_platform.get({"platform_name": "otn200"})

To fetch instrument on platform by instrument identifier

    >>> instrument_on_platform_res5 = sta.instrument_on_platform.get({"identifier": "c"})

##### Sensor

To fetch full list of sensor

    >>> sensor_res = sta.sensor.get({"output": "all"})

To fetch all sensors which are included in output

    >>> sensor_res = sta.sensor.get({"output": True}) # output:False means not include in output

Sensors can be filter by identifier, short_name, and long_name

    >>> sensor_res2 = sta.sensor.get({"identifier": "RMSe", "output": True})
    >>> sensor_res2 = sta.sensor.get({"short_name": "short_name"})
    >>> sensor_res2 = sta.sensor.get({"long_name": "long_name"})

Sensors can be filtered by platform or deployment

    >>> sensor_res3 = sta.sensor.get({"platform_name": "otn200", "start_time": "2017-08-02 19:37:38"})
    >>> sensor_res4 = sta.sensor.get({"platform_name": "otn200"})
    >>> sensor_res5 = sta.sensor.get({"platform_name": "otn200", "start_time": "2017-08-02"})

##### Sensor on Instrument

To fetch a full list of sensor_on_instrument

    >>> ret = sta.sensor_on_instrument.get()

To fetch sensor on instrument for a deployment

    >>> ret = sta.sensor_on_instrument.get({"platform_name": "otn200", "deployment_start_time": "2017-08-02 19:37:38"})

##### platform type

To fetch a full list of platform type

    >>> platform_type_res = sta.platform_type.get()

To fetch platform type by model name

    >>> platform_type_res2 = sta.platform_type.get({"model": "Mooring"})

By default, the given model name should be match the target platform name; alternatively, you can specific filter "how" which can be "contains" or "regex"

    >>> platform_type_res3 = sta.platform_type.get({"model": "slocum", "how": "contains"}) # return all platform type which model contains word "slocum", case in sensitive
    >>> platform_type_res4 = sta.platform_type.get({"model": "Slocum Glider G\d", "how": "regex"}) # return all platform types which model match the regular expression

###### Power

To fetch the full list of power type

    >>> power_res = sta.power.get()

To filter sensor list by power name

    >>> power_res2 = sta.power.get({"name":"power_name"})

##### Deployment

To fetch the full list of deployment

    deployment_res = sta.deployment.get()

To get the deployments by platform name

    >>> deployment_res = sta.deployment.get({"platform_name": "otn200"})

To get the deployment by platform_type

    >>> deployment_res2 = sta.deployment.get({"model": "Slocum Glider G\d", "how": "regex"})
    >>> deployment_res3 = sta.deployment.get({"model": "Slocum", "how": "contains"})

##### Deployment comment

To get full list of deployment comment

    >>> deployment_comment = sta.deployment_comment.get()


    # user detail were hidden
    >>> deployment_comment = sta.deployment_comment.get({"platform_name": "dal556", "depth": 1})
    >>> deployment_comment_res2 = sta.deployment_comment.get({"platform_name": "dal556", "depth": 0})

### POST Operations

The credential must be provided before using any POST operations otherwise it will throw an exception,
POST operations' format is similar to GET operations

    res = sta.target_model.post({"a_data_file": "field_value"})


### Author
    **[CEOTR DATA TEAM](http://ceotr.ocean.dal.ca)**

### License
This project
