#!/usr/bin/python3
# template.py by Barron Stone
# This is an exercise file from Python GUI Development with Tkinter on lynda.com

from tkinter import *
from tkinter import ttk
import pandas as pd
import math
import geopy
import geopandas
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Astra_Test")
import PIL
from PIL import Image
from scipy import stats   
Window_Cost_Per_m2 = 281.1222161 
Roof_Cost_Per_m2 = 262.7622161 
Value_Of_kWh = 0.17
Wall_Eff = 0.0428
Roof_Eff = 0.165 
CO2_Per_kWh = 0.256
Global_CO2_Emissions = 36.15E+09
Business_Sector = 65.9E+06
Average_Electricity_Consumption_Per_m2 = 253 #Figure from data
Global_CO2_Emissions = 36.15E+09
Business_Sector = 65.9E+06
Average_Electricity_Consumption_Per_m2 = 253 #Figure from data
CompanyRoof = 'Roof'
CompanyWindow = 'Window'
CompanyName = 'PV Installer'
CompanyFootprint = 43000
CompanyStoreys = 46
Height_Of_Storey = 4.2672 #m
class SolarApp:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.pack()
        
        self.logo = PhotoImage(file = 'AZHack_logo.gif').subsample(64)
        self.info_label = ttk.Label(self.frame, text = "Please input the following information:", image = self.logo)
        self.info_label.config(compound = 'left', )
        self.info_label.grid(row=0,column=0,columnspan = 3, sticky = 'w')
        
        self.company_label = ttk.Label(self.frame, text = "Company Name")
        self.company_label.grid(row=1,column=0, sticky = 'w',padx = 10)
        self.company_entry = ttk.Entry(self.frame, width = 30)
        self.company_entry.grid(row=1,column =2, pady = 10)
        
        self.location_label = ttk.Label(self.frame, text = "Building Address")
        self.location_label.grid(row=2,column=0, sticky = 'w', padx = 10)
        self.location_entry = Text(self.frame, width = 23, height = 3, wrap = WORD)
        self.location_entry.grid(row=2,column =2, pady = 10)
        
        self.foot_label = ttk.Label(self.frame, text = "Building Footprint (Square m)")
        self.foot_label.grid(row=3,column=0, sticky = 'w', padx = 10)
        self.foot_entry = ttk.Entry(self.frame, width = 30)
        self.foot_entry.grid(row=3,column =2, pady = 10)
        
        self.storeys_label = ttk.Label(self.frame, text = "Building Storeys")
        self.storeys_label.grid(row=4,column=0, sticky = 'w', padx = 10)
        self.storeys_entry = ttk.Entry(self.frame, width = 30)
        self.storeys_entry.grid(row=4,column =2, pady = 10)
        
        
#        self.energy_label = ttk.Label(self.frame, text = "Estimated Energy Usage (kWh)")
#        self.energy_label.grid(row=5, column = 0, sticky = 'w', padx = 10)
#        self.energy_entry = ttk.Entry(self.frame, width = 30)
#        self.energy_entry.grid(row=5,column =2, pady = 10)
        
        self.roof = StringVar()
        self.window = StringVar()
        
        self.roof_button = ttk.Checkbutton(self.frame, text = "Roof panels?")
        self.roof_button.grid(row=6, column = 0, sticky = 'w', padx = 10)
        self.roof_button.config(variable = self.roof, onvalue = "Roof", offvalue = "No Roof")
        
        self.window_button = ttk.Checkbutton(self.frame, text = "Window panels?")
        self.window_button.config(variable = self.window, onvalue = "Window", offvalue = "No Window")
        self.window_button.grid(row = 7, column = 0, sticky = 'w', padx = 10)
        
        
        
        self.window.set("No Window")
        self.roof.set("No Roof")

        submit = ttk.Button(self.frame, text = 'Submit', command = self.Submit)
        submit.grid(row = 7, column = 3)
        
        
    def Submit(self):
        self.CompanyName = self.company_entry.get()
        self.CompanyLocation = self.location_entry.get('1.0','end')
#        self.CompanyEnergy = self.energy_entry.get()
        self.CompanyRoof = self.roof.get()
        self.CompanyWindow = self.window.get()
        self.CompanyFootprint = int(self.foot_entry.get())
        self.CompanyStoreys = int(self.storeys_entry.get())
        
        self.frame.destroy()
        self.test()
        self.frame = ttk.Frame(self.master)
        self.frame.pack()
        self.frame.config(height = 600, width = 600)
        
        Disclaimer_label = ttk.Label(self.frame, text = "Disclaimer: The following information does not take into account any government solar incentives.", image = self.logo, compound = 'left' )
        Disclaimer_label.grid(row = 0, column = 0, columnspan = 2, sticky = 'w')
        
        C_label = ttk.Label(self.frame, text = "CO2 Saved per year = {:#.3g} (kg)".format((Value_Of_Energy_Produced(self.CompanyLocation, self.CompanyFootprint, self.CompanyStoreys, self.CompanyRoof, self.CompanyWindow)/Value_Of_kWh)*CO2_Per_kWh/1000))
        C_label.grid(row = 1, column = 0, sticky = 'w', padx = 10, pady = 10)
