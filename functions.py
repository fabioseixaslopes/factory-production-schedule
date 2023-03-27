# -*- coding: utf-8 -*-
"""
@author: Fabio A. Seixas-Lopes
@email: fl@uninova.pt

Python Course Doctoral School final project
Factory Production Scheduler: Cutlery Polishing Scenario

functions file
WARNING:
    some functions were discontinued during the development.
    they were kept so they can be used later if needed.
"""

'''
imports
'''
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import math
import sys

'''
global variables
'''
file_product_info = 'product_info.xlsx'
folder_production_orders = "production_orders/"

'''
functions
'''
def check_production_orders():
    '''
    checks if there are production order files in the "production_orders" folder
    #exits program if there are none
    '''
    if len(os.listdir("production_orders/")) == 0:
        print('There are no production orders in the "production_orders" folder.')
        sys.exit()

def get_product_table():
    '''
    reads products table into a dataframe
    '''
    return pd.read_excel(file_product_info,
                         index_col=0,
                         sheet_name='Products')

def get_quantity_per_cycle_table():
    '''
    reads quantity per cycle table into a dataframe
    '''
    return pd.read_excel(file_product_info,
                         index_col=1,
                         sheet_name='QuantityPerCycle')

def get_cycles_duration_per_quality_table():
    '''
    reads cycles per quality table into a dataframe
    '''
    return pd.read_excel(file_product_info,
                         index_col=0,
                         sheet_name='CyclesPerQuality')

def get_parts_per_hour_table():
    '''
    reads parts per hour table into a dataframe
    '''
    return pd.read_excel(file_product_info,
                         index_col=0,
                         header=1,
                         sheet_name='PartsPerHour')

def get_setup_time_table(table_index):
    '''
    reads setup time table into a dataframe
    '''
    return pd.read_excel(file_product_info,
                         index_col=table_index,
                         sheet_name='SetupTime')

def get_maintenance_time_table():
    '''
    reads maintenance time table into a dataframe
    '''
    return pd.read_excel(file_product_info,
                         index_col=0,
                         sheet_name='MaintenanceTime')

def get_machines_table():
    '''
    reads machines table into a dataframe
    '''
    return pd.read_excel(file_product_info,
                         index_col=0,
                         sheet_name='Machines')

def get_working_hours_table():
    '''
    reads working hours table into a dataframe
    '''
    return pd.read_excel(file_product_info,
                         index_col=0,
                         sheet_name='WorkingHours')

def get_priorities_table():
    '''
    reads priorities table into a dataframe
    '''
    return pd.read_excel(file_product_info,
                         index_col=0,
                         sheet_name='Priorities')

def get_production_order(filename):
    '''
    reads a production order into a dataframe
    '''
    return pd.read_excel(r'production_orders/' + filename + ".xlsx",
                         index_col=0)

def get_product_info(product_reference):
    '''
    returns data from product in products table
    '''
    return get_product_table().loc[product_reference]

def get_product_designation(product_reference):
    '''
    returns the designation field from product in products table
    '''
    return get_product_table().loc[product_reference,'Designation']

def get_product_type(product_reference):
    '''
    returns the type field from product in products table
    '''
    return get_product_table().loc[product_reference,'Type']

def get_product_quality(product_reference):
    '''
    returns the quality field from product in products table
    '''
    return get_product_table().loc[product_reference,'Quality']

def get_product_polishing_rate(product_reference):
    '''
    returns the polishing rate field from product in products table
    '''
    return get_product_table().loc[product_reference,'Polishing [parts/h]']

def get_type_quantity_per_cycle(product_type):
    '''
    returns the quantity field from type in quantity per cycle table
    '''
    return get_quantity_per_cycle_table().loc[product_type,'Quantity']

def get_cycles_duration_per_quality(product_quality):
    '''
    returns the cycle duration from quality in cycles per quality table
    '''
    return get_cycles_duration_per_quality_table().loc[product_quality,'Cycle Duration (seconds)']

def get_machine_setup_codes(machine_type):
    '''
    returns a list of setup codes from a certain machine type in the setup time table
    '''
    return list(get_setup_time_table(0).loc[machine_type,'Code'])

