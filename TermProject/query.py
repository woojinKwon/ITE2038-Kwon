import psycopg2 as pg
import psycopg2.extras

pg_local = {
    'host': "localhost",
    'user': "postgres",
    'dbname': "postgres",
    'password': "gkdl2255"
}

db_connector = pg_local

connect_string = "host={host} user={user} dbname={dbname} password={password}".format(
    **db_connector)

def select_all(table_name):
    sql = f'''select * from {table_name}

            '''
    try:
        conn = pg.connect(connect_string)   #connect설정
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)   #커서설정
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            return "fail"
        else:
            return result

        conn.commit()
        conn.close()
    except pg.OperationalError as e:   
        print(e)
        return -1


def drop_the_table(table_name):
    sql = f'''drop table {table_name}

            '''
    try:
        conn = pg.connect(connect_string)   
        cur = conn.cursor() 
        cur.execute(sql)
        conn.commit()
        conn.close()
    except:  
        print("삭제할 테이블이 없습니다")

def overlab_check(local,domain):
    sql = f'''select * from user_table u
            where u.local =\'{local}\' and u.domain =\'{domain}\'

            '''
    try:
        conn = pg.connect(connect_string)   
        cur = conn.cursor()   
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            return "pass"
        else:
            return "fail"

        conn.commit()
        conn.close()
    except pg.OperationalError as e:    
        print(e)
        return -1

def login_check(local, domain, pwd):
    sql = f'''select * from user_table u
            where u.local =\'{local}\' and u.domain =\'{domain}\'
            and u.password = \'{pwd}\'

            '''
    try:
        conn = pg.connect(connect_string)   
        cur = conn.cursor()   
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            return "fail"
        else:
            return "pass"

        conn.commit()
        conn.close()
    except pg.OperationalError as e:   
        print(e)
        return -1    

def name_search(table_name,data_name):
    sql = f"""select * from {table_name} t
            where t.name like '%{data_name}%'

            """
    try:
        conn = pg.connect(connect_string)   #connect설정
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)   #커서설정
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            return "fail"
        else:
            return result

        conn.commit()
        conn.close()
    except pg.OperationalError as e:    ##try는 꼭 except 랑 세트임 꼭 써야함
        print(e)
        return -1  

def address_search(table_name,address_name,hospital_name):
    sql = f"""select * from {table_name} t
            where t.address = '{address_name}' and t.name = '{hospital_name}'

            """
    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) 
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            return "fail"
        else:
            return result

        conn.commit()
        conn.close()
    except pg.OperationalError as e:   
        print(e)
        return -1

def hosp_belong_id_search(local,domain):
    sql = f"""select t.hosp_id from hospital_belong t
            where t.local = '{local}' and t.domain = '{domain}'
            """
    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor() 
        cur.execute(sql)
        result = cur.fetchall()
        return result

        conn.commit()
        conn.close()
    except pg.OperationalError as e:   
        print(e)
        return -1   

def store_belong_id_search(local,domain):
    sql = f"""select t.store_id from store_belong t
            where t.local = '{local}' and t.domain = '{domain}'
            """
    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor() 
        cur.execute(sql)
        result = cur.fetchall()
        return result

        conn.commit()
        conn.close()
    except pg.OperationalError as e:   
        print(e)
        return -1   


def hosp_reservation_id_search(id,date):
    sql = f"""select * from hospital_reservation r
            where r.hosp_id = '{id}' and r.date>='{date}'
            and r.prescription_id is NULL
            """
    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) 
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            return "fail"
        else:
            return result

        conn.commit()
        conn.close()
    except pg.OperationalError as e:   
        print(e)
        return -1  

def store_reservation_id_search(id,date):
    sql = f"""select s.*,h.prescription_id as prescription_id2 
            FROM store_reservation s, hospital_reservation h
            where s.store_id = '{id}' and s.date>='{date}'
            and s.user_local = h.user_local and s.user_domain = h.user_domain
            and s.prescription_id != h.prescription_id
            """
    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) 
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            return "fail"
        else:
            return result

        conn.commit()
        conn.close()
    except pg.OperationalError as e:   
        print(e)
        return -1    

