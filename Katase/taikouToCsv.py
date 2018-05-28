def main(Num):
	import pandas as pd
	html = '../schedule/s2016/index.php'
	#読み込んだtableのdataをこの中に入れる
	dataframes = pd.read_html(html)
	name = html.split('/')[1] + '_' + html.split('/')[2].split('.')[0]

	dataframes[Num] = columnRename(dataframes[Num])

	dataframes[Num] = addCompetitionName(dataframes[Num])

	dataframes[Num] = appendRows(dataframes[Num])

	dataframes[Num] = roundSet(dataframes[Num])

	dataframes[Num] = eventSet(dataframes[Num])

	dataframes[Num] = timeSet(dataframes[Num])

	dataframes[Num] = heatnumAndRankSet(dataframes[Num])

	print(dataframes[Num])

	dataframes[Num].to_csv(name + '_track.csv')


def heatnumAndRankSet(df):
	for idx, row in enumerate(df['着順']):

		if '組' in row and '着' in row:

			df.at[idx+1, 'heatnum'] = row.split('組')[0]
			df.at[idx+1, 'rank'] = row.split('組')[1].split('着')[0]

		elif '着' in row:

			df.at[idx+1, 'heatnum'] = 1
			df.at[idx+1, 'rank'] = row.split('着')[0]

		elif '等' in row:

			df.at[idx+1, 'heatnum'] = 1
			df.at[idx+1, 'rank'] = row.split('等')[0]

	return df

def timeSet(df):
	for idx, row in enumerate(df['記録']):

		if ':' in row and '\'' in row:

			df.at[idx+1, 'record_h'] = row.split(':')[0]
			df.at[idx+1, 'record_m'] = row.split(':')[1].split('\'')[0]
			df.at[idx+1, 'record_s'] = row.split(':')[1].split('\'')[1]
			df.at[idx+1, 'comment'] = df.at[idx+1, com]

		elif '\'' in row and '\"' in row:

			df.at[idx+1, 'record_m'] = row.split('\'')[0]
			df.at[idx+1, 'record_s'] = row.split('\'')[1].split('\"')[0]
			df.at[idx+1, 'record_cs'] = row.split('\'')[1].split('\"')[1]
			df.at[idx+1, 'comment'] = df.at[idx+1, com]

		elif '\"' in row:

			df.at[idx+1, 'record_s'] = row.split('\"')[0]
			df.at[idx+1, 'record_cs'] = row.split('\"')[1]

			if '/' in df.at[idx+1, com] and df.at[idx+1, com].split('/')[0].replace('-', '').replace('+', '').replace('.', '').isnumeric():

				df.at[idx+1, 'wind'] = float(df.at[idx+1, com].split('/')[0])
				df.at[idx+1, 'comment'] = df.at[idx+1, com].split('/')[1]

			elif df.at[idx+1, com].replace('-', '').replace('+', '').replace('.', '').isnumeric():

				df.at[idx+1, 'wind'] = float(df.at[idx+1, com])
				df.at[idx+1, 'comment'] = '-'

			else:

				df.at[idx+1, 'comment'] = df.at[idx+1, com]


		elif 'm' in row:

			df.at[idx+1, 'record_s'] = row.split('m')[0]
			df.at[idx+1, 'record_cs'] = row.split('m')[1]

			if '/' in df.at[idx+1, com] and df.at[idx+1, com].split('/')[0].replace('-', '').replace('+', '').replace('.', '').isnumeric():

				df.at[idx+1, 'wind'] = float(df.at[idx+1, com].split('/')[0])
				df.at[idx+1, 'comment'] = df.at[idx+1, com].split('/')[1]

			elif not('-' in df.at[idx+1, com]):

				df.at[idx+1, 'wind'] = float(df.at[idx+1, com])
				df.at[idx+1, 'comment'] = '-'

			else:

				df.at[idx+1, 'comment'] = df.at[idx+1, com]

		else:

			df.at[idx+1, 'DNS'] = 1
			df.at[idx+1, 'reason'] = row
			df.at[idx+1, 'comment'] = df.at[idx+1, com]



	return df

#種目名のOPを除去
def eventSet(df):
	for idx, row in enumerate(df['種目']):
	
		df.at[idx+1, '種目'] = row.split()[0]

	return df

#roundとうまくいけば女子も判定
def roundSet(df):
	for idx, row in enumerate(df['種目']):

		if 'OP' in row:
		
			df.at[idx+1, 'round'] = 'OP'

		elif '予選' in row:

			df.at[idx+1, 'round'] = '予選'

		elif '準決' in row:

			df.at[idx+1, 'round'] = '準決'

		elif '決勝' in row:

			df.at[idx+1, 'round'] = '決勝'

		elif '女子' in row:

			df.at[idx+1, 'round'] = 1

		#人力ソーン始まり
		else:

			df.at[idx+1, 'round'] = '決勝'
		#人力ゾーン終わり

	return df

#足りない列を追加
def appendRows(df):
	df['gender'] = 0
	df['competition_name'] = competition_name
	df['place'] = place
	df['date'] = date
	df['heatnum'] = 0
	df['rank'] = 0
	df['round'] = '0'
	df['record_h'] = 0
	df['record_m'] = 0
	df['record_s'] = 0
	df['record_cs'] = 0
	df['wind'] = 0.0
	df['electric_timing'] = electric_timing
	df['official'] = official
	df['DNS'] = 0
	df['decathron'] = 0
	df['comment'] = '0'
	df['reason'] = '-'

	return df


#列名を種目,着などちゃんとしたものにする
#因みにちゃんとした列名は1行目に入ってる
def columnRename(df):
	#列名を変更
	for i in range(len(df.columns)):
		df = df.rename(columns={i: df[i][0]})

	#0行目の列のインデックスだけのいらないデータを削除
	df = df.drop(0)

	return df

#rowspanの関係で種目名がない人たちがいる
#その人たちに種目名を追加
def addCompetitionName(df):
	for idx, row in enumerate(df['種目']):

		#種目列にちゃんと種目名が入っている場合はスルー
		if row.find('m') != -1 or row.find('投') != -1 or row.find('跳') != -1:
			continue
		
		#種目名が人名になっている場合は1つシフトして、種目名に一つ上の人の種目名を入れる
		else:
			df.iloc[idx] = df.iloc[idx].shift(1)
			df.iloc[idx]['種目'] = df.iloc[idx-1]['種目']

	return df


if __name__ == '__main__':
	competition_name = '農工戦'
	date = '2018-03-17'
	place = '新座'
	electric_timing = 0
	official = 0
	com = '風･備考'

	main(5)