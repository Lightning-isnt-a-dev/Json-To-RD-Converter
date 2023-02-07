import json
import os, sys

def seekwrite(pathtoexists, wfile, inpa, inpb):
    if inpb == "/":
        wstring = "/"
    else:
        wstring = os.path.basename(inpb).split(".")[1]
    wstringlong = os.path.basename(inpb).split(".")[0]
    dirandwrite = os.path.dirname(inpb) + "/" + wstringlong

    sstring = os.path.basename(inpa).split(".")[1]
    sstringlong = os.path.basename(inpa).split(".")[0]
    dirandstring = os.path.dirname(inpa) + "/" + sstringlong
    

    if pathtoexists == True:
        wfile.write("to_ar.Seek(\"" + dirandstring + "\")" + "\n")
        wfile.write("to_ar.Write<string>(\"" + dirandwrite + "\")" + "\n\n")

        wfile.write("to_ar.Seek(\"" + sstring + "\")" + "\n")
        wfile.write("to_ar.Write<string>(\"" + wstring + "\")" + "\n\n")
    elif pathtoexists == False:
            wfile.write("from_ar.Seek(\"" + dirandstring + "\")" + "\n")
            wfile.write("from_ar.Write<string>(\"" + dirandwrite + "\")" + "\n\n")

            wfile.write("from_ar.Seek(\"" + sstring + "\")" + "\n")
            wfile.write("from_ar.Write<string>(\"" + wstring + "\")" + "\n\n")

def json_to_rd(jsonpath):

    if os.path.exists(jsonpath):
        try :
            x = json.load(open(jsonpath, encoding='utf-8'))
        except Exception:
            sys.exit('Oops! Something happened. Report the error on github or to me on discord: Lightning#2538')
    else:
        print("Theres something wrong with your path. Try again.")
        sys.exit()



    while True:
        try:
            x["Name"]
        except KeyError:
            signs = [("swapped_name","Name"), ("default_icon","Icon"), ("messages", "Author")]
            difjson = True
            break
        else:
            signs = [("Name","Name"), ("Swapicon","Icon"), ("Message", "Author")]
            difjson = False
            break

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
            fromar = "\nfrom_ar = import \"" + AssetPath + "\" \n\n"
            wfile.write(fromar)
            toar = "\nto_ar = import \"" + AssetPathTo + "\" "
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
            
        if difjson == True:
            listofswaps = []
            for key, value in swaps.items():                    
                listofswaps.append((key, value))
            swaps_sorted = sorted(listofswaps, key=lambda d: len(d[1]), reverse=True)
            for searchstring, replacestring in swaps_sorted:
                if "Base" in os.path.dirname(replacestring) and ("Skeleton" in os.path.basename(replacestring) or "Fortnite_M_Avg_Player" in os.path.basename(replacestring)):
                    break
                else:
                    seekwrite(pathtoexists, wfile, searchstring, replacestring)
        elif difjson == False:
            swaps_sorted = sorted(swaps, key=lambda d: len(d['replace']), reverse=True)
            for swap in swaps_sorted:
                searchstring = swap["search"]
                replacestring = swap["replace"]
                if "Base" in os.path.dirname(replacestring) and ("Skeleton" in os.path.basename(replacestring) or "Fortnite_M_Avg_Player" in os.path.basename(replacestring)):
                    break
                else:
                    seekwrite(pathtoexists, wfile, searchstring, replacestring)
        if pathtoexists is True:
            wfile.write("from_ar.Swap(to_ar)\n\n")

    print("Wrote imports and swaps!")
    wfile.close()
    return rdpath

def rd_to_csp(rd): 
    os.system('cmd /k \"SSPN.repl.exe "%%localappdata%%/saturn/plugins"  "%s"\"' % (rd))

#listoftests BrilliantBomber.json default_axe_to_stellar_axe.json Selene_To_The_Rogue_LAROI_ELECTRIFIED.json Sludgehammer_To_Candy_Axe.json
if __name__ == "__main__":
    jsonpaths = sys.argv[1:]
    rdpaths = []
    if not jsonpaths:
        jsonpath = input("Please input the paths of your json plugins: ")
        #FOR TESTING
        #jsonpaths.extend(jsonpath.split(" "))
        jsonpaths.append(jsonpath)

    for jsonpath in jsonpaths:
        rdpaths.append(json_to_rd(jsonpath))

    ans = input("Would you like to compile all the plugins?. Please note you need the SSPN.repl.exe in the same folder as the python file for this to work. Type yes or no.\n").lower()
    if ans == "yes":
        for rd in rdpaths:
            rd_to_csp(rd)
        print("Done compiling! The compiled plugins have been automatically put into your plugins folder.")

    sys.exit(0)
