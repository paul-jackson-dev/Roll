import json

while True:
    # print("----------------------")
    print("o : sell a put")
    print("")
    command = input("enter a command: ")

    if command == "o":
        json_object = {}
        json_object["command"] = command
        json_object["symbol"] = input("enter a symbol: ").upper()
        json_object["date"] = input("enter a date: ")
        json_object["strike"] = input("enter a strike: ")
        with open("json/" + "open_option_trade.json", 'w') as file_object:  # open the file in write mode
            json.dump(json_object, file_object)

    print("")
    print("//////////////////////")
    # print("you entered: " + command + " : " + option)
    print(json_object)
    print("//////////////////////")

    print("")
