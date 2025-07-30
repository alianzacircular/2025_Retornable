// Event listener for DOMContentLoaded to render the initial Plotly graph
document.addEventListener('DOMContentLoaded', function () {
    // Render the Plotly graph with initial data
    Plotly.newPlot('graph', graph_json.data, graph_json.layout);
});

/**
 * Run the sample model and update the graph.
 */
async function runSampleModel() {
    // Show loading indicator (optional)
    const button = document.querySelector('.btn-success');
    const originalText = button.innerText;
    button.innerText = 'Running...';
    button.disabled = true;

    try {

        dem_interval_min = document.getElementById('dem_interval_min').value;
        dem_interval_max = document.getElementById('dem_interval_max').value;
        if (dem_interval_min == "" || dem_interval_max == "") {
            alert("Please fill in the minimum and maximum values for the demand interval.");
            return;
        }
        if (parseFloat(dem_interval_min) > parseFloat(dem_interval_max)) {
            alert("The minimum value for the demand interval cannot be greater than the maximum value.");
            return;
        }
        // Validate that the demand interval is a valid JSON array
        const dem_interval = [parseFloat(dem_interval_min), parseFloat(dem_interval_max)];
        // Gather input values
        const parameters = {
            /*
            container_value: parseFloat(document.getElementById('container_value').value),
            deposit: parseFloat(document.getElementById('deposit').value),
            clasification: parseFloat(document.getElementById('clasification').value),
            washing: parseFloat(document.getElementById('washing').value),
            transportation: parseFloat(document.getElementById('transportation').value),
            */
            // Parámetros técnicos
            ccv: parseFloat(document.getElementById('ccv').value),
            acv: parseFloat(document.getElementById('acv').value),
            lpl: parseFloat(document.getElementById('lpl').value),
            apl: parseFloat(document.getElementById('apl').value),
            ta: parseFloat(document.getElementById('ta').value),
            tl: parseFloat(document.getElementById('tl').value),

            // Parámetros de costo
            dep: parseFloat(document.getElementById('dep').value),
            envn: parseFloat(document.getElementById('envn').value),
            enr: parseFloat(document.getElementById('enr').value),
            tri: parseFloat(document.getElementById('tri').value),
            arr_cv: parseFloat(document.getElementById('arr_cv').value),
            arr_pl: parseFloat(document.getElementById('arr_pl').value),
            ade_cv: parseFloat(document.getElementById('ade_cv').value),
            ade_pl: parseFloat(document.getElementById('ade_pl').value),
            qc: parseFloat(document.getElementById('qc').value),
            qt: parseFloat(document.getElementById('qt').value),
            ql: parseFloat(document.getElementById('ql').value),
            qb: parseFloat(document.getElementById('qb').value),
            qa: parseFloat(document.getElementById('qa').value),
            cinv: parseFloat(document.getElementById('cinv').value),
            pinv: parseFloat(document.getElementById('pinv').value),

            // Parámetros del entorno
            wa: parseFloat(document.getElementById('wa').value),
            inflation: parseFloat(document.getElementById('inflation').value),
            recup: parseFloat(document.getElementById('recup').value),
            recup_increm: parseFloat(document.getElementById('recup_increm').value),
            dem_interval: dem_interval,
            adem: parseFloat(document.getElementById('adem').value),

            // Parámetros Ambientales
            em: parseFloat(document.getElementById('em').value),
            el: parseFloat(document.getElementById('el').value),
            et: parseFloat(document.getElementById('et').value),
            en: parseFloat(document.getElementById('en').value)
        };

        // Send POST request to Flask backend
        const response = await fetch('/run_sample_model', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(parameters)
        });

        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();

        // Update the Plotly graph
        updateGraph();
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while running the model.');
    } finally {
        // Reset button state
        button.innerText = originalText;
        button.disabled = false;
    }
}

/**
 * Update the Plotly graph with new data from the server.
 */
