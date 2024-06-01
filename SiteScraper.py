import requests
from bs4 import BeautifulSoup
import os

def download_files(url, file_type):
  """Scrapes a website for links to files of a specific type and downloads them to a folder named after the URL.

  Args:
    url: The URL of the website to scrape.
    file_type: The file type to download (e.g., "pdf", "jpg").
  """
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
  except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    return

  soup = BeautifulSoup(response.content, "html.parser")

  # Find all links
  links = soup.find_all("a")

  # Get the website domain from URL (for folder name)
  domain = url.split("//")[-1].split("/")[0]

  # Create folder named after domain
  os.makedirs(domain, exist_ok=True)  # Create folder if it doesn't exist

  # Download files of the specified type
  for link in links:
    href = link.get("href")
    if href and href.endswith(f".{file_type}"):
      filename = os.path.basename(href)
      download_url = os.path.join(url, href)
      print(f"Downloading {filename}")

      try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        with open(os.path.join(domain, filename), "wb") as f:
          for chunk in response.iter_content(1024):
            f.write(chunk)
      except requests.exceptions.RequestException as e:
        print(f"Failed to download {filename}: {e}")

if __name__ == "__main__":
  url = input("Enter the website URL: ")
  file_type = input("Enter the file type to download (e.g., pdf, jpg): ")
  download_files(url, file_type)