def get_setup_time(setup_code):
    '''
    returns setup time with a setup code from the setup time table
    '''
    return get_setup_time_table(2).loc[setup_code,'Time (minutes)']

def get_maintenance_duration(machine_type,maintenance_type):
    '''
    returns maintenance duration from a machine type of the maintenance time table
    '''
    return get_maintenance_time_table().loc[get_maintenance_time_table()['Maintenance Type']==maintenance_type,['Duration (minutes)']].iloc[0,0]

def get_maintenance_max_time(machine_type,maintenance_type):
    '''
    returns maintenance maximum time from a machine type of the maintenance time table
    '''
    return get_maintenance_time_table().loc[get_maintenance_time_table()['Maintenance Type']==maintenance_type,['Maximum Time (minutes)']].iloc[0,0]

def get_working_hours_start_time(schedule):
    '''
    returns working hours start time from a schedule in working hours table
    '''
    return get_working_hours_table().loc[schedule,'Start']

def get_working_hours_end_time(schedule):
    '''
    returns working hours end time from a schedule in working hours table
    '''
    return get_working_hours_table().loc[schedule,'End']

def get_working_hours_duration(schedule):
    '''
    returns working hours duration from a schedule in working hours table
    '''
    return get_working_hours_table().loc[schedule,'Duration (hours)']

def get_priority_value(priority):
    '''
    returns a priority value from the priorities table (higher value, higher priority)
    '''    
    return get_priorities_table().loc[priority,'Priority Value']

def calculate_product_polishing_rate(product_reference):
    '''
    returns a product's polishing rate from a product reference
    '''   
    return get_type_quantity_per_cycle(get_product_type(product_reference))*3600/get_cycles_duration_per_quality(get_product_quality(product_reference))

def calculate_production_time(product_reference, parts):
    '''
    returns production time of a product (considering how many parts are needed)
    '''   
    return parts/get_product_polishing_rate(product_reference)

def get_production_order_number_items(filename):
    '''
    returns number of items in a production order table/file
    ''' 
    return len(get_production_order(filename).index)

def get_production_order_item_id(filename,index):
    '''
    returns a order id from a production order table/file
    ''' 
    return get_production_order(filename).iloc[index].name

def get_production_order_item_reference(filename,product_id):
    '''
    returns a reference field from an order id in a production order table/file
    ''' 
    return get_production_order(filename).loc[product_id,'Reference']

def get_production_order_item_quantity(filename,product_id):
    '''
    returns a quantity field from an order id in a production order table/file
    ''' 
    return get_production_order(filename).loc[product_id,'Quantity']

def get_production_order_item_service(filename,product_id):
    '''
    returns a service field from an order id in a production order table/file
    ''' 
    return get_production_order(filename).loc[product_id,'Service']

def get_production_order_item_priority(filename,product_id):
    '''
    returns a priority field from an order id in a production order table/file
    ''' 
    return get_production_order(filename).loc[product_id,'Priority']

def load_production_order_into_production_buffer(filename, production_buffer):
    '''
    loads/appends a production order file into a production buffer list of lists
    np.asscalar is used on integer's due to data formats required to handle API process
    ''' 
    for item in range(get_production_order_number_items(filename)):
        list_to_append = []
        product_id = get_production_order_item_id(filename,item)
        list_to_append.append(np.asscalar(product_id))
        list_to_append.append(get_production_order_item_reference(filename, product_id))
        #below, an extra field is added to encompass type of product, to later sort lists
        list_to_append.append(get_product_type(get_production_order_item_reference(filename, product_id)))
        list_to_append.append(np.asscalar(get_production_order_item_quantity(filename, product_id)))
        list_to_append.append(get_production_order_item_service(filename, product_id))
        #below field is converted to integer to later sort lists
        list_to_append.append(np.asscalar(get_priority_value(get_production_order_item_priority(filename, product_id))))
        #below the production time is added to later compute schedule (in seconds)
        list_to_append.append(round(calculate_production_time(get_production_order_item_reference(filename, product_id),
                                                        get_production_order_item_quantity(filename, product_id))*3600))
        production_buffer.append(list_to_append)
        
