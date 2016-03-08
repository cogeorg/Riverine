#!/usr/bin/env python
import datetime

from flask import flash, Flask, g, request, redirect, url_for, render_template
from flask.ext import login as flask_login
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from modules import ModelVisualizerLib as MVLib


# Create the application and initialize it with configuration
# from sde_app.cfg file
sde_app = Flask(__name__)
sde_app.config.from_pyfile('sde_app.cfg')
db = SQLAlchemy(sde_app)

# To use Flask-Login, we need to instantiate LoginManager and
# initialize it with our application instance.  LoginManager contains the
# code that makes sde_app application and Flask-Login work together.
login_manager = flask_login.LoginManager()
login_manager.init_app(sde_app)

# Assign a view handler to respond to login requests from client side
login_manager.login_view = 'login' 


# For authentication we need a User model class that will store the
# username and password associated with a user. We extend the
# SQLAlchemy db.Model class 
class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(50), unique=True, index=True)
    password = db.Column('password', db.String(50))
    registered_on = db.Column('registered_on', db.DateTime)
  
    def __init__(self, username, password):
        self.username = username
        self.set_password(password) # Store hashed version of password
        self.registered_on = datetime.datetime.utcnow()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)
    

# Define function to Register new users
# The register fuction responds to both GET and POST requests:
#  GET:  render register.html 
#  POST: handle registration request (when user submits the form) by
#        storing data to database.  After successful registration, the
#        user will be redirected to the login page
@sde_app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form['username']
    password = request.form['password']
    new_user = User(username, password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))

@sde_app.route('/', methods=['GET'])
@sde_app.route('/index/', methods=['GET'])
@flask_login.login_required
def index():
    return render_template('index.html')


# Define the route that will process the model file upload and visualize the 
# corresponding model
@sde_app.route('/upload/', methods=['GET', 'POST'])
@flask_login.login_required
def upload():
    if request.method == 'POST':
           
        filename = request.values['sel_modelfile']
        # Get name of the uploaded model file        
        if filename != '':
            try:           
                 file = open(filename, 'r')
            except IOError:
                print 'Unable to open file', filename
                return render_template('index.html')           
        else:
            file = request.files['modelfile']   
        # Check if the file exists
        if file:  

            Viz = MVLib.MV.ModelVisualizer()
            if not Viz.read_config_file(file):
                print 'Config file cannot be opened!'
                return render_template('index.html')
                
            file.close();
            
            vizType = Viz.config_obj['model']['visualizer']['view']['@type'];
            if vizType == 'line':
                Viz = MVLib.LMV.LineplotVisualizer(Viz.config_obj)
            elif vizType == 'bar':
                Viz = MVLib.BMV.BarplotVisualizer(Viz.config_obj)
            elif vizType == 'scatter':
                Viz = MVLib.SMV.ScatterplotVisualizer(Viz.config_obj)
            elif vizType == 'geomap':
                Viz = MVLib.GMV.GeomapVisualizer(Viz.config_obj)
            elif vizType == 'network':
                Viz = MVLib.NMV.NetworkVisualizer(Viz.config_obj)
            elif vizType == 'ring':
                Viz = MVLib.RMV.RingVisualizer(Viz.config_obj)
            elif vizType == 'bipartite':
                Viz = MVLib.BpMV.BipartiteVisualizer(Viz.config_obj)
            elif vizType == 'candlestick':
                Viz = MVLib.CsMV.CandlestickVisualizer(Viz.config_obj)
            elif vizType == 'histogram':
                Viz = MVLib.HistMV.HistogramVisualizer(Viz.config_obj)
            elif vizType == 'kde':
                Viz = MVLib.KDEMV.KDEVisualizer(Viz.config_obj)
            else:
                print 'Unknown ModelVizualizer:', vizType
                return render_template('index.html')
                        
            # With the xml file parsed, we can now read the model data
            if not Viz.read_model_data():
                print 'Cannot load the model data!'
                return render_template('index.html')
                
            if not Viz.render_plot():
                print 'Cannot render plot!'
                return render_template('index.html')
                         
            return Viz.plot

    else:   
        return render_template('index.html')

# Debug function for test purposes
@sde_app.route('/buildnetwork/', methods=['POST', 'GET'])
@flask_login.login_required
def buildnetwork():
    return render_template('buildnetwork.html')
    
@sde_app.route('/debug_mode/', methods=['POST', 'GET'])
@flask_login.login_required
def debug_mode():
    if request.method == 'POST':
        param = {}
        param.update({'nNodes': eval(request.values['nNodes'])}) # Warning: not checking for valid input can crash  
        param.update({'minNodeSize': eval(request.values['minSize'])})
        param.update({'maxNodeSize': eval(request.values['maxSize'])})
        param.update({'nEdges': eval(request.values['nEdges'])})        
        param.update({'minEdgeStrength': eval(request.values['minStrength'])})
        param.update({'maxEdgeStrength': eval(request.values['maxStrength'])})
        param.update({'edgeTypes': request.values['edgeTypes'].split(',')})

        nodePosition = request.values['nodePosition']
        generateNodePos_server = True
        if nodePosition == 'client':
            generateNodePos_server = False
        
        conf_obj = None
        viz = MVLib.NMV.NetworkVisualizer(conf_obj)
        viz.debug_mode(param, generateNodePos_server)
        if not viz.render_plot():
            print 'Cannot render plot!'
            return render_template('index.html')        
        return viz.plot
    else:   
        return render_template('index.html')

# Define function to login users
@sde_app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
      return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    remember_me = False
    if remember_me in request.form:
        remember_me = True
    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None:
        flash('Username is invalid', 'error')
        return redirect(url_for('login'))
    if not registered_user.check_password(password):
        flash('Password is invalid', 'error')
        return redirect(url_for('login'))
    flask_login.login_user(registered_user, remember=remember_me)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))

@sde_app.route('/logout/', methods=['GET'])
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))

# Define user_loader_callback function.
# This function loads the user from the database
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
    # Note that IDs in Flask-Login are unicode strings,
    # need to typecast them to ints for sqlquery

@sde_app.before_request
def before_request():
    g.user = flask_login.current_user
    # Note:
    # The g object stores information for one request only and is available
    # from within each function.  Never store such things on other objects
    # because this would not work with threaded environments.

if __name__ == '__main__':
    sde_app.run(port=8000)
