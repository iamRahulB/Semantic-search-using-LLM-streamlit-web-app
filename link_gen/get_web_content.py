from bs4 import BeautifulSoup
import re
import requests


class WebContent:

  def __init__(self):
    pass

  def extract_body_text(self, link):  
    response = requests.get(link)
    
    def remove_a(match):
      return ""

    if response.status_code == 200:
      soup = BeautifulSoup(response.content, "html.parser")
      body_tag = soup.find("body")
      if body_tag:
        cleaned_body_tag = re.sub(r"<a\s*.*?</a>",
                                  remove_a,
                                  str(body_tag),
                                  flags=re.DOTALL)
        soup = BeautifulSoup(cleaned_body_tag, "html.parser")
        body_text = soup.get_text()
        body_text = re.sub("\s+", " ", body_text)
        return str(body_text)
      else:
        print("No body tag found")
    else:
      print("Error getting response")

    print("Extraction successful")

  def fetch_content(self, links):
    all_links_body_text = []

    for link in links:
      all_links_body_text.append(
          self.extract_body_text(link)) 

    return all_links_body_text
