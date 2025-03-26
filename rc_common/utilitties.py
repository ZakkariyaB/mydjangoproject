from .models import CommonConfigurations

class CommonUtility():
    def save_config(self,variables):
        variables_dict = { x.name : x for x in CommonConfigurations.objects.filter(name__in=variables.keys())}

        variables_add_list = []
        variables_update_list = []
        for key, value in variables.items():
            if key in variables_dict :
                v_obj = variables_dict[key]
                v_obj.data = value
                variables_update_list.append(v_obj)
            else:
                variables_add_list.append(
                    CommonConfigurations(name=key,data=value)
                )

        if variables_add_list :
            CommonConfigurations.objects.bulk_create(variables_add_list)

        if variables_update_list :
            CommonConfigurations.objects.bulk_update(variables_update_list,['data'])

    def get_configs(self,keys):
        return_vars = {}
        variables = CommonConfigurations.objects.filter(name__in=keys).values('name','data')
        for var in variables:
            return_vars[var['name']] = var['data']
        return return_vars

    def get_filter_conditions(self,request,filter_items):
        filter_conditions = {}
        if request.GET :
            for key in filter_items:
                if key in request.GET and request.GET[key] != '' and request.GET[key] != None :
                    filter_conditions[key] = request.GET[key]

        return filter_conditions

