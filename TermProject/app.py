from flask import Flask, render_template, request,redirect
from apicall import *
import json
import query
from pprint import pprint
from math import *
import datetime
import time
app = Flask(__name__)
login_user={}
patient_data={}
begin = False
nothing = ""
hosp_data = None
store_data = None
current_id = None
prescription_id = None
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
hanyang_lat = 37.55837671
hanyang_lng = 127.050856
# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/sql_register', methods = ["POST"])
def sql_register():
    name = request.form.get("name")
    phone = request.form.get("phone")
    local = request.form.get("local")
    domain = request.form.get("domain")
    password = request.form.get("pwd")
    service_type = request.form.get("type")
    query.register(name,phone,local,domain,password,service_type)
    return render_template("register_success.html")

@app.route('/overlap_check', methods =["GET"])
def overlap_check():
    local = request.args.get("local")
    domain = request.args.get("domain")
    #print(type(email))
    overlap = query.overlab_check(local, domain)
    context = {'overlap' : overlap}
    return context

@app.route('/init')
def init():
    drop_the_tables()         
    query.create_user_table()
    query.create_prescription_table()
    query.create_belong_table()
    query.create_bookmark_table()
    query.create_hosp_table()
    query.create_store_table()
    query.create_reservation_table() 
    result_hosp = hosp_list(hanyang_lat,hanyang_lng)
    result_store = pharm_list(hanyang_lat,hanyang_lng)
    for row in result_hosp["response"]["body"]["items"]["item"]:
        query.insert_hosp(row["yadmNm"],row["resdntCnt"],row["addr"],row["YPos"],row["XPos"])
    for row in result_store["response"]["body"]["items"]["item"]:
        query.insert_store(row["yadmNm"],row["addr"],row["YPos"],row["XPos"],row["clCdNm"])
    return redirect('/')

@app.route('/')
def index():      
    return render_template("index.html")

@app.route('/login', methods= ["POST"])
def login():
    global current_id
    local = request.form.get("local")
    domain = request.form.get("domain")
    user_info = query.call_user_info(local,domain)
    init_user(user_info)
    if(login_user["user_type"] == "patient"):
        return redirect('/patient_menu')
    if(login_user["user_type"] == "hospital"):
        if (query.belong_check("hospital_belong",login_user["local"],login_user["domain"]) == "fail"):
            return render_template("select_hosp.html")
        else:
            result = query.hosp_belong_id_search(login_user["local"],login_user["domain"])
            current_id = result[0][0]
            return redirect('/hosp_menu')
    if(login_user["user_type"] == "store"):
        if (query.belong_check("store_belong",login_user["local"],login_user["domain"]) == "fail"):
            return render_template("select_store.html")
        else:
            result= query.store_belong_id_search(login_user["local"],login_user["domain"])
            current_id = result[0][0]
        return redirect('/store_menu')

@app.route('/patient_menu')
def patient_menu():
    return render_template("patient.html")

@app.route('/patient_information')
def patient_information():
    return render_template("patient_information.html")

@app.route('/hosp_menu')
def hosp_menu():
    return render_template("hospital.html")

@app.route('/hosp_reservation_manage')
def hosp_reservation_manage():
    return render_template('hosp_reservation_manage.html')

@app.route('/hosp_prescribing',methods = ["POST"])
def hosp_prescribing():
    global patient_data
    data = request.form.get("submit")
    data = data.split(',')
    patient_data["name"] = data[0]
    patient_data["local"] = data[1]
    patient_data["domain"] = data[2]
    patient_data["date"] = data[3]
    patient_data["time"] = data[4]
    return render_template("hosp_prescribing.html")

