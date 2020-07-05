
import pandas as pd
import numpy as np
from tqdm import tqdm

def load_data():
    try :
        file_name = input('Enter file name :')
        data = pd.read_csv(file_name)
        lst = list(data.head(0))
        temp = {}
        for i in lst:
            temp[i] = list(data.head(len(data))[i])
        print('\nData loaded successfully..!!\n')
        return temp,lst
    except:
        print('\nLoading of data failed..!\n')


def check(string):
    return string!=string



def changeAttrType():
    while(1):
        if input('Would you like to change the type of any attribute ?(y/n) : ') == 'y':
            change_attr = []
            while(1):
                change_attr.append(input('Enter the attr name : '))
                if(input('Add more attr?(y/n)')=='n'):
                    break
            for i in change_attr:
                print(i)
                t = int(input('Change attr type to\n1.Float\n2.Integer\n'))
                lst = val[i]
                l = []
                if t == 1:
                    for k in range(len(lst)):
                        if(check(lst[k])):
                            l.append(0)
                        else:
                            if type(lst[k]) == str:
                                if lst[k].isdigit():
                                    l.append(float(lst[k]))
                                else:
                                    l.append(0)
                            else:
                                l.append(float(lst[k]))

#                 elif t==2:
#                     for k in lst:
#                         l.append(str(k))
                elif t ==2 :
                    for k in range(len(lst)):
                        if(check(lst[k])):
                            l.append(0)
                        else:
                            if type(lst[k]) == str:
                                if lst[k].isdigit():
                                    l.append(int(lst[k]))
                                else:
                                    l.append(0)
                            else:
                                l.append(int(lst[k]))
                val[i] = l
        else:
            break



def checkNoisyData():
    if(input('Would you like to identify noisy data?(y/n)') == 'y'):
        print('Checking for noisy data and replacing them as unknown...')
        for i,j in val.items():
            print('Check for attr ',i,'(y/n)')
            if(input() == 'y'): 
                for m in range(len(j)):
                    if(check(j[m]) == False):
                        t = type(j[m])
                        break
                flag = 0
                if t == str:
                    progressbar = tqdm(range(len(j)))
                    for k in progressbar:
                        if check(j[k]):
                            #print('Noisy data',j[k],'found')
                            j[k] = 'unknown'
                            flag = 1
                        else:
                            if j[k].isdigit():
                                #print('Noisy data',j[k],'found')
                                j[k] = 'unknown'
                                flag = 1

                elif t == float:
                    progressbar = tqdm(range(len(j)))
                    for k in progressbar:
                        if check(j[k]):
                            #print('Noisy data',j[k],'found')
                            j[k] = 0
                            flag = 1
                        elif (type(j[k]) == str):
                            #print('Noisy data',j[k],'found')
                            j[k] = 0
                            flag = 1
                elif t == int:
                    progressbar = tqdm(range(len(j)))
                    for k in progressbar:
                        if check(j[k]):
                            #print('Noisy data',j[k],'found')
                            j[k] = 0
                            flag = 1
                        elif (type(j[k]) == str):
                            #print('Noisy data',j[k],'found')
                            j[k] = 0
                            flag = 1
                if(flag == 0):
                    print('No noisy data found..!')
            else:
                print('Aborted..!')
    else:
        print('Noisy data check stopped...')


def deleteTuples():
    while(1):
        if(input('\nWould you like noisy data..?\nTuples with unknown values will be removed..(y/n)') == 'y'):
            print('Removing tuples with unknown values..')
            print('Carefully select an attribute from the list below and tuples will be deleted accordingly\n')
            print(header)

            attr = input()
            idx = []

            remove_tuple = new_val[attr]
            check = 'unknown'
            if type(remove_tuple[0]) == int or type(remove_tuple[0]) == float:
                check = 0
            for i in range(len(remove_tuple)):
                if remove_tuple[i] == check:
                    idx.append(i)
                    
            print('Total tuples with unknown values found : ',len(idx))
            if(input('Proceed deleting...?(y/n)') == 'y'):
                print('Deleting tuples in progress....')

                for i in header:
                    print(i)
                    l = new_val[i]
                    h = 0
                    for k in idx:
                        del l[k-h]
                        h+=1
                    new_val[i] = l
                    print('Tuple length after deletion : ',len(l))
            else:
                print('Deletion aborted...!')
        else:
            print('\nDeleting tuples stopped....\n')
            break




from scipy import stats

