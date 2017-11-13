#!/usr/bin/env python3.6

import json
import time

SHORTWEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
COMPS = ["hot", "more", "profile", "cute", "list", "note", "plain","cool", "funny", "writer", "photos"]

SAMPLE_JSON_BUSINESS = "sample_dataset_business.json"
SAMPLE_JSON_CHECKIN = "sample_dataset_checkin.json"
SAMPLE_JSON_REVIEW = "sample_dataset_review.json"
SAMPLE_JSON_USER = "sample_dataset_user.json"
SAMPLE_JSON_TIP = "sample_dataset_tip.json"

FULL_JSON_BUSINESS = "yelp_academic_dataset_business.json"
FULL_JSON_CHECKIN = "yelp_academic_dataset_checkin.json"
FULL_JSON_REVIEW = "yelp_academic_dataset_review.json"
FULL_JSON_USER = "yelp_academic_dataset_user.json"
FULL_JSON_TIP = "yelp_academic_dataset_tip.json"


def csv_businesses(json_src=SAMPLE_JSON_BUSINESS):
    with open('businesses.csv', 'w') as bus_w:
        with open('attributes.csv', 'w') as attr_w:
            with open('categories.csv', 'w') as cat_w:
                bus_w.write("business_id,name,neighborhood,address," +
                    "city,state,postal_code,latitude,longitude,stars," +
                    "review_count,is_open,Mon,Tue,Wed,Thu,Fri,Sat,Sun\n")
                attr_w.write("business_id,attribute,value\n")
                cat_w.write("business_id,category\n")

                for data in read_json(json_src):
                    if data['categories']:
                        for cat in data['categories']:
                            if cat != 'None':
                                buff = data['business_id'] + "," + cat + "\n"
                                cat_w.write(buff)

                    if data['attributes']:
                        for attr in data['attributes']:
                            if attr != 'None':
                                splitter = attr.index(":")
                                attrName = attr[:splitter].strip()
                                attrVal = '"' + attr[splitter+1:].strip() + '"'
                                buff = ",".join([data['business_id'],
                                    attrName, attrVal]) + "\n"
                                attr_w.write(buff)

                    times = [''] * 7
                    if data['hours']:
                        for hours in data['hours']:
                            values = hours.split(" ")
                            times[SHORTWEEKDAYS.index(values[0])] = values[1]

                    buff = ",".join([data['business_id'],
                        '"' + data['name'] + '"',
                        '"' + data['neighborhood'] + '"',
                        '"' + data['address'] + '"',
                        data['city'],
                        data['state'],
                        data['postal_code'],
                        str(data['latitude']),
                        str(data['longitude']),
                        str(data['stars']),
                        str(data['review_count']),
                        str(data['is_open'])] + times) + "\n"
                    bus_w.write(buff)


def csv_checkins(json_src=SAMPLE_JSON_CHECKIN):
    with open('checkins.csv', 'w') as fw:
        fw.write("business_id")
        for day in SHORTWEEKDAYS:
            for hour in range(24):
                fw.write("," + day + str(hour))
        fw.write("\n")

        for data in read_json(json_src):
            times, counts = [], []
            for day in SHORTWEEKDAYS:
                for hour in range(24):
                    times.append(day + "-" + str(hour))
                    counts.append('NULL')

            for time in data['time']:
                values = time.split(":")
                counts[times.index(values[0])] = values[1]

            buff = ",".join([data['business_id']] + counts) + "\n"
            fw.write(buff)


def csv_reviews(json_src=SAMPLE_JSON_REVIEW):
    with open('reviews.csv', 'w') as fw:
        fw.write("review_id,user_id,business_id,stars," +
            "year,month,day,text,useful,funny,cool\n")

        for data in read_json(json_src):
            date = data['date'].split("-")

            buff = ",".join([data['review_id'],
                data['user_id'],
                data['business_id'],
                str(data['stars']),
                date[0], date[1], date[2],
                '"'+data['text'].replace('"',"'").replace("\n"," ")+'"',
                str(data['useful']),
                str(data['funny']),
                str(data['cool'])]) + "\n"
            fw.write(buff)


