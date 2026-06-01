import json
from pathlib import Path
from utils.paths import sample_product, parent_path
from utils.xlsxTojson import xlsx_to_json_convertor

#### Now it just handles not existed products with sample. it should contain all in the future.

def load_json(file_path:str, sample_path = sample_product):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        sample_path = sample_path + ".json"
        with open(sample_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    return data

def load_bom(factory, category, subcategory, product_name):
    recipe_path = Path(parent_path) / "Factories" / factory / category / subcategory / f"{product_name}.json"
    data = load_json(recipe_path)
    return data, recipe_path

def load_factory_summery(factory):
    fmt = ['json', 'xlsx']
    fac_json_path = str(Path(parent_path) / "Factories" / factory / f"Factory_Data.{fmt[0]}")
    fac_xlsx_path = str(Path(parent_path) / "Factories" / factory / f"Factory_Data.{fmt[1]}")
    xlsx_to_json_convertor(excel_path=fac_xlsx_path, if_sheet=True, sheet_name='Summery')
    data = load_json(fac_json_path)
    return data, fac_json_path

def load_factory_subfield(factory_name:str, subfield:str):
    fmt = ['json', 'xlsx']
    subf_json_path = str(Path(parent_path) / "Factories" / factory_name / f"Factory_Data_{subfield}.{fmt[0]}")
    subf_xlsx_path = str(Path(parent_path) / "Factories" / factory_name / f"Factory_Data.{fmt[1]}")
    xlsx_to_json_convertor(excel_path=subf_xlsx_path, if_sheet=True, sheet_name=subfield, if_subfield=True)
    data = load_json(subf_json_path)
    # print(data)
    return data, subf_json_path

# load_factory_subfield('HajAmini', "AdministrativeandResearch")