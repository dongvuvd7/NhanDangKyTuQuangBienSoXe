import numpy as np #thư viện numpy dùng để xử lý dữ liệu số
import cv2 #thư viện xử lý ảnh
import matplotlib.pyplot as plt #thư viện vẽ đồ thị
import tensorflow as tf #thư viện tensorflow dùng để xây dựng mạng nơ ron
from tensorflow.keras.preprocessing.image import load_img, img_to_array #thư viện xử lý ảnh, hàm load_img() dùng để load ảnh, img_to_array() dùng để chuyển ảnh thành mảng
import pytesseract as pt #thư viện pytesseract dùng để nhận dạng ký tự
import pytesseract

pytesseract.pytesseract.tesseract_cmd ="C:\\Program Files\\Tesseract-OCR\\tesseract.exe" # Path to tesseract.exe

model = tf.keras.models.load_model('./static/models/object_detection_new.h5') # load model đã train

#Hàm nhận diện vùng chứa biển số xe
def object_detection(path,filename): #path là đường dẫn ảnh, filename là tên ảnh
    # read image
    image = load_img(path) # PIL object #load ảnh
    image = np.array(image,dtype=np.uint8) # 8 bit array (0,255) #chuyển ảnh thành mảng
    image1 = load_img(path,target_size=(224,224)) #load ảnh với kích thước 224x224, 224x224 là kích thước mà model đã train
    # data preprocessing, tiền xử lý ảnh muốn chuẩn đoán
    image_arr_224 = img_to_array(image1)/255.0  # convert into array and get the normalized output, chuyển ảnh thành mảng và chuẩn hóa giá trị từ 0-255 thành 0-1
    h,w,d = image.shape #lấy chiều cao, chiều rộng, số kênh màu của ảnh
    test_arr = image_arr_224.reshape(1,224,224,3) #reshape ma trận ảnh thành 1x224x224x3, 1 là số ảnh, 224x224 là kích thước ảnh, 3 là số kênh màu
    # make predictions, tiến hành dự đoán
    coords = model.predict(test_arr) #dự đoán vị trí của object (object ở đây là biển số xe), trả về mảng 1x4, 4 là 4 giá trị xmin, xmax, ymin, ymax
    # denormalize the values, chuyển lại giá trị vị trí bounding box về kích thước ảnh gốc
    denorm = np.array([w,w,h,h]) #tạo 1 mảng gồm 4 phần tử, 2 phần tử đầu là chiều rộng ảnh, 2 phần tử sau là chiều cao ảnh
    coords = coords * denorm #nhân ma trận vị trí bounding box với ma trận kích thước ảnh gốc
    coords = coords.astype(np.int32) #chuyển giá trị vị trí bounding box về dạng số nguyên
    # draw bounding on top the image, vẽ bounding box lên ảnh
    xmin, xmax,ymin,ymax = coords[0] #lấy giá trị vị trí bounding box
    pt1 =(xmin,ymin) #vị trí góc trái trên
    pt2 =(xmax,ymax) #vị trí góc phải dưới
    print(pt1, pt2) #in ra vị trí bounding box
    cv2.rectangle(image,pt1,pt2,(0,255,0),3) #vẽ bounding box lên ảnh
    # convert into bgr, chuyển ảnh về dạng bgr để phù hợp với thư viện cv2
    image_bgr = cv2.cvtColor(image,cv2.COLOR_RGB2BGR) #chuyển ảnh về dạng bgr
    cv2.imwrite('./static/predict/{}'.format(filename),image_bgr) #lưu ảnh đã vẽ bounding box vào thư mục predict
    return coords #trả về vị trí bounding box (xmin, xmax,ymin,ymax)

#Hàm OCR để nhận dạng ký tự trong ảnh
def OCR(path,filename): #path là đường dẫn ảnh, filename là tên ảnh
    img = np.array(load_img(path)) #chuyển ảnh thành mảng
    cods = object_detection(path,filename) #gọi hàm object_detection để lấy vị trí bounding box
    xmin ,xmax,ymin,ymax = cods[0] #lấy vị trí bounding box
    roi = img[ymin:ymax,xmin:xmax] #cắt ảnh theo vị trí bounding box
    roi_bgr = cv2.cvtColor(roi,cv2.COLOR_RGB2BGR) #chuyển ảnh về dạng bgr

    cv2.imwrite('./static/roi/{}'.format(filename),roi_bgr) #lưu ảnh đã cắt vào thư mục roi
    # resize the image, thay đổi kích thước ảnh, tăng kích thước lên 2 lần cả chiều rộng và chiều cao
    resize_test_license_plate = cv2.resize(roi, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)

    # convert into gray scale, chuyển ảnh về dạng xám
    grayscale_resize_test_license_plate = cv2.cvtColor(resize_test_license_plate, cv2.COLOR_BGR2GRAY)

    # khử nhiễu, noise removal, dùng thuật toán GaussianBlur
    gaussian_blur_license_plate = cv2.GaussianBlur(grayscale_resize_test_license_plate, (5, 5), 0)

    text = pt.image_to_string(gaussian_blur_license_plate, lang ='eng', config ='--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHKLMNPSTUVXYZ0123456789') #gọi hàm image_to_string của thư viện pytesseract để nhận dạng ký tự trong ảnh
    text = "".join(text.split()).replace(":", "").replace("-", "")
    # print(text) #in ra kết quả nhận dạng
    return text #trả về kết quả nhận dạng


#Hàm OCR để nhận dạng ký tự trong ảnh
def OCR_TEST(path,filename): #path là đường dẫn ảnh, filename là tên ảnh
    img = np.array(load_img(path)) #chuyển ảnh thành mảng
    cods = object_detection(path,filename) #gọi hàm object_detection để lấy vị trí bounding box
    xmin ,xmax,ymin,ymax = cods[0] #lấy vị trí bounding box
    roi = img[ymin:ymax,xmin:xmax] #cắt ảnh theo vị trí bounding box
    roi_bgr = cv2.cvtColor(roi,cv2.COLOR_RGB2BGR) #chuyển ảnh về dạng bgr

    cv2.imwrite('./static/roi/{}'.format(filename),roi_bgr) #lưu ảnh đã cắt vào thư mục roi
    # resize the image, thay đổi kích thước ảnh, tăng kích thước lên 2 lần cả chiều rộng và chiều cao
    resize_test_license_plate = cv2.resize(roi, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)

    # convert into gray scale, chuyển ảnh về dạng xám
    grayscale_resize_test_license_plate = cv2.cvtColor(resize_test_license_plate, cv2.COLOR_BGR2GRAY)
    # grayscale_resize_test_license_plate = cv2.threshold(grayscale_resize_test_license_plate, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # khử nhiễu, noise removal, dùng thuật toán GaussianBlur
    gaussian_blur_license_plate = cv2.GaussianBlur(grayscale_resize_test_license_plate, (5, 5), 0)

    text = pt.image_to_string(gaussian_blur_license_plate, lang ='eng', config ='--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') #gọi hàm image_to_string của thư viện pytesseract để nhận dạng ký tự trong ảnh
    text = "".join(text.split()).replace(":", "").replace("-", "")
    print(text) #in ra kết quả nhận dạng
    return text #trả về kết quả nhận dạng