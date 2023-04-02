# TextFiles v0.0.1
A convenient Python API for working with the text files CSV, JSON, TXT
This is a shared project with Yael Ben Yair `https://github.com/YaelBenYair`

The library allows handling csv, txt and json files easily from within Python.

## Installation
```terminal
pip install textfiles
```

## How to use:

### Main functions:
    self.get_content()
    self.search()
    self.count()
    
    
### examples:

#### CsvFile.update_cell()
    my_csv = CsvFile('/path/to/my/csv/file.csv')
    my_csv.update_cell(column=3, row=2, value='New content')

#### JsonFile.search()
    with open ("example.json", "w") as f:
        json.dump(f, {"State": "New York", "cities": ["New York", "Albeny", "New Paltz"]})


    my_json = JsonFile('/path/to/my/json/file.json')
    new = my_json.search("new")
    print(new)

    result

