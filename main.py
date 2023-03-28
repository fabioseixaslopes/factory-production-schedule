# -*- coding: utf-8 -*-
"""
Factory Production Scheduler: Cutlery Polishing Scenario

main file
"""

'''
project file imports
'''
import functions as f

'''
variables
'''
production_buffer = []
production_working_hours = 24*60*60 #(86400 seconds)
production_schedule = {}

'''
tests
'''
#f.tests()

'''
main program
'''
## checks if there are production order files in the "production_orders" folder
f.check_production_orders() #exits program if there are none

## load all orders from the production_orders folder
f.load_all_production_order_into_production_buffer(production_buffer)
#print(production_buffer)

## organize by priority (very urgent, urgent, normal, not urgent)
## and type of product (to avoid lengthier setup times)
production_buffer = f.scheduler_organizer(production_buffer)
#print(production_buffer)

## fit into a production schedule (considering production, maintenance and setup times)
## add machine setup times to buffer
production_buffer = f.add_setup_times(production_buffer)
#print(production_buffer)

## add machine maintenance times to buffer
production_buffer = f.add_maintenance_times_cutlerypolishing(production_buffer, 'Standard')

## save total production time
production_time = f.total_production_buffer(production_buffer)
#print(production_time)

## will create a dictionary where the key is the day number and the value is a list with the orders for that day
## e.g. {day1:[[order 100],[order 123], etc.], day2:[[order 301],[order 643], etc.]}
production_schedule = f.production_scheduler(production_buffer, production_working_hours)
#print(production_schedule)
#for day in production_schedule:
#    for order in production_schedule[day]:
#        print(order)

## plot the production schedule and saves it to (root)/schedule/schedule.png
f.plot_production_schedule(production_time,production_buffer,production_schedule)