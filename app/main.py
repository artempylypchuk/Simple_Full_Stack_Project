from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, join, func
import redis
import json
from decimal import Decimal

from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField, IntegerField, DecimalField
from wtforms import validators

username = "Pylypchuk"
password = "3313"
database = "Lab1DB"
host = "db"
port = "5432"

app = Flask(__name__)
app.secret_key = 'key'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

redis_client = redis.Redis(host='redis', port=6379)

#------Models---------
class Place(db.Model):
    __tablename__ = 'place'

    placeid = db.Column(db.Integer, primary_key=True)
    regname = db.Column(db.String, nullable=True)
    areaname = db.Column(db.String, nullable=True)
    tername = db.Column(db.String, nullable=True)
    tertypename = db.Column(db.String, nullable=True)

    tests = db.relationship('Test')
    eduplaces = db.relationship('EduPlace')
    participants = db.relationship('Participant')

class EduPlace(db.Model):
    __tablename__ = 'eduplace'
    
    eduplaceid = db.Column(db.Integer, primary_key=True)
    eoname = db.Column(db.String, nullable=True)
    eotypename = db.Column(db.String, nullable=True)
    eoparent = db.Column(db.String, nullable=True)
    placeid = db.Column(db.Integer, db.ForeignKey('place.placeid'))

    eparticipants = db.relationship('EduplaceParticipant')

class Participant(db.Model):
    __tablename__ = 'participant'
    
    outid = db.Column(db.String, primary_key=True)
    birth = db.Column(db.Integer, nullable=False)
    sextypename = db.Column(db.String, nullable=False)
    regtypename = db.Column(db.String, nullable=False)
    classprofilename = db.Column(db.String, nullable=True)
    classlangname = db.Column(db.String, nullable=True)
    zno_year = db.Column(db.Integer, nullable=False)
    placeid = db.Column(db.Integer, db.ForeignKey('place.placeid'))

    eparticipants = db.relationship('EduplaceParticipant')
    tests = db.relationship('Test')

class EduplaceParticipant(db.Model):
    __tablename__ = 'eduplace_participant'
    
    relid = db.Column(db.Integer, primary_key=True)
    eduplaceid = db.Column(db.Integer, db.ForeignKey('eduplace.eduplaceid'))
    outid = db.Column(db.String, db.ForeignKey('participant.outid'))

class Test(db.Model):
    __tablename__ = 'test'
    
    testid = db.Column(db.Integer, primary_key=True)
    outid = db.Column(db.String, db.ForeignKey('participant.outid'))
    name = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=True)
    ball100 = db.Column(db.Numeric(4,1), nullable=True)
    ball12 = db.Column(db.Integer, nullable=True)
    ball = db.Column(db.Integer, nullable=True)
    adaptscale = db.Column(db.Integer, nullable=True)
    langname = db.Column(db.String, nullable=True)
    dpalevel = db.Column(db.String, nullable=True)
    placeid = db.Column(db.Integer, db.ForeignKey('place.placeid'))

#------------------------------------#

#-------------Flask-Forms------------#
class PlaceForm(Form):
    placeid = StringField('placeID: ')
    regname = StringField('regname: ', validators=[validators.DataRequired("Please enter region"),
                                                   validators.Length(min=5, max=100)])
    areaname = StringField('areaname: ', validators=[validators.DataRequired("Please enter area"),
                                                     validators.Length(min=5, max=100)])
    tername = StringField('tername: ', validators=[validators.DataRequired("Please enter territory"),
                                                   validators.Length(min=5, max=100)])
    tertypename = StringField('tertypename: ', validators=[validators.DataRequired("Please enter territory type"),
                                                           validators.Length(min=5, max=100)])
    submit = SubmitField("Save")

class EduPlaceForm(Form):
    eduplaceid = StringField('EduPlaceID: ')
    eoname = StringField('eoname: ', validators=[validators.DataRequired("Please enter educational"),
                                                 validators.Length(min=5, max=100)])
    eotypename = StringField('eotypename: ', validators=[validators.DataRequired("Please enter educational type"),
                                                         validators.Length(min=5, max=100)])
    eoparent = StringField('eoparent: ', validators=[validators.DataRequired("Please enter parent of educational establishment"),
                                                     validators.Length(min=5, max=100)])
    placeid = StringField('placeid: ', validators=[validators.DataRequired("Please enter placeid"),
                                                   validators.Length(min=5, max=100)])
    submit = SubmitField("Save")

