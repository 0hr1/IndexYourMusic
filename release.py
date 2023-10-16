# =====================================
# Imports
# =====================================

from datetime import datetime
import dataclasses
import json

# =====================================
# Classes
# =====================================

@dataclasses.dataclass
class ReleaseData:
    """!
    @brief  dataclass representing a single release
    """
    artist: str = "ArtistName"
    release_name: str = "ReleaseName"
    release_type: str = "ReleaseType"
    release_date: datetime = datetime(1,1,1)
    rym_rating: float = 0.0
    user_rating: float = 0.0  # no rating = 0.0
    genres: tuple[str] = ("No Primary Genres",)
    secondary_genres: tuple[str] = ("No Secondary Genres",)
    descriptors: tuple[str] = ("No Descriptors",)

    def __str__(self):
        """
        @brief  user friendly representation of Release 
        @return  _Artist - Release_ (as string)
        """
        return "{} - {}".format(self.artist, self.release_name)


class ReleaseDataSaver:
    """!
    @brief  used for saving all the releases data in a json file
    """
    WRITE_MODE = "w"
    READ_MODE = "r"
    RECOVERY_MODE = "a" 

    def __init__(self, file_name: str, mode: str):
        """!
        @param file_name  file name of database
        @param mode  "r" to read file, "w" to create and write to file
        """
        if mode in (self.WRITE_MODE, self.READ_MODE):
            self._file = open(file_name, mode)
            self._releases_written = 0
            self._mode = mode
        elif mode == self.RECOVERY_MODE:
            # in case of recovery, read file, rewrite everything
            self._file = open(file_name, self.READ_MODE)
            self._recovered_data = self.read()
            self._file.close()
            self._releases_written = len(self._recovered_data)
            self._file = open(file_name, self.WRITE_MODE)
            self._mode = self.RECOVERY_MODE
        else:
            raise Exception("invalid mode")

    def __enter__(self):
        if self._mode in (self.WRITE_MODE, self.RECOVERY_MODE):
            self._file.write("[\n")
        if self._mode == self.RECOVERY_MODE:
            self.write_all(self._recovered_data)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._mode in (self.WRITE_MODE, self.RECOVERY_MODE):
            self._file.write("\n]\n")
        self._file.close()

    def write(self, release_data: ReleaseData):
        """!
        @brief  write a single release data object to output file
        @param release_data   save ReleaseData dataclass type to database file (jsonified)
        """
        prefix = ",\n" if self._releases_written > 0  else "" 
        self._file.write(prefix + json.dumps(dataclasses.asdict(release_data), indent=4, default=str))
        self._releases_written += 1

    def write_all(self, all_release_data: list[ReleaseData]):
        """!
        @brief  write a list of ReleaseData objects to output file
        @param all_release_data   list of ReleaseData objects
        """
        for release_data in all_release_data:
            self._file.write(json.dumps(dataclasses.asdict(release_data), indent=4, default=str))
        self._releases_written += len(all_release_data)

    def read(self):
        """
        @return  list of ReleaseData of all releases in json
        """
        data = self._file.read()
        json_parsed_data = json.loads(data)
        dataclass_parsed_data = [ReleaseData(**release) for release in json_parsed_data]
        return dataclass_parsed_data

