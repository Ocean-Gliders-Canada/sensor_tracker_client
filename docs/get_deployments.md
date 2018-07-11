# get deployments

---

Argument could be general mode such as "slocum", which will return a data object which contain all of the slocum deployment data.

```py
data_obj = tracker_api.get_deployments("slocum")
```

Input could be deployment\_number

```py
data_obj = tracker_api.get_deployments(80)
```

Input could be glider model

```py
data_obj = tracker_api.get_deployments("Slocum Glider G3")
```

Input could be platform\_name

```py
data_obj = tracker_api.get_deployments("otn200")
```

Input could be deployment name and time

```py
data_obj = tracker_api.get_deployments("DL", "2018-04-03 12:00:00")
```