class ParticipantForm(Form):
    outid = StringField('outid: ', validators=[validators.DataRequired("Please enter OutID"),
                                                     validators.Length(min=36, max=36, message="Student ID should be exactly 36 symbols")])
    birth = IntegerField("birth: ", validators=[validators.DataRequired("Please enter your birthday")])
    sextypename = StringField('sextypename: ', validators=[validators.DataRequired("Please enter sex type"),
                                                           validators.Length(min=5, max=20)])
    regtypename = StringField('regtypename: ', validators=[validators.DataRequired("Please enter region type"),
                                                           validators.Length(min=5, max=100)])
    classprofilename = StringField('classprofilename: ', validators=[validators.DataRequired("Please enter class profile"),
                                                                     validators.Length(min=5, max=100)])
    classlangname = StringField('classlangname: ', validators=[validators.DataRequired("Please enter class lang"),
                                                               validators.Length(min=5, max=20)])
    zno_year = IntegerField('zno_year: ', validators=[validators.DataRequired("Please enter zno year"),
                                                      validators.number_range(2000, 2024, "Year should be from 2000 to 2024")])
    placeid = StringField('placeid: ', validators=[validators.DataRequired("Please enter placeid"),
                                                   validators.Length(min=5, max=100)])
    submit = SubmitField("Save")

class TestForm(Form):
    testid = StringField('testID: ')
    outid = StringField('outid: ', validators=[validators.DataRequired("Please enter OutID"),
                                                     validators.Length(min=36, max=36, message="Student ID should be exactly 36 symbols")])
    name = StringField('name: ', validators=[validators.DataRequired("Please enter name of subject"),
                                             validators.Length(min=5, max=50)])
    status = StringField('status: ', validators=[validators.DataRequired("Please enter status"),
                                                 validators.Length(min=5, max=20)])
    ball100 = DecimalField('ball100: ', validators=[validators.DataRequired("Please enter ball of test"),
                                                    validators.number_range(100, 200, "ball should be from 100 to 200")])
    ball12 = IntegerField('ball12: ', validators=[validators.DataRequired("Please enter ball in 12 point system"),
                                                  validators.number_range(0, 12, "ball should be from 0 to 12")])
    ball = IntegerField('ball: ', validators=[validators.DataRequired("Please enter ball in test system"),
                                              validators.number_range(0, 200, "ball should be from 0 to 200")])
    adaptscale = IntegerField('adaptscale: ', validators=[validators.DataRequired("Please enter adapts cale"),
                                                          validators.number_range(0, 7, "ball should be from 0 to 7")])
    langname = StringField('langname: ', validators=[validators.DataRequired("Please enter name of language"),
                                                     validators.Length(min=5, max=100)])
    dpalevel = StringField('dpalevel: ', validators=[validators.DataRequired("Please enter DPA level"),
                                                     validators.Length(min=5, max=50)])
    placeid = StringField('placeid: ', validators=[validators.DataRequired("Please enter placeid"),
                                                   validators.Length(min=5, max=100)])
    submit = SubmitField("Save")

#-----------------MainPage---------------------

@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')

#--------------------Place----------------------

@app.route('/place', methods=['GET'])
def place():
    cache_data = redis_client.get('place_data')
    if cache_data:
        return cache_data.decode('utf-8')
    result = db.session.query(Place).limit(10).all()
    redis_client.set('place_data', render_template('place.html', places=result))
    return render_template('place.html', places=result)

