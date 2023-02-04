import json
import os, sys

#str(input("Please input the path of your json plugin: ")) 

jsonpath = input("Please input the path of your json plugin: ")

if os.path.exists(jsonpath):
    x = json.load(open(jsonpath))
else:
    print("Theres something wrong with your path. Try again.")

#checksigns = ["Name", "default_name"]

#for sign in x:
#    if sign == "Name":
#        sys.exit()
#    elif sign == "default_name":
#        print("Detected")
#        sys.exit

signs = [("Name","Name"), ("Swapicon","Icon"), ("Message", "Author")]

print("Writing signs...")
wfile = open(os.path.basename(jsonpath).split(".")[0] + ".rd", "w")
wfile.write("#file plugin\n")
for sign, sign_name in signs:
    signing = ('sign: "%s", "%s"\n' % (sign_name, x[sign]))
    wfile.write(signing)
print("Wrote signs!")

imports = [("AssetPath", "from_ar = import")]
swapargs = [("search", "from_ar.Seek("), ("replace", "from_ar.Write<string>(")]

for asset in x["Assets"]:
    AssetPath = asset["AssetPath"]
    print("Writing imports and swaps...")
    for apath, importing in imports:
        wimports = ('\n%s "%s" \n\n' % (importing, asset[apath]))
        wfile.write(wimports)

    swaps = asset["Swaps"]
    swaps_sorted = sorted(swaps, key=lambda d: len(d['replace']), reverse=True)
    for swap in swaps_sorted:
        searchstring = swap["search"]
        replacestring = swap["replace"]
        if replacestring == "/":
            wstring = "/"
        else:
            wstring = os.path.basename(replacestring).split(".")[0]
        sstring = os.path.basename(searchstring).split(".")[0]

        dirandstring = os.path.dirname(searchstring) + "/" + sstring
        dirandwrite = os.path.dirname(replacestring) + "/" + wstring

        wfile.write("from_ar.Seek(\"" + dirandstring + "\")" + "\n")
        wfile.write("from_ar.Write<string>(\"" + dirandwrite + "\")" + "\n\n")

        wfile.write("from_ar.Seek(\"" + sstring + "\")" + "\n")
        wfile.write("from_ar.Write<string>(\"" + wstring + "\")" + "\n\n")
wfile.close()


print("We will now compile the plugin. Please note you need the SSPN.repl.exe in the same folder as the python file for this to work. Continue? Type yes or no.")
q = input("").lower()
while q != "yes" or q != "no":
    if q == "no":
        sys.exit()
    elif q == "yes":
        outputpath = input("Please input an output path for your plugin: ")
    else:
        print("You did something wrong. Please try again.")
        sys.exit

newpath = os.path.basename(jsonpath).split(".")[0] + ".rd"
rdpath = os.path.dirname(jsonpath) + "/" + newpath

if os.path.exists(outputpath) == True:
    os.system('cmd /k \"SSPN.repl.exe "%s" "%s"\"' % (outputpath, rdpath))
else:
    print("Something went wrong. Please try again.")

print("Done!")
