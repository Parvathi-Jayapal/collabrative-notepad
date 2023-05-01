from flask import Flask, request, jsonify, render_template
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant


app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/token')
def generate_token():
    #add your twilio credentials 
    TWILIO_ACCOUNT_SID='ACb85f91a291176a730263c79a65c34bc0'
    TWILIO_SYNC_SERVICE_SID='IS5a9ef9a2d09ee4f9a1f50279225d3ad0'
    TWILIO_API_KEY='SK372b5d237182e80b42b0d9d89eee5205'
    TWILIO_API_SECRET='vf5RzCm3Zvb2E3G7iNZ8VEWqEuiqET3V'

    username = request.args.get('username', fake.user_name())
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())


@app.route('/',methods=['POST'])
def download_text():
    text_from_notepad=request.form['text']
    with open('workfile.txt','w') as f:
        f.write(text_from_notepad)
    path_to_store_txt="workfile.txt"
    return send_file(path_to_store_txt,as_attachment=True)
if __name__ == "__main__":
    app.run(port=5001)

