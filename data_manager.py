import pandas

DATA_PATH = "./data"


class DataManager:
    """ This Class Is Responsible For reading, Writing And Formatting Data. """

    def __init__(self):
        self.file_path = f'{DATA_PATH}/translations.csv'
        self.translate_from = ''
        self.translate_to = ''

        self.languages = self.find_all_languages()
        self.data_frame = self.create_lang_dataframe()

        self.total_words_len: int = len(self.data_frame[next(iter(self.data_frame))])

        """ 
        How The above line works: First of all In the next and Iter part what it does is that it gets
        The First Item In the data_frame Here It will Be English, Then It gets The Data_frame For English
        Meaning All of the translations for english Then it just gets the length of all those Translations
        """


    def create_lang_dataframe(self) -> dict:
        """ Creates A Language Data Frame and saves it to self.data_frame variable

        Eg This Format: {
            'English': {0: 'part', 1: 'history' ... },
            'Turkish': {0: 'Bölüm', 1: 'Tarih' ... }
            ... For all Languages
            }
        """

        translations = pandas.read_csv(self.file_path)
        return pandas.DataFrame.to_dict(translations)

    @staticmethod
    def find_all_languages() -> list:
        """
        Finds All The Languages In data/languages.csv and Converts It to a List
        """

        languages = pandas.read_csv(f'{DATA_PATH}/languages.csv').Name
        return [lang for lang in languages]


    def words_known(self, word_to_write: str) -> None:
        """This function Writes To a File The Current Word If User Clicks Yes Button"""

        with open(f'{DATA_PATH}/words-known/{self.translate_from}.txt', encoding='utf-8', mode='a') as f:
            f.write(f'{word_to_write}\n')  # Converting The word To Utf-8 If error Occurs


        # generate_random_text()
class Method:

    def __init__(self):
        self.data_manager = DataManager()
        # The Current Word is the Translations Of the Translate From and Translate To that the User Picked

        self.current_word: dict = {
            self.data_manager.translate_from: None,
            self.data_manager.translate_to: None
        }

        self.words_known_data_length: int = 0

    def get_words_known(self):
        """ Gets The length of all The words the user Knows also Returns words_known_data if needed stores in a var"""

        with open(f'{DATA_PATH}/words-known/{self.data_manager.translate_from}.txt', 'r', encoding='utf-8') as f:
            words_known_data = f.readlines()

        self.words_known_data_length: int = len(words_known_data)

        return words_known_data

    def get_translations(self):
        """
        Tries To Read The File with The name of the language That the user's Translating from

         ----------------------------------- Methods & Variables Used ----------------------------------

        1) Words_known_data: It is Basically The Data we Get From the File If it exists(Meaning if the User
        Translated From a Language And Clicked On yes(Considering That they Know the Word, Hopefully they were honest)
        We add the current word that the user was showed to a file)

        2) Words_known_data_len Basically The Amount of words The User Knows

        3) 2 Methods (self.still_has_translations() and self.update_current_word()) used, check their docs for more info

        ----------------------------------------- FILE MANAGEMENT --------------------------------------------

        IF FILE DOESN'T EXIST: we set the words_known_length to 0 meaning That the user does not know any words
        For that specific Language that they're translating from

        IF FILE EXISTS: we read from it and find how much words The user knows Then we start from there

        -------------------------------- MANAGING DATA AND TRANSLATIONS ---------------------------

        We save that the user's Known words In the Words_known Folder in a separate text file with the name
        of the language user's translating from and find the amount Using above Methods

        Now every time(except for the one where the user Knows all those words for lang they selected)
        We update The data see self.update_data() Explanation Below

        """

        # If File Exists We Read It
        try:
            words_known_data = self.get_words_known()

        except FileNotFoundError:
            self.words_known_data_length = 0

        else:
            # Basically Removes New lines from all elements in words_known_data list
            words_known_data = list(map(lambda word: word.strip(), words_known_data))
            # for i in words_known_data:
                # words_known_data[words_known_data.index(i)] = i.strip()

        finally:
            if self.still_has_translations():
                self.update_current_word()


    def update_current_word(self) -> None:
        """Gets The Current Words And saves it to a Current_word dict

        Lets say the user picked english to translate From and Urdu as translate to
        So it would look something like this

        current_word = {
                    translate_from: 'part',
                    translate_to: 'حصہ'
        }

        It will update Everytime The word changes
        """
        dm = self.data_manager
        
        tr_from = dm.data_frame[dm.translate_from][self.words_known_data_length]
        tr_to = dm.data_frame[dm.translate_to][self.words_known_data_length]

        # Changes The current word dic to the new words Everytime when called
        self.current_word[dm.translate_from] = tr_from
        self.current_word[dm.translate_to] = tr_to


    def still_has_translations(self) -> bool:
        """
        This Method Returns True If the user has not completed all the translations for a language

        If it Goes Over the total_words_len it Means That We are out of words For a Language so we return False
        """
        try:
            self.get_words_known()
            
        except FileNotFoundError: 
            pass


        if self.words_known_data_length < self.data_manager.total_words_len:
            return True
        # else
        return False

