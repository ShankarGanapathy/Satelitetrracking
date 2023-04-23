import sys
import tkinter
import tkinter.messagebox
from tkintermapview import TkinterMapView
import geocoder
from geopy.geocoders import Nominatim
import datetime as dt


class App(tkinter.Tk):

    APP_NAME = " Satellite orbits"
    WIDTH = 800
    HEIGHT = 750
    # Below is the sample data used off the REST call made 
    # https://api.n2yo.com/rest/v1/satellite/positions/25544/41.702/-76.014/ {} / {} /&apiKey=589P8Q-SDRYX8-L842ZD-5Z9
    positions = [ 
        {
            "satlatitude": 48.93831553,
            "satlongitude": 32.20823369,
            "sataltitude": 423.48,
            "azimuth": 41.74,
            "elevation": -32.18,
            "ra": 42.47092063,
            "dec": 6.65551562,
            "timestamp": 1682065020,
            "eclipsed": False
        },
        {
            "satlatitude": 48.91655743,
            "satlongitude": 32.29639533,
            "sataltitude": 423.47,
            "azimuth": 41.72,
            "elevation": -32.21,
            "ra": 42.50814991,
            "dec": 6.63768375,
            "timestamp": 1682065021,
            "eclipsed": False
        },
        {
            "satlatitude": 48.89472547,
            "satlongitude": 32.3844769,
            "sataltitude": 423.46,
            "azimuth": 41.7,
            "elevation": -32.24,
            "ra": 42.54534878,
            "dec": 6.61983002,
            "timestamp": 1682065022,
            "eclipsed": False
        },
        {
            "satlatitude": 48.87281887,
            "satlongitude": 32.4724818,
            "sataltitude": 423.45,
            "azimuth": 41.68,
            "elevation": -32.27,
            "ra": 42.58251879,
            "dec": 6.60195376,
            "timestamp": 1682065023,
            "eclipsed": False
        },
        {
            "satlatitude": 48.85083954,
            "satlongitude": 32.5604028,
            "sataltitude": 423.44,
            "azimuth": 41.65,
            "elevation": -32.3,
            "ra": 42.61965701,
            "dec": 6.58405647,
            "timestamp": 1682065024,
            "eclipsed": False
        },
        {
            "satlatitude": 48.82878669,
            "satlongitude": 32.64824333,
            "sataltitude": 423.43,
            "azimuth": 41.63,
            "elevation": -32.34,
            "ra": 42.65676499,
            "dec": 6.5661375,
            "timestamp": 1682065025,
            "eclipsed": False
        },
        {
            "satlatitude": 48.80666046,
            "satlongitude": 32.73600323,
            "sataltitude": 423.42,
            "azimuth": 41.61,
            "elevation": -32.37,
            "ra": 42.6938428,
            "dec": 6.54819689,
            "timestamp": 1682065026,
            "eclipsed": False
        },
        {
            "satlatitude": 48.78446096,
            "satlongitude": 32.82368238,
            "sataltitude": 423.41,
            "azimuth": 41.58,
            "elevation": -32.4,
            "ra": 42.73089049,
            "dec": 6.53023472,
            "timestamp": 1682065027,
            "eclipsed": False
        },
        {
            "satlatitude": 48.76218832,
            "satlongitude": 32.91128064,
            "sataltitude": 423.41,
            "azimuth": 41.56,
            "elevation": -32.43,
            "ra": 42.76790814,
            "dec": 6.51225103,
            "timestamp": 1682065028,
            "eclipsed": False
        },
        {
            "satlatitude": 48.73984265,
            "satlongitude": 32.99879788,
            "sataltitude": 423.4,
            "azimuth": 41.54,
            "elevation": -32.46,
            "ra": 42.8048958,
            "dec": 6.49424589,
            "timestamp": 1682065029,
            "eclipsed": False
        }
    ]
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Return>", self.search)

        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        self.search_bar = tkinter.Entry(self, width=50) # Here we can give input in terms of ( 40.714, -74.006) latitude, longitude
        self.search_bar.grid(row=0, column=0, pady=10, padx=10, sticky="we")
        self.search_bar.focus()

        self.search_bar_button = tkinter.Button(
            master=self, width=8, text="Search", command=self.search)
        self.search_bar_button.grid(row=0, column=1, pady=10, padx=10)

        self.search_bar_clear = tkinter.Button(
            master=self, width=8, text="Clear", command=self.clear)
        self.search_bar_clear.grid(row=0, column=2, pady=10, padx=10)

        self.map_widget = TkinterMapView(
            width=self.WIDTH, height=600, corner_radius=0)
        self.map_widget.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.marker_list_box = tkinter.Listbox(self, height=8)
        self.marker_list_box.grid(row=2, column=0, columnspan=1, sticky="ew", padx=10, pady=10)

        self.listbox_button_frame = tkinter.Frame(master=self)
        self.listbox_button_frame.grid(
            row=2, column=1, sticky="nsew", columnspan=2)

        self.listbox_button_frame.grid_columnconfigure(0, weight=1)

        # self.show_satellite_marker_button = tkinter.Button(master=self.listbox_button_frame, width=20, text="get satellite coordinates",
        #                                             command=self.get_satellite_coordinates)
        # self.show_satellite_marker_button.grid(row=2, column=0, pady=10, padx=10)

        self.save_marker_button = tkinter.Button(master=self.listbox_button_frame, width=20, text="save current marker",
                                                 command=self.save_marker)
        self.save_marker_button.grid(row=0, column=0, pady=10, padx=10)

        self.clear_marker_button = tkinter.Button(master=self.listbox_button_frame, width=20, text="get satellite coordinates",
                                                  command=self.get_satellite_coordinates)
        self.clear_marker_button.grid(row=1, column=0, pady=10, padx=10)

        self.connect_marker_button = tkinter.Button(master=self.listbox_button_frame, width=20, text="connect marker with path",
                                                    command=self.connect_marker)
        self.connect_marker_button.grid(row=2, column=0, pady=10, padx=10)

        # This is the default addresss that the map would show
        self.map_widget.set_address("Jammu, India")

        self.marker_list = []
        self.marker_path = None

        self.search_marker = None
        self.search_in_progress = False

    def search(self, event=None):
        if not self.search_in_progress:   # IF search is not in progress then enters IF loop
            self.search_in_progress = True
            if self.search_marker not in self.marker_list:
                self.map_widget.delete(self.search_marker)

            # getting the location entered in the search bar
            address = self.search_bar.get()
            # print("***** Printing the type of the address {}".format(type(address))) # This is always string

            # print( geocoder.osm(address).latlng)
            # print( type( geocoder.osm(address).latlng) )
            latitude = geocoder.osm(address).latlng[0]
            longitude = geocoder.osm(address).latlng[1]

            print( "*********   Printing input {} \t latitude and longitude  {} {}".format(address, latitude, longitude ) )
            latlong = str( str(latitude)+ " " +str(longitude) )

