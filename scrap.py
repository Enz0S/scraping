import requests
from bs4 import BeautifulSoup
import csv

def get_wawacity_links(title: str, page: int = 1) -> list:
    base_url = 'https://www.wawacity.hair/'
    media_type = "mangas"
    search_query = f"?search={title}&p={media_type}&page={page}"
    response = requests.get(base_url + search_query)

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        media_links = [div.find("div", {"class": "wa-post-link"}).a["href"] for div in soup.findAll("div", {"class": "wa-sub-block"})]

    all_titles = []
    all_links = []
    for media_link in media_links:
        response = requests.get(base_url + media_link)

        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find("table", {"id": "DDLLinks"})
            media_title = soup.findAll("div", {"class": "wa-sub-block-title"})[2].text
            print(media_title)
            tr_tags = soup.findAll('tr')
            episode_tags = soup.findAll("tr", {"class": "episode-title"})

            episode_titles = []
            episode_links = []
            for episode_tag in episode_tags:
                title_parts = media_title.split("\n")[1].split("-")
                title_parts.append(episode_tag.p.text.split("\n")[1].split("-")[2])
                episode_title = "-".join(title_parts)
                episode_titles.append(episode_title.rstrip("\r").strip("\t"))

            for tr_tag in tr_tags:
                td_tags = tr_tag.find_all('td')
                if len(td_tags) >= 2 and td_tags[1].text.strip() == "Uptobox":
                    a_tag = tr_tag.find('a', attrs={'rel': 'external nofollow'})
                    if a_tag is not None:
                        episode_links.append(a_tag['href'])

            all_titles.extend(episode_titles)
            all_links.extend(episode_links)

    return all_titles, all_links


def write_to_csv(filename: str, fieldnames: list, data: list):
    with open(filename, 'w', encoding="UTF8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    titles_and_links = []
    for i in range(1, 4):
        titles, links = get_wawacity_links("Blue lock", page=i)
        titles_and_links.extend(list(zip(titles, links)))

    write_to_csv("episode_titles.csv", fieldnames=["title"], data=[{"title": title} for title, _ in titles_and_links])
    write_to_csv("episode_links.csv", fieldnames=["link"], data=[{"link": link} for _, link in titles_and_links])