def call_prescription_id(local,domain,date,time,id):
    sql = f"""select r.prescription_id from hospital_reservation r
            where r.hosp_id = '{id}' and r.date>='{date}'
            """
    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor() 
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            return "fail"
        else:
            return result

        conn.commit()
        conn.close()
    except pg.OperationalError as e:   
        print(e)
        return -1   

def visit_history_list(table_name,search_type,data,id,date,time):
    if (table_name =="hospital_reservation"):
        if(search_type == "name_search"):
            sql = f"""select * from hospital_reservation r
                    where r.hosp_id = '{id}' and r.user_name like '{data}%' and
                    ( r.date<'{date}' or (r.date ='{date}' and r.time<='{time}'))
                    """
        if(search_type == "phone_search"):
            sql = f"""select * from hospital_reservation r
                    where r.hosp_id = '{id}' and r.user_phone = '{data}' and
                    ( r.date<'{date}' or (r.date ='{date}' and r.time<='{time}'))
                    """
        if(search_type == "date_search"):
            if(data == date):
                sql = f"""select * from hospital_reservation r
                        where r.hosp_id = '{id}' and 
                        r.date ='{data}' and r.time<='{time}'
                        """
            else:
                sql = f"""select * from hospital_reservation r
                        where r.hosp_id = '{id}' and
                        r.date ='{data}'
                        """
    else:
        if(search_type == "name_search"):
            sql = f"""select * from store_reservation r
                    where r.store_id = '{id}' and r.user_name like '{data}%' and
                    ( r.date<'{date}' or (r.date ='{date}' and r.time<='{time}'))
                    """
        if(search_type == "phone_search"):
            sql = f"""select * from store_reservation r
                    where r.store_id = '{id}' and r.user_phone = '{data}' and
                    ( r.date<'{date}' or (r.date ='{date}' and r.time<='{time}'))
                    """
        if(search_type == "date_search"):
            if(data == date):
                sql = f"""select * from store_reservation r
                        where r.store_id = '{id}' and 
                        r.date ='{data}' and r.time<='{time}'
                        """
            else:
                sql = f"""select * from store_reservation r
                        where r.store_id = '{id}' and
                        r.date ='{data}'
                        """       
    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) 
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            return "fail"
        else:
            return result

        conn.commit()
        conn.close()
    except pg.OperationalError as e:   
        print(e)
        return -1      

def recent_hospital(local,domain,date_str):
    sql = f"""select h.name, h.address, R1.date,R1.prescription_id from hospital_reservation R1, hospital h
            where R1.user_local = '{local}' and R1.user_domain = '{domain}' and R1.hosp_id = h.id and R1.hosp_id IN (
            select R2.hosp_id FROM hospital_reservation R2
            where R2.user_local = '{local}' and R2.user_domain = '{domain}' and R2.date <='{date_str}');

            """
    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor()  
        cur.execute(sql)
        result = cur.fetchall()
        return result

        conn.commit()
        conn.close()
    except pg.OperationalError as e:    
        print(e)
        return -1      

def bookmark_search(local,domain):
    sql = f"""select b.hosp_id from bookmark b
            where b.local = '{local}' and b.domain = '{domain}'

            """
    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor()  
        cur.execute(sql)
        result = cur.fetchall()
        return result

        conn.commit()
        conn.close()
    except pg.OperationalError as e:    
        print(e)
        return -1  
    

def insert_hosp(name,num_doctor,address,lat,lng): 
    sql = f'''INSERT INTO hospital 
                     VALUES ( \'{name}\', \'{num_doctor}\',\'{address}\',\'{lat}\',\'{lng}\',
                     trunc(random()*5 + 6), trunc(random()*10+13)
                     );

            '''

    try:
        conn = pg.connect(connect_string)   #connect설정
        cur = conn.cursor()   #커서설정
        result = cur.execute(sql)
        conn.commit()
        conn.close()
    except pg.OperationalError as e:    ##try는 꼭 except 랑 세트임 꼭 써야함
        print(e)
        return -1
    return 0

