from flask import Blueprint, render_template, jsonify, request, session
from utils.auth import login_required
from utils.paths import product_path, material_path
# from utils.load_bom import load_bom
from utils.load_data import load_json, load_bom
import json

product_bp = Blueprint("product", __name__)

@product_bp.route("/product/production_selection")
@login_required
def production_selection():
    with open(product_path+".json", "r") as f:
        product_data = json.load(f)
    return render_template("product/production_selection.html", 
                           table_json = product_data)

@product_bp.route("/product/configuration")
@login_required
def configuration():
    return render_template("product/configuration.html")

@product_bp.route("/product/<product_name>", methods=["POST"])
@login_required
def product_page(product_name):
    factory = request.form["factory"]
    category = request.form["category"]
    subcategory = request.form["subcategory"]
    bom_json, recipe_path = load_bom(factory, category, subcategory, product_name)
    session["recipe_path"] = str(recipe_path)
    # with open(material_path+".json", "r") as f:
    #     material_data = json.load(f)
    material_data = load_json(material_path+".json")
    return render_template("product/product_page.html", 
                           product_name=product_name, bom_json=bom_json,
                            materials_data = material_data)


@product_bp.route("/save_bom", methods=["POST"])
def save_bom():
    # build bom_path however you do now, e.g. using a default factory/category/etc.
    bom_path = session.get("recipe_path")
    payload = request.get_json(force=True)

    final_bom = {
        "_order": payload["_order"],
        "data": payload["data"]
    }

    with open(bom_path, "w", encoding="utf-8") as f:
        json.dump(final_bom, f, ensure_ascii=False, indent=4)

    return jsonify({"status": "ok"})
