"""
This application searches for subtitles for a user
supplied movie or TV show name. The user is able to dowmload
subtitles supplied by the application based on the query supplied

author: Yemi Kudaisi
website: yemikudaisi.com 
last edited: May 2017
"""

import sys
import SubsceneSearch
from movie import Movie
import languages
import utils
from enum import Enum
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import QDeclarativeView

class ResultTypes(Enum):
    MOVIE = 1
    SUBTITLE = 2

class ApplicationView(QWidget):
    
    def __init__(self):
        super(ApplicationView, self).__init__()
        self.selectedLanguage = 0
        self.initUI()
        
    def initUI(self):
        style = """
            QWidget{
                background: #25282D;
                color: #8D9DA4;
            } 
            QPushButton{
                background: #3F464B;
                border: solid 1px #202429;
                padding: 10px 40px; 
            }
            QPushButton:hover:!pressed{
                background: #616B74;
            }
            QPushButton:!enabled{
                background: #A0A8AF;
                color: #5A636B;
            }
            QLineEdit, QComboBox{
                border: solid 1px #1E2226;
                background: #1A1D21;
                padding: 5px 5px;
            }
            QLineEdit:hover:!pressed{
                background: #616B74;
            }
            QListWidgetItem{color: rgb(0, 0, 0); }
            QComboBox::drop-down
            {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;

                border-left-width: 0px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }

            QComboBox::down-arrow
            {
                image: url(:/qss_icons/rc/down_arrow_disabled.png);
            }

            QComboBox::down-arrow:on, QComboBox::down-arrow:hover,
            QComboBox::down-arrow:focus
            {
                image: url(:/qss_icons/rc/down_arrow.png);
            }
            """

        self.setStyleSheet(style)
        self.setWindowTitle('Subtitle Search')  
        self.statusBar = QStatusBar()
        self.statusMessage = QLabel('Ready')
        self.statusBar.addWidget(self.statusMessage)

        mainLayout = QGridLayout()
        formLayout = QFormLayout()

        self.cmbLanguage = QComboBox()
        self.cmbLanguage.addItems(languages.supported)
        self.cmbLanguage.currentIndexChanged.connect(self.languageChanged)

        self.txtTitle = QLineEdit('mother india')

        formLayout.addRow(self.tr('Subtitle Language'), self.cmbLanguage)
        formLayout.addRow(self.tr('Title'), self.txtTitle)

        btnSearch = QPushButton('Search', self)
        btnSearch.clicked.connect(self.searchMovie)

        self.resultList = QListWidget();
        self.resultList.itemClicked.connect(self.resultListItemClicked)

        self.btnDownloadSubtitle = QPushButton("Dowload Selection")
        self.btnDownloadSubtitle.clicked.connect(self.downloadSelectionSubtitle)
        self.btnShowSubtitles = QPushButton("Show subtitles for Selection")
        self.btnShowSubtitles.clicked.connect(self.searchSelectionSubtitles)
        self.btnDownloadSubtitle.setDisabled(True)
        self.btnShowSubtitles.setDisabled(True)
        self.btnClose = QPushButton("Close")

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.btnShowSubtitles)
        hlayout.addWidget(self.btnDownloadSubtitle)
        hlayout.addWidget(self.btnClose)
                 
        mainLayout.addLayout(formLayout, 1, 0)
        mainLayout.addWidget(btnSearch, 1, 1, Qt.AlignTop)
        mainLayout.addWidget(self.resultList,2,0,1,2)
        mainLayout.addLayout(hlayout, 3,0,1,2, Qt.AlignRight)
        mainLayout.addWidget(self.statusBar, 4,0,1,2, Qt.AlignBottom)
        mainLayout.setAlignment(Qt.AlignTop)
        self.setLayout(mainLayout)
         
        self.setGeometry(300, 300, 550, 450)           
        self.show()

    def close(self):
        # sys.exit(0) is not working because of some interpreter lock or timer issues on exit.
 
        # Force kill instead.
        if sys.platform == "win32":
            # This works on Windows
            os.kill(os.getpid(), -9)
        else:
            # This works on Mac/Linux
            os.system("kill -9 %d" % os.getpid())
    
    def changeResultTpe(self, type):
        self.resultType = type
        self.resetButton();

    def resetButton(self):
        if len(self.searchResult) < 1:
            self.btnShowSubtitles.setDisabled(True)
            self.btnDownloadSubtitle.setDisabled(True)
            return

        if self.resultType == ResultTypes.MOVIE:
            self.btnShowSubtitles.setDisabled(False)
            self.btnDownloadSubtitle.setDisabled(True)
            return

        if self.resultType == ResultTypes.SUBTITLE:
            self.btnShowSubtitles.setDisabled(True)
            self.btnDownloadSubtitle.setDisabled(False)
            return
              
    def searchMovie(self):
        self.searchResult = []
        url = utils.string_to_query(self.txtTitle.text())
        self.searchResult = SubsceneSearch.search_movie(url)
        self.statusMessage.setText(str(len(self.searchResult)) + ' result(s) found . Select a movie and click show selection subtitles.')
        self.resultList.clear()

        # loop through the list of movies and add the titles to the result list 
        for movie in self.searchResult:
            self.resultList.addItem(movie.title)
        self.changeResultTpe(ResultTypes.MOVIE)

    def searchSelectionSubtitles(self):
        if len(self.searchResult) < 1:
            self.resetButton()
            return

        movie = self.searchResult[self.resultList.currentRow()]
        self.searchResult =  SubsceneSearch.search_movie_subtitle(movie, languages.supported[self.selectedLanguage])
        self.statusMessage.setText(str(len(self.searchResult)) + ' result(s) found . Select a subtitle and click download selection.')
        self.resultList.clear()

        # loop through the list of subtitle and add the titles to the result list 
        for subtitle in self.searchResult:
            self.resultList.addItem(subtitle.title)
        self.changeResultTpe(ResultTypes.SUBTITLE)  

    def downloadSelectionSubtitle(self):
        if len(self.searchResult) < 1:
            self.resetButton()
            return

        subtitle = self.searchResult[self.resultList.currentRow()]
        filePath = QFileDialog.getSaveFileName(self, 'Save File')
        result = SubsceneSearch.download_movie_subtitle(subtitle, filePath[0])

    
    def languageChanged(self,i):
        self.selectedLanguage = i

    def resultListItemClicked(self, item):
        self.resetButton()  
