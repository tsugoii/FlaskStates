"""
Week 7: Thank God for course feedback
"""

import os
import re
import sys
import subprocess
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

STATES_LIST = []
STATES_LIST.append ( ['Alabama', 'Montgomery', 4903185, 'Camellia','https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/camellia-flower.jpg?itok=K1xKDUI5'] )
STATES_LIST.append ( ['Alaska', 'Juneau', 731545, 'Forget-Me-Not', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/Oak_leaf_hydrangea380.jpg?itok=oKb8UNHC' ] )
STATES_LIST.append ( ['Arizona', 'Phoenix', 7278717, 'Suguaro Catus Blossom','https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/large/public/saguaroflowersFlickr.jpg?itok=QpFj3Opl'] )
STATES_LIST.append ( ['Arkansas', 'Little Rock', 3017825, 'Apple Blossom', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/large/public/primary-images/AppletreeblossomArkansasflower.JPG?itok=Z-Q3rp1D'] )
STATES_LIST.append ( ['California', 'Sacremento ', 39512223, 'Golden Poppy', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/large/public/primary-images/CAflowerCaliforniaPoppy.jpg?itok=Q5Q8X3LE'] )
STATES_LIST.append ( ['Colorado', 'Denver', 5758736, 'Mountain Columbine', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/Colorado_columbine2.jpg?itok=3bfYnk5Y'] )
STATES_LIST.append ( ['Connecticut', 'Hatford', 3565287, 'Mountain Laurel', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/Mountain-Laural-flowers2.jpg?itok=b7tlfk4G'] )
STATES_LIST.append ( ['Delaware', 'Dover', 973764, 'Peach Blossom', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/peachblossomspeachflowers.jpg?itok=Lx-fzlgl'] )
STATES_LIST.append ( ['Florida', 'Tallahassee', 21477737, 'Orange Blossom', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/OrangeBlossomsFloridaFlower.jpg?itok=SK-Tp-rH'] )
STATES_LIST.append ( ['Georgia', 'Atlanta', 10617423, 'Cherokee Rose', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/CherokeeRoseFlower.jpg?itok=TKWxpzcw'] )
STATES_LIST.append ( ['Hawaii', 'Honolulu', 415872, 'Red Hibiscus', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/yellowhibiscusPuaAloalo.jpg?itok=Y2aYqLKY'] )
STATES_LIST.append ( ['Idaho', 'Boise', 1787065, 'Syringa', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/syringaPhiladelphuslewisiiflower.jpg?itok=BKOaOXs0'] )
STATES_LIST.append ( ['Illinois', 'Springfield', 12671821, 'Violet', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/singlebluevioletflower.jpg?itok=8i1uQHwg'] )
STATES_LIST.append ( ['Indiana', 'Indianaplois', 6732219, 'Peony', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/PeonyPaeoniaflowers.jpg?itok=IrFIQ9ZF'] )
STATES_LIST.append ( ['Iowa', 'Des Moines', 3155070, 'Wild Rose', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/WildPrairieRose.jpg?itok=zyo0qIMG'] )
STATES_LIST.append ( ['Kansas', 'Topeka', 2913314, 'Sunflower', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/native-sunflowers.jpg?itok=PB8Qq-IC'] )
STATES_LIST.append ( ['Kentucky', 'Frankfort', 4467673, 'Goldenrod', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/stateflowergoldenrod-bloom.jpg?itok=CCLZ4eiV'] )
STATES_LIST.append ( ['Louisiana', 'Baton Rouge', 4648794, 'Magnolia', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/LouisianaIrisWildflower-0.jpg?itok=lOKBHACo'] )
STATES_LIST.append ( ['Maine', 'Augusta', 1344212, 'Pine Cone &amp; Tassel','https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/whitepinemalecones.jpg?itok=cscy757F'] )
STATES_LIST.append ( ['Tennessee', 'Nashville', 6833174, 'Iris', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/passionflowerwildflower2.jpg?itok=c5CmwPJt'] )
STATES_LIST.append ( ['Maryland', 'Annapolis', 6045680, 'Black-eyed Susan', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/FlowerMDBlack-eyedSusan.jpg?itok=I8jYSvFl'] )
STATES_LIST.append ( ['Massachusettes', 'Boston', 6949503, 'Mayflower', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/MayflowerTrailingArbutus.jpg?itok=uIQd8O6F'] )
STATES_LIST.append ( ['Rhode Island', 'Providence', 1059361, 'Violet', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/violetsflowers.jpg?itok=KNMrrLfu'] )
STATES_LIST.append ( ['Minniesota', 'St.Paul', 5639632, 'Lady-Slipper', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/pinkwhiteladysslipperflower1.jpg?itok=LGYZFl26'] )
STATES_LIST.append ( ['Mississippi', 'Jackson', 2976149, 'Magnolia', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/CoreopsisWildflower1-01.jpg?itok=HPK2l6yQ'] )
STATES_LIST.append ( ['Missouri', 'Jefferson City', 6137428, 'Hawthorne', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/hawthornflowersblossoms1.jpg?itok=LOrlsJ3L'] )
STATES_LIST.append ( ['Michigan', 'Lansing', 9986857, 'Apple Blossom', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/appleblossombeauty.jpg?itok=HxWn6VHl'] )
STATES_LIST.append ( ['Montana', 'Helena', 1068778, 'Bitterroot', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/bitterrootfloweremblem.jpg?itok=SnCwy78x'] )
STATES_LIST.append ( ['Nebraska', 'Lincoln', 1934408, 'Goldenrod', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/goldenrodflowersyellow4.jpg?itok=6X5qpm4c'] )
STATES_LIST.append ( ['Nevada', 'Carson City', 3080156, 'Sagebrush', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/Nevada-Sagebrush-Artemisia-tridentata.jpg?itok=ij6RMnom'] )
STATES_LIST.append ( ['New Hampshire', 'Concord', 1359711, 'Purple Lilac', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/NH-pinkLadysSlipperFlower.jpg?itok=tppHBWs8'] )
STATES_LIST.append ( ['Vermont', 'Montpelier', 623989, 'Red Clover', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/redcloverstateflowerWV.jpg?itok=wvnkPA4C'] )
STATES_LIST.append ( ['New Jersey', 'Trenton', 8882190, 'Violet', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/wood-violet.jpg?itok=IJ0ft_8r'] )
STATES_LIST.append ( ['New Mexico', 'Santa Fe', 2096829, 'Yucca', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/YuccaFlowersclose.jpg?itok=jCUN8toc'] )
STATES_LIST.append ( ['New York', 'Albany', 19453561, 'Rose', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/redrosebeautystateflowerNY.jpg?itok=LDcB_Vc_'] )
STATES_LIST.append ( ['North Carolina', 'Raleigh', 10488084, 'Flowering Dogwood', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/floweringdogwoodflowers2.jpg?itok=p_1PGcNk'] )
STATES_LIST.append ( ['Wyoming', 'Cheyenne', 78759, 'Indian Paintbrush', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/indianpaintbrushWYflower.jpg?itok=ClQHPA55'] )
STATES_LIST.append ( ['North Dakota', 'Bismark', 762062, 'Prairie Rose', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/flowerwildprairierose.jpg?itok=j5Retaxz'] )
STATES_LIST.append ( ['Ohio', 'Columbus', 11689100, 'Scalet Carnation', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/redcarnationOhioflower.jpg?itok=oCdw9u6V'] )
STATES_LIST.append ( ['Oklahoma', 'Oklahoma City', 3956971, 'Mistletoe', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/Indian-blanket-Gaillardia-pulchella.jpg?itok=_7eai2t7'] )
STATES_LIST.append ( ['Oregon', 'Salem', 4217737, 'Oregon Grape', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/Oregongrapeflowers2.jpg?itok=lVSJoqCE'] )
STATES_LIST.append ( ['Pennsylvania', 'Harrisburg', 12801989, 'Mountain Laurel', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/Mt_Laurel_Kalmia_Latifolia.jpg?itok=8VhW2Sms'] )
STATES_LIST.append ( ['South Carolina', 'Columbia', 5148714, 'Yellow Jessamine','https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/CarolinaYellowJessamine101.jpg?itok=1tgcX6mj'] )
STATES_LIST.append ( ['South Dakota', 'Pierre', 88465, 'Pasque flower', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/Pasqueflower-03.jpg?itok=vMlGt_qW'] )
STATES_LIST.append ( ['Texas', 'Austin', 28995881, 'Bluebonnet', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/Texas-dawn-waterlily-Nymphaea.jpg?itok=RuViBaR-'] )
STATES_LIST.append ( ['Utah', 'Salt Lake City', 3202985, 'Sego Lily', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/SegoLily.jpg?itok=Hxt3DOTq'] )
STATES_LIST.append ( ['Virginia', 'Richmond', 8535519, 'Dogwood', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/floweringDogwoodSpring.jpg?itok=DFuNFYgS'] )
STATES_LIST.append ( ['Washington', 'Olympia', 7614893, 'Coast Rhododendron', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/flower_rhododendronWeb.jpg?itok=0Xl911Zf'] )
STATES_LIST.append ( ['West Virginia', 'Charleston', 1792147, 'Rhododendron', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/primary-images/rhododendronWVstateflower.jpg?itok=7lJaeqWT'] )
STATES_LIST.append ( ['Wisconsin', 'Madison', 5822434, 'Wood Violet', 'https://statesymbolsusa.org/sites/statesymbolsusa.org/files/styles/symbol_thumbnail__medium/public/wood-violet.jpg?itok=IJ0ft_8r'] )
STATES_LIST = sorted(STATES_LIST, key=lambda x: x[0], reverse=False)
COMMON_PASSWORDS_LIST = []
app = Flask(__name__)

environment_path = os.path.join(sys.path[0] + "\\" + r"app.py")
environment_command = "$env:FLASK_APP=" + environment_path
password_path = os.path.join(sys.path[0] + "\\" + r"static\CommonPassword.txt")
log_path = os.path.join(sys.path[0] + "\\" + r"static\PasswordLogs.txt")
with open(password_path) as file1:
    COMMON_PASSWORDS_LIST = file1.read().splitlines()
names_passwords = {}
IS_LOGGED_IN = False
LOGGED_IN_USER = ""

def password_check():
    """Does password complexity checking"""
    password = request.form['password']
    flag = 0
    if len(password)<=12:
        flag = -1
    elif not re.search("[a-z]", password):
        flag = -1
    elif not re.search("[A-Z]", password):
        flag = -1
    elif not re.search("[0-9]", password):
        flag = -1
    elif not re.search("[@_!#$%^&*()<>?/|}{~:]", password):
        flag = -1
    elif re.search(r"\s", password):
        flag = -1
    elif password in COMMON_PASSWORDS_LIST:
        flag = -1
    return flag == 0

def common_password_check():
    """Checks against common passwords"""
    password = request.form['password']
    return password not in COMMON_PASSWORDS_LIST

def log_all_the_things():
    """Logs failed logins"""
    ip_addr = request.remote_addr
    with open(log_path, 'a') as file2:
        file2.write(f'{ip_addr} failed to log in at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")} \n')


@app.route('/')
def index():
    """Main Landing Page"""
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
    return render_template('landing_page.html', date_time=date_time)
    #display current date and time

@app.route('/flowers/')
def flowers():
    """Click Again to get to the real content"""
    if IS_LOGGED_IN is False:
        print(IS_LOGGED_IN)
        return redirect(url_for('errorpage'))
    return render_template('flowers.html')

@app.route('/flowers/states')
def states():
    """Aren't states cool?"""
    if IS_LOGGED_IN is False:
        print(IS_LOGGED_IN)
        return redirect(url_for('errorpage'))
    states_list = ""
    for x_x in range(len(STATES_LIST)):
        states_list += find_things(STATES_LIST[x_x])
    return render_template('states.html', states_list = states_list)

@app.route('/flowers/pictures/<state>')
def pictures(state):
    """Wow, pretty pictures"""
    if IS_LOGGED_IN is False:
        print(IS_LOGGED_IN)
        return redirect(url_for('errorpage'))
    row = next((s for s in STATES_LIST if s[0] == state), None)
    if not None:
        return render_template('flower_pictures.html', url=row[4], name =row[3])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Page"""
    error = None
    if request.method == 'POST':
        try:
            if names_passwords[request.form['username']] == request.form['password']:
                global IS_LOGGED_IN
                IS_LOGGED_IN = True
                global LOGGED_IN_USER
                LOGGED_IN_USER = request.form['username']
                return redirect(url_for('flowers'))
            else:
                error = 'Invalid Password'
        except:
            error = 'Invalid Username'
    log_all_the_things()
    return render_template('login.html', error=error)

@app.route('/registration', methods=['GET', 'POST'])
def register():
    """Registration Page"""
    error = None
    if request.method == 'POST':
        if request.form['username'] in names_passwords.keys():
            error = 'User already registered'
        if common_password_check() is False:
            error = 'Password is too commonly used, please use different password'
        elif password_check() is False:
            error = 'Password does not meet complexity requirements: length of 13, 1 uppercase, 1 lowercase, 1 special character required'
        else:
            names_passwords[request.form['username']] = request.form['password']
            return redirect(url_for('index'))
    return render_template('registration.html', error=error)

@app.route('/errorpage')
def errorpage():
    """The error page"""
    error = 'User needs to be logged in to access additional pages'
    return render_template('errorpage.html', error=error)

@app.route('/resetpassword', methods=['GET', 'POST'])
def resetpassword():
    """A page where you reset your password"""
    error = None
    if request.method == 'POST':
        if common_password_check() is False:
            error = 'Password is too commonly used, please use different password'
        elif password_check() is False:
            error = 'Password does not meet complexity requirements: length of 13, 1 uppercase, 1 lowercase, 1 special character required'
        else:
            names_passwords[LOGGED_IN_USER] = request.form['password']
            return redirect(url_for('flowers'))
    return render_template('resetpassword.html', error=error)

def find_things(row):
    """this is where we use our unordered list"""
    if IS_LOGGED_IN is False:
        print(IS_LOGGED_IN)
        return redirect(url_for('errorpage'))
    result = '<tr><td>' + str(row[0]) + '</td><td>' + str(row[1]) + '</td><td>' + str(row[2]) + '</td><td><a href=/flowers/pictures/' + str(row[0]) + '>' + str(row[3]) + '</a></td><td><a href=http://www.google.com/search?q=' + str(row[0]) + '>Google</a></td></tr>'
    return result

if __name__ == "__main__":
    print("*******Press Enter*******")
    input(environment_command)
    subprocess.Popen(r'"' + os.environ["PROGRAMFILES"] + r'\Internet Explorer\IEXPLORE.EXE" http://localhost:5000/')
    app.run()
