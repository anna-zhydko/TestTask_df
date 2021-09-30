from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


path = 'C:\Program Files (x86)\chromedriver'
driver = webdriver.Chrome(path)
url = 'https://www.zooplus.de/tierarzt/results?animal_99=true'

driver.get(url)


# The function gets element text if it exists on a page
def get_element_text(tag, class_name):
    try:
        return tag.find_element_by_class_name(class_name).text
    except:
        return ''


try:
    # Wait until all elements are loaded
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "search-results"))
    )
    count = 0
    with open('Veterinarians.csv', mode='w', encoding='utf-8') as file:
        names = ['Name', 'Institution', 'Working hours', 'Address', 'Stars count', 'Recommendations']
        file_writer = csv.DictWriter(file, fieldnames=names, delimiter=';')
        file_writer.writeheader()
        for page in range(1, 6):
            page = driver.find_element_by_class_name('pagination-group').find_element_by_link_text(str(page))
            driver.execute_script("arguments[0].click();", page)  # move to another page
            articles = driver.find_elements_by_tag_name('article')
            for article in articles:
                title = get_element_text(article, 'result-intro__title')
                subtitle = get_element_text(article, 'result-intro__subtitle')
                daily_hours = get_element_text(article, 'daily-hours__range')
                address = get_element_text(article, 'result-intro__address')
                rating_score = article.find_element_by_class_name('star-rating ')
                stars_count = len(rating_score.find_elements_by_tag_name('span'))
                rating_note = get_element_text(article, 'result-intro__rating__note')
                count += 1
                file_writer.writerow({'Name': title, 'Institution': subtitle, 'Working hours': daily_hours,
                                      'Address': address, 'Stars count': stars_count, 'Recommendations': rating_note})
                print(f'Запись № {count} записана в файл')
finally:
    driver.quit()




