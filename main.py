import sys,os,time
from leetcode.models import Problem
from leetcode.apis import LeetCodeClient
if __name__ == '__main__':
	client = LeetCodeClient()
	if not client.login('whalefalles','qq123456'):
		print('login fail!')
		exit(-1)
	problems = client.get_problems()
	print(client.get_accepted_code())
