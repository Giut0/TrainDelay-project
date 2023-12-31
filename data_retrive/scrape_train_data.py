import requests
from datetime import date

LAST_TRAIN_ID = 36967

detection_date = date.today()
f = open("../dataset/trains_29_08_2023.csv", "w+")
f.write("train_ID,origin,arrival,departure_time,arrival_time,delay,train_type,detection_date\n")

for trainID in range(LAST_TRAIN_ID):
    x = requests.get(f'http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/cercaNumeroTreno/{trainID}')
    # Check the existence of a train with that id 
    if x.status_code == 200:
        train_info = x.json()
        origin_stationID = train_info["codLocOrig"]
        temp = train_info["dataPartenza"]
        try: 
            # Take info of train route 
            y = requests.get(f"http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/andamentoTreno/{origin_stationID}/{trainID}/{temp}")
            train_route_info = y.json()
            origin = train_route_info["origine"]
            arrival = train_route_info["destinazione"]
            departure_time = train_route_info["compOrarioPartenzaZeroEffettivo"]
            arrival_time = train_route_info["compOrarioArrivoZeroEffettivo"]
            delay  = train_route_info["ritardo"]
            train_type = train_route_info["compTipologiaTreno"]
            # Save selected info in a csv file
            string = f"{trainID},{origin},{arrival},{departure_time},{arrival_time},{delay},{train_type},{detection_date}\n"
            f.write(string)
        except:
            print("Error")
f.close()