@app.route('/addPlace', methods=['GET', 'POST'])
def addPlace():
    form = PlaceForm(request.form)

    if request.method == 'POST':
        if form.validate():
            return render_template('place_form.html', form=form, form_name="New place", action="addPlace")
        else:
            new_place = Place(
                placeid=form.placeid.data,
                regname=form.regname.data,
                areaname=form.areaname.data,
                tername=form.tername.data,
                tertypename=form.tertypename.data
            )
            try:
                db.session.add(new_place)
                db.session.commit()
            except:
                db.session.rollback()
            
            redis_client.delete('place_data')
            
            return redirect(url_for('place'))

    return render_template('place_form.html', form=form, form_name="New place", action="addPlace")

@app.route('/editPlace', methods=['GET', 'POST'])
def editPlace():
    form = PlaceForm(request.form)

    if request.method == 'GET':
        placeid = request.args.get('placeid')
        place = db.session.query(Place).filter(Place.placeid == placeid).one()
        form.placeid.data = place.placeid
        form.regname.data = place.regname
        form.areaname.data = place.areaname
        form.tername.data = place.tername
        form.tertypename.data = place.tertypename

        return render_template('place_form.html', form=form, form_name="Edit place", action="editPlace")
    else:
        if form.validate():
            return render_template('place_form.html', form=form, form_name="Edit place", action="editPlace")
        else:
            try:
                place = db.session.query(Place).filter(Place.placeid == form.placeid.data).one()
                place.placeid = form.placeid.data
                place.regname = form.regname.data
                place.areaname = form.areaname.data
                place.tername = form.tername.data
                place.tertypename = form.tertypename.data
                db.session.commit()
            except:
                db.session.rollback()
                
            redis_client.delete('place_data')
            return redirect(url_for('place'))

@app.route('/delPlace', methods=['POST'])
def delPlace():
    placeid = request.form['placeid']
    result = db.session.query(Place).filter(Place.placeid == placeid).one()
    try:
        db.session.delete(result)
        db.session.commit()
    except:
        db.session.rollback()

    redis_client.delete('place_data')

    return redirect(url_for('place'))

#--------------------EduPlace------------------------

@app.route('/eduPlace', methods=['GET'])
def eduPlace():
    cache_data = redis_client.get('eduplace_data')
    if cache_data:
        return cache_data.decode('utf-8')
    result = db.session.query(EduPlace).limit(10).all()
    redis_client.set('eduplace_data', render_template('eduplace.html', eduplaces=result))
    return render_template('eduplace.html', eduplaces=result)

@app.route('/addEduPlace', methods=['GET', 'POST'])
def addEduPlace():
    form = EduPlaceForm(request.form)

    if request.method == 'POST':
        if form.validate():
            return render_template('eduplace_form.html', form=form, form_name="New eduplace", action="addEduPlace")
        else:
            new_eduPlace = EduPlace(
                eduplaceid=form.eduplaceid.data,
                eoname=form.eoname.data,
                eotypename=form.eotypename.data,
                eoparent=form.eoparent.data,
                placeid=form.placeid.data
            )
            try:
                db.session.add(new_eduPlace)
                db.session.commit()
            except:
                db.session.rollback()

            redis_client.delete('eduplace_data')

            return redirect(url_for('eduPlace'))

    return render_template('eduplace_form.html', form=form, form_name="New eduPlace", action="addEduPlace")

@app.route('/editEduPlace', methods=['GET', 'POST'])
def editEduPlace():
    form = EduPlaceForm(request.form)

    if request.method == 'GET':
        eduplaceid = request.args.get('eduplaceid')
        eduplace = db.session.query(EduPlace).filter(EduPlace.eduplaceid == eduplaceid).one()
        form.eduplaceid.data = eduplace.eduplaceid
        form.eoname.data = eduplace.eoname
        form.eotypename.data = eduplace.eotypename
        form.eoparent.data = eduplace.eoparent
        form.placeid.data = eduplace.placeid

        return render_template('eduplace_form.html', form=form, form_name="Edit eduPlace", action="editEduPlace")
    else:
        if form.validate():
            return render_template('eduplace_form.html', form=form, form_name="Edit eduPlace", action="editEduPlace")
        else:
            try:
                eduplace = db.session.query(EduPlace).filter(EduPlace.eduplaceid == form.eduplaceid.data).one()
                eduplace.eduplaceid = form.eduplaceid.data
                eduplace.eoname = form.eoname.data
                eduplace.eotypename = form.eotypename.data
                eduplace.eoparent = form.eoparent.data
                eduplace.placeid = form.placeid.data
                db.session.commit()
            except:
                db.session.rollback()

            redis_client.delete('eduplace_data')

            return redirect(url_for('eduPlace'))

