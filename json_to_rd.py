import json
import os
import sys



#def masterskeletalnull(replacestring):
    #if "Base" in os.path.dirname(replacestring) and ("Skeleton" in os.path.basename(replacestring) or "Fortnite_M_Avg_Player" in os.path.basename(replacestring)):
        #return True

def seekwrite(pathtoexists, wfile, inpa, inpb):
    if "Game" not in os.path.dirname(inpb):
        #wstring = "/"
        dirandwrite = "/"
    else:
        #wstring = os.path.basename(inpb).split(".")[1]
        dirandwrite = os.path.dirname(inpb) + "/" + os.path.basename(inpb) #.split(".")[0]

    if inpa == "CustomCharacterFaceData":
        testskip = True
    else:
        #sstring = os.path.basename(inpa).split(".")[1]
        dirandstring = os.path.dirname(inpa) + "/" + os.path.basename(inpa) #.split(".")[0]
        testskip = False
    

    if pathtoexists == True and testskip is False:
        wfile.write("to_ar.Seek(\"" + dirandstring + "\")" + "\n")
        wfile.write("to_ar.Write<string>(\"" + dirandwrite + "\")" + "\n\n")

        #wfile.write("to_ar.Seek(\"" + sstring + "\")" + "\n")
        #wfile.write("to_ar.Write<string>(\"" + wstring + "\")" + "\n\n")
    elif pathtoexists == False and testskip is False:
            wfile.write("from_ar.Seek(\"" + dirandstring + "\")" + "\n")
            wfile.write("from_ar.Write<string>(\"" + dirandwrite + "\")" + "\n\n")

            #wfile.write("from_ar.Seek(\"" + sstring + "\")" + "\n")
            #wfile.write("from_ar.Write<string>(\"" + wstring + "\")" + "\n\n")

def json_to_rd(jsonpath):

    if os.path.exists(jsonpath):
        try:
            x = json.load(open(jsonpath, encoding='utf-8'))
        except json.decoder.JSONDecodeError:
            try:
                #using yaml cause json doesnt like the extra comma in some plugins
                import yaml
                #if there are tabs, remove them because yaml doesnt like them
                yamlread = open(jsonpath, encoding='utf-8').read()
                yamlread = yamlread.replace("\t", "")
                x = yaml.safe_load(yamlread)
            except ModuleNotFoundError:
                yamlins = input("Would you like to install YAML? This is required for the plugin you want to convert. (yes or no)").lower()
                if yamlins == "no":
                    sys.exit("Exiting!")
                elif yamlins == "yes":
                    os.system('py -m pip install --upgrade pip')
                    os.system('pip install pyyaml')
                    sys.exit("Installed YAML! Please reopen the py.")
                else: 
                    sys.exit("You did something wrong. Exiting.")
    elif not os.path.exists(jsonpath):
        print("Path is wrong! Make sure your plugin is in the same folder as the python file.")
    else:
        sys.exit('Oops! Something happened. Report the error on github or to me on discord: Lightning#2538')




    try:
        x["Name"]
    except KeyError:
        signs = [("default_name","Name"), ("swapped_icon","Icon"), ("messages", "Author")]
        difjson = True
    else:
        signs = [("Name","Name"), ("Swapicon","Icon"), ("Message", "Author")]
        difjson = False

    print("Writing signs...")
    rdpath = os.path.basename(jsonpath).split(".")[0] + ".rd"
    wfile = open(rdpath, "w", encoding="utf-8")
    wfile.write("#file plugin\n")
    for sign, sign_name in signs:
        signing = ('sign: "%s", "%s"\n' % (sign_name, x[sign]))
        wfile.write(signing)
    print("Wrote signs!")

    print("Writing imports and swaps...")
    if difjson == True:
        assets = x["swaps"]
    elif difjson == False:
        assets = x["Assets"]
        
    for asset in assets:
        # path is expected to exist
        pathtoexists = True
        AssetPath = asset["AssetPath"]
        try:
            AssetPathTo = asset["AssetPathTo"]
        except KeyError:
            pathtoexists = False
            
        if pathtoexists == True:
            fromar = "\nfrom_ar = import \"" + AssetPath + "\""
            wfile.write(fromar)
            toar = "\nto_ar = import \"" + AssetPathTo + "\" \n\n"
            wfile.write(toar)
        elif pathtoexists == False:
            fromar = "\nfrom_ar = import \"" + AssetPath + "\" \n\n"
            wfile.write(fromar)

        try:
            swaps = asset["Swaps"]
        except KeyError:
            swaps = asset["swaps"]

        if swaps is None:
            wfile.write("\n\nfrom_ar.Swap(to_ar)\n\n")
            continue

        swap_items = []
        if difjson == True:
            swap_items = swaps.items()
        elif difjson == False:
            swap_items = [(swap["search"], swap["replace"]) for swap in swaps]
        
        swaps_sorted = sorted(swap_items, key=lambda d: len(d[1]), reverse=True)

        for searchstring, replacestring in swaps_sorted:
            #if not masterskeletalnull(replacestring):
                seekwrite(pathtoexists, wfile, searchstring, replacestring)
        if pathtoexists is True:
            wfile.write("\n\nfrom_ar.Swap(to_ar)\n\n")
    print("Wrote imports and swaps!")
    wfile.close()
    return rdpath

def rd_to_csp(rd):
    os.system('SSPN.repl.exe "%%localappdata%%/saturn/plugins"  "%s"' % (rd))

#listoftests BrilliantBomber.json default_axe_to_stellar_axe.json Selene_To_The_Rogue_LAROI_ELECTRIFIED.json Sludgehammer_To_Candy_Axe.json BoogieDownToGetGriddy.json
if __name__ == "__main__":
    jsonpaths = sys.argv[1:]
    if not jsonpaths:
        jsonpath = input("Please input the paths of your json plugins: ")
        #FOR TESTING/MULTIPLE SWAPS (the name cant have any spaces)
        #jsonpaths.extend(jsonpath.split(" "))
        jsonpaths.append(jsonpath)
    
    for jsonpath in jsonpaths:
        json_to_rd(jsonpath)
    
    ans = input("Would you like to compile the plugin? The compiler will be downloaded if not found. Type yes or no.\n").lower()
    while True:
        if ans == "yes":
            if not os.path.exists("SSPN.Repl.exe"):
                print("Complier not found! Downloading compiler...")
                os.system('powershell -Command "wget -O SSPN.Repl.exe https://cdn.discordapp.com/attachments/1078667568082071623/1079002439866388480/SSPN.Repl.exe"')
            rdpath = os.path.basename(jsonpath).split(".")[0] + ".rd"
            rd_to_csp(rdpath)
            print("Done compiling! The compiled plugin has been automatically put into your plugins folder.")
            break
        elif ans == "no":
            break
        else:
            print("You typed something other than yes or no. Please try again.")      
    sys.exit(0)
