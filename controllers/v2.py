# coding: utf8
auth.settings.allow_basic_login = True
@auth.requires_login()
def catalog():
    from gluon.tools import Auth
    import yaml
    import json
    with open('/settings_softlayer.yml', 'r') as f:
        yaml_settings = yaml.load(f)
    json_settings = json.dumps(yaml_settings)
    data = json.loads(json_settings)
    return data['catalog']

@auth.requires_login()
def test():
    import uuid, os, yaml, json, docker, requests
    id = request.args
    return id[0]


@auth.requires_login()
def service_instances():
    import uuid, os, yaml, json, docker, requests, traceback
    from SoftLayer import VSManager, Client
    id = request.args
    with open('/settings_softlayer.yml', 'r') as f:
        yaml_settings = yaml.load(f)
    json_settings = json.dumps(yaml_settings)
    data = json.loads(json_settings)
    sl_api_user = data['pattern']['api_ep'][0]['user']
    sl_api_key = data['pattern']['api_ep'][0]['api_key']
    client = Client(username=sl_api_user, api_key=sl_api_key)
    vs = VSManager(client)
    with open('/softlayer.json', 'r') as json_content_read:
        build_content_read = json.load(json_content_read)
        json_content_read.close()

    build_content_read['hostname'] = id[0]

    with open('/softlayer.json', 'w') as json_content_write:
        json_content_write.write(json.dumps(build_content_read))
        json_content_write.close()

    with open('/softlayer.json') as json_content:
        build_content = json.load(json_content)

    if len(id) == 1:
        if request.env.request_method == "PUT":
            try:
                client['Virtual_Guest'].createObject(build_content)
                response = { "dashboard_url": id }
                return response
            except:
                print traceback.format_exc()
        if request.env.request_method == "DELETE":
            try:
                for i in vs.list_instances():
                    if str(i['hostname']) == str(id[0]):
                        virtual_server_id = i['id']
                vs.cancel_instance(virtual_server_id)
                response = {}
                return response
            except:
                raise HTTP(410, "Gone")
                response = {}
                return response

    if len(id) > 1:
        if request.env.request_method == "PUT":
            try:
                for i in vs.list_instances():
                    if str(i['hostname']) == str(id[0]):
                        virtual_server_id = i['id']
                ip_addr = vs.get_instance(virtual_server_id)['primaryIpAddress']
                #username = vs.get_instance(virtual_server_id)['networkComponents']['operatingSystem']['passwords'][0]['username']
                #password = vs.get_instance(virtual_server_id)['networkComponents']['operatingSystem']['passwords'][0]['password']
                #response = {"credentials": [{"ip_address": ip_addr},{"username": username}, {"password": password}]}
                response = {"credentials": {"ip_address": ip_addr, "port": "11211"}}
                return response
            except:
                return traceback.format_exc()
                #raise HTTP(404, "Not Found")
                #response = {}
                #return response
        if request.env.request_method == "DELETE":
            response = {}
            return response
