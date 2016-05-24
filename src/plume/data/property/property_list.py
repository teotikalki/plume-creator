'''
Created on 13 february 2016

@author:  Cyril Jacquet
'''


import sqlite3
from .db_property_list import DbPropertyList
from .db_property import DbProperty
from .. import cfg


class PropertyList:
    '''
    Property_list
    '''

    def __init__(self, sql_db: sqlite3.Connection, table_name: str
                 , property_type: str, id_name: str, code_name:str):
        '''
        Constructor
        :param property_type:
        :param code_name:
        :type table_name: str
        :type sql_db: sqlite3.Connection
        :type id_name: str
        '''

        self.table_name = table_name
        self.property_type = property_type
        self.code_name = code_name
        self.id_name = id_name
        self.sql_db = sql_db

    def get_all(self)-> list:
        '''
        function:: get_all()
        :return [{"name", value},...}
        '''
        property_list = DbPropertyList(self.sql_db, self.table_name, self.id_name, False)
        return property_list.get_all()

    def get_all_headers(self)-> list:
        '''
        function:: get_all_headers()
        '''
        property_list = DbPropertyList(self.sql_db, self.table_name, self.id_name, False)
        return property_list.get_all_headers()

    def get_name(self, property_id: int):
        '''
        function:: get_title(id: int)
        :param property_id: int:
        '''
        property = DbProperty(self.sql_db, self.table_name, self.id_name,  property_id, False)
        return str(property.get("t_name"))

    def set_name(self, property_id: int, value: str):
        '''
        function:: set_name(id: int)
        :param value:
        :param property_id: int:
        '''
        property = DbProperty(self.sql_db, self.table_name, self.id_name,  property_id, True)
        property.set("t_name", value)

    def get_value(self, property_id: int):
        '''
        function:: get_value(id: int)
        :param property_id: int:
        '''
        property = DbProperty(self.sql_db, self.table_name, self.id_name,  property_id, False)
        return str(property.get("t_value"))

    def set_value(self, property_id: int, value: str):
        '''
        function:: set_value(id: int)
        :param value:
        :param property_id: int:
        '''
        property = DbProperty(self.sql_db, self.table_name, self.id_name,  property_id, True)
        property.set("t_value", value)


    def add_new_properties(self, number: int, paper_id: int):
        '''
        function:: add_new_properties(parent_id: int, number: int)
        :param number: int:
        '''
        return self._add_new_properties(number, paper_id, True)

    def remove_properties(self, property_id_list):
        """

        :param property_id_list:
        :return: list of removed properties
        """
        return self._remove_properties(property_id_list, True)

    def _add_new_properties(self, number: int, paper_id: int, commit: bool):
        '''
        function:: _add_new_properties(number: int, commit: bool)
        :param number: int:
        :param commit: bool:
        '''

        new_id_list = []
        for i in range(number):
            property = DbProperty(self.sql_db, self.table_name, self.id_name
                                  , -1, False)
            new_id_list.append(property.add(self.code_name, paper_id))

        if commit:
            self.sql_db.commit()
            cfg.database.subscriber.announce_update(self.property_type + ".structure_changed")

        return new_id_list

    def _remove_properties(self, property_id_list, commit: bool):
        """

        :param property_id_list:
        :param commit:
        """

        propertyList = DbPropertyList(self.sql_db, self.table_name, self.id_name, False)
        if propertyList.remove_list(property_id_list) == 0:
            return False


        if commit:
            self.sql_db.commit()
            cfg.database.subscriber.announce_update(self.property_type + ".structure_changed")

        return True