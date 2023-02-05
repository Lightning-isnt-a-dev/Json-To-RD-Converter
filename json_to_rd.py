import json
import os, sys

#input("Please input the path of your json plugin: ")

jsonpath = input("Please input the path of your json plugin: ")

if os.path.exists(jsonpath):
    try :
        x = json.load(open(jsonpath, encoding='utf-8'))
    except UnicodeDecodeError:
        sys.exit('Oops! Something happened. Report the error on github or to me on discord: Lightning#2538')
else:
    print("Theres something wrong with your path. Try again.")

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
wfile = open(os.path.basename(jsonpath).split(".")[0] + ".rd", "w", encoding="utf-8")
wfile.write("#file plugin\n")
for sign, sign_name in signs:
    signing = ('sign: "%s", "%s"\n' % (sign_name, x[sign]))
    wfile.write(signing)
print("Wrote signs!")

swapar = 0
print("Writing imports and swaps...")

difjsonassets = ""

if difjson == True:
    difjsonassets = x["swaps"]
elif difjson == False:
    difjsonassets = x["Assets"]
    
for asset in difjsonassets:
    try:
        AssetPathTo = asset["AssetPathTo"]
    except KeyError:
        pathtoexists = False
    else:
        pathtoexists = True

    if pathtoexists == True:
        AssetPathTo = asset["AssetPathTo"]
        AssetPath = asset["AssetPath"]
        if swapar != 0:
            wfile.write("from_ar.Swap(to_ar)\n\n")
            toar = "\nto_ar = import \"" + AssetPathTo + "\" "
            wfile.write(toar)
            fromar = "\nfrom_ar = import \"" + AssetPath + "\" \n\n"
            wfile.write(fromar)
        else:
            toar = "\nto_ar = import \"" + AssetPathTo + "\" "
            wfile.write(toar)
            fromar = "\nfrom_ar = import \"" + AssetPath + "\" \n\n"
            wfile.write(fromar)
            swapar = 1
    elif pathtoexists == False:
        AssetPath = asset["AssetPath"]
        fromar = "from_ar = import \"" + AssetPath + "\" \n"
        wfile.write(fromar)

    try:
        swaps = asset["Swaps"]
    except KeyError:
        swaps = asset["swaps"]
    else:
        swaps = asset["Swaps"]
    if difjson == True:
        print(x["swaps"])
    
    elif difjson == False:
        swaps = asset["Swaps"]
        try:
            swaps_sorted = sorted(swaps, key=lambda d: len(d['replace']), reverse=True)
        except TypeError:
            swapsarenull = True
        else:
            swapsarenull = False
        if swapsarenull == True:
            break
        elif swapsarenull == False:
            for swap in swaps_sorted:
                searchstring = swap["search"]
                replacestring = swap["replace"]
                if replacestring == "/":
                    wstring = "/"
                elif replacestring.__contains__("Base"):
                    break
                else:
                    wstring = os.path.basename(replacestring).split(".")[1]
                    wstringlong = os.path.basename(replacestring).split(".")[0]
                sstring = os.path.basename(searchstring).split(".")[1]
                sstringlong = os.path.basename(searchstring).split(".")[0]

                dirandstring = os.path.dirname(searchstring) + "/" + sstringlong
                dirandwrite = os.path.dirname(replacestring) + "/" + wstringlong

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
print("Wrote imports and swaps!")


newpath = os.path.basename(jsonpath).split(".")[0] + ".rd"
rdpath = os.path.dirname(jsonpath) + "/" + newpath

wfile.close()

if pathtoexists == True and swapsarenull == True:
    with open(rdpath, "a") as appending:
        appending.write("from_ar.Swap(to_ar)\n")
        appending.flush()

print("We will now compile the plugin. Please note you need the SSPN.repl.exe in the same folder as the python file for this to work. Continue? Type yes or no.")

q = input("").lower()
while q != "yes" or q != "no":
    if q == "no":
        sys.exit()
    elif q == "yes":
        os.system('cmd /k \"SSPN.repl.exe "%%localappdata%%/saturn/plugins"  "%s"\"' % (rdpath))
        print("Done compiling! The compiled plugin has been automatically put into your plugins folder.")
        sys.exit
    else:
        print("You did something wrong. Please try again.")
        sys.exit
