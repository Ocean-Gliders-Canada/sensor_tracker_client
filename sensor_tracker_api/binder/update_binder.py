from sensor_tracker_api.binder.post_binder import APIPostMethod


class APIUpdateMethod(APIPostMethod):
    def __init__(self, **kwargs):
        APIPostMethod.__init__(self, **kwargs)

    def update(self, component, component_id, value):
        update_type = "update_component"
        res = dict(
            component=component,
            id=component_id,
        )
        res = {**value, **res}
        res = self.post_content(update_type, res)
        return res

    def update_deployment(self, component_id, content):
        component_type = "deployment"
        self.update(component_type, component_id, content)

    def update_platform(self, component_id, content):
        component_type = "platform"
        self.update(component_type, component_id, content)

    def update_project(self, component_id, content):
        component_type = "project"
        self.update(component_type, component_id, content)

    def update_instruments_platform(self, component_id, content):
        component_type = "instruments_platform"
        self.update(component_type, component_id, content)

    def update_platform_type(self, component_id, content):
        component_type = "platform_type"
        self.update(component_type, component_id, content)

    def update_instrument(self, component_id, content):
        component_type = "instrument"
        self.update(component_type, component_id, content)

    def update_sensor(self, component_id, content):
        component_type = "sensor"
        self.update(component_type, component_id, content)


"""
p = APIUpdateMethod(host="http://127.0.0.1:8001/api/", token='1537ded79296862c889ffe368b9decc3b9c2afe1')
print(p.update("deployment", "1", {"as": "a"}))
"""