def load_all_production_order_into_production_buffer(production_buffer):
    '''
    loads/appends all production order files (inside specific folder) into a production buffer list of lists
    ''' 
    for file in os.listdir(folder_production_orders):
        filename = file[:-5:] #removing file extension
        #print(filename)
        load_production_order_into_production_buffer(filename, production_buffer)
        
def production_buffer_to_production_buffer_dataframe(production_buffer):
    '''
    converts a production buffer list of lists into a production buffer dataframe
    ''' 
    df_production_buffer = pd.DataFrame(production_buffer,columns = ['ID','Reference','Type','Quantity','Service','Priority','ProductionTime'])
    df_production_buffer.set_index('ID',inplace=True)
    return df_production_buffer
    
def pbd_product_order_id(pbd,index):
    '''
    pbd -> production buffer dataframe
    returns order ID from index in pbd
    '''
    return pbd.iloc[index].name

def pbd_product_order_reference(pbd,order_id):
    '''
    returns order reference from product order id in pbd
    '''
    return pbd.loc[order_id,'Reference']

def pbd_product_order_quantity(pbd,order_id):
    '''
    returns order quantity from product order id in pbd
    '''
    return pbd.loc[order_id,'Quantity']
    
def pbd_product_order_service(pbd,order_id):
    '''
    returns order service from product order id in pbd
    '''
    return pbd.loc[order_id,'Service']

def pbd_product_order_priority(pbd,order_id):
    '''
    returns order priority from product order id in pbd
    '''
    return pbd.loc[order_id,'Priority']

def delete_item_from_production_buffer(production_buffer, order_id):
    '''
    deletes an order (list) from the production buffer list of lists
    ''' 
    for order in production_buffer:
        if(order[0]==order_id):
            production_buffer.remove(order)
            
def compare_types_for_setup_times_order(prev_type, curr_type):
    '''
    returns setup order to insert into production buffer
    '''
    if prev_type == curr_type:
        return [0,'CP_==','Setup',0,'Cutlery Polishing',3,15*60]
    else:
        return [0,'CP_!=','Setup',0,'Cutlery Polishing',3,90*60]

def add_setup_times(production_buffer):
    '''
    inserts setup times into production buffer based on type of product
    '''
    previous_order = None
    production_buffer_new = []
    production_buffer_new.append([0,'CP_!=','Setup',0,'Cutlery Polishing',3,90*60])
    for order in production_buffer:
        if previous_order != None:
            production_buffer_new.append(compare_types_for_setup_times_order(previous_order[2],order[2]))
        production_buffer_new.append(order)
        previous_order = order.copy() 
    return production_buffer_new

def add_maintenance_times_cutlerypolishing(production_buffer, maintenance_type):
    '''
    inserts maintenance times into production buffer,
    ignores setup times
    '''
    machine_type = 'Cutlery Polishing'
    maintenance_max_time = np.asscalar(get_maintenance_max_time(machine_type,maintenance_type)*60)
    maintenance_duration = np.asscalar(get_maintenance_duration(machine_type,maintenance_type)*60)
    seconds_working = 0
    maintenance_made = 1
    production_buffer_new = []
    for order in production_buffer:
        if order[0] > 9: #ignore previous setup and maintenance times, and other special work
            seconds_working += order[6]
        if seconds_working > (maintenance_made * maintenance_max_time):
            maintenance_made += 1
            production_buffer_new.append([1,maintenance_type,'Maintenance',0,'Cutlery Polishing',3,maintenance_duration])
        production_buffer_new.append(order)
    return production_buffer_new
    
def scheduler_organizer(production_buffer):
    '''
    scheduler organizer, a bit simplified for now...
    lists organized by priority and type of product (to avoid lengthier setup times)
    '''
    production_buffer = sorted(production_buffer, key=lambda x: x[2], reverse=True)
    production_buffer = sorted(production_buffer, key=lambda x: x[5], reverse=True)
    return production_buffer

def total_production_buffer(production_buffer):
    '''
    returns the total production time left in the production_buffer
    '''
    total_time = 0
    for order in production_buffer:
        total_time += order[6]
    return total_time

