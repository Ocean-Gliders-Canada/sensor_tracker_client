# **Overview**

---

Easier way access to sensor tracker database

sensor tracker api takes advantage of sensor tracker's RESTful web serverices and creates meta data object for results.

### Example

```
tracker_api = AccessApi()
data_obj = tracker_api.get_deployments("DL", "2018-04-03 12:00:00")
```

The result is meta data object, which can easily be converted to different format.

```
panda_df = data_obj.to_pandas()
convert_to_dictionary = data_obj.to_dict()
write_into_csv = data_obj.to_csv()
```

### Usage:

Sensor tacker api has two function which are get and post functions. For this version, we only have get functions, and post functions haven't start yet.

There are four get interface for different data:

We have three get method which can get get\_deployments, getsensors, getinstruments, get\_deployment\_comments, get\_platform

##### get deployments

get\_deployments method can accept different variables:

Input could be general mode such as "slocum", which will return a data object which contain all of the slocum deployment data

```
data_obj = tracker_api.get_deployments("slocum")
```

Input could be deployment\_number

```
data_obj = tracker_api.get_deployments(80)
```

Input could be glider model

```
data_obj = tracker_api.get_deployments("Slocum Glider G3")
```

Input could be platform\_name

```
data_obj = tracker_api.get_deployments("otn200")
```

Input could be deployment name and time

```
data_obj = tracker_api.get_deployments("DL", "2018-04-03 12:00:00")
```



