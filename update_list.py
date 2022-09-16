import json
import requests

if __name__ == '__main__':
	# read client ID, client secret, and refresh token
	with open('client_data.json') as file:
		data = json.load(file)
		client_id = data['CLIENT_ID']
		client_secret = data['CLIENT_SECRET']

	with open('token.json') as file:
		data = json.load(file)
		refresh_token = data['refresh_token']

	# then request a new access token and save it to file
	url = 'https://myanimelist.net/v1/oauth2/token'

	response = requests.post(url, data = {
		'client_id': client_id,
		'client_secret': client_secret,
		'grant_type': 'refresh_token',
		'refresh_token': refresh_token
	})

	response.raise_for_status()
	token = response.json()
	response.close()

	with open('token.json', 'w') as file:
		json.dump(token, file, indent = 4)

	access_token = token['access_token']

	# fetch top 500 most popular anime
	url = 'https://api.myanimelist.net/v2/anime/ranking?ranking_type=bypopularity&limit=500'
	response1 = requests.get(url, headers = {
		'Authorization': f'Bearer {access_token}'
	})

	response1.raise_for_status()
	animes1 = response1.json()
	response1.close()

	# fetch next 500 most popular anime for 1000 total
	url = 'https://api.myanimelist.net/v2/anime/ranking?ranking_type=bypopularity&limit=500&offset=500'
	response2 = requests.get(url, headers = {
		'Authorization': f'Bearer {access_token}'
	})

	response2.raise_for_status()
	animes2 = response2.json()
	response2.close()

	# fetch top 200 highest rated anime
	url = 'https://api.myanimelist.net/v2/anime/ranking?ranking_type=all&limit=200'
	response3 = requests.get(url, headers = {
		'Authorization': f'Bearer {access_token}'
	})

	response3.raise_for_status()
	animes3 = response3.json()
	response3.close()

	with open('docs/anime_list.js', 'w', encoding='utf-8') as file:
		# merge all three sets of animes, handling special characters and removing duplicates
		anime_list = []
		animes = animes1['data'] + animes2['data'] + animes3['data']
		for anime in animes:
			anime_list.append(anime['node']['title'].replace("\"", "'"))
		anime_list = list(set(anime_list))

		# format the list into a Javascript array and write that to the list file
		anime_list_txt = 'var anime_list = [\n'
		for anime in anime_list:
			anime_list_txt += f'\"{anime}\",\n'
		anime_list_txt += ']\n'

		file.write(anime_list_txt)