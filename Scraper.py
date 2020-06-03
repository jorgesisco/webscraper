import requests
from bs4 import BeautifulSoup


for page in range(1, 388): #Loop para que el codigo se repita pagina por pagina!

    page_listing = requests.get(f'https://www.biospace.com/employers/pharmaceutical/{page}')
    soup_listing = BeautifulSoup(page_listing.content, 'html.parser')

    print(f'Getting page {page} data!.')

    for i in range(0, 9):  #Looping cada pagina con info de la compañia!

        #Getting company names!
        companies_1 = soup_listing.find(id='listing')
        companies_2 = companies_1.find_all(class_='lister__item cf block js-clickable')
        companies_3 = companies_2[i].find(class_='lister__header').get_text()

        #findind hiperlink of each company listed in biospace
        company_href = soup_listing.find_all(class_='js-clickable-area-link')
        com_page = company_href[i].get('href')

        #requesting access to each company hiperlink inside biospace
        com_page_req = requests.get(f"https://www.biospace.com{com_page}")
        com_page_soup = BeautifulSoup(com_page_req.content, 'html.parser')

        # Getting company website:
        com_website = com_page_soup.find(target="_blank").get('href')
        # print(com_website)

        # Getting company country
        try:
            com_country = com_page_soup.find(itemprop='addressCountry').get('content')
        except AttributeError:
            com_country = "No country"
            pass

        #saving website and country on txt file!
        with open(f'Companies.txt', 'a') as f:
            f.write("\n")
            f.write(companies_3) + f.write(f' *{com_website}') + f.write(f' *{com_country}')
