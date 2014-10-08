
from Feature import FeatureSpace
import numpy as np
from import_lightcurve import LeerLC_MACHO
from PreprocessLC import Preprocess_LC
import os.path

count = 4
folder = 6
guardar = np.zeros(shape=(1,42))

path = '/Users/isadoranun/Dropbox/lightcurves/'

for j in os.listdir(path)[8:9]:
    
    if os.path.isdir(path + j):

        count = count + 1

        for i in os.listdir(path + j):

            if i.endswith("B.mjd") and not i.startswith('.') and os.path.isfile(path + j +'/'+ i[:-5] + 'R.mjd'):


                lc_B = LeerLC_MACHO(path + j +'/'+ i[:])
                lc_R = LeerLC_MACHO(path + j +'/'+ i[:-5] + 'R.mjd')

        #Opening the light curve

                [data, mjd, error] = lc_B.leerLC()
                [data2, mjd2, error2] = lc_R.leerLC()

                preproccesed_data = Preprocess_LC(data, mjd, error)
                [data, mjd, error] = preproccesed_data.Preprocess()

                preproccesed_data = Preprocess_LC(data2, mjd2, error2)
                [second_data, mjd2, error2] = preproccesed_data.Preprocess()

                a = FeatureSpace(category='all',featureList=None, automean=[0,0], StetsonL=second_data ,  B_R=second_data, Beyond1Std=error, StetsonJ=second_data, MaxSlope=mjd, LinearTrend=mjd, Eta_B_R=second_data, Eta_e=mjd, Q31B_R=second_data, PeriodLS=mjd, CAR_sigma=[mjd, error], SlottedA = mjd)
                
                try:
                    a=a.calculateFeature(data)
                    guardar = np.vstack((guardar, np.hstack((i[3:-6] , a.result(method='array') , folder ))))

                except:
                    pass    
                

        folder = folder + 1      

        if count == 1:
            nombres = np.hstack(("MACHO_Id" , a.result(method='features') , "Class"))   
            guardar = np.vstack((nombres, guardar[1:]))
            np.savetxt('test_real2.csv', guardar, delimiter="," ,fmt="%s")
            guardar = np.zeros(shape=(1,42))

        else:
            nombres = np.hstack(("MACHO_Id" , a.result(method='features') , "Class"))   
            my_data = np.genfromtxt('test_real2.csv', delimiter=',', dtype=None)
            guardar = np.vstack((nombres, my_data[1:], guardar[1:] ))
            np.savetxt('test_real2.csv', guardar, delimiter="," ,fmt="%s")
            guardar = np.zeros(shape=(1,42))

        #B_R = second_data, Eta_B_R = second_data, Eta_e = mjd, MaxSlope = mjd, PeriodLS = mjd, Q31B_R = second_data, StetsonJ = second_data, StetsonL = second_data)