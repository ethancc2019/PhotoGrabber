espnPlayers = {}
with open("MASTERPLAYERS(ESPN).txt") as f:
    for line in f:
        splitValue = line.split(",")
        espnPlayers[splitValue[0]] = splitValue[1]

        # reset values
        splitValue = ""

for key,val in espnPlayers.items():
    print(key + " => " + val)
print("DONE!")
