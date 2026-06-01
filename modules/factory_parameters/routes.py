from flask import Blueprint, render_template, jsonify, request, session
from utils.auth import login_required
from utils.paths import factories_path
from utils.load_data import load_json, load_factory_summery, load_factory_subfield
from utils.updaters import json_to_excel_converter, modify_summery
import json



factory_parameters_bp = Blueprint("factory_parameters", __name__)

@factory_parameters_bp.route("/factory_parameters/", methods=["POST", "GET"])
@login_required
def factory_parameters():
    facs_path = factories_path + ".json"
    session["facs_path"] = facs_path
    data = load_json(facs_path)
    return render_template("factory_parameters/factories.html", 
                           table_json = data)

@factory_parameters_bp.route("/save", methods=["POST"])
def save_params():
    payload = request.get_json(force=True)
    
    # Extract saving_file from payload
    saving_file = payload.get("saving_file")
    
    if not saving_file:
        return jsonify({"error": "saving_file not specified in payload"}), 400
    
    final_data = {
        "_order": payload["_order"],
        "data": payload["data"]
    }
    
    # Determine saving path based on saving_file
    if saving_file == "factory":
        saving_path = factories_path
    elif saving_file == "factory_details":
        saving_path = session.get("fac_path")
    elif saving_file == "subfield":
        saving_path = session.get("sub_path")
    else:
        return jsonify({"error": f"Invalid saving_file: {saving_file}"}), 400
    
    # Check if saving_path exists
    if not saving_path:
        return jsonify({"error": f"Path not found for {saving_file}"}), 400
    
    # Save the file
    with open(f"{saving_path}.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

    if saving_file == "subfield":
        json_to_excel_converter(f"{saving_path}.json", f"{session.get("fac_path")}.xlsx", sheet_name=session.get("subfield"), update_only=True)
        modify_summery(session.get("factory_name"))
    else:
        json_to_excel_converter(f"{saving_path}.json", f"{saving_path}.xlsx")

    return jsonify({"status": "ok", "saved_to": saving_path})

######### This is the next part: categories, subcategories, and costing data related to just a factory should be added here.
@factory_parameters_bp.route("/factory_parameters/<factory_name>", methods=["POST"])
@login_required
def factory_details(factory_name):
    factory = request.form["factory name"]
    session["factory_name"] = factory
    factory_json, fac_path = load_factory_summery(factory)
    session["fac_path"] = fac_path.replace(".json", "")
    return render_template("/factory_parameters/factory_details.html", 
                           table_json = factory_json, factory_name = factory)


@factory_parameters_bp.route("/factory_parameters/<factory_name>/<Subfield>", methods=["POST"])
@login_required
def subfield(factory_name, Subfield):
    factory_name = session.get("factory_name")
    Subfield = request.form["Subfield"]
    subfield_json, sub_path = load_factory_subfield(factory_name, Subfield)
    session["sub_path"], session["subfield"] = sub_path.replace(".json", ""), Subfield
    # print(subfield_json)
    return render_template("/factory_parameters/factory_subfield.html", 
                           table_json = subfield_json, factory_name = factory_name,
                            Subfield=Subfield)

