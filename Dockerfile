FROM python:3.10-slim
#작업할 폴더 생성
WORKDIR /app
# 작업했던 파일들을 복사해서 넣어 줍니다.
COPY . .
#파이썬 라이브러리 설치					         
RUN pip3 install -r requirements.txt		  

#5000 포트 사용 예정
EXPOSE 5000
#플라스크 실행 
#외부 접속 가능 --host=0.0.0.0
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]