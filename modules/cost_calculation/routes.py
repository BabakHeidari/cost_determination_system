from flask import Blueprint, render_template
from utils.auth import login_required
from utils.paths import product_path
from utils.load_data import load_json

cost_calculation_bp = Blueprint("cost_calculation", __name__)

@cost_calculation_bp.route("/cost_calculation")
@login_required
def cost_cal():
    products = load_json(product_path+".json")
    return render_template("cost/calculation.html", table_json = products)

