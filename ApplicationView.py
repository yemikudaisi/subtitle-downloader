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
import utils
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import QDeclarativeView

class ApplicationView(QWidget):
    
    def __init__(self):
        super(ApplicationView, self).__init__()
        self.initUI()
        
    def initUI(self):
        style = """
            QPushButton{
                color: rgb(230, 116, 44); 
            }
            QListWidgetItem{color: rgb(0, 0, 0); }
            """

        self.setStyleSheet(style)
        self.setWindowTitle('Subtitle Downloader')  
        self.statusBar = QStatusBar()
        self.statusMessage = QLabel('Ready')
        self.statusBar.addWidget(self.statusMessage)

        mainLayout = QGridLayout()
        formLayout = QFormLayout()

        self.cmbLanguage = QComboBox()
        languages = ['English', 'Arabic','Yoruba']
        self.cmbLanguage.addItems(languages)

        self.txtTitle = QLineEdit('mother india')
        self.txtSeason = QLineEdit('')
        self.txtEpisode = QLineEdit('')

        formLayout.addRow(self.tr('Subtitle Language'), self.cmbLanguage)
        formLayout.addRow(self.tr('Title'), self.txtTitle)
        formLayout.addRow(self.tr('Season (series)'), self.txtSeason)
        formLayout.addRow(self.tr('Episode (series)'), self.txtEpisode)

        btnSearch = QPushButton('Search', self)
        btnSearch.clicked.connect(self.searchSubtitle)

        self.resultList = QListWidget();
        self.resultList.itemClicked.connect(self.resultListItemClicked)

        self.btnDownload = QPushButton("Dowload Selection")
        self.btnClose = QPushButton("Close")

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.btnDownload)
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
            
    def searchSubtitle(self):
        url = utils.string_to_query(self.txtTitle.text())
        self.statusMessage.setText('Query string: '+ url)
        self.searchResult = SubsceneSearch.search_movie_subtitle(url)
        self.statusMessage.setText(str(len(self.searchResult)) + ' result(s) found')
        self.resultList.clear()
        #self.resultList.addItems(self.searchResult)
        # loop through the list of movies and add the titles to the result list 
        for movie in self.searchResult:
            self.resultList.addItem(movie.title)

    def resultListItemClicked(self, item):
       QMessageBox.information(self, "ListWidget", "You selected: "+item.text())
