FROM python
WORKDIR C:/Users/91812/Desktop/Final year/ibm assignments/Assignment 4
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python","./app.py"]