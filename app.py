from flask import Flask, render_template, request, jsonify
from calculate_distances import calculate_distances
import plotly
import os
import json
import requests
from pyomo.environ import *
from pyomo.opt import SolverFactory
from utilities import read_data, create_instance, create_map, create_df_coord
from opt_pyomo import create_model_pyomo, get_vars_sol_pyomo
from opt_gurobipy import create_model_gb, get_vars_sol_gb
import gurobipy as gp
from gurobipy import GRB

# Initialize Flask application
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global variables to store optimization solution and default controls
opt_solution = {}
controls_default = {}

# Paths to data files
json_path = "data/data.json"
url_coord = 'https://docs.google.com/uc?export=download&id=1VYEnH735Tdgqe9cS4ccYV0OUxMqQpsQh'
url_dist = 'https://docs.google.com/uc?export=download&id=1Apbc_r3CWyWSVmxqWqbpaYEacbyf1wvV'
url_demand = 'https://docs.google.com/uc?export=download&id=1w0PMK36H4Aq39SAaJ8eXRU2vzHMjlWGe'
parameters = read_data(json_path, url_coord, url_dist, url_demand)

def get_controls_default(parameters):
    """
    Generate default control values based on parameters.

    Parameters
    ----------
    parameters : dict
        Dictionary containing parameter values.

    Returns
    -------
    dict
        Dictionary containing default control values.
    """
    controls_default = {
        'container_value': parameters['enr'],
        'container_min': 0,
        'container_max': 10 * parameters['enr'],
        'deposit_value': parameters['dep'],
        'deposit_min': 0,
        'deposit_max': 10 * parameters['dep'],
        'clasification_value': parameters['qc'],
        'clasification_min': 0,
        'clasification_max': 10 * parameters['qc'],
        'washing_value': parameters['ql'],
        'washing_min': 0,
        'washing_max': 10 * parameters['ql'],
        'transportation_value': parameters['qa'],
        'transportation_min': 0,
        'transportation_max': 10 * parameters['qa'],
        'transportation_step': 0.1,

        # ### New parameters into accordion ### #
        # ### Parámetros técnicos ### #
        'ccv_value': parameters['ccv'],
        'ccv_min': 0,
        'ccv_max': 10 * parameters['ccv'],
        'acv_value': parameters['acv'],
        'acv_min': 0,
        'acv_max': 10 * parameters['acv'],
        'lpl_value': parameters['lpl'],
        'lpl_min': 0,
        'lpl_max': 10 * parameters['lpl'],
        'apl_value': parameters['apl'],
        'apl_min': 0,
        'apl_max': 10 * parameters['apl'],
        'ta_value': parameters['ta'],
        'ta_min': 0,
        'ta_max': 10 * parameters['ta'],
        'tl_value': parameters['tl'],
        'tl_min': 0,
        'tl_max': 10 * parameters['tl'],

        # ### Parámetros técnicos ### #
        'dep_value': parameters['dep'],
        'dep_min': 0,
        'dep_max': 10 * parameters['dep'],
        'envn_value': parameters['envn'],
        'envn_min': 0,
        'envn_max': 10 * parameters['envn'],
        'enr_value': parameters['enr'],
        'enr_min': 0,
        'enr_max': 10 * parameters['enr'],
        'tri_value': parameters['tri'],
        'tri_min': 0,
        'tri_max': 10 * parameters['tri'],
        'arr_cv_value': parameters['arr_cv'],
        'arr_cv_min': 0,
        'arr_cv_max': 10 * parameters['arr_cv'],
        'arr_pl_value': parameters['arr_pl'],
        'arr_pl_min': 0,
        'arr_pl_max': 10 * parameters['arr_pl'],
        'ade_cv_value': parameters['ade_cv'],
        'ade_cv_min': 0,
        'ade_cv_max': 10 * parameters['ade_cv'],
        'ade_pl_value': parameters['ade_pl'],
        'ade_pl_min': 0,
        'ade_pl_max': 10 * parameters['ade_pl'],
        'qc_value': parameters['qc'],
        'qc_min': 0,
        'qc_max': 10 * parameters['qc'],
        'qt_value': parameters['qt'],
        'qt_min': 0,
        'qt_max': 10 * parameters['qt'],
        'ql_value': parameters['ql'],
        'ql_min': 0,
        'ql_max': 10 * parameters['ql'],
        'qb_value': parameters['qb'],
        'qb_min': 0,
        'qb_max': 10 * parameters['qb'],
        'qa_value': parameters['qa'],
        'qa_min': 0,
        'qa_max': 10 * parameters['qa'],
        'cinv_value': parameters['cinv'],
        'cinv_min': 0,
        'cinv_max': 10 * parameters['cinv'],
        'pinv_value': parameters['pinv'],
        'pinv_min': 0,
        'pinv_max': 10 * parameters['pinv'],
        
        # ### Parámetros del entorno ### #
        'wa_value': parameters['wa'],
        'wa_min': 0,
        'wa_max': 10 * parameters['wa'],
        'inflation_value': parameters['inflation'],
        'inflation_min': 0,
        'inflation_max': 10 * parameters['inflation'],
        'recup_value': parameters['recup'],
        'recup_min': 0,
        'recup_max': 10 * parameters['recup'],
        'recup_increm_value': parameters['recup_increm'],
        'recup_increm_min': 0,
        'recup_increm_max': 10 * parameters['recup_increm'],
        'dem_interval_value': parameters['dem_interval'],
        'dem_interval_min': 0,
        'dem_interval_max': 10 * parameters['dem_interval'],
        'adem_value': parameters['adem'],
        'adem_min': 0,
        'adem_max': 10 * parameters['adem'],

        # ### Parámetros ambientales ### #
        'em_value': parameters['em'],
        'em_min': 0,
        'em_max': 10 * parameters['em'],
        'el_value': parameters['el'],
        'el_min': 0,
        'el_max': 10 * parameters['el'],
        'et_value': parameters['et'],
        'et_min': 0,
        'et_max': 10 * parameters['et'],
        'en_value': parameters['en'],
        'en_min': 0,
        'en_max': 10 * parameters['en'],
        'wa_value': parameters['wa'],
        'wa_min': 0,
        'wa_max': 10 * parameters['wa'],
        

    }
    print(parameters['dem_interval'][1])
    return controls_default

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and update parameters.

    Returns
    -------
    json
        JSON response containing graph data and default controls.
    """
    global parameters

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        # TODO: Decide how to load coord and distances
        parameters = read_data(filepath, url_coord, url_dist, url_demand)
        fig = create_map(parameters['df_coord'])
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        controls_default = get_controls_default(parameters)
        return jsonify({'graph_json': graph_json, 'controls_default': controls_default})

@app.route('/run_sample_model', methods=['POST'])
def run_sample_model():
    """
    Run the sample optimization model.

    Returns
    -------
    json
        JSON response indicating the result of the model run.
    """
    inputs = request.get_json()
    #parameters['enr'] = inputs['container_value']
    #parameters['dep'] = inputs['deposit']
    #parameters['qc'] = inputs['clasification']
    #parameters['ql'] = inputs['washing']
    #parameters['qa'] = inputs['transportation']
    
    # Parámetros sin clasificación
    parameters['n_acopios'] = 5
    parameters['n_centros'] = 5
    parameters['n_plantas'] = 3
    parameters['n_productores'] = 5
    parameters['n_envases'] = 3
    parameters['n_periodos'] = 10

    # Parámetros técnicos
    parameters['ccv'] = inputs['ccv']
    parameters['acv'] = inputs['acv']
    parameters['lpl'] = inputs['lpl']
    parameters['apl'] = inputs['apl']
    parameters['ta'] = inputs['ta']
    parameters['tl'] = inputs['tl']

    # Parámetros de costo
    parameters['dep'] = inputs['dep']
    parameters['envn'] = inputs['envn']
    parameters['enr'] = inputs['enr']
    parameters['tri'] = inputs['tri']
    parameters['arr_cv'] = inputs['arr_cv']
    parameters['arr_pl'] = inputs['arr_pl']
    parameters['ade_cv'] = inputs['ade_cv']
    parameters['ade_pl'] = inputs['ade_pl']
    parameters['qc'] = inputs['qc']
    parameters['qt'] = inputs['qt']
    parameters['ql'] = inputs['ql']
    parameters['qb'] = inputs['qb']
    parameters['qa'] = inputs['qa']
    parameters['cinv'] = inputs['cinv']
    parameters['pinv'] = inputs['pinv']

    # Parámetros del entorno
    parameters['wa'] = inputs['wa']
    parameters['inflation'] = inputs['inflation']
    parameters['recup'] = inputs['recup']
    parameters['recup_increm'] = inputs['recup_increm']
    parameters['dem_interval'] = inputs['dem_interval']
    parameters['adem'] = inputs['adem']

    # Parámetros Ambientales
    parameters['em'] = inputs['em']
    parameters['el'] = inputs['el']
    parameters['et'] = inputs['et']
    parameters['en'] = inputs['en']

    instance = create_instance(parameters, seed=7)
    
    # Uncomment the following lines to use Gurobi solver
    # model = create_model_gb(instance)
    # model.setParam('MIPGap', 0.05)  # Set the MIP gap tolerance to 5% (0.05)
    # model.optimize()
    # opt_solution['variables'] = get_vars_sol_gb(model)

    # Use Pyomo solver
    solver = SolverFactory('appsi_highs')
    solver.options['mip_rel_gap'] = 0.01
    model = create_model_pyomo(instance)
    solver.solve(model, tee=True)
    opt_solution['variables'] = get_vars_sol_pyomo(model)

    return jsonify({'result': True})

@app.route('/update_graph', methods=['POST'])
def update_graph():
    """
    Update the graph based on the optimization solution.

    Returns
    -------
    json
        JSON response containing updated graph data.
    """
    global opt_solution

    df_coord = create_df_coord(opt_solution['variables'], parameters['df_coord'])
    fig = create_map(df_coord)
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json

@app.route('/calculate_distances', methods=['GET'])
def calculate_distances_route():
    return calculate_distances()


@app.route('/')
def index():
    """
    Render the main page with initial graph and controls.

    Returns
    -------
    html
        Rendered HTML template for the main page.
    """
    controls_default = get_controls_default(parameters)
    fig = create_map(parameters['df_coord'])
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', graph_json=graph_json, controls_default=controls_default)

if __name__ == '__main__':
    app.run(debug=True)