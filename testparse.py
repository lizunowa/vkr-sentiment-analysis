import requests
from bs4 import BeautifulSoup
import csv
# pip install beautifulsoup4
# pip install lxml
# План
# 1. Выяснить кол-во страниц
# 2. Сформировать список уролов на страницы выдачи
# 3. Собрать данные

def get_html(url):
	headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
	r = requests.get(url, headers = headers)
	return r.text

def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')
	pages = soup.find('ul', class_='aRWg5').find_all('a', class_='_2xCrO')[-1].get('href')
	total_pages = pages.split('=')[1]

	return int(total_pages)

def write_csv(data):
	with open('reviews_data_base.csv','a') as f:
		writer = csv.writer(f)

		writer.writerow( (data['company'], data['city'], data['product'], data['header'], data['full_text'], data['mark'], data['date'], data['link']) )

def get_page_data(html):
	soup = BeautifulSoup(html, 'lxml')
	reviews = soup.find('div', class_='_1ZC3Z').find_all('div', class_='_227VT')

	for review in reviews:
		name =  review.find('div', class_='_3bNvn').find_all('a')[0].get('href').split('/')[2]

		if 'rosgosstrah' not in name:
		#company, product,  header, full_text,  mark, date, link
			try:
				company = review.find('div', class_='_3bNvn').find_all('a')[0].get('href').split('/')[2]
			except:
				company = ''

			try:
				city = review.find('div', class_='_3bNvn').find_all('div', class_='_2iHTj')[0].text.split(', ')[1]
			except:
				city = ''

			try:
				product = review.find('div', class_='Ws2f2').find_all('span', class_='_1RwOX')[0].text
			except:
				product = ''

			try:
				header = review.find('a', class_ = 'mrfZC').find_all('div', class_='_3SgnA _2mg0e')[0].text
			except:
				header = ''

			try:
				full_text = review.find('div', class_ = '_3p0dD').find_all('p')[0].text
			except:
				full_text = ''

			try:
				mark = int(review.find('div', class_='_3bNvn').find_all('span',class_='_1OBr6')[0].text)
			except:
				mark = ''

			try:
				date = review.find('div', class_='_3bNvn').find_all('div', class_='_2iHTj')[0].text.split(', ')[2] + ' ' + review.find('div', class_='_3bNvn').find_all('div', class_='_2iHTj')[0].text.split(', ')[3]
			except:
				date = ''

			try:
				link = 'https://www.sravni.ru' + review.find('a', class_ = 'mrfZC').get('href')
			except:
				link = ''

			data = {'company' : company,
			'city' : city,
			'product' : product,
			'header' : header,
			'full_text' : full_text,
			'mark' : mark,
			'date' : date,
			'link' : link
			}

			write_csv(data)
		else:
			continue

def main():
	url = "https://www.sravni.ru/strakhovye-kompanii/otzyvy/"
	base_url = "https://www.sravni.ru/strakhovye-kompanii/otzyvy/?"
	page_part = "page="
	total_pages = get_total_pages(get_html(url))


	for i in range(1, total_pages):
		url_gen = base_url+page_part+str(i)
		#print(url_gen)
		html = get_html(url_gen)
		get_page_data(html)



if __name__ == '__main__':
	main()