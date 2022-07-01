
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime
import re
from PIL import Image
from PIL import ImageDraw

def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url

def init_phantomjs_driver(*args, **kwargs):

    headers = { 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Connection': 'keep-alive'
    }

    for key, value in headers.iteritems():
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value

    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'

    driver =  webdriver.PhantomJS(*args, **kwargs)
    driver.set_window_size(1400,1000)

    return driver
    
#dcap = dict(DesiredCapabilities.PHANTOMJS)
#dcap["phantomjs.page.settings.userAgent"] = ( 
#"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36")
#driver = webdriver.PhantomJS(desired_capabilities=dcap)
#driver.set_window_size(1400,1000)

def page_is_loading(driver):
    while True:
        x = driver.execute_script("return document.readyState")
        if x == "complete":
            return True
        else:
            yield False

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'image/'

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/page',  methods=['GET', 'POST'])
def page():
    if request.method == 'POST':
       path = request.form['img_url']
       path = formaturl(path)
       print (path)
       
    #_________________________________________
    
   
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    #driver.set_window_size(1400,1000)

    """options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1400,1000)
   

    try:
       driver.get(path)
       #_________________________________________
       if "youtube.com" in path:
           print ('................')
           WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@class='style-scope ytd thumbnail-overlay-time-status-renderer']")))
       while not page_is_loading(driver):
           continue
           
       #-----------------------------------------
       now = datetime.now()
       time = now.strftime("%H:%M:%S")
       import uuid
       uuid = str(uuid.uuid4().hex)
       image_pth = os.getcwd() + '/image/'
       image = image_pth + str(driver.current_url).split('/')[2] + '_' + uuid + '_'  + str(request.remote_addr) + '_' + str(time) + '.png'
       image_ = str(driver.current_url).split('/')[2] + '_' + uuid + '_' + str(request.remote_addr) + '_' + str(time) + '.png'
       driver.save_screenshot(image)
       driver.close()
       driver.quit()
       
       #-----------------------------------------
       img_url_ = 'http://0.0.0.0:8081/image/'+ image_
       img = Image.open(image)
       I1 = ImageDraw.Draw(img)
       dateTimeObj = datetime.now()
       timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
       imgtext = timestampStr + ' fb.com/paradox.jabed/'
       I1.text((28, 36), imgtext, fill=(0, 0, 255))
       img.save(image)
       print(request.remote_addr)
       embeded_html = '''<embed type="image/jpg" src="{}" width="500" height="500"> </EMBED>'''.format(img_url_)
       return render_template('image.html', image=img_url_, image_nm=image_, embeded_html=embeded_html, error=error)
       
    except:
       error = "Error Loading Website."
       return render_template('image.html', image="", image_nm="", embeded_html="", error="")
       """
    
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    driver.get(path)
    if "youtube.com" in path:
        print ('................')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@class='style-scope ytd-thumbnail-overlay-time-status-renderer']")))
        
    
    while not page_is_loading(driver):
          continue
    
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    import uuid
    uuid = str(uuid.uuid4().hex)
    image_pth = os.getcwd() + '/image/'
    image = image_pth + str(driver.current_url).split('/')[2] + '_' + uuid + '_'  + str(request.remote_addr) + '_' + str(time) + '.png'
    image_ = str(driver.current_url).split('/')[2] + '_' + uuid + '_' + str(request.remote_addr) + '_' + str(time) + '.png'
    total_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    total_height = driver.execute_script('return document.body.parentNode.scrollHeight')

    driver.set_window_size(total_width, total_height)
    driver.save_screenshot(image)
    driver.close()
    img_url_ = 'http://:8081/image/'+ image_
    driver.quit()
    
    img = Image.open(image)
    I1 = ImageDraw.Draw(img)
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    imgtext = timestampStr + ' fb.com/paradox.jabed/'
    I1.text((28, 36), imgtext, fill=(0, 0, 255))
    img.save(image)
    
    print(request.remote_addr)
    #return '''..........'''
    #return redirect(url_for('index'))
    embeded_html = '''<embed type="image/jpg" src="{}" width="500" height="500"> </EMBED>'''.format(img_url_)
    return render_template('image.html', image=img_url_, image_nm=image_, embeded_html=embeded_html)#, error= if error else None)

@app.route('/image/<filename>')
def get_gile(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("8081"),
        debug=True
    )