def csv_tips(json_src=SAMPLE_JSON_TIP):
    with open('tips.csv', 'w') as fw:
        fw.write("user_id,business_id,year,month,day,likes,text\n")

        for data in read_json(json_src):
            date = data['date'].split("-")

            buff = ",".join([data['user_id'],
                data['business_id'],
                date[0], date[1], date[2],
                str(data['likes']),
                '"' + data['text'].replace('"',"'").replace("\n"," ") + '"'
                ]) + "\n"
            fw.write(buff)


def csv_users(json_src=SAMPLE_JSON_USER):
    with open('users.csv', 'w') as users_w:
        with open('friends.csv', 'w') as friends_w:
            users_w.write("user_id,name,review_count,year,month,day," +
                "useful,funny,cool,fans,average_stars,")
            for i in COMPS:
                users_w.write("compliment_{},".format(i))
            for i in range(2004, 2017):
                users_w.write("{},".format(i))
            users_w.write("2017\n")
            friends_w.write("user_id,friend_user_id\n")

            for data in read_json(json_src):
                yelping_since = data['yelping_since'].split("-")

                elite_years = ['0'] * 14
                for year in data['elite']:
                    if year != 'None':
                        elite_years[int(year) - 2004] = '1'

                buff = ",".join([data['user_id'],
                    '"' + data['name'] + '"',
                    str(data['review_count']),
                    yelping_since[0], yelping_since[1], yelping_since[2],
                    str(data['useful']),
                    str(data['funny']),
                    str(data['cool']),
                    str(data['fans']),
                    str(data['average_stars'])] + 
                    [str(data['compliment_{}'.format(i)]) for i in COMPS] +
                    elite_years) + "\n"
                users_w.write(buff)

                for friend in data['friends']:
                    if friend != 'None':
                        buff = data['user_id'] + "," + friend + "\n"
                        friends_w.write(buff)


# note for self: yelp_academic_dataset_business.json has 144072 lines
def get_businesses(src=FULL_JSON_BUSINESS, sample_size=700):
    businesses = []
    check_sample = True

    # open full json file to parse
    with open(src) as f:
        for i, line in enumerate(f):
            if len(businesses) >= sample_size:
                break

            # sample every 100th business or if previously
            # sampled business did not pass consistency/sanity checks
            if check_sample or i%100 == 0:
                check_sample = True
                data = json.loads(line)

                # business table sanity checks
                if ("business_id" in data and "name" in data and "neighborhood" in data and "address" in data and "city" in data and
                        "state" in data and "postal_code" in data and "latitude" in data and "longitude" in data and "stars" in data and
                        "review_count" in data and "is_open" in data and
                        "attributes" in data and
                        "categories" in data and
                        "hours" in data and "type" in data and data["business_id"] and data["stars"] >= 0 and data["stars"] <= 5 and
                        data["review_count"] >= 200 and data["review_count"] <= 300 and data["is_open"] == 1 and type(data["hours"]) == type([]) and
                        len(data["hours"]) == 7):
                    check_sample = False
                    for k, hours in enumerate(data["hours"]):
                        day, times = hours.split()
                        starttime, endtime = times.split("-")
                        if not (day in WEEKDAYS and
                                ":0" in starttime and
                                ":0" in endtime):
                            check_sample = True
                            break
                        shortday = SHORTWEEKDAYS[WEEKDAYS.index(day)]
                        data["hours"][k] = hours.replace(":0", "") \
                                                .replace(day, shortday)

                # ignore next business(es) if current businsse
                # passes consistency/sanity checks
                if not check_sample:
                    businesses.append(data)
    return businesses