#        Cper_label = ttk.Label(self.frame, text = "Percentage reduction of **")
#        Cper_label.grid(row = 1, column = 1, sticky = 'w', padx = 10, pady = 10)
        
        Cost_label = ttk.Label(self.frame, text = "Total Cost = {:#.3g} (£) ".format(Total_Cost(self.CompanyFootprint, self.CompanyStoreys, self.CompanyRoof, self.CompanyWindow)))
        Cost_label.grid(row = 3, column = 0, sticky = 'w', padx = 10, pady = 10)
        
        E_label = ttk.Label(self.frame, text = "Energy Produced per year = {:#.3g} (kWh/year)".format(Value_Of_Energy_Produced(self.CompanyLocation, self.CompanyFootprint, self.CompanyStoreys, self.CompanyRoof, self.CompanyWindow)/Value_Of_kWh))
        E_label.grid(row = 5, column = 0, sticky = 'w', padx = 10, pady = 10)
#        Eper_label = ttk.Label(self.frame, text = "Percentage reduction of **")
#        Eper_label.grid(row = 5, column = 1, sticky = 'w', padx = 10, pady = 10)
        EV_label = ttk.Label(self.frame, text = "Value of Energy Produced per year ={:#.3g} (£/year)".format(Value_Of_Energy_Produced(self.CompanyLocation, self.CompanyFootprint, self.CompanyStoreys, self.CompanyRoof, self.CompanyWindow)))
        EV_label.grid(row = 6, column = 0, sticky = 'w', padx = 10, pady = 10)
        
        ROI_label = ttk.Label(self.frame, text = "Time for return on investment = {:#.3g} (years)".format(Total_Cost(self.CompanyFootprint, self.CompanyStoreys, self.CompanyRoof, self.CompanyWindow)/Value_Of_Energy_Produced(self.CompanyLocation, self.CompanyFootprint, self.CompanyStoreys, self.CompanyRoof, self.CompanyWindow)))
        ROI_label.grid(row = 7, column = 0, sticky = 'w', padx = 10, pady = 10)
        
    def test(self):
        print(self.CompanyName)
        print(self.CompanyLocation)
        print(self.CompanyRoof)
        print(self.CompanyStoreys)
        print(self.CompanyFootprint)
        print(self.CompanyWindow)
        print(Value_Of_Energy_Produced(self.CompanyLocation, self.CompanyFootprint, self.CompanyStoreys, self.CompanyRoof, self.CompanyWindow))

   
        
def main():
    root = Tk()
    app = SolarApp(root)
    root.mainloop()
            

def Value_Of_Energy_Produced(address, footprint, storeys, checkbox1, checkbox2):
    location = geolocator.geocode(address)
    Longitude = location.longitude
    Latitude = location.latitude
    Height_Of_Storey = 4.2672 #m
    Wall_Area = math.sqrt(footprint)*storeys*Height_Of_Storey
    Power_Input = [[Latitude, Longitude]]
    Exposure = Find_Power(Power_Input)*365
    if checkbox1 == 'Roof':
        Roof_Value = footprint*Exposure*Roof_Eff*Value_Of_kWh
    else:
        Roof_Value = 0
    if checkbox2 == 'Window':
        Wall_Value = Wall_Area*Exposure*Wall_Eff*Value_Of_kWh*(0.38+(1-0.2333)+(1-0.2217)+1)
    else:
        Wall_Value = 0
    Total_Energy_Value = Wall_Value + Roof_Value
    return Total_Energy_Value
def Total_Wall_Cost(footprint, storeys):
    cost = Window_Cost_Per_m2*4*(math.sqrt(footprint))*storeys*Height_Of_Storey
    return cost
def Total_Roof_Cost(footprint):
    cost = Roof_Cost_Per_m2*footprint
    return cost
def Total_Cost(footprint, storeys, checkbox1, checkbox2):
    if checkbox1 == 'Roof':
        Roof_Cost = Roof_Cost_Per_m2*footprint
    else:
         Roof_Cost = 0
    if checkbox2 == 'Window':
        Window_Cost = Window_Cost_Per_m2*4*(math.sqrt(footprint))*storeys*Height_Of_Storey
    else:
        Window_Cost = 0
    Total_Cost = Window_Cost + Roof_Cost
    return Total_Cost
def colour_sample(coords):
    x = int(945 + coords[0][1]*77/15)
    y = int(530 - coords[0][0]*77/15)
    grid = []
    red_image = PIL.Image.open("world.png")
    red_image_rgb = red_image.convert("RGB")
    rgb_pixel_value_grid = []
    for i in range(x-3,x+4):
        for j in range(y-3,y+4):
            grid.append([[i,j]])
            rgb_pixel_value_grid.append(red_image_rgb.getpixel((i,j)))
    return stats.mode(rgb_pixel_value_grid)[0][0], rgb_pixel_value_grid