def insert_store(name,address,lat,lng,code): 
    sql = f'''INSERT INTO store 
                     VALUES ( \'{name}\',\'{address}\',\'{lat}\',\'{lng}\',\'{code}\',
                     trunc(random()*5 + 6), trunc(random()*10+13)
                     );

            '''

    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor()  
        cur.execute(sql)
        conn.commit()
        conn.close()
    except pg.OperationalError as e:    
        print(e)
        return -1
    return 0

def register_prescription(date_str,patient_name,local,domain,hosp_name,
medi_name1,one_dose1,perday1,total1,medi_name2,one_dose2,perday2,total2,
medi_name3,one_dose3,perday3,total3,medi_name4,one_dose4,perday4,total4):
    sql = f'''INSERT INTO prescription 
                     VALUES ( \'{date_str}\', \'{patient_name}\', \'{local}\',\'{domain}\',\'{hosp_name}\',
                     \'{medi_name1}\',\'{one_dose1}\',\'{perday1}\',\'{total1}\',
                     \'{medi_name2}\',\'{one_dose2}\',\'{perday2}\',\'{total2}\',
                     \'{medi_name3}\',\'{one_dose3}\',\'{perday3}\',\'{total3}\',
                     \'{medi_name4}\',\'{one_dose4}\',\'{perday4}\',\'{total4}\');
            '''

    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor() 
        cur.execute(sql)
        conn.commit()
        conn.close()
    except pg.OperationalError as e:   
        print(e)
        return -1
    return 0  

def hosp_prescribed(local,domain,date,time,issued_date):
    sql = f"""UPDATE hospital_reservation h SET prescription_id = 
                     (SELECT p.id FROM prescription p where p.issued_date = '{issued_date}')
                     where h.user_local = '{local}' and h.user_domain = '{domain}'
                     and h.date = '{date}' and h.time = '{time}';
            
            """

    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor()  
        cur.execute(sql)
        conn.commit()
        conn.close()
    except pg.OperationalError as e:    
        print(e)
        return -1
    return 0

def store_prescribed(local,domain,date,time,id):
    sql = f"""UPDATE store_reservation s SET prescription_id = '{id}'
                     where s.user_local = '{local}' and s.user_domain = '{domain}'
                     and s.date = '{date}' and s.time = '{time}';
            
            """

    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor()  
        cur.execute(sql)
        conn.commit()
        conn.close()
    except pg.OperationalError as e:    
        print(e)
        return -1
    return 0

def insert_reservation(table_name,name,phone,local,domain,id,date,time,zero):
    if(table_name=="hospital_reservation"):
        sql = f'''INSERT INTO {table_name} 
                        VALUES ( \'{name}\', \'{phone}\', \'{local}\',\'{domain}\',\'{id}\',\'{date}\',\'{time}\');
                '''
    else:
        sql = f'''INSERT INTO {table_name} 
                        VALUES ( \'{name}\', \'{phone}\', \'{local}\',\'{domain}\',\'{id}\',\'{date}\',\'{time}\',\'{zero}\');
                '''

    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor() 
        cur.execute(sql)
        conn.commit()
        conn.close()
    except pg.OperationalError as e:   
        print(e)
        return -1
    return 0   

def delete_reservation(table_name,local,domain,date,time):
    sql = f"""DELETE 
            FROM {table_name} t
            WHERE t.user_local = '{local}' and t.user_domain = '{domain}' 
                    and t.date ='{date}' and t.time='{time}'
            """
    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor() 
        cur.execute(sql)
        conn.commit()
        conn.close()
    except pg.OperationalError as e:   
        print(e)
        return -1
    return 0


def insert_bookmark(local,domain,hosp_id):
    sql = f'''INSERT INTO bookmark 
                     VALUES ( \'{local}\', \'{domain}\', \'{hosp_id}\');
            '''

    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor() 
        cur.execute(sql)
        conn.commit()
        conn.close()
    except pg.OperationalError as e:   
        print(e)
        return -1
    return 0    