#########################################
 # Plotting for satellite positions
            # for i in self.positions:
            #     latitude = (i.get('satlatitude'))
            #     longitude =(i.get('satlongitude'))
            #     latlong = str( str(latitude)+ " " +str(longitude) )
            
            # # Checking to see if the latitude and longitude are being concatinated as expected for input to the setAddress function
            #     print( "*********   Printing input latitude and longitude  {}".format(latlong) )
            
            self.search_marker = self.map_widget.set_address(
            address , marker=True )
            self.save_marker()

            ############## This is the function call for setting satellite's loc marker
            # self.set_satellite_map_marker(latitude, longitude)

            if self.search_marker is False:
                # address was invalid (return value is False)
                self.search_marker = None
            # self.get_satellite_coordinates()
            self.search_in_progress = False

    def save_marker(self):
        print("\n inside Save_Marker()\n")
        if self.search_marker is not None:
            # print("****** Printing inside Save Marker")
            # print(self.search_marker)
            self.marker_list_box.insert(
                tkinter.END, f" {len(self.marker_list)}. {self.search_marker.text} ")
            self.marker_list_box.see(tkinter.END)
            self.marker_list.append(self.search_marker)

    def clear_marker_list(self):
        for marker in self.marker_list:
            self.map_widget.delete(marker)

        self.marker_list_box.delete(0, tkinter.END)
        self.marker_list.clear()
        self.connect_marker()

    def connect_marker(self):
        print("\tInside connect_marker() \n")
        print("\t\tprinting the marker_List \n {}".format(self.marker_list) )
        position_list = []

        for marker in self.marker_list:
            position_list.append(marker.position)

        if self.marker_path is not None:
            self.map_widget.delete(self.marker_path)

        if len(position_list) > 0:
            print("+++++++ . Printing Connect Marker position List here {}".format(position_list))
            self.marker_path = self.map_widget.set_path(position_list)

    def clear(self):
        self.search_bar.delete(0, last=tkinter.END)
        self.map_widget.delete(self.search_marker)

    def on_closing(self, event=0):
        self.destroy()
        exit()

    def start(self):
        self.mainloop()

    # @Author M Shankar Ganapathy
    # This function is to set markers based on the lat and long for 150 min duration
    def set_satellite_map_marker(self, lat, long):
        # print("Latitude {} /t Longitude {}".format(lat, long))
        self.map_widget.set_marker(lat, long)
        self.save_satellite_marker(lat, long)
        self.connect_satellite_marker()

    # Dummy function
    def connect_satellite_marker(self):
        for index, value in enumerate(self.marker_list):
            print("Index {} , {} \t values: {} {}".format(index, index+1, self.marker_list[index], self.marker_list[index+1] ))
        # self.map_widget.set_path() # this takes an input list only
    
    # Function to save the satellite marker into the marker list
    def save_satellite_marker(self, satAddress):
        if self.search_marker is not None:
            
            self.marker_list_box.insert(
                tkinter.END, f" {len(self.marker_list)}. {satAddress} ")
            self.marker_list_box.see(tkinter.END)
            self.marker_list.append(self.search_marker)


    # Function to make HTTP requests 
    def get_satellite_coordinates(self):
        print("Inside get_Satellite_coordinates() \n")
    #  PLotting for satellite positions
        for i in self.positions:
            latitude = (i.get('satlatitude'))
            longitude =(i.get('satlongitude'))

            latlong = str( str(latitude)+ " " +str(longitude) )
        
        # Checking to see if the latitude and longitude are being concatinated as expected for input to the setAddress function
            print( "*********   Printing input latitude and longitude  {} @ {} \n".format(latlong, dt.datetime.utcfromtimestamp(i.get('timestamp'))) )

        # Reverse Geocoding the latitude and longitude before setting the address down below
            locator = Nominatim(user_agent="sample")
            coordinates = tuple( ( latitude, longitude ))
            location = locator.reverse(coordinates)
            satAddress = location.address
            print(" \t \t Satellite is at  {} \n".format(satAddress) )
            self.search_marker = self.map_widget.set_address(
                satAddress , marker=True )
            # self.save_marker()
            self.save_satellite_marker(satAddress)

if __name__ == "__main__":
    app = App()
    app.start()