@app.route('/register_prescription',methods = ["POST"])
def register_prescription():
    medi_name1 = request.form.get("medi_name1")
    one_dose1 =  request.form.get("one_dose1")
    perday1= request.form.get("perday1")
    total1= request.form.get("total1")
    medi_name2 = request.form.get("medi_name2")
    one_dose2 =  request.form.get("one_dose2")
    perday2= request.form.get("perday2")
    total2= request.form.get("total2")
    medi_name3 = request.form.get("medi_name3")
    one_dose3 =  request.form.get("one_dose3")
    perday3= request.form.get("perday3")
    total3= request.form.get("total3")
    medi_name4 = request.form.get("medi_name4")
    one_dose4 =  request.form.get("one_dose4")
    perday4= request.form.get("perday4")
    total4= request.form.get("total4")
    date =datetime.datetime.today()
    date_str = date.strftime('%Y-%m-%d %H:%M')
    login_hospital = query.id_search("hospital",current_id)
    query.register_prescription(date_str,patient_data["name"],
    patient_data["local"],patient_data["domain"],login_hospital[0]["name"],
    medi_name1,one_dose1,perday1,total1,medi_name2,one_dose2,perday2,total2,
    medi_name3,one_dose3,perday3,total3,medi_name4,one_dose4,perday4,total4)
    query.hosp_prescribed(patient_data["local"],patient_data["domain"],patient_data["date"],patient_data["time"],date_str)
    return redirect('/hosp_reservation_manage')

@app.route('/hosp_rejection',methods =["POST"])
def rejection():
    data= request.form.get("delete")
    data = data.split(',')
    query.delete_reservation("hospital_reservation",data[0],data[1],data[2],data[3])
    return redirect('/hosp_reservation_manage')

@app.route('/hosp_current_reservation')
def hosp_current_reservation():
    global current_id
    date =datetime.datetime.today()
    date_str = date.strftime('%Y-%m-%d')
    result = query.hosp_reservation_id_search(current_id,date_str)
    if(result =="fail"):
        result = {"result": result}
    return json.dumps(result)

@app.route('/hosp_patient_record')
def hosp_patient_record():
    return render_template("hosp_patient_record.html")

@app.route('/visit_history', methods=["POST"])
def visit_history():
    date =datetime.datetime.today()
    date_str = date.strftime('%Y-%m-%d')
    time_str = date.strftime('%H')
    form = request.get_json()
    table_name = form["table_name"]
    search_type = form["search_type"]
    data = form["data"]
    history = query.visit_history_list(table_name,search_type,data,current_id,date_str,time_str)
    if(history == "fail"):
        history = {"result" : "fail"}
    return json.dumps(history)

@app.route('/hosp_open_prescription', methods = ["POST"])
def hosp_open_prescription():
    global prescription_id
    prescription_id = request.form.get("submit")
    return render_template("hosp_open_prescription.html")

@app.route('/store_open_prescription', methods = ["POST"])
def store_open_prescription():
    global prescription_id
    prescription_id = request.form.get("submit")
    return render_template("store_open_prescription.html")

@app.route('/patient_open_prescription', methods = ["POST"])
def patient_open_prescription():
    global prescription_id
    prescription_id = request.form.get("submit")
    return render_template("patient_open_prescription.html")

@app.route('/prescription_data')
def prescription_data():
    result = query.id_search("prescription",prescription_id)
    return json.dumps(result[0])


@app.route('/store_menu')
def store_menu():
    return render_template("store.html")

@app.route('/store_reservation_manage')
def store_reservation_manage():
    return render_template('store_reservation_manage.html')

@app.route('/store_current_reservation')
def store_current_reservation():
    date =datetime.datetime.today()
    date_str = date.strftime('%Y-%m-%d')
    result = query.store_reservation_id_search(current_id,date_str)
    if(result =="fail"):
        result = {"result": "fail"}
    return json.dumps(result)

@app.route('/store_prescribing',methods = ["POST"])
def store_prescribing():
    global patient_data
    global prescription_id
    data = request.form.get("submit")
    data = data.split(',')
    patient_data["name"] = data[0]
    patient_data["local"] = data[1]
    patient_data["domain"] = data[2]
    patient_data["date"] = data[3]
    patient_data["time"] = data[4]
    print(patient_data)
    prescription_id = data[5]
    return render_template("store_prescribing.html")

