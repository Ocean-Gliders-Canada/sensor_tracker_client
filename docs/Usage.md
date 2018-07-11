### Usage: {#0}

Sensor tacker api has two function which are get and post functions. For this version, we only have get functions, and post functions haven't start yet.

There are four get interface for different data:

We have three get method which can get get\_deployments, getsensors, getinstruments, get\_deployment\_comments, get\_platform

* ##### [get deployments](#1) {#1}
* ##### [get sensors](#2)
* ##### [get instruments](#3)
* ##### [get deployment comments](#4)
* ##### [get platform](#5)

---

### [get deployments](#0)

Parameter could be general mode such as "slocum", which will return a data object which contain all of the slocum deployment data.

```py
data_obj = tracker_api.get_deployments("slocum")
```

Parameter could be deployment\_number

```py
data_obj = tracker_api.get_deployments(80)
```

Parameter could be glider model

```py
data_obj = tracker_api.get_deployments("Slocum Glider G3")
```

Parameter could be platform\_name

```py
data_obj = tracker_api.get_deployments("otn200")
```

Parameter could be deployment name and time

```py
data_obj = tracker_api.get_deployments("DL", "2018-04-03 12:00:00")
```

---

### [**get sensors**](#0) {#2}

Parameter could be platform name and deployment time, and specific it is a output sensor or no.

```py
data_obj = tracker_api.get_sensors("DL", "2018-04-03 12:00:00", output=True)
data_obj = tracker_api.get_sensors("DL", "2018-04-03 12:00:00", output=False)
```

---

### [**get instruments**](#0) {#3}

Parameter could be deployment\_number

```py
data_obj = tracker_api.get_deployments(80)
```

Parameter could be platform\_name

```py
data_obj = tracker_api.get_deployments("otn200")
```

Parameter could be deployment name and time

```py
data_obj = tracker_api.get_deployments("DL", "2018-04-03 12:00:00")
```

---

### [**get deployment comments**](#0) {#4}

Parameter could be deployment name and time

```py
data_obj = tracker_api.get_deployments("DL", "2018-04-03 12:00:00")
```

---

### [**get platform**](#0) {#5}

Parameter could be general mode such as "slocum", which will return a data object which contain all of the slocum deployment data.

```py
data_obj = tracker_api.get_deployments("slocum")
```

Parameter could be glider model

```py
data_obj = tracker_api.get_deployments("Slocum Glider G3")
```

---



