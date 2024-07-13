from abc import ABC, abstractmethod

from django.db import connection


class GenerateSQL(ABC):
    CREATE_TABLE_PREFIX = "CREATE TABLE IF NOT EXISTS"
    INSERT_INTO = "INSERT INTO"

    def __init__(self, models: list = None):
        self.models = models
        self.table_create_items = []

    @abstractmethod
    def sql_create(self):
        """Creates tables in SQL using the given models"""

    @staticmethod
    @abstractmethod
    def get_field_names_and_description(model):
        """Returns field names and descriptions"""

    @abstractmethod
    def get_field_type(self, description):
        """Determine field type for create"""

    @staticmethod
    @abstractmethod
    def _insert_str(model, fields_str, values_str):
        """Create SQL insert string"""

    @abstractmethod
    def get_insert_type(self, description):
        """Determine field type for insert"""

    @staticmethod
    def _sql_create_str(table_fields, final_field):
        """Create string with fields or values"""
        fields_str = """ ("""
        for ft in table_fields:
            fields_str += f"""{ft}, """
        fields_str += f"""{final_field})"""
        return fields_str

    def sql_insert(self, model, to_insert):
        """Create SQL insert string"""
        field_info = self.get_field_names_and_description(model)
        field_names = []
        values_str = """ VALUES ("""

        for field_name, description in field_info[:-1]:
            if field_name == "id":
                continue
            field_names.append(field_name)
            values_str += f"""{self.get_insert_type(description)}, """
        values_str += f"""{self.get_insert_type(field_info[-1][1])})"""

        final_field = field_info[-1][0]
        fields_str = self._sql_create_str(field_names, final_field)
        insert_str = self._insert_str(model, fields_str, values_str)
        field_names.append(final_field)
        self.execute_insert(insert_str, self._align_insert_data(to_insert, field_names))

    def execute_create(self):
        """Create table"""
        with connection.cursor() as c:
            for table_create in self.table_create_items:
                c.execute(table_create)

    @staticmethod
    def execute_insert(insert_str, data):
        """Insert into table"""
        with connection.cursor() as c:
            for row in data:
                c.execute(insert_str % tuple(row))

    @staticmethod
    def _align_insert_data(data_import, field_names):
        """Ensure data import elements align with field names"""
        return [[d.get(f, None) for f in field_names] for d in data_import]


class GenerateSQLClass(GenerateSQL):
    """Generate table in SQL from standard class"""

    _POSSIBLE_TYPES = {"str": "text", "bool": "boolean"}
    _NUMERIC_INSERTS = ["int", "decimal", "float"]

    @staticmethod
    def get_field_names_and_description(model):
        """Returns field names and descriptions"""
        field_names = list(model.__annotations__.items())
        if model.__base__.__name__ != "object":
            # class has parent with potential additional fields
            field_names += list(model().__class__.__base__.__annotations__.items())

        return [(name, desc.__name__) for name, desc in field_names if name != "db_table"]

    def sql_create(self):
        """Creates tables in SQL using the given models"""
        for model in self.models:
            # get field names of model and determine type
            field_info = self.get_field_names_and_description(model)
            table_fields = [f"{field_name}{self.get_field_type(desc)}" for field_name, desc in field_info]
            fields_str = self._sql_create_str(table_fields, table_fields.pop(-1))
            self.table_create_items.append(f"""{GenerateSQL.CREATE_TABLE_PREFIX} {model.db_table}{fields_str}""")

        self.execute_create()

    def get_field_type(self, description):
        """Determine field type for create"""
        return f""" {self._POSSIBLE_TYPES.get(description, description)}"""

    @staticmethod
    def _insert_str(model, fields_str, values_str):
        """Generate insert SQL"""
        return f"""{GenerateSQL.INSERT_INTO} {model.db_table}{fields_str}{values_str}"""

    def get_insert_type(self, description):
        """Determine field type for insert"""
        if any(f == description for f in self._NUMERIC_INSERTS):
            return """%s"""
        return """'%s'"""


class GenerateSQLModel(GenerateSQL):
    """Generate table in SQL from Django Model"""

    _POSSIBLE_TYPES = [
        ("Integer", "int"),
        ("integer", "int"),
        ("Decimal", "decimal"),
        ("Float", "float"),
        ("Date", "date"),
        ("String", "text"),
        ("Text", "text"),
        ("Boolean", "boolean"),
        ("Bool", "bool"),
    ]
    _NUMERIC_INSERTS = ["Integer", "integer", "Decimal", "Float"]

    def sql_create(self):
        """Creates tables in SQL using the given models"""
        for model in self.models:
            table_fields = []

            # get field names of model and determine type
            field_info = self.get_field_names_and_description(model)
            for field_name, description in field_info:
                field_type = self.get_field_type(description)
                table_fields.append(f"{field_name}{field_type}")
            fields_str = self._sql_create_str(table_fields, table_fields.pop(-1))
            self.table_create_items.append(f"""{GenerateSQL.CREATE_TABLE_PREFIX} {model._meta.db_table}{fields_str}""")
        self.execute_create()

    @staticmethod
    def _insert_str(model, fields_str, values_str):
        """Generate insert SQL"""
        return f"""{GenerateSQL.INSERT_INTO} {model._meta.db_table}{fields_str}{values_str}"""

    def get_insert_type(self, description):
        """Determine field type for insert"""
        if any(f in description for f in self._NUMERIC_INSERTS):
            return """%s"""
        return """'%s'"""

    def get_field_type(self, description):
        """Determine field type for create"""
        for value, sql_type in self._POSSIBLE_TYPES:
            if value in description:
                return f""" {sql_type}"""
        return ""

    @staticmethod
    def get_field_names_and_description(model):
        """Returns field names and descriptions"""
        return [(f.name, f.description) for f in model._meta.fields]


class SQLGenerator:
    CLASS_REFERENCE = {
        "basic": GenerateSQLClass,
        "django": GenerateSQLModel,
    }

    def __init__(self, model_type: str, models: list):
        self.model_type = model_type
        self.models = models

    def initiate(self):
        if self.model_type not in SQLGenerator.CLASS_REFERENCE:
            raise KeyError(f"Unsupported model type. Choices are {list(SQLGenerator.CLASS_REFERENCE.keys())}")

        return SQLGenerator.CLASS_REFERENCE[self.model_type](models=self.models)

