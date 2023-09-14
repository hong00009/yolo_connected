from django.shortcuts import render
import os
from django.core.files.storage import FileSystemStorage
from uuid import uuid4 # 고유번호 생성
from . import yolo_detect

# Create your views here.
def index(request):
    return render(request, 'detect/img_up_res.html')

def rename_imagefile_to_uuid(filename): # 고유번호로 이미지파일명 변경
    ext = filename.split('.')[-1] # 파일 이름에서 확장자만 분리
    uuid = uuid4().hex
    filename = '{}.{}'.format(uuid,ext)

    return filename


# 전달된 이미지를 받아서 yolo 모델에 주입 후 검출된 결과 이미지를 클라이언트에게 전송
def detect(request):
    img = request.FILES.get('images') # 사용자가 전송한 이미지 파일 가져오기
    fs = FileSystemStorage() # 파일 저장소 접근 객체 생성

    # 전송된 파일명 변경해서 저장
    # 서버에서 사용할 유일한 파일면 생성
    file_name = rename_imagefile_to_uuid(img.name)
    img_up_url = fs.save(file_name, img) # media 디렉터리에 저장
    print(img_up_url)

    img = 'media/' + img_up_url

    # 이미지 객체 검출 함수 호출 yolov5_detect.py
    res_url = yolo_detect.y_detect(img, img_up_url)

    return render(request, 'detect/result.html', {'image':res_url}) 
