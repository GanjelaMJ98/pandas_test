import pandas as pd
from operator import itemgetter, attrgetter

# Представим событие как класс
class Event:
	# первичный приоритет lifestyle < run < partners
	first_priority = {'partners': 1, 'run': 2, 'lifestyle': 3}
	def __init__(self,subject,category, participants):
		self.subject = subject
		self.category = category
		self.participants = participants
	def __str__(self):
		return "{}-{}-{}".format(self.subject,self.category, self.participants)


# key function for sorted
def first_priority_key(x):
	return x.first_priority[x.category]


def priority(df):
	output = []
	for user in pd.unique(df["tabnum"]):
		Event_objects = []
		df_user = df[df['tabnum'] == user]
		for index, row in df_user.iterrows():
			Event_objects.append(Event(row['subject'],row['category'],row['participants_count']))

		# вторичный приоритет lifestyle(participants_count = 1) < lifestyle(participants_count = 2)
		second_sort = sorted(Event_objects,key=attrgetter('participants') , reverse= True)
		full_sort = sorted(second_sort, key = first_priority_key)

		rows = []
		for i, event in enumerate(full_sort, start=1):
			rows.append([user, event.subject,i])
		user_priority= pd.DataFrame(rows, columns=["user", "subject","priority"])
		output.append(user_priority)
	return pd.concat(output)

if __name__ == '__main__':
	df = pd.read_excel("test_case_my.xlsx")
	out = priority(df)
	print(out.head(25))