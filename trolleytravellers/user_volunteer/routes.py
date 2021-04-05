from flask import Blueprint, jsonify, request, abort
from trolleytravellers import db
from trolleytravellers.models import Volunteer, VolunteerSchema

user_volunteer = Blueprint('user_volunteer', __name__)

@user_volunteer.route('/volunteer_list', methods=['GET'])
def list_volunteers():
    volunteers = Volunteer.query.all()
    volunteer_schema = VolunteerSchema(many=True)
    output = volunteer_schema.dump(volunteers)
    return jsonify({'volunteer' : output})

@user_volunteer.route('/single_volunteer/<id>', methods=['GET'])
def list_volunteer(id):
    try:
        volunteer = Volunteer.query.get(id)
        volunteer_schema = VolunteerSchema()
        return volunteer_schema.jsonify(volunteer)
    except:
        abort(404)

@user_volunteer.route('/add_volunteer', methods=['POST'])
def new_volunteer():
    try:
        email_data = request.json['email']
        username_data = request.json['username']
        password_data = request.json['password']
        postcode_data = request.json['postcode']
        house_number_data = request.json['house_number']
        new_volunteer = Volunteer(email=email_data, username=username_data, password=password_data, postcode=postcode_data, house_number=house_number_data)
        db.session.add(new_volunteer)
        db.session.commit()
        volunteer_schema = VolunteerSchema()
        return volunteer_schema.jsonify(new_volunteer)
    except:
         abort(400)

@user_volunteer.route('/add_multiple_volunteers', methods=['POST'])
def new_volunteers():
    try:
        jsonBody = request.get_json()
        for json_object in jsonBody:
            email_data = json_object.get('email')
            username_data = json_object.get('username')
            password_data = json_object.get('password')
            postcode_data = json_object.get('postcode')
            house_number_data = json_object.get('house_number')
            new_volunteer = Volunteer(email=email_data, username=username_data, password=password_data, postcode=postcode_data, house_number=house_number_data)
            db.session.add(new_volunteer)
            db.session.commit()
            volunteer_schema = VolunteerSchema()
            volunteer_schema.jsonify(new_volunteer)
        volunteers = Volunteer.query.all()
        volunteer_schema = VolunteerSchema(many=True)
        output = volunteer_schema.dump(volunteers)
        return jsonify({'# volunteers in database' : len(output)})
    except:
         abort(400)

@user_volunteer.route('/update_volunteer/<id>', methods=['PUT'])
def update_volunteer(id):
    try:
        volunteer = Volunteer.query.get(id)
        email_data = request.json['email']
        username_data = request.json['username']
        password_data = request.json['password']
        postcode_data = request.json['postcode']
        house_number_data = request.json['house_number']

        volunteer.email = email_data
        volunteer.username = username_data
        volunteer.password = password_data
        volunteer.postcode = postcode_data
        volunteer.house_number = house_number_data
       
        db.session.commit()

        volunteer_schema = VolunteerSchema()
        return volunteer_schema.jsonify(volunteer)
    except:
         abort(404)

@user_volunteer.route('/delete_volunteer/<id>', methods=['DELETE'])
def delete_volunteer(id):
    try:
        volunteer = Volunteer.query.get(id)
        db.session.delete(volunteer)
        db.session.commit()
        volunteer_schema = VolunteerSchema()
        return volunteer_schema.jsonify({volunteer})
    except:
        abort(404)



