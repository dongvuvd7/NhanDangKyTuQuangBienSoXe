from flask import Flask, render_template, request #thư viện flask để tạo web app, render_template để render html, request để lấy dữ liệu từ form
import os #thư viện os thao tác với hệ thống
from deeplearning import OCR #import hàm OCR từ file deeplearning.py
from flask_mysqldb import MySQL #thư viện flask_mysqldb để kết nối tới mysql
from datetime import datetime #thư viện datetime để lấy thời gian hiện tại
# webserver gateway interface
app = Flask(__name__)
app.config['DEBUG'] = True

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'baidoxe'
mysql = MySQL(app)

BASE_PATH = os.getcwd() #lấy đường dẫn hiện tại
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/') #tạo đường dẫn đến thư mục upload
UPLOAD_PATH_OUT = os.path.join(BASE_PATH,'static/uploadout/') #tạo đường dẫn đến thư mục upload
TOTAL_SLOT = 100 #tổng số chỗ đỗ xe


@app.route('/',methods=['POST','GET','PUT','DELETE']) #tạo route cho trang chủ
#tạo hàm index để render trang chủ
def index():
    print( request.form.to_dict())
    print ('submitin' in request.form.to_dict())
    print ('submitoutt' in request.form.to_dict())
    if request.method == 'POST': #nếu có request từ form
        
        #Nếu input có name là submitoutt 
        if 'submitin' in request.form.to_dict():
            upload_file = request.files['image_name'] #lấy file từ form
            filename = upload_file.filename #lấy tên file
            path_save = os.path.join(UPLOAD_PATH,filename) #tạo đường dẫn đến file
            upload_file.save(path_save) #lưu file muốn chuẩn đoán vào đường dẫn đến folder upload
            text = OCR(path_save,filename) #gọi hàm OCR từ file deeplearning.py để nhận dạng ký tự

            #Lấy thông tin chủ xe từ database
            car_owner_info = get_car_owner_info(text)
            print(car_owner_info)
            #Nếu không có thông tin chủ xe thì set cost = 10000
            cost = 0
            if car_owner_info is None:
                cost = 10000
            #Thêm thông tin vào bảng parking_ledger
            update_parking_ledger(car_owner_info, text, 'in', cost)
            #Cập nhật thông tin thống kê
            parking_infor = get_parking_infor()

            return render_template('index.html',upload=True,upload_image=filename,text=text, car_owner=car_owner_info, cost=cost, parking_infor=parking_infor) #trả kết quả cho index.html, các tham số: upload=True có hiển thị kết quả hay không, upload_image=filename tên ảnh để sang index.html lấy ra ảnh tương ứng từng thư mục (upload, predict, roi), text=text để hiển thị kết quả nhận dạng

        if 'submitoutt' in request.form.to_dict():
            upload_file = request.files['image_name'] #lấy file từ form
            filename = upload_file.filename #lấy tên file
            path_save = os.path.join(UPLOAD_PATH,filename) #tạo đường dẫn đến file
            upload_file.save(path_save) #lưu file muốn chuẩn đoán vào đường dẫn đến folder upload
            text = OCR(path_save,filename) #gọi hàm OCR từ file deeplearning.py để nhận dạng ký tự
            #Lấy thông tin chủ xe từ database
            car_owner_info = get_car_owner_info(text)
            #Thêm thông tin vào bảng parking_ledger
            update_parking_ledger(car_owner_info, text, 'out', 0)
            #Cập nhật thông tin thống kê
            parking_infor = get_parking_infor()

            return render_template('index.html',upload=True,upload_image=filename,text=text, car_owner=car_owner_info, cost=0, parking_infor=parking_infor) #trả kết quả cho index.html, các tham số: upload=True có hiển thị kết quả hay không, upload_image=filename tên ảnh để sang index.html lấy ra ảnh tương ứng từng thư mục (upload, predict, roi), text=text để hiển thị kết quả nhận dạng

    if request.method == 'PUT': #nếu có request từ form
        if(request.files['image_name_out']):

            upload_file = request.files['image_name_out'] #lấy file từ form
            filename = upload_file.filename #lấy tên file
            path_save = os.path.join(UPLOAD_PATH_OUT,filename) #tạo đường dẫn đến file
            upload_file.save(path_save) #lưu file muốn chuẩn đoán vào đường dẫn đến folder upload
            text = OCR(path_save,filename) #gọi hàm OCR từ file deeplearning.py để nhận dạng ký tự

            return render_template('index.html',upload_out=True,upload_image_out=filename,text_out=text) #trả kết quả cho index.html, các tham số: upload=True có hiển thị kết quả hay không, upload_image=filename tên ảnh để sang index.html lấy ra ảnh tương ứng từng thư mục (upload, predict, roi), text=text để hiển thị kết quả nhận dạng

    parking_infor_init = get_parking_infor()
    return render_template('index.html',upload=False, upload_out=False, parking_infor=parking_infor_init) #nếu không có request từ form thì trả về trang chủ không có kết quả

