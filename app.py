import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import send_file, make_response


app = Flask(__name__)
CORS(app)

user = 'root'
password = 'Meina9758'
database = 'AnProtect'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@10.1.0.110:3306/%s' % (user, password, database)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class animaldata(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Class = db.Column(db.String(255), nullable=False)
    Order = db.Column(db.String(255), nullable=False)
    Animal = db.Column(db.String(255), nullable=False)
    Level = db.Column(db.Integer, nullable=False)
    SN = db.Column(db.String(255), nullable=False)
    Profile = db.Column(db.String(255), nullable=False)
    Location = db.Column(db.JSON, nullable=False)


class locationquery(db.Model):
    Animal = db.Column(db.String(255), primary_key=True, nullable=False)
    Location = db.Column(db.JSON, nullable=False)

    def to_feature(self):
        return {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': self.location
            },
            'properties': {
                'animal': self.name
            }
        }


# 前端初始化时获取所有动物的经纬度在地图上进行标记
@app.route('/api/location', methods=['GET'])
# def get_location():
#     try:
#         users = locationquery.query.all()
#         animal = [u.Animal for u in users]
#         location = [u.Location for u in users]
#         jsonf = {'status':'success','data':{'Animal':animal,'Location':location}}
#         return jsonify(jsonf)
#     except Exception as e:
#         return jsonify({'status': 'fail', 'error': str(e)})

# def test_getlocation():
#     # 从数据库中读取名称和经纬度转换为geojson数据返回
#     try:
#         # animal = animaldata.query.all()
#         users = locationquery.query.all()
#         animal = [u.Animal for u in users]
#         location = [u.Location for u in users]
#         features = {
#             'type': 'Feature',
#             'geometry': {
#                 'type': 'Point',
#                 'coordinates': location[0]
#             },
#             'properties': {
#                 'animal': animal
#             }
#         }
#         jsonf = {
#             'type': 'FeatureCollection',
#             'features': [features]
#         }
#         return jsonify(jsonf)
#     except Exception as e:
#         return jsonify({'status': 'fail', 'error': str(e)})

def test_getlocation():
    try:
        users = locationquery.query.all()
        features = []
        for user in users:
            animal = user.Animal
            location = user.Location
            feature = {
                'type': 'Feature',
                'properties': {
                    'name': animal
                },
                'geometry': {
                    'type': 'Point',
                    'coordinates': location
                }
            }
            features.append(feature)
        jsonf = {
            'type': 'FeatureCollection',
            'features': features
        }
        return jsonify(jsonf)
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})


