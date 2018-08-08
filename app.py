from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import json
import re

app = Flask(__name__)
api = Api(app)
CORS(app)

DUMMY_DATA = {
        'data': 'hello, world'
}

pattern = re.compile(r'_(\d+)_percent_full')

def getDamLevels():
    '''gets dam levels'''
    with open('dams.json', 'r') as f:
       dat = f.readlines()
       jsonData = json.loads(''.join(dat))
       return [transformDamData(j) for j in jsonData]

def transformDamData(provinceData):
    response = {}
    levelMapped = {pattern.match(k).groups()[0]: float(v) for (k, v) in provinceData.items() if pattern.match(k)}
    response['levels'] = [{'date': k, 'measurement': v} for (k,v) in levelMapped.items()]
    response['province'] = provinceData['summary_province']
    response['fsc'] = float(provinceData['fsc_1_000_000m'])
    response['waterInStorage'] = float(provinceData['water_in_storage_1_000_000m'])
    response['capital'] = provinceData.get('capital')

    return response


DAM_LEVELS = getDamLevels()

class DummyData(Resource):
    def get(self):
        return DUMMY_DATA
    
    def put(self):
        json_data = request.get_json()
        DUMMY_DATA['data'] = json_data
        return {}, 204

class DamController(Resource):
    def get(self):
        return DAM_LEVELS

api.add_resource(DummyData, '/data')
api.add_resource(DamController, '/dam-levels')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
