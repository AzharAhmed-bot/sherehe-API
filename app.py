from flask import Flask, jsonify, make_response, request,render_template
from models import db, Users, Sherehe
from flask_cors import CORS
from config import AppConfig
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mpesa import MpesaAPI
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True, allow_headers=["*"], methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])


app.config['API_ENVIRONMENT']="sandbox"
app.config['APP_KEY']="e5DGZf81E9ASLXaQZQLQvA1HfRoSoIfX2w296uGah31Aw8Rj"
app.config['APP_SECRET']="u5dWLVNQLSR2XNS8XqxofExaPXGEb6ejjGmP7pDx91CkYAcLhoXEa87ffVzTbeZH"
# Start mpesa
mpesa_api=MpesaAPI(app)
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

@app.route('/update/<int:id>', methods=["GET", "PATCH", "DELETE", "OPTIONS"])
def update(id):
    user = Users.query.filter_by(id=id).first()
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'https://icssherehe.netlify.app')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,PATCH,OPTIONS')
        return response

    if request.method == "GET":
        if not user:
            return jsonify({"error": "User does not exist."}), 404
        return make_response(jsonify({"User": user.to_dict()}), 200)
    elif request.method == "DELETE":
        if not user:
            return make_response(jsonify({"message": f"No user with id {id}"}), 400)
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message": f"User {id} has been successfully deleted"}), 200)
    elif request.method == "PATCH":
        if not user:
            return make_response(jsonify({"message": f"No user with id {id}"}), 400)

        data = request.get_json()
        for attr, value in data.items():
            if attr == "password":
                hashed_password = bcrypt.generate_password_hash(value).decode('utf-8')
                setattr(user, "password", hashed_password)
            else:
                setattr(user, attr, value)

        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({"message": f"User {id}'s information updated"}), 200)

@app.route('/sherehe', methods=['GET', 'POST'])
def sherehe():
    if request.method == "GET":
        sherehe = [sherehe.to_dict() for sherehe in Sherehe.query.all()]
        if not sherehe:
            return make_response(jsonify({"message":"No info yet"}))
        return jsonify(sherehe)
    elif request.method == "POST":
        data = request.get_json()
        new_sherehe = Sherehe(**data)
        db.session.add(new_sherehe)
        db.session.commit()
        return jsonify(new_sherehe.to_dict()), 201

@app.route('/sherehe/<int:id>', methods=["GET", "PATCH", "DELETE", "OPTIONS"])
def sherehe_by_id(id):
    sherehe = Sherehe.query.filter_by(id=id).first()
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'https://icssherehe.netlify.app')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,PATCH,OPTIONS')
        return response

    if request.method == "GET":
        if not sherehe:
            return jsonify({"error": "Sherehe does not exist."}), 404
        return make_response(jsonify({"User": sherehe.to_dict()}), 200)
    elif request.method == "DELETE":
        if not sherehe:
            return make_response(jsonify({"message": f"No Sherehe with id {id}"}), 400)
        db.session.delete(sherehe)
        db.session.commit()
        return make_response(jsonify({"message": f"Sherehe {id} has been successfully deleted"}), 200)
    elif request.method == "PATCH":
        if not sherehe:
            return make_response(jsonify({"message": f"No Sherehe with id {id}"}), 400)

        data = request.get_json()
        for attr, value in data.items():
            setattr(sherehe, attr, value)

        db.session.add(sherehe)
        db.session.commit()
        return make_response(jsonify({"message": f"Sherehe {id}'s information updated"}), 200)

origin=[
    'https://localhost5173',
    'https://icssherehe.netlify.app'
]

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://icssherehe.netlify.app'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS,PATCH'
    return response




# Trying flask mpesa with daraja API
@app.route('/transact/mpesaexpress')
def simulate_stk_push():
    data = {
        "business_shortcode": "174379", #from developers portal
        "passcode": "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919",#from developers portal
        "amount": "1", # choose amount preferrably KSH 1
        "phone_number":"254705359447", #phone number to be prompted to pay
        "reference_code": "HelloWorld",#Code to inform the user of services he/she is paying for.
        "callback_url": "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query", # cllback url should be exposes. for testing putposes you can route on host 0.0.0.0 and set the callback url to be https://youripaddress:yourport/endpoint
        "description": "Hello World" #a description of the transaction its optional
    }
    resp = mpesa_api.MpesaExpress.stk_push(**data)  # ** unpacks the dictionary
    ##use resp to capture the response
    try:
        resp = mpesa_api.MpesaExpress.stk_push(**data)
        print("Response:", resp)  # Debug print
        return resp
    except Exception as e:
        print("Error:", str(e))  # Debug print
        return jsonify({"error": str(e)}), 500

@app.route('/callback-url',methods=["POST"])
def callback_url():
    #get json data set to this route
    json_data = request.get_json()
    #get result code and probably check for transaction success or failure
    result_code=json_data["Body"]["stkCallback"]["ResultCode"]
    message={
        "ResultCode":json_data['ResultCode'],
        "ResultDesc":"success",
        "ThirdPartyTransID":"h234k2h4krhk2"
    }
    #if result code is 0 you can proceed and save the data else if its any other number you can track the transaction
    return jsonify(message),200


if __name__ == "__main__":
    app.run(debug=True, port=5500)
