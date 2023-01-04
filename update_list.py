import requests
from requests.auth import HTTPBasicAuth

if __name__ == '__main__':
	# please don't steal my client ID
	header = {'X-MAL-CLIENT-ID': '865edc428f4197b494945019f50eb1b5'}

	# fetch top 500 most popular anime
	url = 'https://api.myanimelist.net/v2/anime/ranking?ranking_type=bypopularity&limit=500&fields=alternative_titles'
	response1 = requests.get(url, headers=header)

	response1.raise_for_status()
	animes1 = response1.json()
	response1.close()

	# fetch next 500 most popular anime for 1000 total
	url = 'https://api.myanimelist.net/v2/anime/ranking?ranking_type=bypopularity&limit=500&offset=500&fields=alternative_titles'
	response2 = requests.get(url, headers=header)

	response2.raise_for_status()
	animes2 = response2.json()
	response2.close()

	# fetch top 200 highest rated anime
	url = 'https://api.myanimelist.net/v2/anime/ranking?ranking_type=all&limit=200&fields=alternative_titles'
	response3 = requests.get(url, headers=header)

	response3.raise_for_status()
	animes3 = response3.json()
	response3.close()

	with open('docs/anime_list.js', 'w', encoding='utf-8') as file:
		anime_list = []
		animes = animes1['data'] + animes2['data'] + animes3['data']
		for anime in animes:
			# add the default and English title of each anime to the list
			title = anime['node']['title']
			title_en = anime['node']['alternative_titles']['en']
			if title_en == title or title_en == "":
				anime_list.append(title.replace("\"", "'"))
			else:
				anime_list.append((f'{title} / {title_en}').replace("\"", "'"))
		# remove duplicate entries
		anime_id_list = list(set(anime_list))

		# format the list into a Javascript array and write that to the list file
		anime_list_txt = 'var anime_list = [\n'
		for anime in anime_list:
			anime_list_txt += f'\"{anime}\",\n'
		anime_list_txt += ']\n'

		file.write(anime_list_txt)