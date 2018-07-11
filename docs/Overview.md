# **Overview**

---

Easier way access to sensor tracker database

sensor tracker api takes advantage of sensor tracker's RESTful web serverices and creates meta data object for results.

### Install

```
pip install git+https://gitlab.oceantrack.org/ocean-gliders-canada/tracker_api.git
```

### Example

```
from sensor_tracker_api.api import AccessApi
tracker_api = AccessApi()
data_obj = tracker_api.get_deployments("DL", "2018-04-03 12:00:00")
```

The result is meta data object, which can easily be converted to different format.

```
panda_df = data_obj.to_pandas()
convert_to_dictionary = data_obj.to_dict()
write_into_csv = data_obj.to_csv("path_to_csv_file")
```

### 



