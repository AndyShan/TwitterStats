from flask import Flask, jsonify,abort
import sys
import db_mongo
import random
import json

reload(sys)
sys.setdefaultencoding( "utf-8" )

app = Flask(__name__)
@app.route('/api/v1.0/hop1/<string:task_id>',methods=['GET'])
def get_1hop(task_id):
    nodes = [{"y": 0, "x": 50, "size": 2, "id": 0, "label": "AndySgd1995"}]
    edges = []
    db = db_mongo.init_db()
    coll = db_mongo.get_doc("user_1hop", db).find()
    coll2 = db_mongo.get_doc("relationship_1hop",db)
    j = 0
    for i in coll:
        j += 1
        legth = len(str(i['followers_count']))
        nodes.append({"id":j, "label":str(i['id']), "x":0 + random.randint(10,100),"y":0 + random.randint(10,50),"size":legth})
        edges.append({"id":j, "source":0,"target":j})
    result = {"nodes":nodes,"edges":edges}
    return json.dumps(result)

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)