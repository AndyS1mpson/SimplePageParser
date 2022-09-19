# Simple WB Subcategory page parser

## Project structure

```
-> *src*
   -> exceptions.py - core project exceptions
   -> items.py - contains DTOs
   -> main.py - main project file
   -> parser.py - simple class for parsing WB category filters
   -> settings.py - contains project settings
-> docker-compose.yaml - contains a description of the headless browser image
```

## How to run project
1. Export environments:
```
export PROXY=<your proxy server url>
```
2. Install requirements:
```
pip insall -r requirements.txt
```
3. Run project:
```
python src/main.py
```