def get_checkins(businesses, src=FULL_JSON_CHECKIN):
    checkins = []
    business_ids = [i["business_id"] for i in businesses]
    business_ids_set = set(business_ids)

    with open(src) as f:
        for i, line in enumerate(f):
            data = json.loads(line)
            
            if not ("business_id" in data and
                    "time" in data and
                    "type" in data and
                    data["business_id"] in business_ids_set and
                    type(data["time"]) == type([])):
                continue

            for k, times in enumerate(data["time"]):
                weekday, stats = times.split("-")
                hour, num_checks = [int(x) for x in stats.split(":")]
                if not (weekday in SHORTWEEKDAYS and
                        hour >= 0 and hour < 24 and
                        num_checks >= 0):
                    continue

                if num_checks > 0:
                    idx = business_ids.index(data["business_id"])
                    for l in businesses[idx]["hours"]:
                        if weekday in l:
                            hours = l.split()[1]
                            break
                    starttime, endtime = [int(x) for x in hours.split("-")]
                    tmp_endtime, tmp_hour = endtime, hour
                    if endtime <= starttime:
                        tmp_endtime += 24
                    if hour <= starttime:
                        tmp_hour += 24
                    if tmp_hour < starttime or tmp_hour > tmp_endtime:
                        data["time"][k] = "{}-{}:NULL".format(weekday, hour)
            checkins.append(data)
    return checkins


def get_reviews(businesses, src=FULL_JSON_REVIEW):
    reviews = []

    business_ids = [i["business_id"] for i in businesses]
    business_ids_set = set(business_ids)
    business_review_count = [0] * len(businesses)

    with open(src) as f:
        for i, line in enumerate(f):
            data = json.loads(line)

            if not ("business_id" in data and
                    "review_id" in data and
                    "user_id" in data and
                    "stars" in data and
                    "date" in data and
                    "text" in data and
                    "useful" in data and
                    "funny" in data and
                    "cool" in data and
                    "type" in data and
                    data["business_id"] in business_ids_set and
                    valid_date(data["date"])):
                continue

            idx = business_ids.index(data["business_id"])
            if business_review_count[idx] >= businesses[idx]["review_count"]:
                continue
            business_review_count[idx] += 1

            data["stars"] = max(0, min(5, data["stars"]))
            data["useful"] = max(0, data["useful"])
            data["funny"] = max(0, data["funny"])
            data["cool"] = max(0, data["cool"])

            reviews.append(data)
    return reviews


def get_tips(businesses, users, src=FULL_JSON_TIP):
    tips = []
    business_ids_set = set([i["business_id"] for i in businesses])
    user_ids_set = set([i["user_id"] for i in users])

    with open(src) as f:
        for i, line in enumerate(f):
            data = json.loads(line)

            if not ("user_id" in data and
                    "business_id" in data and
                    "text" in data and
                    "date" in data and
                    "likes" in data and
                    "type" in data and
                    data["business_id"] in business_ids_set and
                    data["user_id"] in user_ids_set and
                    valid_date(data["date"])):
                continue

            data["likes"] = max(0, data["likes"])
            tips.append(data)
    return tips


def get_users(reviews, src=FULL_JSON_USER):
    users = []
    user_ids_set = set([i["user_id"] for i in reviews])

    with open(src) as f:
        for i, line in enumerate(f):
            data = json.loads(line)

            if not ("user_id" in data and
                    "name" in data and
                    "review_count" in data and
                    "yelping_since" in data and
                    "friends" in data and
                    "useful" in data and
                    "funny" in data and
                    "cool" in data and
                    "fans" in data and
                    "elite" in data and
                    "average_stars" in data and
                    "type" in data and
                    data["user_id"] in user_ids_set and
                    valid_date(data["yelping_since"])):
                continue

            data["average_stars"] = max(0, min(5, data["average_stars"]))
            data["useful"] = max(0, data["useful"])
            data["funny"] = max(0, data["funny"])
            data["cool"] = max(0, data["cool"])
            data["review_count"] = max(0, data["review_count"])
            data["fans"] = max(0, data["fans"])

            continueloop = False
            for comp in COMPS:
                comp = "compliment_{}".format(comp)
                if comp not in data:
                    continueloop = True
                    break
                data[comp] = max(0, data[comp])
            if continueloop:
                continue

            elite_years = ["None"]
            if data["elite"][0] != "None":
                elite_years = set()
                for year in data["elite"]:
                    year = int(year)
                    if year >= 2004 and year <= 2017:
                        elite_years.add(year)

            data["elite"] = list(elite_years)
            data["friends"] = list(user_ids_set.intersection(data["friends"]))
            users.append(data)
    return users