def Find_Power(coords):
    modal_colour, colours = colour_sample(coords)
    modal_colour.tolist()
    Array_Of_Values = ([[91,155,168],2.1],
                    [[95,169,176],2.3],
                    [[99,186,176],2.5],
                    [[105,201,169],2.7],
                    [[112,219,145],2.9],
                    [[137,232,116],3.1],
                    [[168,237,102],3.3],
                    [[196,240,83],3.5],
                    [[219,242,70],3.7],
                    [[236,245,69],3.9],
                    [[250,246,69],4.1],
                    [[252,233,57],4.3],
                    [[251, 219,50],4.5],
                    [[250, 200,45],4.7],
                    [[249, 179,25],4.9],
                    [[247, 159,17],5.1],
                    [[245, 138,15],5.3],
                    [[238, 120,14],5.5],
                    [[235, 98,23],5.7],
                    [[231, 76,37],5.9],
                    [[222, 55,65],6.1],
                    [[226, 74,97],6.3],
                    [[231, 92,124],6.5],
                    [[238, 110,150],6.7],
                    [[242, 130,172],6.9],
                    [[247, 148,188],7.1],
                    [[252, 167,202],7.3],
                    [[255, 186,216],7.5])
    for i in range(0, len(Array_Of_Values)):
        j=0
        if modal_colour[0]==Array_Of_Values[i][0][0] and modal_colour[1]==Array_Of_Values[i][0][1] and modal_colour[2]==Array_Of_Values[i][0][2]:
            Power = Array_Of_Values[i][1]
        else:
            j+=1
    if j==28:
        for i in range(0, len(Array_Of_Values)):
            for k in range(0, len(colours)):
                if colours[k]==Array_Of_Values[i][0]:
                    Power = Array_Of_Values[i][1]
    return Power
if __name__ == "__main__": main()

#Window_Cost_Per_m2 = 281.1222161 #£/m2
#Roof_Cost_Per_m2 = 262.7622161 #£/m2
#Value_Of_kWh = 0.17
#Value_Of_kWh = 0.17
#Wall_Eff = 0.0428
#Roof_Eff = 0.165 
#CO2_Per_kWh = 0.256
#Global_CO2_Emissions = 36.15E+09
#Business_Sector = 65.9E+06
#Average_Electricity_Consumption_Per_m2 = 253 #Figure from data
#CompanyRoof = 'Roof'
#CompanyWindow = 'Window'
#CompanyName = 'PV Installer'
#CompanyFootprint = 43000
#CompanyStoreys = 46
#Height_Of_Storey = 4.2672 #m
#CompanyAddress = '110 Bishopsgate London'
#Footprint = CompanyFootprint
#Storeys = CompanyStoreys
#Address = CompanyAddress
#Address_Values = {}
#Address_Values[Address] = {
#    'Footprint (square m)' : "%.2f" % Footprint,
#    'Exposure Footprint/year' : "%.2f" % (4*math.sqrt(Footprint)*Storeys*Height_Of_Storey + Footprint),
#    'Average Energy Consumption (kWh/year)' : "%.2f" % (Average_Electricity_Consumption_Per_m2*Footprint*Storeys),
#    'Energy Produced From PV (kWh/year)' : "%.2f" % (Value_Of_Energy_Produced(Address, Footprint, Storeys, CompanyRoof, CompanyWindow)/Value_Of_kWh),
#    'Total Value of Electricity Produced (£/year)' : "%.2f" % (Value_Of_Energy_Produced(Address, Footprint, Storeys, CompanyRoof, CompanyWindow)),
#    'Total Cost of Installation (£)' : "%.2f" % Total_Cost(Footprint, Storey, CompanyRoof, CompanyWindow),
#    'Payback Time (year(s))' : "%.2f" % (Total_Cost(Footprint, Storey, CompanyRoof, CompanyWindow)/Value_Of_Energy_Produced(Address, Footprint, Storeys, CompanyRoof, CompanyWindow)),
#    'Kgs of CO2 saved (tonnes/year)' :  "%.2f" % ((Value_Of_Energy_Produced(Address, Footprint, Storeys, CompanyRoof, CompanyWindow)/Value_Of_kWh)*CO2_Per_kWh/1000),
#    'Percentage saved in relation to global' : "%.7f" % ((((Value_Of_Energy_Produced(Address, Footprint, Storeys, CompanyRoof, CompanyWindow)/Value_Of_kWh)*CO2_Per_kWh/1000)/(Global_CO2_Emissions))*100),
#    'Percentage saved in relation to business sector' : "%.5f" % ((((Value_Of_Energy_Produced(Address, Footprint, Storeys, CompanyRoof, CompanyWindow)/Value_Of_kWh)*CO2_Per_kWh/1000)/(Business_Sector))*100)
#}