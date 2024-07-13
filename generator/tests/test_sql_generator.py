from datetime import datetime

from django.db import connection
from django.test import TestCase

from generator.models import Product
from generator.sql_generator import SQLGenerator, GenerateSQLClass
from generator.util import query_to_dicts


class TestBasicSQLGeneratorMethods(TestCase):
    GENERATOR = GenerateSQLClass

    def setUp(self) -> None:
        self.generator = SQLGenerator(model_type="basic", models=[Product]).initiate()
        self.generator.sql_create()

    def test_get_field_names_and_description(self):
        field_info = self.GENERATOR.get_field_names_and_description(Product)
        expected = {
            "date_created": "date",
            "title": "str",
            "market": "str",
            "price": "float",
            "description": "str",
            "tax_rate": "float",
        }
        for field_name, field_type in field_info:
            self.assertEqual(expected[field_name], field_type)

    def test_sql_create(self):
        query = """select * from products"""
        results = query_to_dicts(query)
        self.assertEqual(results, [])

    def test_sql_insert(self):
        insert_data = [
            {
                "date_created": "2024-07-12",
                "title": "Product1",
                "market": "US",
                "price": 30.0,
                "description": "P1 Description",
                "tax_rate": 6.25,
            }
        ]
        self.generator.sql_insert(Product, insert_data)
        query = """select * from products"""
        results = query_to_dicts(query)
        self.assertEqual(len(results), 1)

        row = results[0]
        self.assertEqual(row["date_created"], datetime.strptime(insert_data[0].pop("date_created"), "%Y-%m-%d").date())
        for key, value in insert_data[0].items():
            self.assertEqual(row[key], value)

