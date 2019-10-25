import datetime
import time
import random
import requests


def main():
    sleep_min = 60
    sleep_max = 120

    # file_type = "html"
    # file_type = "csv"
    file_type = "json"
    language = "en"
    url_BFIAUU1 = f"https://www.twse.com.tw/{language}/block/BFIAUU?response={file_type}&date="
    url_BFIAUU2 = "&selectType=S"

    date_start = "20191001"
    date = datetime.datetime(int(date_start[:4]), int(date_start[4:6]), int(date_start[6:]))
    date_now = datetime.datetime.now()

    while date <= date_now:
        date_string = date.strftime("%Y%m%d")
        print(f"Going to get BFIAUU at date {date_string}.")
        url_BFIAUU3 = f"&_={str(int(time.time() * 1000))}"  # this parameter seems not necessary
        url = f"{url_BFIAUU1}{date_string}{url_BFIAUU2}{url_BFIAUU3}"

        try:
            res = requests.get(url)
        except ConnectionError:
            print("Can not connect to twse, need wait and retry.")
            time.sleep(random.randint(sleep_min, sleep_max))
            continue

        # html
        # I think just need to parse tags <tbody></tbody> and <td></td>.
        # But in this case it seems that get csv or json version would be better.

        # csv
        # filename = f"BFIAUU{date_string}.csv"
        # file = open(filename, 'wb')
        # file.write(res.content)
        # file.close()
        
        # json
        res_json = res.json()
        filename = f"BFIAUU{date_string}.csv"
        file = open(filename, 'w')

        if 'data' not in res_json:
            print("key 'data' not in res_json, retry.")
            continue

        for row in res_json['data']:
            # columns are
            # res_json['fields'][0] "Security Code"
            # res_json['fields'][1] "Trading Classification"
            # res_json['fields'][2] "Trade Price"
            # res_json['fields'][3] "Trade Volume"
            # res_json['fields'][4] "Trade Value"

            file.write(",".join(row) + "\n")
        file.close()

        print("Sleeping...")
        time.sleep(random.randint(sleep_min, sleep_max))  # sleep for a while for preventing blocked by twse
        date += datetime.timedelta(days=1)
    
    print(f"Finished all jos, last date is {date_string}")


if __name__ == "__main__":
    main()