# encoding=utf-8

from leetcode.apis import LeetCodeClient
from leetcode import urls
from bs4 import BeautifulSoup
import requests
import base64

leetcode_username = 'whalefalles'
leetcode_password = ''

gh_access_token = ''

if __name__ == '__main__':
	# leetcode crawler
	client = LeetCodeClient()
	if not client.login(leetcode_username, leetcode_password):
		print('login fail!')
		exit(-1)
	submission_list = client.s.get(urls.SUBMISSION_LIST).json().get('submissions_dump', None)
	# problem = None
	print("开始爬取leetcode 并提交到github仓库...")
	for submission in submission_list:
		if submission['status_display'] == 'Accepted':
			rsp = client.s.get("https://leetcode-cn.com/submissions/detail/{}/".format(submission['id']))
			html = rsp.text
			soup = BeautifulSoup(html, 'html.parser')
			question_slug = soup.a.get('href')[10:-1]
			problem = client.get_problem_detail(question_slug)
			# print(problem.id,problem.title,problem.description)
			# print("\n".join(["~~~",submission['code'],"~~~"]))
			# ---------------------------------------------------------------------
			api = 'https://api.github.com/repos/{}/{}/contents/{}?access_token={}'.format('whalefalles',   # your gh username
			                                                                              'leetcode-solution',   # your repr
			                                                                              problem.id + '-' + problem.title + '.md', # file path
			                                                                              gh_access_token) # your gh access_token
			data = {
				'message': 'create ' + problem.id + '-' + problem.title + '.md',  # commit message
				'content': str(base64.encodestring("\n".join([
					problem.id + ' ' + problem.title,  # commit file.content
					problem.description,
					"答案:",
					"~~~",
					submission['code'],
					"~~~",
				]).encode('utf-8')), 'utf-8')
			}
			rsp = requests.put(url=api, json=data)
			print(problem.id + '-' + problem.title, "提交成功" if rsp.status_code == '201' else "已重复提交")
	# break
	print("提交完毕")
	client.close()
