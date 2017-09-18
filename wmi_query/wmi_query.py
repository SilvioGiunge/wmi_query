#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-


import wmi_conn
from collections import defaultdict
from impacket.dcerpc.v5.dcom.wmi import DCERPCException


class wmi_query(object):

    def __init__(self, opts):
        self.user = opts['user']
        self.password = opts['password']
        self.host = opts['host']
        self.domain = opts['domain']
        self.delimiter = opts['delimiter']
        self.namespace = opts['namespace']
        self.query = opts['query']
        self.data_dict = defaultdict(lambda: False)
        self.dict_name = ""

    def get_wmi_data(self):
        _wmi_data = wmi_conn.wmi_conn(self.host, self.user, self.password, self.domain, self.namespace, self.query)
        _list_wmi_data = []
        try:
            while True:
                _list_wmi_data.append(_wmi_data.Next(0xffffffff, 1)[0])
        except DCERPCException:
            pass
        _cont = 0
        self.dict_name = _list_wmi_data[0].getClassName()
        self.data_dict[self.dict_name] = defaultdict()
        for data in _list_wmi_data:
            self.data_dict[self.dict_name][_cont] = defaultdict(lambda: False)
            data_properties = data.getProperties()
            for item in data_properties:
                self.data_dict[self.dict_name][_cont][item] = data_properties[item]['value']
            _cont = _cont + 1

    def get_item(self, item_name, value_name):
        return [self.data_dict[self.dict_name][x] for x, y in enumerate(self.data_dict[self.dict_name])
                if value_name in self.data_dict[self.dict_name][x][item_name]]

    def get_items(self, item_name):
        return set([self.data_dict[self.dict_name][x][item_name] for x, y in enumerate(self.data_dict[self.dict_name])])

    def get_item_keys(self):
        return [x for x in self.data_dict[self.dict_name][0]]

    def name(self):
        return self.dict_name

    def run(self):
        self.get_wmi_data()
