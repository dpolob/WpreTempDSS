from flask import Flask, jsonify, request
from flask import Response, make_response

import globals
from predictors.temp import temp_prediction

from multiprocessing.dummy import Pool
from send_mmt import send_mmt

# Logging module
import logging
import logging.config
import loggly.handlers

import exceptions

if globals.LOGLY:
    logging.config.fileConfig('loggly.conf')
else:
    logging.basicConfig(filename='mylog.log', level=logging.INFO)
logger = logging.getLogger()


pool = Pool(2)
app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'status': 'TEMP PREDICTION route not found'}), 404)

# API for entry point commands
@app.route('/stop_alg', methods=['GET'])
def get_stopalg():
    if request.method == 'GET':
        logger.info("[{}] /stop_alg {} method requested from {}".format(globals.NAME, request.method, request.url))
        return Response("{\"status\" : \"STOPPED\", \"msg\" : {\"OK\" : \"Algorithm stopped\"}}", status=200, mimetype='application/json')

@app.route('/run_alg', methods=['POST'])
def post_runalg():
    global pool
    if request.method == 'POST':
        try:
            logger.info("[{}][/run_alg] {} method requested from {}".format(globals.NAME, request.method, request.url))
            data = request.get_json()
            if 'config' not in data.keys() or 'request_id' not in data.keys() or 'dss_api_endpoint' not in data.keys():
                raise exceptions.json_key_incorrect_exception(log=logger, value="[{}][/run_alg] Json Keys are wrong".format(globals.NAME))
     
            status, maxima, minima = temp_prediction.temp_prediction()

            logger.info("[{}][/run_alg] Status: {} Max: {} Min: {} from temp predictor".format(globals.NAME, status, maxima, minima, logger))
            if status == "ERROR":
                raise exceptions.error_result_exception(log=logger, value="[{}][/run_alg] rain_prediction throwed an error".format(globals.NAME))
            else:
                #convey to MMT through DSS
                pool.apply_async(send_mmt, (data, maxima, "irrigation", "ºC Max " + str(minima) + " ºC Min", logger))
                # Reply to DSS 
                print(maxima, "ºC Max - " + str(minima) + " ºC Min")
                logger.info("[{}][/run_alg] {} Reply to DSS. Algorithm started and info sent to MMT".format(globals.NAME, request.method))
                return Response("{\"status\" : \"STARTED\", \"msg\" : {\"OK\" : \"Algorithm started and info sent to MMT\"}}", status=200,    mimetype='application/json')
                
        except exceptions.json_key_incorrect_exception as e:
            return make_response(jsonify(dict({"status" : "ERROR", "msg" : str(e)})), 500)
        except exceptions.error_result_exception as e:
            return make_response(jsonify(dict({"status" : "ERROR", "msg" : str(e)})), 500)
        except Exception as e:
            return make_response(jsonify(dict({"status" : "ERROR", "msg" : str(e)})), 500)

@app.route('/status_alg', methods=['GET'])
def get_statusalg():
    if request.method == 'GET':
        logger.info("[{}][/run_status] {} method requested from {}".format(globals.NAME, request.method, request.url))
        values = {"status": "STARTED",
                  "msg" : {
                            "flask_port" : globals.FLASKPORT,
                    }
                }
        return make_response(jsonify(values), 200)      

if __name__ == '__main__':
    #parameters=read_parameters.read_parameters()
    app.run(debug=True, host='0.0.0.0', port=globals.FLASKPORT)
