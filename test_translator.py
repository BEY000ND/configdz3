import unittest
from translator import ConfigTranslator, ConfigLanguageError


class TestConfigTranslator(unittest.TestCase):

    def setUp(self):
        """Инициализация перед каждым тестом."""
        self.translator = ConfigTranslator()

    def test_translate_server(self):
        yaml_input = """
Server:
  Host: "127.0.0.1"
  Port: 8080
  Routes: ["/", "/api", "/status"]
"""
        expected_output = """%{
Это структура Server
%}
def Host := "127.0.0.1"
def Port := 8080
def Routes := [ "/" "/api" "/status" ]
"""
        result = self.translator.translate(yaml_input)
        self.assertEqual(result.strip(), expected_output.strip())  # сравниваем без учета завершающих новых строк

    def test_translate_database(self):
        yaml_input = """
Database:
  Name: "TestDB"
  MaxConnections: 100
  Ports: [5432, 5433, 5434]
"""
        expected_output = """%{
Это структура Database
%}
def Name := "TestDB"
def MaxConnections := 100
def Ports := [ 5432 5433 5434 ]
"""
        result = self.translator.translate(yaml_input)
        self.assertEqual(result.strip(), expected_output.strip())  # сравниваем без учета завершающих новых строк

    def test_translate_app(self):
        yaml_input = """
App:
  Version: "1.2"
  Features:
    - "Login"
    - "Signup"
    - "Profile"
"""
        expected_output = """%{
Это структура App
%}
def Version := "1.2"
def Features := [ "Login" "Signup" "Profile" ]
"""
        result = self.translator.translate(yaml_input)
        self.assertEqual(result.strip(), expected_output.strip())  # сравниваем без учета завершающих новых строк

    def test_invalid_name(self):
        yaml_input = """
Invalid:
  123abc: "value"
"""
        with self.assertRaises(ConfigLanguageError):
            self.translator.translate(yaml_input)

    def test_invalid_value(self):
        yaml_input = """
InvalidValue:
  SomeKey: !!python/str 'undefined'
"""
        with self.assertRaises(ConfigLanguageError):
            self.translator.translate(yaml_input)


if __name__ == "__main__":
    unittest.main()
