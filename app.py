from flask import Flask, render_template, send_from_directory
import folium
from geopy.geocoders import Nominatim
import json

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def dashboard():

    start_coords = (1.2935926, 103.7838815) #Currently is queenstown MRT
    end_coords = (1.2985751, 103.7874177)
    f_map = folium.Map(location=start_coords, zoom_start=16) #Shows map with location as queenstown MRT
    coords = [(1.2935926, 103.7838815), (1.2932914, 103.7839604), (1.2932082, 103.7839548), (1.2929286, 103.7839468), (1.2928673, 103.7841151), (1.2925721, 103.783987), (1.2923085, 103.7840427), (1.2922075, 103.7841775), (1.293021, 103.784993), (1.293272, 103.7852133), (1.2933356, 103.7852735), (1.2935367, 103.7854522), (1.2945734, 103.7858159), (1.2954668, 103.7857428), (1.2961, 103.7856915), (1.2969304, 103.785621), (1.2987699, 103.7853193), (1.2993846, 103.7854078), (1.2994958, 103.785436), (1.2994257, 103.7855463), (1.2992828, 103.7858048), (1.2990491, 103.7862876), (1.299014, 103.7863665), (1.2986761, 103.7871796), (1.2985751, 103.7874177)]
    f_map = folium.Map(location=start_coords, zoom_start=15)
    folium.Marker(location=start_coords, popup="<b>You are here!</b>" ).add_to(f_map)
    folium.Marker(location=end_coords, popup="<b>Destination</>", icon=folium.Icon(color="red")).add_to(f_map)
    # Creating a path based on the coords provided
    folium.PolyLine(coords, color="red", weight=3).add_to(f_map)
    
    return render_template("index.html", f_map=f_map._repr_html_())

# Convert coords to address
def getAddress(coords):
    geolocator = Nominatim(user_agent="my_request")
    address = geolocator.reverse(coords)
    return address


@app.route("/passengers")
def _():
    return send_from_directory("data", "passengers.json", as_attachment=False)

@app.route("/driversjson")
def __():
    return send_from_directory("data", "drivers.json", as_attachment=False)

@app.route("/stylesheet")
def ___():
    return send_from_directory("style", "stylesheet.css", as_attachment=False)

@app.route("/passengersDetailed")
def ____():
    #Convert json file to dict
    with open("./data/passengers.json") as json_file:
        passenger = json.load(json_file)

    with open("./data/nodes.json") as json_file:
        nodes = json.load(json_file)

    for i in range(len(passenger)):
        if(("toAddr" in passenger) and ("fromAddr" in passenger)):
            for j in range(len(nodes)):
                if (passenger[i]["passengerFromNode"] == nodes[j]["nodeId"]):
                    coords = (nodes[j]['latitude'],nodes[j]['longitude'])
                    address = getAddress(coords)
                    passenger[i].update({"fromAddr":address.address})
                if (passenger[i]["passengerToNode"] == nodes[j]["nodeId"]):
                    coords = (nodes[j]['latitude'],nodes[j]['longitude'])
                    address = getAddress(coords)
                    passenger[i].update({"toAddr":address.address})
                    
    out_file = open("./data/passengers.json", "w")
    json.dump(passenger, out_file)
    out_file.close()
    return send_from_directory("data", "passengers.json", as_attachment=False)


if __name__ == "__main__":
    app.run()





## PROBABLY REMOVED LATER ON


# @app.route("/testplot", methods=["GET", "POST"])
# @login_required
# def dashboard():
#     form = rideInput()
#     geolocator = Nominatim(user_agent="my_request")
#     # Display map after successful login
#     start_coords = (1.2946226, 103.8060366) #Currently is queenstown MRT
#     f_map = folium.Map(location=start_coords, zoom_start=16) #Shows map with location as queenstown MRT
#     # After user has submitted address info
#     if form.is_submitted:
#         if form.addressFrom.data and form.destination.data is not None:
#             # Geocode to convert address into coords
#             location = geolocator.geocode(form.addressFrom.data + ", Singapore")
#             start_coords = (location.latitude, location.longitude)
#             dest = geolocator.geocode(form.destination.data + ", Singapore")
#             end_coords = (dest.latitude, dest.longitude)

#             # Fit to and from on map
#             f_map.fit_bounds([start_coords, end_coords], padding=[15,15])
#             folium.Marker(location=start_coords, popup="<b>You are here!</b>" ).add_to(f_map)
#             folium.Marker(location=end_coords, popup="<b>Destination</b>", icon=folium.Icon(color="red") ).add_to(f_map)
#     #Coordinates for the path
#     # coords = [(1.2946226, 103.8060366), (1.29589,103.80513), (1.29679, 103.80449), (1.29747,103.80371), (1.29682,103.80314), (1.29632, 103.80348)]
#     # f_map = folium.Map(location=start_coords, zoom_start=15)
#     # folium.Marker(location=start_coords, popup="<b>You are here!</b>" ).add_to(f_map)
#     # folium.Marker(location=end_coords, popup="<b>Destination</>", icon=folium.Icon(color="red")).add_to(f_map)
#     # # Creating a path based on the coords provided
#     # folium.PolyLine(coords, color="red", weight=3).add_to(f_map)
#     return render_template("index.html",  f_map=f_map._repr_html_(), form=form)

