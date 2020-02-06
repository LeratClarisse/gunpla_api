from selenium import webdriver
import json

browser = webdriver.Firefox()

#liste des URLs à parcourir
urlList = {
    "PerfectGrade" : "https://gundam.fandom.com/wiki/Perfect_Grade",
    "MasterGrade" : "http://gundam.wikia.com/wiki/Master_Grade#Lineup",
    "HGUC" : "https://gundam.fandom.com/wiki/High_Grade_Universal_Century#List",
    "RE100" : "https://gundam.fandom.com/wiki/Reborn-One_Hundred"
}

for key,url in urlList.items():
    print('page : ' + url)
    browser.get(url)
    
    #suppression de la popup overlay pour la vie privée
    try:
        browser.execute_script("document.getElementsByClassName('_1ouSF3xnwUjIOquxopuxSZ')[0].style.display = 'none';")
    except:
        print("pas d'overlay")
    
    #liste des onglets à parcourir
    ulYear = browser.find_elements_by_class_name("tabbernav")[0]
    
    kits = []
    dictionary = {}
    
    for year in ulYear.find_elements_by_tag_name("li"):
        if(year.text == "Other"):
            continue
        
        browser.find_elements_by_link_text(year.text)[0].click()
        print ("clicking ", year.text)
        table = browser.find_element_by_css_selector(".tabbertab[style='display: block;'] > .wikitable")
        tds = table.find_elements_by_css_selector("tr > td")
        
        for i in range(len(tds)):
            if(i % 6 == 0):
                try:
                    image = tds[i].find_elements_by_css_selector('div > a')[0].get_attribute('href')
                except IndexError:
                    image = "No image available"
                dictionary['image'] = image
            
            elif(i % 6 == 1):
                title = tds[i].get_attribute('innerHTML')
                dictionary['title'] = title
                
            elif(i % 6 == 2):
                try:
                    series = tds[i].find_element_by_css_selector('a').get_attribute("title")
                except:
                    series = tds[i].text
                dictionary['series'] = series
               
            elif(i % 6 == 4):
                release_date = tds[i].get_attribute('innerHTML')
                dictionary['release_date'] = release_date
            
            elif(i % 6 == 5):
                notes = tds[i].get_attribute('innerHTML')
                dictionary['notes'] = notes
                kits.append(dictionary)
                dictionary = {}
    print ("==================================")    
    #écriture du fichier de sortie
    with open(key + '.json', 'w') as fp:
        json.dump(kits, fp)
    
browser.close()

print ("program finished successfully")