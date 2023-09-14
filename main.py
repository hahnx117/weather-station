import time
import board
import adafruit_bmp3xx
import pickle
import datetime
#from picamera2 import Picamera2
#from libcamera import controls
from jinja2 import Environment, FileSystemLoader
import subprocess

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('website.j2')
site_directory = "/var/www/html"

i2c = board.I2C()

#picam2 = PiCamera2()
#picam2.rotation = 180
image_width = 1024
image_height = 768
image_rotation = 180
image_path = f"{site_directory}/image.jpg"


bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2

pickle_filename = "data/environment.pickle"

data_dict = {}

while True:
    temperature_C = float(bmp.temperature)
    pressure_hPa = float(bmp.pressure)
    altitude_m = float(bmp.altitude)
    
    d = datetime.datetime.now()
    date_dict = d.isoformat()
    date_string = d.strftime("Today is %A, %B %d, %Y")
    time_string = d.strftime("The time is %H:%M")
        
    data_dict[date_dict] = {}
    data_dict[date_dict]['temperature'] = temperature_C
    data_dict[date_dict]['pressure'] = pressure_hPa
    data_dict[date_dict]['altitude'] = altitude_m

    #os.system("v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0")
    #picam2.start(show_preview=False)
    #picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast})
    #picam2.start_and_capture_files("/var/www/html/image.jpg")
    #picam2.stop()
    #os.system("v4l2-ctl --set-ctrl wide_dynamic_range=0 -d /dev/v4l-subdev0")
    subprocess.check_output(["libcamera-still", "--width", str(image_width), "--height", str(image_height), "--rotation", str(image_rotation), "--hdr", "on", "-o",image_path])
    #sleep(5)

    with open(pickle_filename, 'wb') as handle:
        pickle.dump(data_dict, handle)
    
    website_output = template.render(
        date_string=date_string,
        time_string=time_string,
        temperature_C=round(temperature_C, 2),
        pressure_hPa=round(pressure_hPa, 2),
        altitude_m=round(altitude_m, 2)
    )

    with open(f"{site_directory}/index.html", "w") as fh:
        fh.write(website_output)

    time.sleep(10)