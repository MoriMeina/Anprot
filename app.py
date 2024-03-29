import os
import uuid
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
    Level = db.Column(db.String(255), nullable=False)
    SN = db.Column(db.String(255), nullable=False)
    Profile = db.Column(db.String(255), nullable=False)
    Location = db.Column(db.JSON, nullable=False)

    # class locationquery(db.Model):
    #     Animal = db.Column(db.String(255), primary_key=True, nullable=False)
    #     Location = db.Column(db.JSON, nullable=False)

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


class userdata(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(255), nullable=False)
    isadmin = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), nullable=True)


class waitcheck(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Class = db.Column(db.String(255), nullable=False)
    Order = db.Column(db.String(255), nullable=False)
    Animal = db.Column(db.String(255), nullable=False)
    Level = db.Column(db.String(255), nullable=False)
    SN = db.Column(db.String(255), nullable=False)
    Profile = db.Column(db.String(255), nullable=False)
    Location = db.Column(db.JSON, nullable=False)


# 前端初始化时获取所有动物的经纬度在地图上进行标记
@app.route('/trans/api/location', methods=['GET'])
def test_getlocation():
    try:
        users = animaldata.query.all()
        features = []
        for data in users:
            animal = data.Animal
            location = data.Location
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


# 获取动物名对应的pdf文件名，返回给前端
@app.route('/trans/api/pdfname', methods=['GET'])
def get_pdfname():
    try:
        name = request.args.get('name')
        users = animaldata.query.filter(animaldata.Animal.like(name)).all()
        pdfname = [u.Profile for u in users]
        profile = ''.join(pdfname)
        return profile
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})


# 根据type和动物名搜索数据库，返回给前端
@app.route('/trans/api/search', methods=['GET'])
def search_animal_byfilter():
    name = request.args.get('name')
    search = request.args.get('type')
    try:
        # 按照类查询
        if search == 'all':
            users = animaldata.query.filter(animaldata.Animal.like('%' + name + '%')).all()
            # users = animaldata.query.filter_by(Animal={name}).all()
            Class = [u.Class for u in users]
            Order = [u.Order for u in users]
            Animal = [u.Animal for u in users]
            Level = [u.Level for u in users]
            SN = [u.SN for u in users]
            Profile = [u.Profile for u in users]
            Location = [u.Location for u in users]
            if (len(Class) == 0 and len(Order) == 0 and len(Animal) == 0 and len(Level) == 0 and len(SN) == 0 and len(
                    Profile) == 0):
                return ''
            else:
                jsonf = {'status': 'success',
                         'data': {'Class': Class, 'Order': Order, 'label': Animal, 'Level': Level, 'SN': SN,
                                  'value': Profile, 'Location': Location}
                         }
                return jsonify(jsonf)
        else:
            if search == 'Class':
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
                if search == 'Order':
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
                                 'data': {'Class': Class, 'Order': Order, 'label': Animal, 'Level': Level, 'SN': SN,
                                          'value': Profile}
                                 }
                        return jsonify(jsonf)
                else:
                    if search == 'Level':
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
                    else:
                        users = animaldata.query.filter_by(Animal=name).all()
                        location = [u.Location for u in users]
                    jsonf = {
                        'location': location
                    }
                    return jsonify(jsonf)

    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})


# 从请求pdf名称，返回动物信息和动物简介，然后在前端覆盖页面中显示
# @app.route('/pdf/<animal>', methods=['GET'])
# def search_file(animal):
#     try:
#         file_path = './pdf/' + animal
#         if os.path.exists(file_path):
#             headers = ("Content-Disposition", f"inline;filename={file_path}")
#             as_attachment = False
#             response = make_response(send_file(file_path, as_attachment=as_attachment))
#             response.headers[headers[0]] = headers[1]
#             return response
#         else:
#             return 'fail'
#
#     except Exception as e:
#         return jsonify({'status': 'fail', 'error': str(e)})
@app.route('/trans/api/pdf/<animal>', methods=['GET'])
def search_file(animal):
    try:
        file_path = './pdf/' + animal
        if os.path.exists(file_path):
            filename_bytes = animal.encode('utf-8')
            filename = filename_bytes.decode('latin-1')
            headers = ("Content-Disposition", f"inline;filename={filename}")
            as_attachment = False
            response = make_response(send_file(file_path, as_attachment=as_attachment))
            response.headers[headers[0]] = headers[1]
            return response
        else:
            return 'fail'

    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})


