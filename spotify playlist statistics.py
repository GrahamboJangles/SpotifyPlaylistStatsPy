import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "your_client_id"
client_secret = "your_client_secret"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Power Workout
playlist_url = "https://open.spotify.com/playlist/37i9dQZF1DWUVpAXiEPK8P"
# R&B Christmas
playlist_url = "https://open.spotify.com/playlist/37i9dQZF1DX4ELVW61Sklr"

print_individual = True

playlist_id = playlist_url.split("/")[-1]
playlist_id = playlist_id.split('&')[0]
# print(playlist_id)

try:
    results = sp.playlist_tracks(playlist_id)
except spotipy.exceptions.SpotifyException as e:
    print(e)
    if "album" in playlist_url:
        raise Exception("The spotify API does not allow entering album URLs")
    raise Exception("Please enter a valid playlist URL")

# Create a dictionary to map the numerical values of keys to letters
key_mapping = {
    0: "C",
    1: "C#/Db",
    2: "D",
    3: "D#/Eb",
    4: "E",
    5: "F",
    6: "F#/Gb",
    7: "G",
    8: "G#/Ab",
    9: "A",
    10: "A#/Bb",
    11: "B"
}

# Create variables to store the sum of the BPMs and the counts of each key letter
bpm_sum = 0
key_counts = {}

danceability_list = []
energy_list = []
loudness_list = []
speechiness_list = []
acousticness_list = []
instrumentalness_list = []
liveness_list = []
# Valence is a measure of musical positiveness, a high score is happy, low is sad song
valence_list = []
duration_ms_list = []
time_signature_list = []

for track in results['items']:
    try:
        track_id = track['track']['id']
    except TypeError:
        continue

    audio_features = sp.audio_features(track_id)
    # for audio_feature in audio_features:
    #     print(f"audio feature: {audio_feature}")
    track_info = sp.track(track_id)
    

    # Use the dictionary to map the numerical values of keys to letters
    key = audio_features[0]['key']
    key_letter = key_mapping[key]

    # Add the BPM to the BPM sum
    bpm_sum += audio_features[0]['tempo']

    # Increase the count of the key letter in the dictionary
    if key_letter not in key_counts:
        key_counts[key_letter] = 1
    else:
        key_counts[key_letter] += 1

    key = audio_features[0]['key']
    bpm = audio_features[0]['tempo']
    mode = audio_features[0]['mode']
    danceability = audio_features[0]['danceability']
    energy = audio_features[0]['energy']
    loudness = audio_features[0]['loudness']
    speechiness = audio_features[0]['speechiness']
    acousticness = audio_features[0]['acousticness']
    instrumentalness = audio_features[0]['instrumentalness']
    liveness = audio_features[0]['liveness']
    valence = audio_features[0]['valence']
    duration_ms = audio_features[0]['duration_ms']
    time_signature = audio_features[0]['time_signature']
    
    mode_mapping = {0: "minor", 1: "major"}
    mode_string = mode_mapping[mode]

    danceability_list.append(danceability)
    energy_list.append(energy)
    loudness_list.append(loudness)
    speechiness_list.append(speechiness)
    acousticness_list.append(acousticness)
    instrumentalness_list.append(instrumentalness)
    liveness_list.append(liveness)
    valence_list.append(valence)
    duration_ms_list.append(duration_ms)
    time_signature_list.append(time_signature)

    if print_individual:
        print(f"Track: {track['track']['name']}")
        # print(f"Key: {key}")
        # Print the key in letter form
        print(f"Key: {key_letter}")
        print(f"Mode: {mode_string}")
        print(f"BPM: {bpm}")
        print(f"Danceability: {danceability}")
        print(f"Energy: {energy}")
        print(f"Loudness: {loudness}")
        print(f"Speechiness: {speechiness}")
        print(f"Acousticness: {acousticness}")
        print(f"Instrumentalness: {instrumentalness}")
        print(f"Liveness: {liveness}")
        print(f"Valence: {valence}")
        print(f"Duration: {duration_ms}")
        print(f"Time Signature: {time_signature}")
        print("--------------------------------------")
    

# Calculate the average BPM by dividing the BPM sum by the number of tracks
average_bpm = bpm_sum / len(results['items'])

average_danceability = sum(danceability_list) / len(results['items'])
average_energy = sum(energy_list) / len(results['items'])
average_loudness = sum(loudness_list) / len(results['items'])
average_speechiness = sum(speechiness_list) / len(results['items'])
average_acousticness = sum(acousticness_list) / len(results['items'])
average_instrumentalness = sum(instrumentalness_list) / len(results['items'])
average_liveness = sum(liveness_list) / len(results['items'])
average_valence = sum(valence_list) / len(results['items'])
average_duration_ms = sum(duration_ms_list) / len(results['items'])
minutes = int(average_duration_ms / 60000)
seconds = int((average_duration_ms % 60000) / 1000)

formatted_duration = f"{minutes}:{seconds:02d}"

average_time_signature = sum(time_signature_list) / len(results['items'])

# Find the most frequent key letter by finding the key with the maximum value in the dictionary
most_frequent_key_letter = max(key_counts, key=key_counts.get)

# Print the average BPM and the most frequent key
print("Average BPM:", average_bpm)
print("Most frequent key:", most_frequent_key_letter)

print("average_danceability:", average_danceability)
print("average_energy:", average_energy)
print("average_loudness:", average_loudness)
print("average_speechiness:", average_speechiness)
print("average_acousticness:", average_acousticness)
print("average_instrumentalness:", average_instrumentalness)
print("average_liveness:", average_liveness)
print("average_valence:", average_valence)
print("average_duration:", formatted_duration)
print("average_time_signature:", average_time_signature)