@app.route('/delEduPlace', methods=['POST'])
def delEduPlace():
    eduplaceid = request.form['eduplaceid']
    result = db.session.query(EduPlace).filter(EduPlace.eduplaceid == eduplaceid).one()
    try:
        db.session.delete(result)
        db.session.commit()
    except:
        db.session.rollback()
        
    redis_client.delete('eduplace_data')

    return redirect(url_for('eduPlace'))

#-------------------Participant------------------------

@app.route('/participant', methods=['GET'])
def participant():
    cache_data = redis_client.get('participant_data')
    if cache_data:
        return cache_data.decode('utf-8')
    result = db.session.query(Participant).limit(10).all()
    redis_client.set('participant_data', render_template('participant.html', participants=result))
    return render_template('participant.html', participants=result)

@app.route('/addParticipant', methods=['GET', 'POST'])
def addParticipant():
    form = ParticipantForm(request.form)

    if request.method == 'POST':
        if form.validate():
            return render_template('participant_form.html', form=form, form_name="New participant", action="addParticipant")
        else:
            new_participant = Participant(
                outid=form.outid.data,
                birth=form.birth.data,
                sextypename=form.sextypename.data,
                regtypename=form.regtypename.data,
                classprofilename=form.classprofilename.data,
                classlangname=form.classlangname.data,
                zno_year=form.zno_year.data,
                placeid=form.placeid.data
            )
            try:
                db.session.add(new_participant)
                db.session.commit()
            except:
                db.session.rollback()

            redis_client.delete('participant_data')

            return redirect(url_for('participant'))

    return render_template('participant_form.html', form=form, form_name="New participant", action="addParticipant")

@app.route('/editParticipant', methods=['GET', 'POST'])
def editParticipant():
    form = ParticipantForm(request.form)

    if request.method == 'GET':
        outid = request.args.get('outid')
        participant = db.session.query(Participant).filter(Participant.outid == outid).one()
        form.outid.data = participant.outid
        form.birth.data = participant.birth
        form.sextypename.data = participant.sextypename
        form.regtypename.data = participant.regtypename
        form.classprofilename.data = participant.classprofilename
        form.classlangname.data = participant.classlangname
        form.zno_year.data = participant.zno_year
        form.placeid.data = participant.placeid

        return render_template('participant_form.html', form=form, form_name="Edit participant", action="editParticipant")
    else:
        if form.validate():
            return render_template('participant_form.html', form=form, form_name="Edit participant", action="editParticipant")
        else:
            try:
                participant = db.session.query(Participant).filter(Participant.outid == form.outid.data).one()
                participant.outid = form.outid.data
                participant.birth = form.birth.data
                participant.sextypename = form.sextypename.data
                participant.regtypename = form.regtypename.data
                participant.classprofilename = form.classprofilename.data
                participant.classlangname = form.classlangname.data
                participant.zno_year = form.zno_year.data
                participant.placeid = form.placeid.data

                db.session.commit()
            except:
                db.session.rollback()

            redis_client.delete('participant_data')

            return redirect(url_for('participant'))

@app.route('/delParticipant', methods=['POST'])
def delParticipant():
    outid = request.form['outid']
    result = db.session.query(Participant).filter(Participant.outid == outid).one()
    result1 = db.session.query(Test).filter(Test.outid == outid)
    try:
        db.session.delete(result1)
        db.session.delete(result)
        db.session.commit()
    except:
        db.session.rollback()

    redis_client.delete('participant_data')

    return redirect(url_for('participant'))

#-----------------------Test-------------------------

@app.route('/test', methods=['GET'])
def test():
    cache_data = redis_client.get('test_data')
    if cache_data:
        return cache_data.decode('utf-8')
    result = db.session.query(Test).limit(10).all()
    redis_client.set('test_data', render_template('test.html', tests=result))
    return render_template('test.html', tests=result)

