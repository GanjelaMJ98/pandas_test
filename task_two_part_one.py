import pandas as pd
import time as t
import datetime



def stat_part_one(df):
	output = []
	for user in pd.unique(df["tabnum"]):
		df_user = df[df["tabnum"] == user]
		early_time,full_time = (0,0)
		for index, row in df_user.iterrows():
			dt_start = pd.Timestamp(row['start_time']).to_pydatetime()
			dt_end = pd.Timestamp(row['end_time']).to_pydatetime()
			full_time += (dt_end - dt_start).total_seconds()
			# event before 10
			if(dt_end.time() <= datetime.time(10,0,0)): 
				duration = dt_end - dt_start 
				early_time += duration.total_seconds()
			# part of the event before 10
			elif(dt_start.time() < datetime.time(10,0,0) and dt_end.time() > datetime.time(10,0,0)):
				deadline =  datetime.datetime(dt_start.year, dt_start.month, dt_start.day, 10, 0, 0)
				duration = deadline - dt_start 
				early_time += duration.total_seconds()

		output.append([user, early_time/full_time])

	output_df = pd.DataFrame(output, columns = ['Tabnum', '1'])
	return output_df




if __name__ == '__main__':
	df = pd.read_excel("test_case_my.xlsx")
	out = stat_part_one(df)
	print(out.head())