import requests
from bs4 import BeautifulSoup

def extract_data(url,url_id,output_files_path):
  
  file = f"{output_files_path}/{url_id}.txt"
  try:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    file_object  = open(file, "a+")

    try:
      header = soup.find('header')
      title = header.find("h1",class_="entry-title").text
    except Exception as e:
      title=""
      print(f"Exception in fetching title of {url_id}: ",str(e))
    file_object.write(str(title))

    body_div = soup.find_all("div", class_="td-ss-main-content")
    if body_div:
      for p in body_div:
          para = p.find_all("p") 
          for p in para:
              file_object.write(f" {p.text}")        
    else:
      print(f"Unable to find main content as body is empty for {url_id} ")
    file_object.close()
  except Exception as e:
    print(f"Exception in extract_data() for {url_id} : ",str(e))
  return file