def get_car_owner_info(license_plate_number):
    #Tạo kết nối tới mysql
    cursor = mysql.connection.cursor()
    #Lấy thông tin chủ xe từ database
    cursor.execute("SELECT * FROM baidoxe.car_owner WHERE number_plate = %s", (license_plate_number,))
    car_owner_info = cursor.fetchone()
    cursor.close()
    return car_owner_info

def update_parking_ledger(car_owner_info, number_plate, way, cost):
    #Tạo kết nối tới mysql
    cursor = mysql.connection.cursor()
    #Nếu thông tin chủ xe là none
    if car_owner_info is None:
        if way == 'in':
            cursor.execute("INSERT INTO baidoxe.parking_ledger (number_plate, parking_fee, ticket_type, on_time, way) VALUES (%s, %s, %s, %s, %s)", ('unknown', cost, 'Vé ngày', datetime.now(), 'in'))
        else:
            cursor.execute("INSERT INTO baidoxe.parking_ledger (number_plate, parking_fee, ticket_type, on_time, way) VALUES (%s, %s, %s, %s, %s)", ('unknown', cost, 'Vé ngày', datetime.now(), 'out'))
    #Nếu xe đã đăng ký vé từ trước
    else:
        if way == 'in':
            cursor.execute("INSERT INTO baidoxe.parking_ledger (number_plate, parking_fee, ticket_type, on_time, way) VALUES (%s, %s, %s, %s, %s)", (number_plate, cost, car_owner_info[5], datetime.now(), 'in'))
        else:
            cursor.execute("INSERT INTO baidoxe.parking_ledger (number_plate, parking_fee, ticket_type, on_time, way) VALUES (%s, %s, %s, %s, %s)", (number_plate, cost, car_owner_info[5], datetime.now(), 'out'))

    mysql.connection.commit()
    cursor.close()

def get_parking_infor():
    #Tạo kết nối tới mysql
    cursor = mysql.connection.cursor()
    #Lấy số chỗ còn trống = Tổng số chỗ - (Tổng số lượt vào - Tổng số lượt ra)
    total_in = cursor.execute("SELECT * FROM baidoxe.parking_ledger WHERE way = 'in'")
    total_out = cursor.execute("SELECT * FROM baidoxe.parking_ledger WHERE way = 'out'")
    print(TOTAL_SLOT, [total_in, total_out])
    available_slot = TOTAL_SLOT - (total_in - total_out)
    #Lấy tổng số lượt gửi xe trong ngày hôm nay
    total_parking_today = cursor.execute("SELECT * FROM baidoxe.parking_ledger WHERE DATE(on_time) = DATE(NOW()) AND way = 'in'")
    #Lấy tổng số lượt gửi xe của vé ngày, vé đã đăng ký trong ngày hôm nay
    total_parking_default_ticket_today = cursor.execute("SELECT * FROM baidoxe.parking_ledger WHERE DATE(on_time) = DATE(NOW()) AND ticket_type = 'Vé ngày' AND way = 'in'")
    total_parking_registered_ticket_today = cursor.execute("SELECT * FROM baidoxe.parking_ledger WHERE DATE(on_time) = DATE(NOW()) AND ticket_type != 'Vé ngày' AND way = 'in'")
    #Tổng số tiền thu được trong ngày hôm nay
    total_fee_today = total_parking_default_ticket_today * 10000

    print([TOTAL_SLOT, available_slot, total_parking_today, total_parking_default_ticket_today, total_parking_registered_ticket_today, total_fee_today])
    #Trả về mảng các thông tin
    return [TOTAL_SLOT, available_slot, total_parking_today, total_parking_default_ticket_today, total_parking_registered_ticket_today, total_fee_today]



if __name__ =="__main__":
    app.run(debug=True)