@app.route('/register_store_prescription',methods=["POST"])
def register_store_prescription():
    global prescription_id
    comment = request.form.get("remedy")
    date =datetime.datetime.today()
    date_str = date.strftime('%Y-%m-%d %H:%M')
    login_store = query.id_search("store",current_id)
    query.update_prescription(login_store[0]["name"],date_str,comment,prescription_id)
    query.store_prescribed(patient_data["local"],patient_data["domain"],
            patient_data["date"],patient_data["time"],prescription_id)
    return redirect('/store_reservation_manage')

@app.route('/store_rejection')
def store_rejection():
    date_str ="처방불가"
    comment = "처방불가"
    login_store = query.id_search("store",current_id)
    query.delete_reservation("store_reservation",patient_data["local"],patient_data["domain"],patient_data["date"],patient_data["time"])
    query.update_prescription(login_store[0]["name"],date_str,comment,prescription_id)
    return redirect('/store_reservation_manage')

@app.route('/store_patient_record')
def store_patient_record():
    return render_template("store_patient_record.html")

@app.route('/log_out')
def log_out():
    global current_id
    global login_user
    login_user={}
    current_id = None
    return redirect('/')

@app.route('/login_check', methods = ["GET"])
def login_check():
    local = request.args.get("local")
    domain = request.args.get("domain")
    pwd = request.args.get("pwd")  
    result = query.login_check(local, domain,pwd)
    context = {'login' : result}
    return context

@app.route('/belong_hosp', methods = ["POST"])
def belong_hosp():
    global current_id
    current_id = request.form.get("submit")
    query.insert_belong("hospital_belong",login_user["local"],login_user["domain"],current_id)
    return render_template("hospital.html")

@app.route('/belong_store', methods = ["POST"])
def belong_store():
    global current_id
    current_id = request.form.get("submit")
    query.insert_belong("store_belong",login_user["local"],login_user["domain"],current_id)
    return render_template("store.html")


@app.route('/patient_search')
def patient_search():
    return render_template("patient_search.html")

@app.route('/hosp', methods=["POST"])
def hosp():
    position = request.get_json()
    lat = position["lat"]
    lng = position["lng"]
    if (distance(lat,lng) < 2000): #2km 내에 위치
        result = query.select_all("hospital")
        return json.dumps(result)
    else:  ## 2km밖에서 요청이 있을시
        extra_result = pharm_list(lat,lng)
        for row in extra_result["response"]["body"]["items"]["item"]:
            query.insert_hosp(row["yadmNm"],row["resdntCnt"],row["addr"],row["YPos"],row["XPos"])
        result = query.select_all("hospital")
        return json.dumps(result)


@app.route('/name_search',methods = ["POST"])
def name_search():
    name = request.get_json()
    result = query.name_search(name["table_name"],name["data_name"])
    if(result == "fail"):
        return {"result" : "fail"}
    else:
        return json.dumps(result)

@app.route('/subject_search',methods = ["POST"])
def subject():
    data = request.get_json()
    subject_code = data['subject']
    lat = data['lat']
    lng = data['lng']
    result = subject_search(subject_code,lat,lng)
    modified_result=[]
    if(result == "fail"):
        return {"result":"fail"}
    else:
        for row in result["response"]["body"]["items"]["item"]:
            select = query.address_search("hospital",row["addr"],row["yadmNm"])
            if(select != "fail"):
                modified_result.append(select)

        final = json.dumps(modified_result)
        return final

@app.route('/store_search')
def store_search():
    return render_template("store_search.html")

@app.route('/store_api', methods=["POST"])
def store_api():
    position = request.get_json()
    lat = position["lat"]
    lng = position["lng"]
   ## pprint(hosp_list(lat, lng))
    if (distance(lat,lng) < 2000): #2km 내에 위치
        result = query.select_all("store")
        return json.dumps(result)
    else:  ## 2km밖에서 요청이 있을시
        extra_result = pharm_list(lat,lng)
        for row in extra_result["response"]["body"]["items"]["item"]:
            query.insert_store(row["yadmNm"],row["addr"],row["YPos"],row["XPos"],row["clCdNm"])
        result = query.select_all("store")
        return json.dumps(result)


@app.route('/reservation_hosp',methods=["POST"])
def reservation_hosp():
    global hosp_data
    hosp_data = None
    hosp_id = request.form.get("submit")
    hosp_data = query.id_search("hospital",hosp_id)
    return render_template("reservation_hosp.html")

