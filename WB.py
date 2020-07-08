# import required modue lib for usage
import serial
import time
import configparser
from flask import Flask
from flask_cors import CORS

# Flask Home for testing
app = Flask(__name__)
CORS(app)
app.config['TESTING'] = True


# Flask with weigh bridge
@app.route('/WB4', methods=['GET'])
def weight_bridge():
    # getting current working
    global raw_data
    global data
    config_file_path = 'C:\WB\setup.ini'
    config = configparser.ConfigParser()
    config.read(config_file_path)
    dport = config.get('Port_setting', 'Port')
    dbaudrate = config.get('Port_setting', 'B_rate')
    while True:
        ser = serial.Serial(dport, dbaudrate)
        ser.flushInput()
        time.sleep(2)
        if ser.is_open:
            raw_data = '0'
            for x in range (2):
                data = ser.read_until(b'\r')
                #print(data)
            decodedata = data.decode('windows-1252', errors='replace')
            #print(decodedata)
            aData = decodedata.split()[1].replace(" ", "")
            #substring = '3'
            #res = aData.partition(substring)[2]
            #re_value = res.split()[1].replace(" ", "")
            decimalvalue = aData[-1:]
            wholevalue = aData[:-1]
            raw_data = wholevalue + "." + decimalvalue
            return raw_data.encode('utf-8')
            ser.close()
        else:
            ser.close()
        ser.close()
        break


app.run(host='127.0.0.3', port='5000', debug=False)
