import pandas as pd
import requests
import json
import time

def thething(strava_tokens, ind):
    idofathlete = strava_tokens['athlete']['id']

    ## If access_token has expired then use the refresh_token to get the new access_token
    if strava_tokens['expires_at'] < time.time():
        print("🔐-access_token expired. Requesting new access_token-🔐.")
        #Make Strava auth API call with current refresh token
        response = requests.post(
                            url = 'https://www.strava.com/oauth/token',
                            data = {
                                    'client_id': INSERT_ID_HERE,
                                    'client_secret': 'INSERT CLIENT SECRET HERE',
                                    'grant_type': 'refresh_token',
                                    'refresh_token': strava_tokens['refresh_token']
                                    }
                        )

        #Save response as json in new variable
        new_strava_tokens = response.json()
        # Save new tokens to file
        # with open('strava_tokens.json', 'w') as outfile:
        #     json.dump(new_strava_tokens, outfile)
        #Use new Strava tokens from now
        strava_tokens = new_strava_tokens

    # set start_date_local as yesterday.
    nowtime = time.time();
    cutoffday_midnight = (int(nowtime // 86400)) * 86400 - (10*86400) - 19800;
    # 19800 to deduct 5:30 Hrs to

    # Loop through all activities
    page = 1
    url = "https://www.strava.com/api/v3/activities"
    access_token = strava_tokens['access_token']
    print(access_token)
    
    ## Create the dataframe ready for the API call to store your activity data
    activities = pd.DataFrame(
        columns = [
                "athlete_id",
                "id",
                "name",
                "start_date_local",
                "distance",
                "moving_time",
                "elapsed_time",
                "total_elevation_gain"
        ]
    )

    while True:

        # get page of activities from Strava
        r = requests.get(url + '?access_token=' + access_token + '&per_page=10'+'&after='+ str(cutoffday_midnight) + '&page=' + str(page))
        r = r.json()
        # if no results then exit loop
        if (not r) and (page != 1):
            break
        elif (not r) and (page == 1):
            print("❌-This person didn't do any activites-❌")
            activities.loc[0,'athlete_id'] = idofathlete
            break
        
        #print(json.dumps(r))
        # otherwise add new data to dataframe
        for x in range(len(r)):
            if (r[x]['type'] == 'Ride'):
                activities.loc[x + (page-1)*30,'athlete_id'] = r[x]['athlete']['id']
                activities.loc[x + (page-1)*30,'id'] = r[x]['id']
                activities.loc[x + (page-1)*30,'name'] = r[x]['name']
                activities.loc[x + (page-1)*30,'start_date_local'] = r[x]['start_date_local']
                activities.loc[x + (page-1)*30,'distance'] = r[x]['distance']
                activities.loc[x + (page-1)*30,'moving_time'] = r[x]['moving_time']
                activities.loc[x + (page-1)*30,'elapsed_time'] = r[x]['elapsed_time']
                activities.loc[x + (page-1)*30,'total_elevation_gain'] = r[x]['total_elevation_gain']
        # increment page
        page += 1
    
    print("👆-------"+str(ind)+"-------👆")
    activities.to_csv('day_activity.csv', mode='a', index=False, header=False)

# Main code
oct_kcc = pd.read_csv('octkcc.csv')

for index, row in oct_kcc.iterrows():
    #print(row['athlet_id'])
    print(row['profile_json'])
    jaison = json.loads(row['profile_json'])
    #print(jaison['access_token'])
    thething(jaison, int(index))