def main():
    print("\nInitiating data sampling...\n")

    # businesses sampled as reference point
    timestamp = time.time()
    sample_businesses = get_businesses()
    print("{}: {} ({:.0f}ms)" .format("businesses found".ljust(20), len(sample_businesses), 1000 * (time.time() - timestamp)))

    # checkins expected/found
    print("{}: {}" .format("checkins expected".ljust(20), len(sample_businesses)))
    timestamp = time.time()
    sample_checkins = get_checkins(sample_businesses)
    print("{}: {} ({:.0f}ms)"
        .format("checkins found".ljust(20),
        len(sample_checkins),
        1000 * (time.time() - timestamp)))

    # reviews expected/found
    print("{}: {}"
        .format("reviews expected".ljust(20),
        sum([i["review_count"] for i in sample_businesses])))
    timestamp = time.time()
    sample_reviews = get_reviews(sample_businesses)
    print("{}: {} ({:.0f}ms)"
        .format("reviews found".ljust(20),
        len(sample_reviews),
        1000 * (time.time() - timestamp)))

    # users expected/found
    print("{}: {}"
        .format("users expected".ljust(20),
        len(set([i["user_id"] for i in sample_reviews]))))
    timestamp = time.time()
    sample_users = get_users(sample_reviews)
    print("{}: {} ({:.0f}ms)"
        .format("users found".ljust(20),
        len(sample_users),
        1000 * (time.time() - timestamp)))

    # tips found
    timestamp = time.time()
    sample_tips = get_tips(sample_businesses, sample_users)
    print("{}: {} ({:.0f}ms)\n\nDumping raw JSON samples...\n"
        .format("tips found".ljust(20),
        len(sample_tips),
        1000 * (time.time() - timestamp)))

    timestamp = time.time()
    with open(SAMPLE_JSON_BUSINESS, "w") as fw:
        json.dump(sample_businesses, fw)
    with open(SAMPLE_JSON_CHECKIN, "w") as fw:
        json.dump(sample_checkins, fw)
    with open(SAMPLE_JSON_REVIEW, "w") as fw:
        json.dump(sample_reviews, fw)
    with open(SAMPLE_JSON_USER, "w") as fw:
        json.dump(sample_users, fw)
    with open(SAMPLE_JSON_TIP, "w") as fw:
        json.dump(sample_tips, fw)
    print("JSON dump complete ({:.0f}ms).\n\nExporting CSV files...\n"
        .format(1000 * (time.time() - timestamp)))

    timestamp = time.time()
    csv_businesses()
    print("Exported businesses JSON to CSV ({:.0f}ms)."
        .format(1000 * (time.time() - timestamp)))
    timestamp = time.time()
    csv_checkins()
    print("Exported checkins JSON to CSV ({:.0f}ms)."
        .format(1000 * (time.time() - timestamp)))
    timestamp = time.time()
    csv_reviews()
    print("Exported reviews JSON to CSV ({:.0f}ms)."
        .format(1000 * (time.time() - timestamp)))
    timestamp = time.time()
    csv_users()
    print("Exported users JSON to CSV ({:.0f}ms)."
        .format(1000 * (time.time() - timestamp)))
    timestamp = time.time()
    csv_tips()
    print("Exported tips JSON to CSV ({:.0f}ms).\n\nSUCCESS!\n"
        .format(1000 * (time.time() - timestamp)))


def read_json(src):
    with open(src) as f:
        return json.load(f)


def valid_date(date):
    try:
        year, month, day = [int(x) for x in date.split("-")]
        if (year < 2004 or year > 2017 or
                month < 0 or month > 12 or
                day < 0 or day > 31):
            return False
    except:
        return False

    return True


if __name__ == "__main__":
    main()