@app.route('/reservation_store',methods=["POST"])
def reservation_store():
    global store_data
    store_data = None
    store_id = request.form.get("submit")
    store_data = query.id_search("store",store_id)
    return render_template("reservation_store.html")

@app.route('/hosp_data',methods=["GET"]) # 예약시 필요한 정보를 ajax로 reservation에 넘기는 함수
def hospital_data():
    return json.dumps(hosp_data[0])

@app.route('/store_data',methods=["GET"]) # 예약시 필요한 정보를 ajax로 reservation에 넘기는 함수
def pharm_data():
    return json.dumps(store_data[0])

@app.route('/reservation_hosp_success',methods=["POST"])
def reservation_hosp_success():
    zero =0
    reservation_time = request.form.get("time")
    reservation_date = request.form.get("datepicker")
    query.insert_reservation("hospital_reservation",login_user["name"],login_user["phone"],login_user["local"],login_user["domain"],hosp_data[0]["id"],reservation_date,reservation_time,zero)
    return render_template("reservation_success.html")

@app.route('/reservation_store_success',methods=["POST"])
def reservation_store_success():
    reservation_time = request.form.get("time")
    reservation_date = request.form.get("datepicker")
    zero = 0
    query.insert_reservation("store_reservation",login_user["name"],login_user["phone"],login_user["local"],login_user["domain"],store_data[0]["id"],reservation_date,reservation_time,zero)
    return render_template("reservation_success.html")

@app.route('/reservation_list')
def reservation_list():
    date =datetime.datetime.today()
    date_str = date.strftime('%Y-%m-%d')
    result = query.recent_hospital(login_user["local"],login_user["domain"],date_str)
    return json.dumps(result)

@app.route('/register_bookmark', methods=["POST"])
def register_bookmark():
    data = request.form.get("bookmark_button")
    result = query.bookmark_overlab_check(login_user["local"],login_user["domain"],data)
    if(result =="pass"):
        query.insert_bookmark(login_user["local"],login_user["domain"],data)
        return render_template("register_bookmark_success.html")
    else:
        return render_template("register_bookmark_fail.html")

@app.route('/bookmark_list')
def bookmark_list():
    result = []
    id_list = query.bookmark_search(login_user["local"],login_user["domain"])
    for row in id_list:
        result = result + query.id_search("hospital",row[0])
    return json.dumps(result)

@app.route('/delete_bookmark', methods=["POST"])
def delete_bookmark():
    hosp_id = request.form.get("delete") 
    query.delete_bookmark(login_user["local"],login_user["domain"],hosp_id)
    return redirect("/patient_information")
    
##########################################범용함수########################    

def distance(dLat2,dLon2):
    dLat1 = hanyang_lat
    dLon1 = hanyang_lng
    Distance = acos(sin(deg2rad(dLat1))*sin(deg2rad(dLat2)) + cos(deg2rad(dLat1))*cos(deg2rad(dLat2))*cos(deg2rad(dLon1 - dLon2)))
    Distance = rad2deg(Distance)
    Distance = Distance* 60 * 1.1515 * 1.609344 * 1000
    return round(Distance)

def deg2rad(deg):
  return deg*pi / 180

def rad2deg(rad):
  return rad *180 /pi


def init_user(user_info):
    login_user["name"] = user_info[0][0]
    login_user["phone"] = user_info[0][1]
    login_user["local"] = user_info[0][2]
    login_user["domain"] = user_info[0][3]
    login_user["pwd"] = user_info[0][4]
    login_user["user_type"] = user_info[0][5]

def drop_the_tables():
    query.drop_the_table("user_table")
    query.drop_the_table("hospital")
    query.drop_the_table("store")
    query.drop_the_table("hospital_reservation")  
    query.drop_the_table("store_reservation")   
    query.drop_the_table("bookmark")
    query.drop_the_table("hospital_belong")
    query.drop_the_table("store_belong")
    query.drop_the_table("prescription")


if __name__ == ("__main__"):
    app.run(debug=True)