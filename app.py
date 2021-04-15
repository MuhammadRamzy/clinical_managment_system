from flask import Flask,render_template,request,redirect
from datetime import datetime
import pymongo

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["clinicMng"]
patients = mydb['patientRegister']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reception',methods=['GET','POST'])
def reception():
    if request.method == 'POST':
        patientName = request.form['Name']
        phoneNo = request.form['ph.no']
        houseName = request.form['Ho.name']
        gender = request.form['gender']
        DOB = request.form['DOB']
        now = datetime.now()
        token = request.form['token']
        data = {
            'tokenNo':token,
            'name':patientName,
            'phNo':phoneNo,
            'hoName':houseName,
            'gender':gender,
            'DOB':DOB,
            'time':now.strftime('%I:%M:%S'),
            'date':now.strftime('%d/%m/%y')
        }
        print(data)
        patients.insert_one(data)
        return redirect('/reception')
    else:
        return render_template('reception.html')

@app.route('/doctor')
def doctor():
    details = []
    for x in patients.find():
        details.append(x)
    return render_template('doctor.html',datas = details)

@app.route('/doctor/<string:token>',methods = ['GET','POST'])
def checkUp(token):
    details = []
    if request.method == 'POST':
        patientName = request.form['Name']
        phoneNo = request.form['ph.no']
        houseName = request.form['Ho.name']
        symptoms = request.form['symptoms']
        prescription = request.form['prescription']
        notes = request.form['notes']
        old = []
        for x in patients.find({ "tokenNo": token }):
            old.append(x)
        data = {
            "$set":{
                'tokenNo':token,
                'name':patientName,
                'phNo':phoneNo,
                'hoName':houseName,
                'symptoms':symptoms,
                'prescription':prescription,
                'notes':notes,
            }
        }
        patients.update_many(old[0],data)
        return redirect('/doctor')
    else:
        for x in patients.find({ "tokenNo": token }):
            details.append(x)
        return render_template('checkup.html',data=details)

@app.route('/pharmacy')
def pharmacy():
    details = []
    for x in patients.find():
        details.append(x)
    return render_template('pharmacy.html',datas = details)

@app.route('/billing/<string:token>',methods = ['GET','POST'])
def billing(token):
    if request.method == 'GET':
        details = []
        for x in patients.find({ "tokenNo": token }):
                details.append(x)
        medicne = x.pop('prescription')
        medicne = medicne.split()
        return render_template('billing.html',datas = details,medicnes=medicne)
    else:
        print(request.form)
        return f'{request.form}'

if __name__ == '__main__':
    app.run(debug=True)