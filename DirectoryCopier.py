#PreiSBET Automation Program
#Author: Krishna Solanki
#Last Updated: 05/10/2019

#import os module
import os, sys, glob, shutil

#error message for any invalid entries
def invalid():
    print ("Invalid Entry Error: Please try again!")

def main():
    #program will run until valid respone
    while True:
    
        print ("-----------------------------------------------------------------")    
        print ("|                          ~PreiSBET~                           |") 
        print ("|* Automation designed to create directory, copy over contents *|") 
        print ("|* and delete directory once task is complete                  *|") 
        print ("|                                                               |") 
        print ("|Please have following data ready:                              |")
        print ("| 1. ARAN Number                                                |")
        print ("| 2. Batch Number                                               |")
        print ("| 3. State Initial                                              |")
        print ("| 4. Project Year                                               |")
        print ("-----------------------------------------------------------------")   

        #loop variables to force a valid user input- all set to true
        a =1
        b =1 
        c =1
        d =1

        #source path- from where all data will be copied from
        basepath = "\\\\video-01"

        #get ARAN ID
        while a == 1:
            ar = input ("Please enter the ARAN number: ")
        
            if (ar.isdigit()): #ensure int exists in the input string
                break
            else:
                invalid()
        
        #get batch number
        while b == 1:
            batch = input ("Please enter the Batch number: ")

            if (batch.isdigit()):
                break
            else:
                invalid()
        
        #get the state initals given by - e.g. AZ is arizona
        while c == 1:
            proj1 = input ("Please enter the State initials: ")

            if (proj1.isdigit()): # here we check to make sure its not an integer but a valid string
                invalid
            else:
                break

        #get project year - e.g. 2019 -> 19
        while d == 1:
            proj2 = input ("Please enter the last two digits of project year: ")

            if (proj2.isdigit()):
                break
            else:
                invalid()
    
        proj = proj1  + proj2 + "*" #wildcard to tell os to only look for state and year - e.g. AZ19
    
        #change directory if possible else will restore it our source path
        try:
             os.chdir(basepath)
        except:
            print ("Could not enter directory. Exception- ", sys.exc_info())
            print("restoring path")
            os.chdir(basepath)
            print ("You are in: ", os.getcwd())

        print ("Starting in "+ basepath)

        project = glob.glob(proj)  #glob is designed to search for patterns and return list of closest matches - workes like SEDT or GREP for dir

        #make sure glob actually finds a match other wise the directory does not exists and program will require user to make it
        if (len(project)==0):
            print ("Error: Project not found")
            sys.exit()
        else:
             print (project[0])
             temp = project[0] # get the closests match and save it to update our directory path

        update = basepath + "\\" + temp # updates our path

        #move in to next directory if possible
        try:
             os.chdir(update)
        except:
            print ("Could not enter directory. Exception- ", sys.exc_info())
            print("restoring path")
            os.chdir(basepath)
            print ("You are in: ", os.getcwd())
            update = os.getcwd()

        print ("You are now in "+ update)

        batch = "*" + batch #only care about if the batch is at end of directory name
        bach = glob.glob(batch) #search for matching batch
    
        if (len(bach)==0): #make sure a match is found
            print ("Error: Bach not found")
            break
        else:
             print (bach[0])
             temp = bach[0]

        update = update + "\\" + temp #update path
   
        #go in to directory
        try:
             os.chdir(update)
        except:
            print ("Could not enter directory. Exception- ", sys.exc_info())
            print("restoring path")
            os.chdir(basepath)
            print ("You are in: ", os.getcwd())
            update = os.getcwd()

        print ("You are now in "+ update)
        data = glob.glob('posdata')
    
        if (len(data)==0):
            print ("Error: posdata not found")
            break
        else:
             print (data[0])
             temp = data[0]

        update = update + "\\" + temp

        try:
             os.chdir(update)
        except:
            print ("Could not enter directory. Exception- ", sys.exc_info())
            print("restoring path")
            os.chdir(basepath) 
            print ("You are in: ", os.getcwd())
            update = os.getcwd()
    
        print ("You are now in "+ update)

        Mvpath = "\\\\video-01\\Operations\\SBETs" # perform same exercise for the destination subdirectory

        try:
             os.chdir(Mvpath)
        except:
            print ("Could not enter directory. Exception- ", sys.exc_info())
            print("restoring path")
            os.chdir(Mvpath)
            print ("You are in: ", os.getcwd())
        

        print ("Starting in "+ Mvpath)

        projd = glob.glob(proj)  

        if (len(projd)==0):
            print ("Error: Project in Operation//SBETs not found")
            break
        else:
             print (projd[0])
             temp = projd[0]

        updateD = Mvpath + "\\" + temp

        try:
             os.chdir(updateD)
        except:
            print ("Could not enter directory. Exception- ", sys.exc_info())
            print("restoring path")
            os.chdir(basepath)
            print ("You are in: ", os.getcwd())
            updateD = os.getcwd()

        print ("You are now in "+ updateD)

        aran =  "ARAN" + ar + "_Posdata" 
        aranD = glob.glob(aran)

        #once in the last folder will look for ARANXX_Posdata to see if it exists - if it does it deletes it and will create a new folder 
        #else if no folder found, later on it will create one for the user - the reason stems from the limited functionality of shutils copy tool
        if (len(aranD) == 0):
            break
        else:
            try:
                check = updateD +"\\"+ aran
                shutil.rmtree(check) # here we remove existing directory if created
 
            except:
                print ("Could not Remove directory. Exception- ", sys.exc_info())
                print ("Please ensure ARAN directory is empty")
                sys.exit()
         

        updateD = updateD + "\\" + aran


        print ("Destination is set to: "+ updateD)
        print ("Source is set to: " + update)
    
        if ((updateD != Mvpath) & (update != basepath)): #another err check to ensure source and dest are not the base strings we made initially
        
            #the following will actually do the copy process from both folders - note copy will create a directory with dest name
            #hence why we deleted an instance before
            try:
                shutil.copytree(update,updateD)
                print("Copying files in progress")
            except:
                print ("Could not copy directory. Exception- ", sys.exc_info())
                print ("Please fix issue, ensure dest directory is empty and try again")
                sys.exit()

            print ("Files Transfer was sucessful")
            print ("Now wait till end of process.")

            done = False
            while (done == False): #an infinite loop used to query for when process is complete and will begin deletion process
            
                proc = input ("Is process complete(y/n): ")

                if (proc == "y"):
                    done = True
                    break
                elif (proc == "n"):
                    done = False
                else:
                    done = False
                    invalid()
            # rmtree works by recursively destroy subdir and files in dest directory
            try:
                shutil.rmtree(updateD)
 
            except:
                print ("Could not Remove directory. Exception- ", sys.exc_info())
                sys.exit()
        
            print ("Program is Complete")
            sys.exit() #exit when done

if __name__  == "__main__":
    main()  
