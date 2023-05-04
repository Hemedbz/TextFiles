# TextFiles v0.0.4
A convenient Python API for working with the text files CSV, JSON, TXT

The library allows handling csv, txt and json files easily from within Python.

## Installation
```terminal
pip install textfiles
```

## How to use:

Import TextFile: Once you install the library you can import the TextFile class into your Python code. To do this, simply add the following line to your code:

```python
from textfiles.file_factory import TextFile
```

Use TextFile: You can now use the TextFile class to create instances of CsvFile, TxtFile, and JsonFile classes. The factory has two methods:

make_file_instance: This method creates an instance of the file class for an existing text file.

make_file: This method creates a new file and a corresponding Python instance of it.

To create an instance of a CsvFile, TxtFile, or JsonFile class, simply call the appropriate static method and pass in the necessary parameters. The factory will then return an instance of the appropriate class.

Examples: Here are some examples of how to use TextFile:

To create an instance of an existing file:

```python
file = TextFile.make_file_instance('path/to/file.csv', 'csv', has_header=True, delimiter=',')
file = TextFile.make_file_instance('path/to/file.txt', 'txt')
file = TextFile.make_file_instance('path/to/file.json', 'json')
```

To create a new file:

```python
file = TextFile.make_file('csv', 'path/to/file.csv', ['Header1', 'Header2'])
file = TextFile.make_file('txt', 'path/to/file.txt')
file = TextFile.make_file('json', 'path/to/file.json')
```
Note - When creating a CSV file, it is mandatory to pass a header.

### Main functions:
```python
    self.get_content()
    self.search()
    self.count()
```

### examples:

#### CsvFile.update_cell()
```python
    my_csv = CsvFile('/path/to/my/csv/file.csv')
    my_csv.update_cell(column=3, row=2, value='New content')
```

#### JsonFile.search()
```python
    with open ("example.json", "w") as f:
        json.dump(f, {"State": "New York", "cities": ["New York", "Albeny", "New Paltz"]})


    my_json = JsonFile('/path/to/my/json/file.json')
    new = my_json.search("new")
    print(new)
```

output:
```python
[{'State': 'New York'}, {'cities': [{'index[0]': 'New York'}, {'index[2]': 'New Paltz'}]}]
```
