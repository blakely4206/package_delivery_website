import os
from datetime import datetime
from flask import Flask, session, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from graph import Graph
from graph import Vertex
from package import Package
from truck import Truck

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

package_list = {}
location_list = []
the_graph = Graph()
time = [8,0]
total_mileage = 0
trucks = [Truck(1), Truck(2)]
HUB = 0

def load_dists():
    weights_list = []
    fo = open("distances.txt")

    while True:
        line = fo.readline()
        if (line.count("*") == 1):
            break
        distances = line.split("|")
        weights_list.append(distances)
    fo.close()

    number_of_verts = len(weights_list)
    the_graph.load_graph(number_of_verts)

    for i in range(number_of_verts):
        for j in range(number_of_verts):
            the_graph.insert_edge(the_graph.return_vertex(i), the_graph.return_vertex(j), float(weights_list[i][j]))

    fo = open("addresses.txt")

    while True:
        line = fo.readline()
        if(line.count("+") == 1):
            break
        location_list.append(line.replace("\n", ""))
    fo.close()

def get_loc_id(package: Package):
    address = "%s|%s|%s|%s" % (package.address, package.city, package.state, package.zip)
    package.location_id = location_list.index(address)
    return package.location_id

def load_packages():
    fo = open("packagelist.txt")

    while True:
        line = fo.readline()
        if ("" == line):
            fo.close()
            break

        package_info = line.split("|")
        the_package = Package(package_info[0],package_info[1],package_info[2],package_info[3],package_info[4],package_info[5],package_info[6],"At HUB")
        the_package.location_id = get_loc_id(the_package)
        package_list[the_package.ID] = the_package
    for x in package_list:
        print(str(package_list.get(x)))
        
load_dists()
load_packages()

@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")
    
#@app.route("/channel/<string:room>", methods=["GET", "POST"])
#def channel_view(room):
##    session["current_channel"] = room
#    this_chat_log = chat_rooms[room]
#   return render_template("channel.html", user_id = session["user_id"], room=room, chat_log = this_chat_log, chat_rooms = chat_rooms)

@app.route("/run_delivery", methods=["GET", "POST"])
def run_delivery():
    return render_template("run_delivery.html")

@app.route("/show_cargo", methods=["GET", "POST"])
def show_cargo():
    return render_template("show_cargo.html")

@app.route("/lookup_package", methods=["GET", "POST"])
def lookup_package():
    return render_template("lookup_package.html")

@app.route("/list_packages", methods=["GET", "POST"])
def list_packages():
    return render_template("list_packages.html", packages=list(package_list.values()))

@app.route("/load_trucks", methods=["GET", "POST"])
def load_trucks():
    return render_template("load_trucks.html")
    
#@socketio.on("submit")
#def reply(data, room):
#    message = session['user_id'] + " (" + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ")::   " + data;
#
 #   emit("send reply", message, broadcast=True)


