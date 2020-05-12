import tkinter as tk                
from tkinter import font  as tkfont 
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import earthquakes

df1 = DataFrame(earthquakes.df1, columns=['HOURS','MAGNITUDE'])
df2 = DataFrame(earthquakes.df2, columns=['YEAR','MAGNITUDE'])
df3 = DataFrame(earthquakes.df3, columns=['data_description','MAGNITUDE'])

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Bar, Line, Sccater, Predict, Visualization):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Welcome to earthquakes prediction", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button4 = tk.Button(self, text="Visualization",
                            command=lambda: controller.show_frame("Visualization"))
        button5 = tk.Button(self, text="Predict",
                            command=lambda: controller.show_frame("Predict"))
        button4.pack()
        button5.pack()
        
class Bar(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
                
        global df3
        figure1 = plt.Figure(figsize=(6,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self)
        bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df3 = df3[['data_description','MAGNITUDE']].groupby('data_description').sum()
        df3.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('Description of magnitude')
        
        button = tk.Button(self, text="Go to the Visualization page",
                           command=lambda: controller.show_frame("Visualization"))
        button.pack()

class Line(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        global df2
        figure2 = plt.Figure(figsize=(6,5), dpi=100)
        ax2 = figure2.add_subplot(111)
        line2 = FigureCanvasTkAgg(figure2, self)
        line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df2 = df2[['YEAR','MAGNITUDE']].groupby('YEAR').sum()
        df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
        ax2.set_title('Number of earthquakes per year')
        
        button = tk.Button(self, text="Go to the Visualization page",
                           command=lambda: controller.show_frame("Visualization"))
        button.pack()
        
class Sccater(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        global df1
        figure3 = plt.Figure(figsize=(6,5), dpi=100)
        ax3 = figure3.add_subplot(111)
        ax3.scatter(df1['HOURS'],df1['MAGNITUDE'], color = 'g')
        scatter3 = FigureCanvasTkAgg(figure3, self) 
        scatter3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        ax3.legend(['Number of earthquakes']) 
        ax3.set_xlabel('HOURS')
        ax3.set_title('Number of earthquakes per hours')
        
        button = tk.Button(self, text="Go to the Visualization page",
                           command=lambda: controller.show_frame("Visualization"))
        button.pack()
        
class CustomException(Exception):
    """Base class for other exceptions"""
    pass
class InputError(CustomException):
    pass
        
class Predict(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        fields = ('Year', 'Month', 'Day', 'Hours', 'Minutes', 'Latitude', 'Longitude', 'Predicted Magnitude', 'Message')

        def get_values(entries):
            
            entries['Message'].delete(0, tk.END)
            
            try:
                year = int(entries['Year'].get())
                month = int(entries['Month'].get())
                day = int(entries['Day'].get())
                hours = int(entries['Hours'].get())
                minutes = int(entries['Minutes'].get())
                latitude = float(entries['Latitude'].get())
                longitude = float(entries['Longitude'].get())            
                
                if year < 1901 or year > 2100:
                    raise InputError("Viti te jete ne rangun 1901-2100")
                elif month < 1 or month > 12:
                    raise InputError("Muaji te jete ne rangun 1-12")
                elif not (day >= 1 and day <= 31):
                    raise InputError("Dita te jete ne rangun 1-31")
                elif not (hours >= 0 and hours <= 23):
                    raise InputError("Ora te jete ne rangun 0-23")
                elif not (minutes >= 0 and minutes <= 59):
                    raise InputError("Minutat te jete ne rangun 0-59")  
                
                try:
                    userInput = [[year, month, day, hours, minutes, latitude, longitude]]
                    
                    magnitude = earthquakes.model.predict(userInput)                
                    magnitude = float(magnitude)
                    entries['Predicted Magnitude'].delete(0, tk.END)
                    entries['Predicted Magnitude'].insert(0, float("{:.1f}".format(magnitude)))   
                except UnboundLocalError as err:
                    entries['Predicted Magnitude'].delete(0, tk.END)
                    entries['Message'].delete(0, tk.END)
                    entries['Message'].insert(1, "Error: {0}".format(err))
                           
            except InputError as err:
                entries['Predicted Magnitude'].delete(0, tk.END)
                entries['Message'].delete(0, tk.END)
                entries['Message'].insert(1, "Error: {0}".format(err))
            except Exception as err:
                entries['Predicted Magnitude'].delete(0, tk.END)
                entries['Message'].delete(0, tk.END)
                entries['Message'].insert(1, "Error: {0}".format(err))
                            
            
        def makeform(root, fields):
                entries = {}
                for field in fields:
                        row = tk.Frame(root)
                        lab = tk.Label(row, width=22, text=field+": ", anchor='w')
                        ent = tk.Entry(row)
                        ent.insert(0, "")
                        row.pack(side=tk.TOP, 
                                fill=tk.X, 
                                padx=5, 
                                pady=5)
                        lab.pack(side=tk.LEFT)
                        ent.pack(side=tk.RIGHT, 
                                expand=tk.YES, 
                                fill=tk.X)
                        entries[field] = ent
                return entries

        ents = makeform(self, fields)
        b1 = tk.Button(self, text='Predicted Magnitude',
                command=(lambda e=ents: get_values(e)))
        b1.pack(side=tk.LEFT, padx=5, pady=5)
        
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        
class Visualization(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Zgjedhni opsionin per vizualizim", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        button1 = tk.Button(self, text="Description of magnitude",
                            command=lambda: controller.show_frame("Bar"))
        button2 = tk.Button(self, text="Number of earthquakes per year",
                            command=lambda: controller.show_frame("Line"))
        button3 = tk.Button(self, text="Number of earthquakes per hours",
                            command=lambda: controller.show_frame("Sccater"))
        
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        button1.pack()
        button2.pack()
        button3.pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()