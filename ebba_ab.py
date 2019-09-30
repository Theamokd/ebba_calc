from tkinter import *
from tkinter import filedialog, messagebox
import pandas as pd
import statistics as st


window = Tk()
window.title('EBBA abundance calculator')

dat50 = pd.DataFrame()
dat50_control = ['50x50_square', 'Years', 'Survey_completeness', 'EBBA2_species_code', 'EBBA2_scientific_name', 'Highest_ atlas_code', 'Expert_breeding_assessment', 'Breeding_status', 'Population_type', 'Abundance_code', 'Minimum_precise_abundance', 'Maximum_precise_abundance', 'Abundance_method', 'Comments']
def ask_data():
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select data file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    global dat50
    dat50=pd.read_csv(filename)
    if dat50_control != list(dat50.columns):
        messagebox.showerror("Error", "The header for the data file is not ok!")
        dat50 = pd.DataFrame()
    else:
        t1.insert(END,'The data file has been loaded!\n')

hab = pd.DataFrame()
hab_control=['square', 'habitat', 'area']
def ask_hab():
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select habitat coverage file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    global hab
    hab=pd.read_csv(filename)
    if hab_control != list(hab.columns):
        messagebox.showerror("Error", "The header for the habitat coverage file is not ok!")
        hab = pd.DataFrame()
    else:
        t1.insert(END,'The habitat coverage file has been loaded!\n')

spec_dens = pd.DataFrame()
spec_dens_control =['habitat', 'EBBA2_scientific_name', 'min', 'max']
def ask_dens():
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select species densities file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    global spec_dens
    spec_dens=pd.read_csv(filename)
    if spec_dens_control != list(spec_dens.columns):
        messagebox.showerror("Error", "The header for the species densities file is not ok!")
        spec_dens = pd.DataFrame()
    else:
        t1.insert(END,'The species densities file has been loaded!\n')


def magic():
    global dat50
    global hab
    global spec_dens
    t1.insert(END,"Don't panic! This may take a while!\n")
    if dat50.empty or hab.empty or spec_dens.empty:
        messagebox.showerror("Error", "You didnt load all the files!")
    else:
        rows_dat50 = list(dat50.index)
        for i in rows_dat50:
            square_code = dat50.loc[i,'50x50_square']
            species = dat50.loc[i,'EBBA2_scientific_name']
            t_hab = hab[hab['square'] == square_code]
            t_dens = spec_dens[spec_dens['EBBA2_scientific_name'] == species]
            temp=t_hab.merge(t_dens)
            temp = temp.fillna(0)
            temp['ab_min'] = temp['min']*temp['area']
            temp['ab_max'] = temp['max']*temp['area']
            dat50.loc[i,'Minimum_precise_abundance']=round(sum(temp['ab_min']))
            dat50.loc[i,'Maximum_precise_abundance']=round(sum(temp['ab_max']))
            mean_ab = st.mean([dat50.loc[i,'Minimum_precise_abundance'] ,dat50.loc[i,'Maximum_precise_abundance']])
            if pd.isnull(dat50.loc[i,'Abundance_code']):
                if mean_ab<10:
                    dat50.loc[i,'Abundance_code']='A'
                    if pd.isnull(dat50.loc[i,'Comments']):
                        dat50.loc[i,'Comments'] = 'Abundance calculator'
                    else:
                        dat50.loc[i,'Comments'] = str(dat50.loc[i,'Comments'])+' Abundance calculator'
                elif mean_ab<100:
                    dat50.loc[i,'Abundance_code']='B'
                    if pd.isnull(dat50.loc[i,'Comments']):
                        dat50.loc[i,'Comments'] = 'Abundance calculator'
                    else:
                        dat50.loc[i,'Comments'] = str(dat50.loc[i,'Comments'])+' Abundance calculator'
                elif mean_ab<1000:
                    dat50.loc[i,'Abundance_code']='C'
                    if pd.isnull(dat50.loc[i,'Comments']):
                        dat50.loc[i,'Comments'] = 'Abundance calculator'
                    else:
                        dat50.loc[i,'Comments'] = str(dat50.loc[i,'Comments'])+' Abundance calculator'
                elif mean_ab<10000:
                    dat50.loc[i,'Abundance_code']='D'
                    if pd.isnull(dat50.loc[i,'Comments']):
                        dat50.loc[i,'Comments'] = 'Abundance calculator'
                    else:
                        dat50.loc[i,'Comments'] = str(dat50.loc[i,'Comments'])+' Abundance calculator'
                elif mean_ab<100000:
                    dat50.loc[i,'Abundance_code']='E'
                    if pd.isnull(dat50.loc[i,'Comments']):
                        dat50.loc[i,'Comments'] = 'Abundance calculator'
                    else:
                        dat50.loc[i,'Comments'] = str(dat50.loc[i,'Comments'])+' Abundance calculator'
                elif mean_ab>100000:
                    dat50.loc[i,'Abundance_code']='F'
                    if pd.isnull(dat50.loc[i,'Comments']):
                        dat50.loc[i,'Comments'] = 'Abundance calculator'
                    else:
                        dat50.loc[i,'Comments'] = str(dat50.loc[i,'Comments'])+' Abundance calculator'

        t1.insert(END,'All good! Please choose where you want to save the file!\n')
        fn =  filedialog.asksaveasfilename(initialdir = "/",title = "Where do you want to save the results? (save as *.csv)")
        dat50.to_csv(fn, index = False)
        t1.insert(END,'The job is done, please check the file you saved!\n')



l2=Label(window, text='First load each of the three files using the buttons below\nThen press the big button and set the "name_of_the_file.csv" and where to save it \nThe files loaded must be csv and must have the headers provided with the program!!!')
l2.grid(row=0, column=0, columnspan=2, sticky=W, padx=5, pady=5)
l2.config(font=("Arial", 10), relief='ridge', justify=LEFT)



b1=Button(window, text='Load data file',  command=ask_data)
b1.grid(row=1, column=0, sticky=W, padx=5, pady=5)

b2=Button(window, text='Load habitat coverage file', command=ask_hab)
b2.grid(row=2, column=0, sticky=W, padx=5, pady=5)

b3=Button(window, text='Load species densities file', command=ask_dens)
b3.grid(row=3, column=0, sticky=W, padx=5, pady=5)

b4=Button(window, text="Calculate abundances!\nDon't panic! This may take a while!", command=magic,height=10)
b4.grid(row=1, column=1, rowspan=3, sticky=E, padx=5, pady=5)

t1=Text(window)
t1.grid(row=4, column=0, columnspan=2)

l3=Label(window, text='© Judit Veres-Szászka, Dorin Damoc - 2018')
l3.grid(row=5, column=1, sticky=E)
l3.config(font=("Arial", 8))

window.mainloop()
