# -*- coding: utf-8 -*-

"""Main module NgoOpenApiClient """
import json
import dpath
import inflection
from types import MethodType
import requests
from simple_rest_client.api import API as API_src
from simple_rest_client.resource import BaseResource
from simple_rest_client.request import make_request
from simple_rest_client.models import Request

from ngoschema import get_builder, decorators
from ngoschema_plus.converters.openapi2jsonschema import convert as to_json_schema
from jsonschema import RefResolver


class Resource(BaseResource):
    actions = {}

    def __repr__(self):
        return "<Resource '" + self.resource_name + "'\n\t" + '\n\t'.join(self.get_action_list()) + "\n>"

    def __init__(self, **kwargs):
        BaseResource.__init__(self, **kwargs)
        self.actions = dict(self.__class__.actions) # reset default actions
        self.session = requests.Session()

    def add_action(self, action_name):
        def action_method(
            self, *args, body=None, params=None, headers=None, action_name=action_name, **kwargs
        ):
            f"""{self.actions[action_name].get('description', '')}"""
            url = self.get_action_full_url(action_name, *args)
            method = self.get_action_method(action_name)
            if self.json_encode_body and body:
                body = json.dumps(body)
            request = Request(
                url=url,
                method=method,
                params=params or {},
                body=body,
                headers=headers or {},
                timeout=self.timeout,
                ssl_verify=self.ssl_verify,
                kwargs=kwargs,
            )
            request.params.update(self.params)
            request.headers.update(self.headers)
            resp = make_request(self.session, request)

            met_resp = self.actions[action_name]['responses']
            resp_cls = met_resp[str(resp.status_code)]['__class__']
            return resp_cls(**resp.body)

        setattr(self, action_name, MethodType(action_method, self))

    def get_action_list(self):
        return list(self.actions.keys())

    def get_action_full_url(self, action_name, *parts):
        action = self.get_action(action_name)
        try:
            data = {p['name']: parts[i] for i, p in enumerate(action['parameters']) if p['required']}
            url = action["url"].format(*parts, **data)
        except IndexError:
            raise Exception('No url match for "{}"'.format(action_name))

        if self.append_slash and not url.endswith("/"):
            url += "/"
        if not self.api_root_url.endswith("/"):
            self.api_root_url += "/"
        if url.startswith("/"):
            url = url.replace("/", "", 1)
        return self.api_root_url + url



class API(API_src):

    def __repr__(self):
        actions = ["\t\t"+k+": "+str(v) for k, v in self.get_action_resource_dict().items()]
        info = dict(self._openapi['info'])
        info.update({
            'definitions': list(self._definitions.keys()),
            'resources': list(self._resources.keys()),
            'actions': "\n" + "\n".join(actions)
        })
        return "<API '"+ self._url + "'\n\t" + "\n\t".join([k+": "+str(v) for k, v in info.items()]) + "\n>"


    def __init__(self, base_url, swagger_url='/swagger'):
        self._base_url = base_url

        swagger_url = self._base_url + swagger_url.rstrip(".json").rstrip("/") + '.json'
        r = requests.get(swagger_url)

        openapi = to_json_schema(r.json())
        self._resolver = RefResolver(base_url, openapi)
        self._openapi = openapi
        self._url = openapi['host'] + openapi['basePath']
        self._paths = openapi.get('paths', [])

        self._definitions = {}
        for d, info in openapi.get('definitions').items():
            self._definitions[d] = get_builder(resolver=self._resolver).construct(f'{base_url}{swagger_url}.json#/definitions/{d}', info)

        API_src.__init__(
            self,
            api_root_url='http://' + openapi['host'] + openapi['basePath'],  # base api url
            params={},  # default params
            headers={},  # default headers
            timeout=2,  # default timeout in seconds
            append_slash=False,  # append slash to final url
            json_encode_body=True,  # encode body as json
        )

        tags = set([y for x in dpath.util.values(self._paths, '/*/*/tags') for y in x])
        for tag in tags:
            self.add_resource(resource_name=tag, resource_class=Resource)

        for url, info in self._paths.items():
            for met, met_details in info.items():
                action = dict(met_details)
                action['url'] = url
                action['method'] = met.upper()
                met_name = inflection.underscore(met_details['operationId'])
                tags = met_details.get('tags', []) or ['core']
                for k, pd in enumerate(met_details['parameters']):
                    sch = pd.get('schema', {'type': 'string'})
                    sch.setdefault('type', 'object')
                    pd['class'] = get_builder(resolver=self._resolver).construct(base_url + url + '/parameters/%s' % k, sch)
                for k, rd in met_details['responses'].items():
                    sch = rd.get('schema', {'type': 'string'})
                    sch.setdefault('type', 'object')
                    rd['__class__'] = get_builder(resolver=self._resolver).construct(base_url + url + '/response/%s' % k, sch)

                for tag in tags:
                    resource = getattr(self, tag)
                    resource.actions.update({met_name: action})
                    resource.add_action(met_name)
                    met = getattr(resource, met_name)
                    for k, pd in enumerate(met_details['parameters']):
                        decorators.assert_arg(k, pd)(met)

    def get_action_resource_dict(self):
        return {rn: list(r.actions.keys()) for rn, r in self._resources.items()}
