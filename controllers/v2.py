# coding: utf8
auth.settings.allow_basic_login = True
@auth.requires_login()
def catalog():
    from gluon.tools import Auth
    import yaml
    import json
    with open('/settings_sco.yml', 'r') as f:
        yaml_settings = yaml.load(f)
    json_settings = json.dumps(yaml_settings)
    data = json.loads(json_settings)
    return data['catalog']

@auth.requires_login()
def test_sco():
    import uuid, os, yaml, json, docker, requests
    id = request.args
    return id[0]


@auth.requires_login()
def service_instances():
    import uuid, os, yaml, json, docker, requests
    id = request.args
    with open('/settings_sco.yml', 'r') as f:
        yaml_settings = yaml.load(f)
    json_settings = json.dumps(yaml_settings)
    data = json.loads(json_settings)
    sco_api_url = data['pattern']['api_ep'][0]['url']
    sco_api_user = data['pattern']['api_ep'][0]['user']
    sco_api_password = data['pattern']['api_ep'][0]['password']
    sco_api_headers = data['pattern']['api_ep'][0]['headers']
    with open('/sco_pattern.json', 'r') as json_content_read:
        build_content_read = json.load(json_content_read)
	json_content_read.close()

    build_content_read['name'] = id[0]

    with open('/sco_pattern.json', 'w') as json_content_write:
        json_content_write.write(json.dumps(build_content_read))
	json_content_write.close()

    with open('/sco_pattern.json') as json_content:
	build_content_load = json.load(json_content)
        build_content = json.dumps(build_content_load)

    if len(id) == 1:
        if request.env.request_method == "PUT":
            r = requests.post(sco_api_url+'/resources/virtualSystems', verify=False, auth=(sco_api_user, sco_api_password), headers=sco_api_headers, data=build_content)
            response = { "dashboard_url": id }
            return response
        if request.env.request_method == "DELETE":
            try:
            	r = requests.get(sco_api_url+'/resources/virtualSystems', verify=False, auth=(sco_api_user, sco_api_password), headers=sco_api_headers)
		for i in r.json():
			if str(i['name']) == str(id[0]):
				sco_id = str(i['id'])
				delete = requests.delete(sco_api_url+'/resources/virtualSystems/'+sco_id, verify=False, auth=(sco_api_user, sco_api_password), headers=sco_api_headers)
               	response = {}
               	return response
            except:
                raise HTTP(410, "Gone")
                response = {}
                return response

#    if len(id) > 1:
#        if request.env.request_method == "PUT":
#            list = []
#            containers_l = c.containers()
#            for x in containers_l:
#                cont_deep = c.inspect_container(x['Id'])
#                list.append(cont_deep)
#            for y in list:
#                if y['Config']['Hostname'] == host:
#                    IpAddr = y['NetworkSettings']['IPAddress']
#                    Port = y['NetworkSettings']['Ports']
#            response = {"credentials": {"password": password,"host": IpAddr,"port": Port}}
#            return response
#        if request.env.request_method == "DELETE":
#            response = {}
#            return response
