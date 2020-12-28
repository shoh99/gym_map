import folium
import json
from shapely.geometry import shape, Point
from bs4 import BeautifulSoup
from folium.plugins import LocateControl, MarkerCluster


#  create map
MyMap = folium.Map(location=[40.129584, 67.835709], tiles='OpenStreetMap',
                   zoom_start=13.5, max_zoom=19, control_scale=True)


border_style = {'color': '#000000', 'weight': '1.5',
                'fillColor': '#58b5d1', 'fillOpacity': 1.0}

boundary = folium.GeoJson(open('./data/jizzax.json').read(),
                          name='Uzb', style_function=lambda x: border_style, overlay=False)
boundary.add_to(MyMap)

# create custom beer glass icon for map markers
gym_img = 'gym2.png'


# load json and create shaply geometry from it
with open('data/jizzax.json', 'r') as file:
    uzb_json = json.load(file)
uzb_boundary = shape(uzb_json['features'][0]['geometry'])

uzb_cluster = MarkerCluster(options={
    'showCoverageOnHover': False,
    'zoomToBoundsOnClick': True,
    'spiderfyOnMaxZoom': False,
    'disableClusteringAtZoom': 13
})


places = {

    'olymp_kachka': [(40.1092901, 67.8383707), 'https://vymaps.com/UZ/Olymo-Kacka-Club-1582/', 'https://vymaps.com/UZ/Olymo-Kacka-Club-1582/', 'https://goo.gl/maps/dv8QkaiRgiTV3Fz18'],

    'life_gym': [(40.112250, 67.855117), 'https://www.instagram.com/p/CJJuaLQFwuI/', 'https://www.instagram.com/life.fitness.gym.club/', 'https://goo.gl/maps/JV8XQ2Do5kPYuQuZ6'],

    'life_fitness': [(40.137166, 67.8241034), 'https://www.instagram.com/p/BxPcfAEnhwm/', 'https://www.instagram.com/life_fitness_jizzax/', 'https://goo.gl/maps/HR77stqxC3cxHEix7'],

    'total_fitness': [(40.1477442, 67.8156008), 'https://vymaps.com/UZ/Total-Fitness-1543/', 'https://vymaps.com/UZ/Total-Fitness-1543/', 'https://goo.gl/maps/ohXFBRWWWDuaxdmB7'],

    'olimp_fitness': [(40.164151, 67.837508), 'https://www.instagram.com/p/BHwKTJMjung/', 'https://goo.gl/maps/pMM7Q3mcYB4FaHzt9', 'https://goo.gl/maps/pMM7Q3mcYB4FaHzt9'],

    'urda': [(40.1541963, 67.8199567), 'http://urda.zn.uz/', 'http://urda.zn.uz/', 'https://goo.gl/maps/x99pQ937XkVA7uSv8'],
}

for gym, details in places.items():
    # define marker variable
    name = gym
    coordinates = details[0]
    insta_post = details[1]
    website = details[2]
    directions = details[3]

    custom_icon = folium.CustomIcon(
        gym_img, icon_size=(35, 35), popup_anchor=(0, -22))

    # define html inside marker pop-up
    pub_html = folium.Html(f"""<p style="text-align: center;"><b><span style="font-family: Didot, serif; font-size: 18px;">{name}</b></span></p>
    <p style="text-align: center;"><iframe src={insta_post}embed width="220" height="270" frameborder="0" scrolling="auto" allowtransparency="true"></iframe>
    <p style="text-align: center;"><a href={website} target="_blank" title="{name} Website"><span style="font-family: Didot, serif; font-size: 14px;">{name} Website</span></a></p>
    <p style="text-align: center;"><a href={directions} target="_blank" title="Directions to {name}"><span style="font-family: Didot, serif; font-size: 14px;">Directions to {name}</span></a></p>
    """, script=True)

    # Create pop-up with html content
    popup = folium.Popup(pub_html, max_width=700)
    # Create marker with custom icon and pop-up.
    custom_marker = folium.Marker(
        location=coordinates, icon=custom_icon, tooltip=name, popup=popup)

    # If pub is within Oxford boundary, add to Oxford marker cluster
    if uzb_boundary.contains(Point((coordinates[1], coordinates[0]))):
        custom_marker.add_to(uzb_cluster)
    else:
        # Else add marker to map
        custom_marker.add_to(MyMap)

# Add oxford cluster to the map
uzb_cluster.add_to(MyMap)

# Enable geolocation button on map.
LocateControl(auto_start=False).add_to(MyMap)

# Define webpage title html and add to script.
tab_title = """<title>Gyms location in Jihakh city</title>"""
MyMap.get_root().html.add_child(folium.Element(tab_title))

# Save map to HTML
MyMap.save('index.html')
