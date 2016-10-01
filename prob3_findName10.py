
combined = open('/Users/lijiahui/Desktop/Prj2/project_2_data/combined.txt', 'r')
combined_list=[]
for line in combined:
     combined_list.append(line)
     


NameTop1 = 180966
print combined_list[NameTop1][0:combined_list[NameTop1].find('\t')]

NameTop2 = 66948
print combined_list[NameTop2][0:combined_list[NameTop2].find('\t')]

NameTop3 = 57601
print combined_list[NameTop3][0:combined_list[NameTop3].find('\t')]

NameTop4 = 13715
print combined_list[NameTop4][0:combined_list[NameTop4].find('\t')]

NameTop5 = 70569
print combined_list[NameTop5][0:combined_list[NameTop5].find('\t')]

NameTop6 = 137185
print combined_list[NameTop6][0:combined_list[NameTop6].find('\t')]

NameTop7 = 124109
print combined_list[NameTop7][0:combined_list[NameTop7].find('\t')]

NameTop8 = 117937
print combined_list[NameTop8][0:combined_list[NameTop8].find('\t')]

NameTop9 = 42765
print combined_list[NameTop9][0:combined_list[NameTop9].find('\t')]

NameTop10 = 71424
print combined_list[NameTop10][0:combined_list[NameTop10].find('\t')]

'''
35920-1 DiCaprio, Leonardo
193334-1 scarlett johansson
30249-1 tom cruise
110499-1 brad pitt
23561-1 jackie chan
240107-1 Watson, Emma (II)
25337-1 Chou, Jay
200117-1 jennifer lawrence
232147-1 Meryl Streep
130682-1 will smith
179519-1 fan binging
'''

NameTop = 35920 -1
print combined_list[NameTop][0:combined_list[NameTop].find('\t')]