def bookmark_overlab_check(local,domain,hosp_id):
    sql = f'''select * from bookmark b
            where b.local =\'{local}\' and b.domain =\'{domain}\' and b.hosp_id=\'{hosp_id}\'

            '''
    try:
        conn = pg.connect(connect_string)   #connect설정
        cur = conn.cursor()   #커서설정
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            return "pass"
        else:
            return "fail"

        conn.commit()
        conn.close()
    except pg.OperationalError as e:    ##try는 꼭 except 랑 세트임 꼭 써야함
        print(e)
        return -1   

def register(name,phone,local,domain,password,user_type): 
    sql = f'''INSERT INTO user_table
                     VALUES ( \'{name}\', \'{phone}\',\'{local}\',\'{domain}\',\'{password}\',\'{user_type}\');

            '''
    print(sql)

    try:
        conn = pg.connect(connect_string)   
        cur = conn.cursor() 
        result = cur.execute(sql)
        conn.commit()
        conn.close()
    except pg.OperationalError as e:   
        print(e)
        return -1
    return 0

def call_user_info(local,domain):
    sql = f'''select * from user_table u
            where u.local =\'{local}\' and u.domain =\'{domain}\'

            '''
    try:
        conn = pg.connect(connect_string)   
        cur = conn.cursor()   
        cur.execute(sql)
        result = cur.fetchall()
        print(result)
        conn.commit()
        conn.close()
        return result
    except pg.OperationalError as e:   
        print(e)
        return -1

###################################테이블생성##########################

def create_user_table():
    sql = f'''CREATE TABLE user_table(
            name varchar(20),
            phone char(11),
            local varchar(20),
            domain varchar(40), 
            password varchar(20),
            type varchar(15)
    )
             '''
    try:
        conn = pg.connect(connect_string)   
        cur = conn.cursor()  
        cur.execute(sql)
        print("계정테이블 생성완료!")
        conn.commit()
        conn.close()
    except:   
        print("Something wrong!")

def create_hosp_table():
    sql = f'''CREATE TABLE hospital(
            name varchar(40),
            num_doctor integer,
            address varchar(200),
            lat real,
            lng real,
            start_time integer,
            end_time integer,
            id serial
    )
             '''
    try:
        conn = pg.connect(connect_string)   
        cur = conn.cursor()  
        cur.execute(sql)
        print("병원테이블 생성완료!")
        conn.commit()
        conn.close()
    except:   
        print("Something wrong!")

def create_store_table():
    sql = f'''CREATE TABLE store(
            name varchar(40),
            address varchar(200),
            lat real,
            lng real,
            code varchar(20),
            start_time integer,
            end_time integer,
            id serial
    )
             '''
    try:
        conn = pg.connect(connect_string)   
        cur = conn.cursor()  
        cur.execute(sql)
        print("상점테이블 생성완료!")
        conn.commit()
        conn.close()
    except:   
        print("Something wrong!")

def create_reservation_table():
    sql1 = f'''CREATE TABLE hospital_reservation(
            user_name varchar(40),
            user_phone char(11),
            user_local varchar(20),
            user_domain varchar(30),
            hosp_id integer,
            date varchar(20),
            time integer,
            prescription_id integer
    )
             '''
    sql2 = f'''CREATE TABLE store_reservation(
            user_name varchar(40),
            user_phone char(11),
            user_local varchar(20),
            user_domain varchar(30),
            store_id integer,
            date varchar(20),
            time integer,
            prescription_id integer
    )
             '''
    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor()  
        cur.execute(sql1)
        cur.execute(sql2)
        print("예약 테이블 생성완료!")
        conn.commit()
        conn.close()
    except:    
        print("Something wrong!")

def create_belong_table():
    sql1 = f'''CREATE TABLE hospital_belong(
            local varchar(20),
            domain char(30),
            hosp_id integer
    )
             '''
    sql2 = f'''CREATE TABLE store_belong(
            local varchar(20),
            domain char(30),
            store_id integer
    )
             '''
    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor()  
        cur.execute(sql1)
        cur.execute(sql2)
        print("소속 테이블 생성완료!")
        conn.commit()
        conn.close()
    except:    
        print("Something wrong!")

