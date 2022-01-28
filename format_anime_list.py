# with open('anime_list.txt', encoding = 'utf-8') as anime_list:
# 	animes = anime_list.readlines()
# 	animes = [anime.replace('\n', '').replace('"', "'") for anime in animes]
# 	animes = '",\n"'.join(animes)
# 	animes = 'var anime_list = [\n"' + animes + '"\n]'
#
# 	with open('docs/anime_list.js', 'w', encoding = 'utf-8') as output:
# 		output.write(animes)

# the above, compacted into two lines for shits and giggles
with open('anime_list.txt', encoding = 'utf-8') as al, open('docs/anime_list.js', 'w', encoding = 'utf-8') as o:
		o.write('var anime_list = [\n"' + '",\n"'.join([a.replace('\n', '').replace('"', "'") for a in al.readlines()]) + '"\n]')