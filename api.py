# -*- coding: utf-8 -*-
"""
Factory Production Scheduler: Cutlery Polishing Scenario

API
"""

'''
project file imports
'''
import functions as f
from flask import Flask, send_file, make_response, render_template, request, redirect, url_for, abort
from flask_restful import Resource, Api
import os
from werkzeug.utils import secure_filename

'''
API
(hosted locally with Flask, typically on http://127.0.0.1:5000/)
(Warning: sometimes the browser saves the GET responses, so
refresh the browser at least one time if result is not the expected)

http://127.0.0.1:5000/schedule -> executes the main program and returns image of the schedule

http://127.0.0.1:5000/all_production_orders -> executes part of main program and returns
a dictionary with all orders in format
e.g. {day1:[[order 100],[order 101], etc.], day2:[[order 200],[order 201], etc.]}

http://127.0.0.1:5000/ -> index, has a menu that allows the see the loaded production
orders and has links to the above url's

(port number may be different if flask decides to use another one, please check terminal after running)
'''

app = Flask(__name__)
app = Flask(__name__, template_folder='template')
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 #max 1MB
app.config['UPLOAD_EXTENSIONS'] = ['.xlsx'] #only this type of excel
app.config['UPLOAD_PATH'] = 'production_orders' #destination folder
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0
api = Api(app)

@app.route('/')
def index():
    '''
    displays main menu (in html) with options:
        upload files
        check uploaded files
        refresh uploaded files (if nedeed, typically is dynamic)
        navigate to other features (scheduler and all_production_orders)
    '''
    return render_template('index.html',list_orders=os.listdir("production_orders/"))

class scheduler(Resource):
    def get(self):
        '''
        executes main program upon GET /schedule request
        returns .png of the schedule
        if there are no production orders, display a error message
        '''
        if len(os.listdir("production_orders/")) == 0:
            return 'There are no production orders uploaded.'
        production_buffer = []
        production_working_hours = 24*60*60 #(86400 seconds)
        production_schedule = {}
        f.load_all_production_order_into_production_buffer(production_buffer)
        production_buffer = f.scheduler_organizer(production_buffer)
        production_buffer = f.add_setup_times(production_buffer)
        production_buffer = f.add_maintenance_times_cutlerypolishing(production_buffer, 'Standard')
        production_time = f.total_production_buffer(production_buffer)
        production_schedule = f.production_scheduler(production_buffer, production_working_hours)
        f.plot_production_schedule(production_time,production_buffer,production_schedule)
        return make_response(send_file(r'schedule\schedule.png',mimetype='image/png', cache_timeout=0),200) #OK Code
    pass

class all_production_orders(Resource):
    def get(self):
        '''
        executes main program (except plot) upon GET /all_production_orders request
        returns dictionary {int:list[list]} 
        e.g. {day1:[[order 100],[order 101], etc.], day2:[[order 200],[order 201], etc.]}
        if there are no production orders, display a error message
        '''
        if len(os.listdir("production_orders/")) == 0:
            return 'There are no production orders uploaded.'
        production_buffer = []
        production_working_hours = 24*60*60 #(86400 seconds)
        production_schedule = {}
        f.load_all_production_order_into_production_buffer(production_buffer)
        production_buffer = f.scheduler_organizer(production_buffer)
        production_buffer = f.add_setup_times(production_buffer)
        production_buffer = f.add_maintenance_times_cutlerypolishing(production_buffer, 'Standard')
        production_schedule = f.production_scheduler(production_buffer, production_working_hours)
        return production_schedule
    pass

@app.route('/', methods=['POST'])
def upload_files():
    '''
    handles POST for file uploading
    check if the production order has the correct extension
    '''
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return 'File extension not supported'
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('index'))

api.add_resource(scheduler,'/schedule')
api.add_resource(all_production_orders,'/all_production_orders')

if __name__ == '__main__':
    app.run() #run flask