def list_of_order_ids_production_buffer(production_buffer):
    '''
    returns a list with the order id's in the production_buffer
    removes duplicates and maintains order, to plot from up to down
    '''
    list_to_append = []
    list_to_append = ['Setup', 'Maintenance'] # for visualization purposes
    for order in production_buffer:
        if order[0] == 0:
            list_to_append.append('Setup') #redundant
        elif order[0] == 1:
            list_to_append.append('Maintenance') #redundant    
        else:
            list_to_append.append("Order " + str(order[0]))
    return list(dict.fromkeys(list_to_append))[::-1]

def number_orders_production_buffer_filtered(production_buffer):
    '''
    returns the total number of order in the buffer, ignoring repeated maintenance and setup times
    '''
    total_orders = 0
    for order in production_buffer:
        if order[0] > 9:
            total_orders += 1
    return total_orders + 2 #adds a single entry for maintenance and other for setup

def priority_color(priority):
    if priority == 3:
        return 'tab:red'
    if priority == 2:
        return 'tab:orange'
    if priority == 1:
        return 'tab:green'
    if priority == 0:
        return 'tab:blue'

def production_scheduler(production_buffer, production_working_hours):
    '''
    fit into a production schedule (considering production and setup times), 
    adds machine setup times to buffer and creates a dictionary where the key
    is the day number and the value is a list with the orders for that day
    '''
    production_schedule = {}
    day = 0
    while (total_production_buffer(production_buffer)) > 0: #while there are orders with time in the buffet
        day += 1 #increments the day
        seconds_spent = 0
        list_to_append = []
        for order in production_buffer:
            seconds_spent += order[6] #adds time spent to do this order
            if seconds_spent <= production_working_hours: #if all fits in the day, put 0 in the buffer
                if order[6] > 0:
                    list_to_append.append(order.copy()) #puts order object in current day
                order[6]=0
            if seconds_spent > production_working_hours: #if it does not fit, break to another day, leave remaining time in the buffer for the next day
                order[6] -= seconds_spent-production_working_hours # this is to append only the part of the order done in the current day
                list_to_append.append(order.copy())
                order[6] = seconds_spent-production_working_hours #remaining time stays in the list for the next day
                break
        production_schedule[day] = list_to_append
    return production_schedule

def plot_production_schedule(production_time,production_buffer,production_schedule):
    '''
    plot a visual representation of the schedule for the polishing machine orders
    with setup, maintenance times on top, then the orders (colored by priority)
    and in order of completion.
    it also saves a figure of the plot on a specific folder within the root of the program
    (root)/schedule
    '''
    # change style
    plt.style.use('ggplot')
    # Declaring a figure "gnt"
    fig, gnt = plt.subplots()
    # Setting X-axis limits
    gnt.set_xlim(0, int(math.ceil(production_time/60/60)))
    # Setting Y-axis limits
    gnt.set_ylim(-1, number_orders_production_buffer_filtered(production_buffer))
    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('Time (hours)')
    gnt.set_ylabel('Polishing Machine Orders')
    # Setting graph attribute
    gnt.grid(True)
    # Setting ticks on y-axis
    gnt.set_yticks([x for x in range(0,number_orders_production_buffer_filtered(production_buffer))])
    # set x ticks spacing
    plt.xticks(np.arange(0, int(math.ceil(production_time/60/60)), 3))
    # Labelling tickes of y-axis
    gnt.set_yticklabels(list_of_order_ids_production_buffer(production_buffer))
    # Adjust Spacing of labels in y-axis and x-axis (this is problematic in matplotlib, occurs
    # overlapping of label on both axis when the number of labels is more than a few)
    ## the values for adjustment were experimented, the correct label visibility is not guaranteed
    ## when considering a lot of orders. but for the context of this program (3 to 5 production orders at once)
    ## these values/factors for adjustment were calculated and vary based on the number of orders
    plt.subplots_adjust(bottom=number_orders_production_buffer_filtered(production_buffer)/-45) 
    #60 orders/ -45 factor ~= -1.33 "adjustment"
    plt.subplots_adjust(right=int(math.ceil(production_time/60/60))/43)
    #same as above, but for time (x-axis) and with a factor of 43
    # Declaring bars in schedule
    start_time = 0
    y_position = number_orders_production_buffer_filtered(production_buffer)-2.5
    y_position_for_setup = number_orders_production_buffer_filtered(production_buffer)-1.5
    y_position_for_maintenance = number_orders_production_buffer_filtered(production_buffer)-2.5
    height = 1
    for day in production_schedule:
        for order in production_schedule[day]:
            start_time = round(start_time,5)
            #if it's a setup
            if order[0] == 0:
                duration = round(order[6]/60/60,5)
                gnt.broken_barh([(start_time, duration)], (y_position_for_setup, height), facecolors =('tab:cyan'))
                start_time = round(start_time + duration,5)
                previous_order = order.copy()
                continue
            #if it's a maintenance
            if order[0] == 1:
                duration = round(order[6]/60/60,5)
                gnt.broken_barh([(start_time, duration)], (y_position_for_maintenance, height), facecolors =('tab:purple'))
                start_time = round(start_time + duration,5)
                previous_order = order.copy()
                continue
            #if it's a regular order
            if order[0] != previous_order[0]:
                y_position -= 1
            duration = round(order[6]/60/60,5)
            '''gnt.broken_barh([(start_time, duration)],
                 (lower_yaxis, height),
                facecolors=('tab:colours'))'''
            gnt.broken_barh([(start_time, duration)], (y_position, height), facecolors =(priority_color(order[5])))
            start_time = round(start_time + duration,5)
            previous_order = order.copy()
    plt.savefig('schedule/schedule.png',bbox_inches='tight')
    plt.show()
            