@app.route('/addTest', methods=['GET', 'POST'])
def addTest():
    form = TestForm(request.form)

    if request.method == 'POST':
        if form.validate():
            return render_template('test_form.html', form=form, form_name="New test", action="addTest")
        else:
            new_test = Test(
                testid=form.testid.data,
                outid=form.outid.data,
                name=form.name.data,
                status=form.status.data,
                ball100=form.ball100.data,
                ball12=form.ball12.data,
                ball=form.ball.data,
                adaptscale=form.adaptscale.data,
                langname=form.langname.data,
                dpalevel=form.dpalevel.data,
                placeid=form.placeid.data
            )
            try:
                db.session.add(new_test)
                db.session.commit()
            except:
                db.session.rollback()

            redis_client.delete('test_data')

            return redirect(url_for('test'))

    return render_template('test_form.html', form=form, form_name="New test", action="addTest")

@app.route('/editTest', methods=['GET', 'POST'])
def editTest():
    form = TestForm(request.form)

    if request.method == 'GET':
        testid = request.args.get('testid')
        test = db.session.query(Test).filter(Test.testid == testid).one()

        form.testid.data = test.testid
        form.outid.data = test.outid
        form.name.data = test.name
        form.status.data = test.status
        form.ball100.data = test.ball100
        form.ball12.data = test.ball12
        form.ball.data = test.ball
        form.adaptscale.data = test.adaptscale
        form.langname.data = test.langname
        form.dpalevel.data = test.dpalevel
        form.placeid.data = test.placeid

        return render_template('test_form.html', form=form, form_name="Edit test", action="editTest")
    else:
        if form.validate():
            return render_template('test_form.html', form=form, form_name="Edit test", action="editTest")
        else:
            try:
                test = db.session.query(Test).filter(Test.testid == form.testid.data).one()
                test.test.id = form.testid.data
                test.outid = form.outid.data
                test.name = form.name.data
                test.status = form.status.data
                test.ball100 = form.ball100.data
                test.ball12 = form.ball12.data
                test.ball = form.ball.data
                test.adaptscale = form.adaptscale.data
                test.langname = form.langname.data
                test.dpalevel = form.dpalevel.data
                test.placeid = form.placeid.data

                db.session.commit()
            except:
                db.session.rollback()

            redis_client.delete('test_data')

            return redirect(url_for('test'))

@app.route('/delTest', methods=['POST'])
def delTest():
    testid = request.form['testid']
    result = db.session.query(Test).filter(Test.testid == testid).one()
    try:
        db.session.delete(result)
        db.session.commit()
    except:
        db.session.rollback()

    redis_client.delete('test_data')

    return redirect(url_for('test'))

@app.route('/task', methods=['GET', 'POST'])
def task():
    selected_subject = request.form.get('subject')
    selected_region = request.form.get('region')
    selected_year = request.form.get('year')

    cache_key = f'task:{selected_subject}:{selected_region}:{selected_year}'
    cached_results = redis_client.get(cache_key)

    if cached_results is not None:
        data = json.loads(cached_results)
    else:
        query = db.session.query(Test.name, Place.regname, Participant.zno_year, func.round(func.avg(Test.ball100), 3).label('average')).\
            select_from(Test).join(Place).join(Participant).\
            filter(Test.status == 'Зараховано').\
            group_by(Test.name, Place.regname, Participant.zno_year).\
            order_by(Test.name, Place.regname, Participant.zno_year)
        
        if selected_subject:
            query = query.filter(Test.name == selected_subject)

        if selected_region:
            query = query.filter(Place.regname == selected_region)

        if selected_year:
            query = query.filter(Participant.zno_year == selected_year)

        data = query.all()
        data_dict = []
        for row in data:
            row_dict = {}
            for column, value in row._asdict().items():
                if isinstance(value, Decimal):
                    row_dict[column] = float(value)
                else:
                    row_dict[column] = value
            data_dict.append(row_dict)
        redis_client.set(cache_key, json.dumps(data_dict))
    
    return render_template('task.html', data=data, action='task')
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    db.create_all()
