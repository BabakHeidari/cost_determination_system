import pandas as pd
from utils.paths import parent_path
from pathlib import Path
import json
from typing import Union, Optional
from flask import session, jsonify
from datetime import datetime, date, time


def modify_summery(factory):
    file_path = Path(parent_path) / "Factories" / factory / "Factory_Data.xlsx"
    data_list = list()
    all_sheets = pd.read_excel(file_path, sheet_name=None)
    sheet_names = list(all_sheets.keys())
    selling_share, summery_sheet = sheet_names.pop(-2), sheet_names.pop()

    for i, subfield in enumerate(sheet_names):
        subfield_sheet = all_sheets[subfield]
        row = [subfield, sum(subfield_sheet['cost']), None]
        data_list.append(row)
    all_sheets[summery_sheet] = pd.DataFrame(data=data_list, columns=["Subfield", "Cost", "PercentageOfAll"])
    all_sheets[summery_sheet]["PercentageOfAll"] = (all_sheets[summery_sheet]["Cost"]/sum(all_sheets[summery_sheet]["Cost"]))*100

    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        all_sheets[summery_sheet].to_excel(writer, sheet_name=summery_sheet, index=False)
    
    return all_sheets[summery_sheet]


# modify_summery(factory='HajAmini')


def json_to_excel_converter(
    json_path: Union[str, Path], 
    output_path: Optional[Union[str, Path]] = None,
    sheet_name: str = "Sheet1",
    update_only: bool = True
) -> str:
    """
    Convert a JSON file to Excel, optionally updating only a specific sheet.
    
    Args:
        json_path: Path to the input JSON file
        output_path: Path for the output Excel file (optional)
        sheet_name: Name of the Excel sheet to update/create (default: "Sheet1")
        update_only: If True, update only the specified sheet; if False, create new file
    
    Returns:
        Path to the Excel file
    """
    json_path = Path(json_path)
    
    # Read JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract data
    columns = data.get('_order', [])
    values_dict = data.get('data', {})
    date_string = data.get('last_modification_date', [])

    date_string_clean = date_string.replace('Z', '+00:00')
    date_obj = datetime.fromisoformat(date_string_clean)

    modified_datetime = [date(date_obj.year, date_obj.month,  date_obj.day), 
                         time(date_obj.hour, date_obj.minute,  date_obj.second)]
    
    if not columns or not values_dict or not modified_datetime:
        raise ValueError("JSON file missing '_order' or 'data' keys or 'last_modification_date'.")
    
    # Create DataFrame
    df = pd.read_excel(output_path, sheet_name=sheet_name)
    # df = pd.DataFrame()
    for col in columns:
        if col in values_dict:
            df[col] = values_dict[col]
        else:
            print(f"Warning: Column '{col}' not found in data")
            df[col] = []
    
    # Determine output path
    if output_path is None:
        output_path = json_path.parent / f"{json_path.stem}.xlsx"
    else:
        output_path = Path(output_path)
    
    # Save/Update Excel file
    if update_only and output_path.exists():
        # Update only the specified sheet in existing file
        with pd.ExcelWriter(output_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"✅ Updated sheet '{sheet_name}' in: {output_path.name}")
    else:
        # Create new file or overwrite entire file
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"✅ Created new file with sheet '{sheet_name}': {output_path.name}")
    
    return str(output_path)

def batch_json_to_excel(
    input_dir: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    pattern: str = "*.json"
) -> list:
    """
    Convert multiple JSON files in a directory to Excel files.
    
    Args:
        input_dir: Directory containing JSON files
        output_dir: Directory to save Excel files (optional, uses same as input)
        pattern: File pattern to match (default: "*.json")
    
    Returns:
        List of created Excel file paths
    """
    input_dir = Path(input_dir)
    
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    json_files = list(input_dir.glob(pattern))
    
    if not json_files:
        print(f"No JSON files found matching '{pattern}' in {input_dir}")
        return []
    
    excel_files = []
    for json_file in json_files:
        if output_dir:
            output_path = output_dir / f"{json_file.stem}.xlsx"
        else:
            output_path = None
        
        excel_path = json_to_excel_converter(json_file, output_path)
        excel_files.append(excel_path)
    
    print(f"\n✅ Converted {len(excel_files)} file(s)")
    return excel_files


def save_json_and_excel(module:str, saving_file:str):
    if module == 'factory':
        if saving_file == "factory":
            saving_path = session.get("facs_path")
        elif saving_file == "factory_details":
            saving_path = session.get("fac_path")
        elif saving_file == "subfield":
            print(session.items())
            saving_path = session.get("sub_path")
        else:
            return jsonify({"error": f"Invalid saving_file: {saving_file}"}), 400
    
        
# json_path = "B:\Courses\Maktabkhooneh\Python-Bigdeli\Web_App\cost_determination_app\Data\Overall\material_costs.json"
# json_path = Path(json_path)

# # Read JSON file
# with open(json_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Extract data
# from datetime import datetime, date, time

# columns = data.get('_order', [])
# values_dict = data.get('data', {})
# date_string = data.get('last_modification_date', [])

# date_string_clean = date_string.replace('Z', '+00:00')
# date_obj = datetime.fromisoformat(date_string_clean)

# modified_date = date(date_obj.year, date_obj.month,  date_obj.day)
# modified_time = time(date_obj.hour, date_obj.minute,  date_obj.second)

# print(f"Day is: {modified_date}\nand time is: {modified_time}")

# print(modification_date)