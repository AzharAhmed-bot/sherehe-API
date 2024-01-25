from flask import Flask, jsonify, make_response, request
from models import db, Users
from flask_cors import CORS
from config import AppConfig
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config.from_object(AppConfig)
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return make_response(jsonify({"Message": "Welcome to sherehe API"}))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        users = [user.to_dict() for user in Users.query.all()]
        return jsonify({'users': users})
    elif request.method == "POST":
        data = request.get_json()
        password = data.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        data['password'] = hashed_password
        new_user = Users(**data)  
        db.session.add(new_user)
        db.session.commit()
        response = make_response(new_user.to_dict()) 
        return jsonify({"New user": response}), 201


@app.route('/update/<int:id>',methods=["GET","PATCH","DELETE"])
def update(id):
    user=Users.query.filter_by(id=id).first()
    if request.method=="GET":
        if not user:
            return jsonify({"error":"User does not exist."}),404
        return make_response(jsonify({"User":user.to_dict()}),200)
    elif request.method=="DELETE":    
        if not user:
            return make_response(jsonify({"message":f"No user with id {id}"}),400)
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message" : f"User {id} has been sucessfully deleted"} ),200)
    elif request.method=="PATCH":
        if not user:
            return make_response(jsonify({"message":f"No user with id {id}"}),400)

        data=request.get_json()
        for attr, value in data.items():
            if attr == "password":
                hashed_password = bcrypt.generate_password_hash(value).decode('utf-8')
                setattr(user, "password", hashed_password)
            else:
                setattr(user, attr, value)

        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({"message": f"User {id}'s information updated"}), 200)
    





if __name__ == "__main__":
    app.run(debug=True, port=5500)