@app.route('/search', methods=['GET'])
def search_animal_byfilter():
    name = request.args.get('name')
    search = request.args.get('type')
    try:
        # 按照类查询
        if (search == 'all'):
            users = animaldata.query.filter(animaldata.Animal.like('%' + name + '%')).all()
            # users = animaldata.query.filter_by(Animal={name}).all()
            Class = [u.Class for u in users]
            Order = [u.Order for u in users]
            Animal = [u.Animal for u in users]
            Level = [u.Level for u in users]
            SN = [u.SN for u in users]
            Profile = [u.Profile for u in users]
            if (len(Class) == 0 and len(Order) == 0 and len(Animal) == 0 and len(Level) == 0 and len(SN) == 0 and len(
                    Profile) == 0):
                return ''
            else:
                jsonf = {'status': 'success',
                         'data': {'Class': Class, 'Order': Order, 'label': Animal, 'Level': Level, 'SN': SN,
                                  'value': Profile}
                         }
                return jsonify(jsonf)
        else:
            if (search == 'Class'):
                users = animaldata.query.filter(animaldata.Class.like('%' + name + '%')).all()
                # users = animaldata.query.filter_by(Class={name}).all()
                Class = [u.Class for u in users]
                Order = [u.Order for u in users]
                Animal = [u.Animal for u in users]
                Level = [u.Level for u in users]
                SN = [u.SN for u in users]
                Profile = [u.Profile for u in users]
                if (len(Class) == 0 and len(Order) == 0 and len(Animal) == 0 and len(Level) == 0 and len(
                        SN) == 0 and len(Profile) == 0):
                    return ''
                else:
                    jsonf = {'status': 'success',
                             'data': {'Class': Class, 'Order': Order, 'label': Animal, 'Level': Level, 'SN': SN,
                                      'value': Profile}
                             }
                    return jsonify(jsonf)
            else:
                if (search == 'Order'):
                    users = animaldata.query.filter(animaldata.Order.like('%' + name + '%')).all()
                    # users = animaldata.query.filter_by(Order={name}).all()
                    Class = [u.Class for u in users]
                    Order = [u.Order for u in users]
                    Animal = [u.Animal for u in users]
                    Level = [u.Level for u in users]
                    SN = [u.SN for u in users]
                    Profile = [u.Profile for u in users]
                    if (len(Class) == 0 and len(Order) == 0 and len(Animal) == 0 and len(Level) == 0 and len(
                            SN) == 0 and len(Profile) == 0):
                        return ''
                    else:
                        jsonf = {'status': 'success',
                                 'data': {'Class': Class,'Order': Order, 'label': Animal, 'Level': Level, 'SN': SN, 'value': Profile}
                                 }
                        return jsonify(jsonf)
                else:
                    if (search == 'Level'):
                        users = animaldata.query.filter(animaldata.Level.like('%' + name + '%')).all()
                        # users = animaldata.query.filter_by(Level={name}).all()
                        Class = [u.Class for u in users]
                        Order = [u.Order for u in users]
                        Animal = [u.Animal for u in users]
                        Level = [u.Level for u in users]
                        SN = [u.SN for u in users]
                        Profile = [u.Profile for u in users]
                        if (len(Class) == 0 and len(Order) == 0 and len(Animal) == 0 and len(Level) == 0 and len(
                                SN) == 0 and len(Profile) == 0):
                            return ''
                        else:
                            jsonf = {'status': 'success',
                                     'data': {'Class': Class, 'Order': Order, 'label': Animal, 'Level': Level, 'SN': SN,
                                              'value': Profile}
                                     }
                            return jsonify(jsonf)
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})


# @app.route('/api/queryall', methods=['GET'])
# def api_query_first():
#     try:
#         # db.session.execute(text('select * from LocationQuery;'))
#         # return jsonify({'status': 'success'})
#         # users = LocationQuery.query.all()
#         users = animaldata.query.all()
#         ID = [u.ID for u in users]
#         Class = [u.Class for u in users]
#         Order = [u.Order for u in users]
#         Animal = [u.Animal for u in users]
#         Level = [u.Level for u in users]
#         SN = [u.SN for u in users]
#         pdf = [u.pdf for u in users]
#         Location = [u.Location for u in users]
#         jsonf = {'status': 'success', 'data': {'ID': ID, 'Class': Class, 'Order': Order, 'Animal': Animal,
#                                                'Level': Level, 'SN': SN, 'pdf': pdf, 'Location': Location}}
#         return jsonify(jsonf)
#     except Exception as e:
#         return jsonify({'status': 'fail', 'error': str(e)})


# 从前端POST过来的动物名称，返回动物信息和动物简介，然后在前端覆盖页面中显示
@app.route('/pdf/<animal>', methods=['GET'])
def search_file(animal):
    try:
        # users = animaldata.query.filter_by(Animal=animal).all()
        # Profile = [u.Profile for u in users]
        # File = ''.join(Profile)
        file_path = './pdf/' + animal
        if os.path.exists(file_path):
            headers = ("Content-Disposition", f"inline;filename={file_path}")
            as_attachment = False
            response = make_response(send_file(file_path,as_attachment=as_attachment))
            response.headers[headers[0]] = headers[1]
            return response
        else:
            return 'fail'

    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})


# 当点击地图标记点时回传经纬度，在数据库中查找该经纬度附近的动物，返回动物名称，在前端用列表或表单显示
@app.route('/api/location/<location>', methods=['POST'])
def search_animal_from_loc(location):
    try:
        Location = animaldata.query.filter_by(Location=location).all()
        Animal = [u.Animal for u in Location]
        jsonf = {'status': 'success', 'data': {'Animal': Animal}}
        return jsonify(jsonf)
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})


if __name__ == '__main__':
    app.run()
