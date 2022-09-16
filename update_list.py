import json
import requests

if __name__ == '__main__':
	with open('token.json') as file:
		data = json.load(file)
		access_token = data['access_token']

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
		list(set(anime_list))

		# format the list into a Javascript array and write that to the list file
		anime_list_txt = 'var anime_list = [\n'
		for anime in anime_list:
			anime_list_txt += f'\"{anime}\",\n'
		anime_list_txt += ']\n'

		file.write(anime_list_txt)