def create_bookmark_table():
    sql = f'''CREATE TABLE bookmark(
            local varchar(20),
            domain varchar(30),
            hosp_id integer
    )
             '''
    try:
        conn = pg.connect(connect_string)   
        cur = conn.cursor()  
        cur.execute(sql)
        print("북마크테이블 생성완료!")
        conn.commit()
        conn.close()
    except:   
        print("Something wrong!")

def create_prescription_table():
    sql = f'''CREATE TABLE prescription(
            issued_date varchar(30),
            patient_name varchar(20),
            patient_local varchar(20),
            patient_domain varchar(30),
            hosp_name varchar(30),
            medi_name1 varchar(30),
            one_dose1 varchar(5),
            perday1 varchar(5),
            totalday1 varchar(5),
            medi_name2 varchar(30),
            one_dose2 varchar(5),
            perday2 varchar(5),
            totalday2 varchar(5),
            medi_name3 varchar(30),
            one_dose3 varchar(5),
            perday3 varchar(5),
            totalday3 varchar(5),
            medi_name4 varchar(30),
            one_dose4 varchar(5),
            perday4 varchar(5),
            totalday4 varchar(5),
            pharmacy_name varchar(30),
            pharmacy_date varchar(30),
            comment varchar(100),
            id serial
    )
             '''
    try:
        conn = pg.connect(connect_string)   
        cur = conn.cursor()  
        result = cur.execute(sql)
        print("처방전테이블 생성완료!")
        conn.commit()
        conn.close()
    except:   
        print("Something wrong!")
        
############################################################

def id_search(table_name,id):
    sql = f'''SELECT * FROM {table_name} p WHERE p.id = \'{id}\';

            '''
    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)  
        cur.execute(sql)
        result = cur.fetchall()
        conn.commit()
        conn.close()
        return result
    except pg.OperationalError as e:  
        print(e)
        return -1  

def delete_bookmark(local,domain,hosp_id):
    sql = f"""DELETE 
            FROM bookmark b
            WHERE b.local = '{local}' and b.domain = '{domain}' and b.hosp_id ='{hosp_id}'
            """
    try:
        conn = pg.connect(connect_string)  
        cur = conn.cursor() 
        cur.execute(sql)
        conn.commit()
        conn.close()
    except pg.OperationalError as e:   
        print(e)
        return -1
    return 0

def belong_check(table_name,local,domain):
    sql = f"""select * 
            FROM {table_name} b
            WHERE b.local = '{local}' and b.domain = '{domain}'
            """
    try:
        conn = pg.connect(connect_string)   
        cur = conn.cursor()  
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            return "fail"
        else:
            return "success"
        conn.commit()
        conn.close()
    except pg.OperationalError as e:    
        print(e)
        return -1
    return 0   

def insert_belong(table_name,local,domain,id):
    sql = f'''INSERT INTO {table_name} 
                     VALUES ( \'{local}\', \'{domain}\',\'{id}\');

            '''

    try:
        conn = pg.connect(connect_string)   
        cur = conn.cursor()   
        result = cur.execute(sql)
        conn.commit()
        conn.close()
    except pg.OperationalError as e:  
        print(e)
        return -1
    return 0

def update_prescription(store_name,date,comment,id): 

    sql = f"""UPDATE prescription SET pharmacy_name = '{store_name}',
            pharmacy_date = '{date}' , comment = '{comment}'
            WHERE id = {id};
            """
    try:
        conn = pg.connect(connect_string)   
        cur = conn.cursor()   
        cur.execute(sql)
        print(sql)
        conn.commit()
        conn.close()
    except pg.OperationalError as e:    
        print(e)
        return -1
    return 0


# with pg.connect(connect_string) as conn:
#     with conn.cursor() as cur:
#         cur.execute(
#             "CREATE TABLE guser (      id integer primary key,      name varchar(20),      email varchar(20)    );")
def main():
    return 0
    
if __name__ == ("__main__"):
    main()