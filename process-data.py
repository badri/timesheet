# processing.py
import time
import calendar
 
f = open('op')
time_clocked = 0
idle_time = 0
app_dict = {}
html_part = ''
js_graph1 = ''
js_graph2 = ''
 
time_display = ''
 
def convert_to_hrs_and_mins(secs):
    hrs = secs/3600
    mins = 0
    rem = secs%3600
    if rem > 60:
        mins = rem/60
    return (hrs, mins)
 
js_graph1 += "["
for each_line in f.readlines():
    timestamp, application = each_line.split('|')
    # print timestamp.strip()
    y = calendar.timegm(time.strptime(timestamp.strip(), "%a, %d %b %Y %H:%M:%S"))*1000
    application = application.strip()
    if application:
        time_clocked+=10
        app_dict[application] = app_dict.get(application, 0) + 1
        js_graph1 += "[" + str(y) + ", 1],"
    else:
        idle_time+=10
        js_graph1 += "null,"
 
#js_graph1[-1] = "]"
 
time_clocked_hrs, time_clocked_mins = convert_to_hrs_and_mins(time_clocked)
idle_time_hrs, idle_time_mins = convert_to_hrs_and_mins(idle_time)
 
time_display += '<p>Effective time clocked: <b> %d </b> hours, <b> %d </b> minutes</p>' % (time_clocked_hrs, time_clocked_mins)
time_display += '<p>Idle time: <b> %d </b> hours, <b> %d </b> minutes</p>' % (idle_time_hrs, idle_time_mins)
 
from operator import itemgetter
app_dict = sorted(app_dict.items(), key=itemgetter(1))
 
 
js_graph2 += "["
for i,v in enumerate(reversed(app_dict)):    
    pc = float((float(v[1])*float(10)/float(time_clocked))*float(100))
    if round(pc) > 1:
        html_part += "<p>" + str(i+1) + " - " + v[0] + "</p>"
        js_graph2 += "[" + str(i+1) + "," + str(round(pc)) + "],"
 
#js_graph2[-1] = "]"
print html_part
print js_graph1
print js_graph2
print time_display
