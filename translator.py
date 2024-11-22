import sys
import re
import yaml


class ConfigLanguageError(Exception):
    """Кастомное исключение для ошибок в конфигурационном языке."""
    pass


class ConfigTranslator:
    def __init__(self):
        self.output = []

    def validate_name(self, name):
        """Проверяет корректность имени."""
        if not re.match(r"^[_A-Z][_a-zA-Z0-9]*$", name):
            raise ConfigLanguageError(f"Недопустимое имя: {name}")

    def validate_value(self, value):
        """Проверяет допустимость значения (число или массив)."""
        if isinstance(value, (int, float)):
            return
        if isinstance(value, list):
            for item in value:
                self.validate_value(item)
            return
        if isinstance(value, str):
            return  # строки считаются допустимыми
        raise ConfigLanguageError(f"Недопустимое значение: {value}")

    def translate_constant(self, name, value):
        """Транслирует объявление константы."""
        self.validate_name(name)
        self.validate_value(value)
        
        # Преобразование значения
        if isinstance(value, list):
            value_str = f"[ {' '.join(map(self.format_value, value))} ]"
        else:
            value_str = self.format_value(value)
        
        self.output.append(f"def {name} := {value_str}")

    def format_value(self, value):
        """Форматирует значение (оборачивает строки в кавычки)."""
        if isinstance(value, str):
            return f'"{value}"'  # строковые значения оборачиваются в кавычки
        return str(value)  # для чисел и других типов возвращаем их строковое представление

    def translate_evaluation(self, name):
        """Транслирует вычисление константы."""
        self.validate_name(name)
        self.output.append(f"!( {name} )")

    def process_node(self, name, node):
        """Обрабатывает узел YAML (рекурсивно)."""
        self.validate_name(name)
        
        if isinstance(node, dict):
            # Добавление многострочного комментария
            self.output.append(f"%{{\nЭто структура {name}\n%}}")
            for key, value in node.items():
                self.process_node(key, value)
        elif isinstance(node, list):
            # Обработка массивов как значения
            self.translate_constant(name, node)
        elif isinstance(node, (int, float)):
            # Обработка чисел
            self.translate_constant(name, node)
        elif isinstance(node, str):
            # Обработка строк
            self.translate_constant(name, node)
        else:
            raise ConfigLanguageError(f"Недопустимое значение: {node}")

    def translate(self, yaml_input):
        """Основной метод перевода из YAML в конфигурационный язык."""
        try:
            data = yaml.safe_load(yaml_input)
            if not isinstance(data, dict):
                raise ConfigLanguageError("Корневой элемент должен быть словарём.")
            for key, value in data.items():
                self.process_node(key, value)
        except yaml.YAMLError as e:
            raise ConfigLanguageError(f"Ошибка разбора YAML: {e}")
        return "\n".join(self.output)


if __name__ == "__main__":
    # Чтение входных данных
    yaml_input = sys.stdin.read()
    
    # Создание транслятора
    translator = ConfigTranslator()
    
    try:
        # Перевод YAML в учебный конфигурационный язык
        result = translator.translate(yaml_input)
        # Вывод результата
        print(result)
    except ConfigLanguageError as e:
        # Вывод ошибок
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