def fillMissingValues():
    while(1):
        if (input('Would you like to fill missing values?(y/n)') == 'y'):

            print('Filling missing values\nSelect only attributes of type float/integer\n')
            print('Select a primary key\n')#all the missing values will be replaced by the mean,median,mode value 
                                        #calculated for a attribute w.r.t primary key
            print(header)
            primary_key = new_val[input()]
            unique_primary = {}
            l = []
            for i in primary_key:  #creating unique list
                if i not in l:
                    l.append(i)
            print('No of unquie keys :',len(l))
            if(input('Proceed?(y/n)') == 'y'): 
                while(1):
                    for i in l:
                        unique_primary[i] = []        
                    try:
                        c = input('Select an attribute :')
                        secondary = new_val[c]
                    except:
                        print('Check input')
                        continue
                    for i,j in zip(primary_key,secondary):
                        if j!=0:
                            unique_primary[i].append(j) 

                    ch = int(input('Select a method :\n1.Mean\n2.Median\n3.Mode\n'))
                    if ch == 1:
                        for i in l:
                            unique_primary[i] = np.mean(unique_primary[i])
                    elif ch == 2:
                        for i in l:
                            unique_primary[i] = np.median(unique_primary[i])
                    else :
                        for i in l:
                            unique_primary[i] = stats.mode(unique_primary[i])[0]
                    lst = []
                    for j in range(len(secondary)):
                        if secondary[j]==0:
                            k = unique_primary[primary_key[j]]
                            lst.append(k)
                            continue
                        lst.append(secondary[j])

                    new_val[c] = lst
                    if(input('Would like to continue filling missing value(Select attributes of type int/float)(y/n)') == 'n'):
                        break
            else:
                print('Aborted..!')
        else:
            print('Filling missing values stopped....\n')
            break



def findOutliers(x):
    q1 = np.percentile(x,25)
    q3 = np.percentile(x,75)
    iqr = q3-q1
    floor = q1 - (1.5*iqr)
    ceiling = q3 + (1.5*iqr)
    idx = []
    for i in range(len(x)):
        if (x[i]<floor) or (x[i]>ceiling):
            idx.append(x.index(x[i]))
    return idx





def normalization(x):
    min_1 = min(x)
    max_1 = max(x)
    new_min = 0
    new_max = 1.0
    
    for i in range(len(x)):
        x[i] = ((x[i] - min_1)/(max_1-min_1))*(new_max-new_min) + new_min
    return x




while(1):
    print('What would you like to perform ?\n1.Basic data preprocessing.\n2.Remove unwanted attributes from dataset\n'+
    '3.Identify outliers\n4.Data normalization\n5.None\n')
    choice = int(input())
    if choice == 1: 
        val,header = load_data()
        print('Attributes are\n',header,'\n')
        for j in header:
            print(j)
            print('Number of values : ',len(val[j]))
        print('\n\n')
        for i,j in val.items():
            print(i)
            for m in range(len(j)):
                if(check(j[m]) == False):
                    print( type(j[m]))
                    break
        changeAttrType()   
        checkNoisyData()
        new_val = val
        deleteTuples()
        fillMissingValues()
        if(input('\nSave preprocessed data (y/n) ?') == 'y'):
            df = pd.DataFrame(new_val)
            df.to_csv('basic_preprocessing.csv',index=False)
            print('\nData saved successfully..!!\n')
    elif choice == 2:
        val,header = load_data()
        print('Attributes are\n',header,'\n')
        delete_attr = []
        while(1):
            if(input('Add attribute ?(y/n)')=='y'):
                delete_attr.append(input('Select from attribute list above : '))
            else:
                break
        for h in delete_attr:
            del val[h]
        if(input('Save data?(y/n)') == 'y'):    
            df = pd.DataFrame(val)
            df.to_csv('new_data.csv',index=False)
            print('\nData saved successfully..!!\n')
    elif choice == 3:
        val,header = load_data()
        print('Attributes are\n',header,'\n')
        while(1):
            attr = input('Select an attribute from the list above\n')
            lst = findOutliers(val[attr])
            print(len(lst))
            if(input('Proceed deleting outliers?(y/n)') == 'y'):
                print('Deleting tuples in progress....')
                for i in header:
                    print(i)
                    l = val[i]
                    h = 0
                    for k in lst:
                        del l[k-h]
                        h+=1
                    val[i] = l
                    print('Tuple length after deletion : ',len(l))
            if(input('Continue identifying outliers?(y/n)') == 'n'):
                break
        if(input('Save data?(y/n)') == 'y'):
            df = pd.DataFrame(val)
            df.to_csv('outlier_removed.csv',index=False)
            print('\nData saved successfully..!!\n')
    elif choice == 4:
        val,header = load_data()
        print('Attributes are\n',header,'\n')
        while(1):
            attr = input('Select an attribute from the list above\n')
            if(input('Proceed?(y/n)') == 'y'):
                lst = normalization(val[attr])
                val[attr] = lst
                print('\nNormalization done...')
                if(input('Continue normalization?(y/n)') == 'n'):
                    df = pd.DataFrame(val)
                    df.to_csv('normalized_data.csv',index=False)
                    print('\nData saved successfully..!!\n')
                    break
    else :
        break

