from flask import Flask, jsonify,abort
import sys
import db_mongo
import random
import json

reload(sys)
sys.setdefaultencoding( "utf-8" )

app = Flask(__name__)


@app.route('/api/v1.0/init/<string:task_id>',methods=['GET'])
def get_gra(task_id):
    nodes = [{"y": 0, "x": 5000 , "size": 2, "id": "0", "label": "AndySgd1995"}]
    edges = []
    db = db_mongo.init_db()
    coll = db_mongo.get_doc("user_1hop", db).find()
    coll2 = db_mongo.get_doc("relationship_2hop",db).find()
    j = 0
    for i in coll:
        j += 1
        legth = len(str(i['followers_count']))
        nodes.append({"id":str(i['id']), "label":j, "x":0 + random.randint(100 * j,100 * j + 50),"y":0 + random.randint(400,500),"size":legth})
        edges.append({"id":str(i['id']), "source":0,"target":str(i['id'])})
    j += 1

    for i in coll2:
        if (str(i['edge'][0]) != str(i['edge'][1])):
            nodes.append({"id":str(i['edge'][1]),"label":j, "x":random.randint(j,j+20),"y":0 + random.randint(2000,6000),"size":2})
            edges.append({"id":j,"source":str(i['edge'][0]),"target":str(i['edge'][1])})
            j += 1
    result = {"nodes":nodes,"edges":edges}
    return json.dumps(result)

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)