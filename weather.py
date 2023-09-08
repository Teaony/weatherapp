import requests
import tkinter as tk
from PIL import Image, ImageTk

#authkey for openweathermap api
authkey = ""

#create base window
window = tk.Tk()
window.title("Weather")
window.geometry("500x500")

#class for cities, used for combobox later
class city:
    def __init__(self, name, country, temp, tempmax, tempmin, desc, icon):
        self.name = name
        self.country = country
        self.temp = temp
        self.tempmax = tempmax
        self.tempmin = tempmin
        self.desc = desc
        self.icon = icon

    def __str__(self):
        return f"{self.name}, {self.country}"

#clear frames below search frame
def clearFrame():
    for labels in dataframe.winfo_children():
        labels.destroy()
    for labels in displayframe.winfo_children():
        labels.destroy()

#show icon and temperature
def showWeather(icon, temp):
    url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
    image = Image.open(requests.get(url, stream=True).raw)
    displayimg = ImageTk.PhotoImage(image)
    displaylabel = tk.Label(displayframe, image=displayimg)
    displaylabel.configure(bg="light blue")
    displaylabel.pack(side="left", anchor="w")
    displaylabel.image = displayimg
    tk.Label(displayframe, text=f"{temp}", font=("arial 30")).pack(side="left", anchor="w")

#get weather data from api and show
def getWeather():
    city = input.get()
    url=f"http://api.openweathermap.org/data/2.5/find?q={city}&units=metric&type=accurate&mode=json&APPID={authkey}"
    cities = []
    try:
        data = requests.get(url).json().get("list")[0]
        cname= data.get("name")
        temp = round(data.get("main").get("temp"))
        tempmin = round(data.get("main").get("temp_min"))
        tempmax = round(data.get("main").get("temp_max"))
        desc = data.get("weather")[0].get("description")
        icon = data.get("weather")[0].get("icon")
        clearFrame()
        showWeather(icon, temp)
        tk.Label(dataframe, text=f"City: {cname}", font=("arial 15")).pack(side="top", anchor="nw", padx=10, pady=10)
        tk.Label(dataframe, text=f"Min. Temperature: {tempmin}", font=("arial 15")).pack(side="top", anchor="nw", padx=10, pady=10)
        tk.Label(dataframe, text=f"Max. Temperature: {tempmax}", font=("arial 15")).pack(side="top", anchor="nw", padx=10, pady=10)
        tk.Label(dataframe, text=f"The weather consists of {desc}", font=("arial 15")).pack(side="top", anchor="nw", padx=10, pady=10)
    except IndexError:
        clearFrame()
        tk.Label(dataframe, text=f"Unfortunately, {city} could not be found.", font=("arial 15")).pack(side="top", anchor="nw", padx=10, pady=10)

def enterevent(event):
    getWeather()

#bind enter key to search
window.bind("<Return>", enterevent)

#Frame for App description
descframe = tk.Frame(window)
descframe.pack(side="top", anchor="nw")
info = tk.Label(descframe, text="Search for a city to display the weather", font=("arial", 12))
info.pack(side="left")

#Frame for search bar and button
searchframe = tk.Frame(window)
searchframe.pack(side="top", anchor="nw")
citylabel = tk.Label(searchframe, text="City", font=("arial", 12))
citylabel.pack(side="left", anchor="sw")

input = tk.Entry(searchframe, font=("arial", 12), width=15)
input.pack(side="left", anchor="sw")
input.focus()
search = tk.Button(searchframe, text="Search", command=getWeather)
search.pack(side="left", anchor="w")

#TODO frame for combobox selection

#frame for weather icon and current temperature
displayframe = tk.Frame(window)
displayframe.pack(side="top", anchor="n")

#frame for api data
dataframe = tk.Frame(window, width=0.7, height=1.0)
dataframe.pack(side="left", anchor="w")



window.mainloop()


