# Python Script for hosting the website
import serial
import time
from flask import Flask, render_template
from multiprocessing import Process
from flask import jsonify
from random import randint
import sys
import MySQLdb

app = Flask (__name__)
dbConn = MySQLdb.connect("localhost","pi","","car_db") or die("Could not connect to database")

sensor = {
0: {'name' : 'ultrasonic sensor', 'value' : 0},
1: {'name' : 'light resistor', 'value' : 0},
2: {'name' : 'distance limit', 'value' : 20}
}

car = {
0: {'name': 'Car movement','value':'static'},
1: {'name': 'Direction headed','value':'straight'}
}

lights = {
0: {'name': 'Led', 'value': 0, 'automatic' : 0}
}

automatic = False

@app.route("/")
def index():
    templateData = {
    'sensor' :sensor,
    'car' :car,
    'lights': lights,
    }
    return render_template('index.html', **templateData)

@app.route("/data")
def data():
    return render_template('data.html')

@app.route("/<mvm>/<trn>")
def move(mvm,trn):
    make_move(mvm,trn)
    templateData = {
    'sensor' :sensor,
    'car' :car,
    'lights': lights,
    }
    return render_template('index.html', **templateData)

@app.route("/update", methods=['POST'])
def update():
    getSensorData()
    automatic_d()
    if(lights[0]['automatic'] == 1):
        if(sensor[1]['value']<50):
            switch_lights(1)
        else:
            switch_lights(0)
    templateData = {
    'sensor' :sensor,
    'car' :car,
    'lights': lights,
    }
    return jsonify(templateData)

@app.route("/toggle_auto", methods=['GET'])
def toggle_auto():
    global automatic
    automatic = not automatic
    if(automatic):
        return "1"
    else:
        return "0"

@app.route("/switches/<cond>", methods=['POST'])
def switches(cond):
    swch = 0
    lights[0]['automatic'] = 0
    if(cond == "1"):
        swch = 1
    if(cond =="2"):
        lights[0]['automatic'] = 1
        
    switch_lights(swch)
    return cond

@app.route("/update_dlim/<dlim>", methods=['POST'])
def update_dlim(dlim):
    distance_limit = int(dlim)
    sensor[2]['value'] = distance_limit
    return str(distance_limit)

def getStepsPerRev(mvm):
    if(mvm == "forward"):
        movement = "2048"
    elif(mvm == "backward"):
        movement = "-2048"
    else:
        movement = "0"
    return movement

def getServoAngle(trn):
    if(trn == "left"):
        turn = "0"
    elif(trn == "right"):
        turn = "70"
    else:
        turn = "35"
    return turn

def getSensorData():
    with dbConn:
        cursor = dbConn.cursor()
        cursor.execute("SELECT * FROM sensorLog ORDER BY id DESC LIMIT 1")
        values = cursor.fetchone()
        ult = int(values[1])
        ldr = int(values[2])
        sensor[0]['value'] = ult
        sensor[1]['value'] = ldr
        cursor.close()
        
def make_move(mvm,trn):
    car[0]['value'] = mvm
    car[1]['value'] = trn
    stri = "0,"+getStepsPerRev(mvm)+","+getServoAngle(trn)+";"
    update_data_file(stri)
    # cmd = stri.encode()
    # ser.write(cmd)
    
def update_data_file(cmd):
    file = open('templates/data.html','w')
    file.write(cmd)
    file.close()
    
def switch_lights(cond):
    if(lights[0]['value'] != cond):
        lights[0]['value'] = cond
        stri = str(cond)
        cmd = "2," + stri +";"
        file = open('templates/data.html','r')
        cur_data = file.read();
        file.close()
        if(cur_data != cmd):
            update_data_file(cmd);
            
def automatic_d():
    if(automatic):
        a = sensor[0]['value']
        b = sensor[2]['value']
        if(a>=(b+5)):
            make_move("forward","straight")
        else:
            if(car[1]['value']=='straight'):
                random = randint(0,2)
                if(random<2):
                    make_move("forward","right")
                else:
                    make_move("forward","left")
                    
                    
if __name__ == "__main__" :
    # ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    # ser.flush()
    app.run(host='0.0.0.0', port = 80, debug = True, threaded=True)