def tests():
    '''
    executes various tests (used for development)
    '''
    print(get_product_table())
    print(get_product_info('PP-7310'))
    print(calculate_product_polishing_rate('PP-10005')) 
    print(get_product_designation('PP-7310'))
    print(get_product_type('PP-7310')) 
    print(get_product_quality('PP-7310')) 
    print(get_product_polishing_rate('PP-7310'))
    print(get_quantity_per_cycle_table())
    print(get_type_quantity_per_cycle('Rice Spoon'))
    print(get_cycles_duration_per_quality_table())
    print(get_cycles_duration_per_quality('Standard'))
    print(calculate_production_time('PP-10002',6000))
    print(get_parts_per_hour_table())
    print(get_setup_time_table(0))
    print(get_machine_setup_codes('Cutlery Polishing'))
    print(get_setup_time('CC_**'))
    print(get_maintenance_time_table())
    print(get_maintenance_duration('Cutlery Polishing', 'Old Model'))
    print(get_maintenance_max_time('Cutlery Polishing', 'Standard'))
    print(get_machines_table())
    print(get_working_hours_table())
    print(get_working_hours_start_time('Full Day'))
    print(get_working_hours_end_time('Full Day'))
    print(get_working_hours_duration('Full Day'))
    print(get_priorities_table())
    print(get_priority_value('Urgent'))
    
    print(get_production_order('6'))
    print(get_production_order('21'))
    print(get_production_order_number_items('6'))
    print(get_production_order_item_id('6',1))
    print(get_production_order_item_reference('6', 605))
    print(get_production_order_item_quantity('6', 605))
    print(get_production_order_item_service('6', 605))
    print(get_production_order_item_priority('6', 605))
    print(get_priority_value(get_production_order_item_priority('6', 615)))
    
    production_buffer = []
    print(production_buffer)
    load_production_order_into_production_buffer('6', production_buffer)
    load_production_order_into_production_buffer('21', production_buffer)
    print(production_buffer)
    
    pbd = production_buffer_to_production_buffer_dataframe(production_buffer)
    print(pbd)
    print(pbd.loc[2115,'Reference'])
    print(pbd.iloc[29,0])
    print(pbd_product_order_id(pbd, 0))
    print(pbd_product_order_reference(pbd, 601))
    print(pbd_product_order_quantity(pbd, 601))
    print(pbd_product_order_service(pbd, 601))
    print(pbd_product_order_priority(pbd, 601))
    
    print(production_buffer)
    delete_item_from_production_buffer(production_buffer,601)
    delete_item_from_production_buffer(production_buffer,602)
    print(production_buffer)
    
    print(folder_production_orders)
    production_buffer = []
    load_all_production_order_into_production_buffer(production_buffer)
    print(production_buffer)
    
    production_buffer = sorted(production_buffer, key=lambda x: x[5], reverse=True)
    print(production_buffer)