# 根据类搜索动物的经纬度，返回给前端geojson，在地图上标记。用于filter按钮，请求格式[POST]：http://localhost:5000/trans/api/byclass
@app.route('/trans/api/byclass', methods=['POST'])
def search_class_from_loc():
    data = request.get_json()
    classes = data['class']
    try:
        features = []
        for name in classes:
            users = animaldata.query.filter_by(Class=name).all()
            for data in users:
                animal = data.Animal
                location = data.Location
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


# 根据濒危等级搜索动物的经纬度，返回给前端geojson，在地图上标记。用于filter按钮，请求格式[POST]：http://localhost:5000/trans/api/bylevel
@app.route('/trans/api/bylevel', methods=['POST'])
def search_level_from_loc():
    data = request.get_json()
    levels = data['level']
    try:
        features = []
        for name in levels:
            users = animaldata.query.filter_by(Level=name).all()
            for data in users:
                animal = data.Animal
                location = data.Location
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


# 登录API
@app.route('/trans/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    try:
        users = userdata.query.filter_by(username=username).all()
        if len(users) == 0:
            return jsonify({'status': 'fail', 'error': '用户名不存在'})
        else:
            user = users[0]
            if user.password == password:
                token = uuid.uuid1()
                user.token = token
                db.session.commit()
                return jsonify({'status': 'success', 'token': token})
            else:
                return jsonify({'status': 'fail', 'error': '密码错误'})
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})


# 注册API
@app.route('/trans/api/register', methods=['POST'])
def register():
    data = request.get_json()
    nickname = data['nickname']
    email = data['email']
    username = data['username']
    password = data['password']
    phone = data['phone']
    try:
        users = userdata.query.filter_by(username=username).all()
        if len(users) == 0:
            user = userdata(nickname=nickname, email=email, username=username, password=password, phone=phone)
            db.session.add(user)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'fail', 'error': '用户名已存在'})
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})


# 临时上传pdf
@app.route('/trans/api/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = file.filename
        save_file_path = './save/'
        # 设置缓存文件夹
        file.save(os.path.join(save_file_path, filename))
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail', 'error': '上传失败'})


# 修改密码API
@app.route('/trans/api/changepass', methods=['POST'])
def changepass():
    data = request.get_json()
    username = data['username']
    oldPassword = data['oldPassword']
    newPassword = data['newPassword']
    try:
        users = userdata.query.filter_by(username=username).all()
        if len(users) == 0:
            return jsonify({'status': 'fail', 'error': '用户名不存在'})
        else:
            user = users[0]
            if user.password == oldPassword:
                user.password = newPassword
                db.session.commit()
                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'fail', 'error': '原密码错误'})
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})


# 忘记密码API
@app.route('/trans/api/forgotpass', methods=['POST'])
def forgotpass():
    data = request.get_json()
    username = data['username']
    mail = data['mail']
    newPassword = data['newPassword']
    try:
        users = userdata.query.filter_by(username=username).all()
        if len(users) == 0:
            return jsonify({'status': 'fail', 'error': '用户名不存在'})
        else:
            user = users[0]
            if user.email == mail:
                user.password = newPassword
                db.session.commit()
                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'fail', 'error': '原密码错误'})
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})


# 或许个人信息API
@app.route('/trans/api/personal', methods=['POST'])
def personal():
    data = request.get_json()
    token = data['token']
    try:
        users = userdata.query.filter_by(token=token).all()
        if len(users) == 0:
            return jsonify({'status': 'fail', 'error': '用户名不存在'})
        else:
            user = users[0]
            return jsonify(
                {'status': 'success', 'username': user.username, 'nickname': user.nickname, 'email': user.email,
                 'phone': user.phone})
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})


# 更新个人信息API
@app.route('/trans/api/updatepersonal', methods=['POST'])
def updatepersonal():
    data = request.get_json()
    token = data['token']
    nickname = data['nickname']
    email = data['email']
    profile = data['profile']
    phone = data['phone']
    try:
        users = userdata.query.filter_by(token=token).all()
        if len(users) == 0:
            return jsonify({'status': 'fail', 'error': '用户名不存在'})
        else:
            user = users[0]
            user.nickname = nickname
            user.email = email
            user.phone = phone
            user.profile = profile
            db.session.commit()
            return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})


# 上传文件API
@app.route('/trans/api/uploadfile', methods=['POST'])
def uploadfile():
    data = request.get_json()
    Class = data['Class']
    Order = data['Order']
    Animal = data['Animal']
    Level = data['level']
    SN = data['SN']
    location = data['Lat']
    profile = data['profile']
    try:
        users = waitcheck(Class=Class, Order=Order, Animal=Animal, Level=Level, SN=SN, Location=location,
                          Profile=profile)
        db.session.add(users)  # 添加到会话中
        db.session.commit()  # 提交会话
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