async function updateGraph() {
    try {
        const response = await fetch('/update_graph', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const graph_json = await response.json();
        Plotly.newPlot('graph', graph_json.data, graph_json.layout);
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while updating the graph.');
    }
}

/**
 * Upload a file and update the graph and control values based on the uploaded data.
 */
async function uploadFile() {
    // Show loading indicator (optional)
    const button = document.getElementById('btn_load');
    const originalText = button.innerText;
    button.innerText = 'Loading...';
    button.disabled = true;

    try {
        let fileInput = document.getElementById('file-input');
        if (fileInput.files.length === 0) {
            alert("Please select a file first!");
            return;
        }

        let formData = new FormData();
        formData.append("file", fileInput.files[0]);

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();      
        const graph_json = JSON.parse(data.graph_json);        
        const controls_default = data.controls_default;

        Plotly.newPlot('graph', graph_json.data, graph_json.layout);

        /* Update control column default values
        document.getElementById('container_value').value = controls_default['container_value'];
        document.getElementById('container_value').min = controls_default['container_value_min'];
        document.getElementById('container_value').max = controls_default['container_value_max'];
        document.getElementById('deposit').value = controls_default.deposit_value;
        document.getElementById('deposit').min = controls_default.deposit_min;  
        document.getElementById('deposit').max = controls_default.deposit_max;
        document.getElementById('clasification').value = controls_default.clasification_value;
        document.getElementById('clasification').min = controls_default.clasification_min;
        document.getElementById('clasification').max = controls_default.clasification_max;
        document.getElementById('washing').value = controls_default.washing_value;
        document.getElementById('washing').min = controls_default.washing_min;
        document.getElementById('washing').max = controls_default.washing_max;
        document.getElementById('transportation').value = controls_default.transportation_value;
        document.getElementById('transportation').min = controls_default.transportation_min;
        document.getElementById('transportation').max = controls_default.transportation_max;
        */
       /* New parameters into accordion  */
        /* Parámetros técnicos */
        console.log(controls_default)
        document.getElementById('ccv').value    = controls_default.ccv_value;
        document.getElementById('ccv').min      = controls_default.ccv_min;
        document.getElementById('ccv').max      = controls_default.ccv_max;
        document.getElementById('acv').value    = controls_default.acv_value;
        document.getElementById('acv').min      = controls_default.acv_min;
        document.getElementById('acv').max      = controls_default.acv_max;
        document.getElementById('lpl').value    = controls_default.lpl_value;
        document.getElementById('lpl').min      = controls_default.lpl_min;
        document.getElementById('lpl').max      = controls_default.lpl_max;
        document.getElementById('apl').value    = controls_default.apl_value;
        document.getElementById('apl').min      = controls_default.apl_min;
        document.getElementById('apl').max      = controls_default.apl_max;
        document.getElementById('ta').value     = controls_default.ta_value;
        document.getElementById('ta').min       = controls_default.ta_min;
        document.getElementById('ta').max       = controls_default.ta_max;
        document.getElementById('tl').value     = controls_default.tl_value;
        document.getElementById('tl').min       = controls_default.tl_min;
        document.getElementById('tl').max       = controls_default.tl_max;

        /* Parámetros de costo */
        document.getElementById('dep').value    = controls_default.dep_value;
        document.getElementById('dep').min      = controls_default.dep_min;
        document.getElementById('dep').max      = controls_default.dep_max;
        document.getElementById('envn').value   = controls_default.envn_value;
        document.getElementById('envn').min     = controls_default.envn_min;
        document.getElementById('envn').max     = controls_default.envn_max;
        document.getElementById('enr').value    = controls_default.enr_value;
        document.getElementById('enr').min      = controls_default.enr_min;
        document.getElementById('enr').max      = controls_default.enr_max;
        document.getElementById('tri').value    = controls_default.tri_value;
        document.getElementById('tri').min      = controls_default.tri_min;
        document.getElementById('tri').max      = controls_default.tri_max;
        document.getElementById('arr_cv').value = controls_default.arr_cv_value;
        document.getElementById('arr_cv').min   = controls_default.arr_cv_min;
        document.getElementById('arr_cv').max   = controls_default.arr_cv_max;
        document.getElementById('arr_pl').value = controls_default.arr_pl_value;
        document.getElementById('arr_pl').min   = controls_default.arr_pl_min;
        document.getElementById('arr_pl').max   = controls_default.arr_pl_max;
        document.getElementById('ade_cv').value = controls_default.ade_cv_value;
        document.getElementById('ade_cv').min   = controls_default.ade_cv_min;
        document.getElementById('ade_cv').max   = controls_default.ade_cv_max;
        document.getElementById('ade_pl').value = controls_default.ade_pl_value;
        document.getElementById('ade_pl').min   = controls_default.ade_pl_min;
        document.getElementById('ade_pl').max   = controls_default.ade_pl_max;
        document.getElementById('qc').value     = controls_default.qc_value;
        document.getElementById('qc').min       = controls_default.qc_min;
        document.getElementById('qc').max       = controls_default.qc_max;
        document.getElementById('qt').value     = controls_default.qt_value;
        document.getElementById('qt').min       = controls_default.qt_min;
        document.getElementById('qt').max       = controls_default.qt_max;
        document.getElementById('ql').value     = controls_default.ql_value;
        document.getElementById('ql').min       = controls_default.ql_min;
        document.getElementById('ql').max       = controls_default.ql_max;
        document.getElementById('qb').value     = controls_default.qb_value;
        document.getElementById('qb').min       = controls_default.qb_min;
        document.getElementById('qb').max       = controls_default.qb_max;
        document.getElementById('qa').value     = controls_default.qa_value;
        document.getElementById('qa').min       = controls_default.qa_min;
        document.getElementById('qa').max       = controls_default.qa_max;
        document.getElementById('cinv').value   = controls_default.cinv_value;
        document.getElementById('cinv').min     = controls_default.cinv_min;
        document.getElementById('cinv').max     = controls_default.cinv_max;
        document.getElementById('pinv').value   = controls_default.pinv_value;
        document.getElementById('pinv').min     = controls_default.pinv_min;
        document.getElementById('pinv').max     = controls_default.pinv_max;
        
        /* Parámetros del entorno */
        document.getElementById('wa').value         = controls_default.wa_value;
        document.getElementById('wa').min           = controls_default.wa_min;
        document.getElementById('wa').max           = controls_default.wa_max;
        document.getElementById('inflation').value  = controls_default.inflation_value;
        document.getElementById('inflation').min    = controls_default.inflation_min;
        document.getElementById('inflation').max    = controls_default.inflation_max;
        document.getElementById('recup').value      = controls_default.recup_value;
        document.getElementById('recup').min        = controls_default.recup_min;
        document.getElementById('recup').max        = controls_default.recup_max;
        document.getElementById('recup_increm').value = controls_default.recup_increm_value;
        document.getElementById('recup_increm').min = controls_default.recup_increm_min;
        document.getElementById('recup_increm').max = controls_default.recup_increm_max;
        // document.getElementById('dem_interval').value = controls_default.dem_interval_value;
        // document.getElementById('dem_interval').min = controls_default.dem_interval_min;
        // document.getElementById('dem_interval').max = controls_default.dem_interval_max;
        document.getElementById('dem_interval_min').value = controls_default.dem_interval_value[0];
        document.getElementById('dem_interval_max').value = controls_default.dem_interval_value[1];
        document.getElementById('adem').value       = controls_default.adem_value;
        document.getElementById('adem').min         = controls_default.adem_min;
        document.getElementById('adem').max         = controls_default.adem_max;

        /* Parámetros ambientales */
        document.getElementById('em').value     = controls_default.em_value;
        document.getElementById('em').min       = controls_default.em_min;
        document.getElementById('em').max       = controls_default.em_max;
        document.getElementById('el').value     = controls_default.el_value;
        document.getElementById('el').min       = controls_default.el_min;
        document.getElementById('el').max       = controls_default.el_max;
        document.getElementById('et').value     = controls_default.et_value;
        document.getElementById('et').min       = controls_default.et_min;
        document.getElementById('et').max       = controls_default.et_max;
        document.getElementById('en').value     = controls_default.en_value;
        document.getElementById('en').min       = controls_default.en_min;
        document.getElementById('en').max       = controls_default.en_max;
        document.getElementById('wa').value     = controls_default.wa_value;
        document.getElementById('wa').min       = controls_default.wa_min;
        document.getElementById('wa').max       = controls_default.wa_max;
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while uploading the file.');
    } finally {
        // Reset button state
        button.innerText = originalText;
        button.disabled = false;
    }
}


async function upload_dist_file() {
    const button = document.getElementById('btn_load_dist');
    const originalText = button.innerText;
    button.innerText = 'Loading...';
    button.disabled = true;

    try {
        let fileInput = document.getElementById('file-dist');
        if (fileInput.files.length === 0) {
            alert("Please select a file first!");
            return;
        }

        let formData = new FormData();
        formData.append("file_dist", fileInput.files[0]);

        const response = await fetch('/upload_dist_file', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();      
        const graph_json = JSON.parse(data.graph_json);        
        const controls_default = data.controls_default;
        Plotly.newPlot('graph', graph_json.data, graph_json.layout);

    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while uploading the file.');
    } finally {
        // Reset button state
        button.innerText = originalText;
        button.disabled = false;
    }

}

/** Upload the coordinates file for generate the distance file */
async function upload_coord_file() {
    const button = document.getElementById('btn_load_coord');
    const originalText = button.innerText;
    button.innerText = 'Loading...';
    button.disabled = true;
    document.getElementById('fullscreen-spinner').style.display = 'block';

    try {
        let fileInput = document.getElementById('file_coord');
        if (fileInput.files.length === 0) {
            alert("Please select a file first!");
            return;
        }

        let formData = new FormData();
        formData.append("file_coord", fileInput.files[0]);

        const response = await fetch('/calculate_distances', {
            method: 'POST',
            body: formData
        }).then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'distances.csv';
            document.body.appendChild(a);
            a.click();
            a.remove();
            alert('File downloaded');
        });

        // if (!response.ok) {
        //     throw new Error('Network response was not ok');
        // }else {
        //     return response.json();
        // }

        
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while uploading the file.');
    } finally {
        // Reset button state
        button.innerText = originalText;
        button.disabled = false;
        document.getElementById('fullscreen-spinner').style.display = 'none';
    }

}



