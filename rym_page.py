
# =====================================
# Imports
# =====================================

from bs4 import Tag
from datetime import datetime
from release import ReleaseData
import dateutil.parser
import typing

# =====================================
# Classes
# =====================================

class RymPage:
    """! class, meant to be used as parent class for all types of RYM pages"""
    COLLECTION_PAGE = "collection"
    RELEASE_PAGE = "release"
    def __init__(self, soup, page_type):
        self.soup = soup 
        self.page_type = page_type 

    def _scrape_page(self):
        raise NotImplementedError()

class CollectionPage(RymPage):
    """!
    Class representing Collection Page 
    """
    RELEASE_URL = "https://rateyourmusic.com{}" # releasetype/artist/release
    def __init__(self, soup):
        super().__init__(soup, self.COLLECTION_PAGE)
        self._release_urls_on_page = []  #TODO - give this a better name
        self._scrape_page()

    def _scrape_page(self):
        albums_tag = self.soup.find_all("div", class_="or_q_albumartist")
        for rating in albums_tag:
            self._release_urls_on_page.append(self.RELEASE_URL.format(rating.i.a['href']))

    @property
    def release_urls(self):
        """!
        @return - list of urls found on collection page
        """
        return self._release_urls_on_page
    
    @property
    def pages_in_collection(self):
        """!
        @return - total pages in collection
        """
        potential_pages = [int(val.string) for val in self.soup.find_all("a", class_="navlinknum")]
        return max(potential_pages) if len(potential_pages) > 0 else 1

class ReleasePage(RymPage):
    def __init__(self, soup, rating=None):
        super().__init__(soup, self.RELEASE_PAGE)
        self._release_data = ReleaseData()
        self._scrape_page()

        # bc of complexity of receiving user rating (requires signin thru browser) option to send on creation
        if rating is not None:
            self._release_data.user_rating = rating

    @property
    def release_data(self):
        return self._release_data

    def _scrape_page(self):
        self._set_release_name()
        self._get_release_info()

    def _set_release_name(self):
        self._release_data.release_name = self.soup.find("div", class_="album_title").text.split("\n")[0].strip()

    def _set_user_rating(self):
        """!
        @note  not really using this for now bc getting user like this requires being logged in, which
               seems failure prone
        """
        try:
            self.release_data.user_rating = float(self.soup.find(class_="rating_num").text.strip())
        # if there is no rating, rating will appear as "---" and we'll have an exception
        except Exception as e:
            pass

    def _get_release_info(self):
        set_funcs = {"Artist": self._set_artist, "Type": self._set_release_type, "Released": self._set_release_date, "RYM Rating": self._set_rym_rating, "Genres": self._set_genres, "Descriptors": self._set_descriptors}

        album_info_table = self.soup.find("table", class_="album_info") 

        for col in album_info_table.find_all("tr"):
            table_header = col.find("th", class_="info_hdr").text.strip()
            if table_header in set_funcs:
                set_funcs[table_header](col.find("td"))

    def _set_artist(self, artist: Tag):
        self._release_data.artist = artist.text.strip()

    def _set_release_type(self, release_type: Tag):
        self._release_data.release_type = release_type.text.strip()

    def _set_release_date(self, release_date: Tag):
        release_date =  release_date.text.strip()
        try:
            self._release_data.release_date = dateutil.parser.parse(release_date)
        except:
            pass


    def _set_genres(self, genres: Tag):
        try:
            parsed_genres = genres.find("span", class_="release_pri_genres").text.split(", ")
            if len(parsed_genres) > 0:
                self._release_data.genres = parsed_genres
        except Exception as e:
            pass
        try:
            self._release_data.secondary_genres = genres.find("span", class_="release_sec_genres").text.split(", ")
        except Exception as e:
            pass
    
    def _set_descriptors(self, descriptors: Tag):
        try:
            parsed_descriptors = descriptors.find("span", class_="release_pri_descriptors").text.strip()
            if len(parsed_descriptors) > 0:
                self.release_data.descriptors = [descriptor.strip() for descriptor in parsed_descriptors.split(",")]
        except Exception as e:
            pass
    
    
    def _set_rym_rating(self, rym_rating: Tag):
        try:
            self.release_data.rym_rating = float(rym_rating.find("span", class_="avg_rating").text.strip())
        except Exception as e:
            pass

