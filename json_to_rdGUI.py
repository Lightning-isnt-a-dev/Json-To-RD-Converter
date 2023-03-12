import json, yaml
import os
import tkinter, customtkinter
import subprocess as sp
import easygui

#installed with pip: easygui, customtkinter, pyyaml

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
            #using yaml cause json doesnt like the extra comma in some plugins
            #if there are tabs, remove them because yaml doesnt like them
            yamlread = open(jsonpath, encoding='utf-8').read()
            yamlread = yamlread.replace("\t", "")
            x = yaml.safe_load(yamlread)
    elif not os.path.exists(jsonpath):
        done.configure("Path is wrong! Make sure your plugin is in the same folder as the python file.", text_color="red")
    else:
        done.configure('Oops! Something happened. Report the error on github or to me on discord: Lightning#2538', text_color="red")
    try:
        x["Name"]
    except KeyError:
        signs = [("default_name","Name"), ("swapped_icon","Icon"), ("messages", "Author")]
        difjson = True
    else:
        signs = [("Name","Name"), ("Swapicon","Icon"), ("Message", "Author")]
        difjson = False

    done.configure("Writing signs...", text_color="white")
    rdpath = os.path.basename(jsonpath).split(".")[0] + ".rd"
    wfile = open(rdpath, "w", encoding="utf-8")
    wfile.write("#file plugin\n")
    for sign, sign_name in signs:
        signing = ('sign: "%s", "%s"\n' % (sign_name, x[sign]))
        wfile.write(signing)
    done.configure("Wrote signs!", text_color="white")

    done.configure("Writing imports and swaps...", text_color="white")
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
    done.configure(text="Done converting!", text_color="white")
    wfile.close()

def rd_to_csp(rd):
    if os.path.exists(rd):
        sp.Popen('SSPN.repl.exe "%%localappdata%%/saturn/plugins"  "%s"' % (rd), shell=True)
        done.configure(text="Done compiling!", text_color="white")
    else:
        done.configure(text="Please convert your json first.", text_color="red")


#listoftests BrilliantBomber.json default_axe_to_stellar_axe.json Selene_To_The_Rogue_LAROI_ELECTRIFIED.json Sludgehammer_To_Candy_Axe.json BoogieDownToGetGriddy.json
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("500x250")
app.title("JSON to RD converter")

title = customtkinter.CTkLabel(app, text="Input the path to your json:")
title.pack(padx=10, pady=10)

pathfielddata = tkinter.StringVar()
pathfield = customtkinter.CTkEntry(app, width=350, height=40, textvariable=pathfielddata)
pathfield.pack()

done = customtkinter.CTkLabel(app, text="")
done.pack()

jsonpathbutton = customtkinter.CTkButton(app, text="Select a JSON file", command=lambda : pathfielddata.set(easygui.fileopenbox()))
jsonpathbutton.pack(padx=5, pady=5)

converttord = customtkinter.CTkButton(app, text="Convert to RD", command=lambda : json_to_rd(pathfielddata.get()))
converttord.pack(padx=5, pady=5)

converttocsp = customtkinter.CTkButton(app, text="Compile", command=lambda : rd_to_csp(os.path.basename(pathfielddata.get()).split(".")[0] + ".rd"))
converttocsp.pack(padx=5, pady=5)

app.mainloop()
