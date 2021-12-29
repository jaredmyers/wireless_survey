# Jared Myers
# Book Library Application -- Google API
# DEC 2020


import sys
sys.path.append('/usr/local/lib/python3.7/dist-packages')
import sqlite3
from googlebooks import list_books
import requests
import wget
import os

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar 
import matplotlib.pyplot as plt 


from PyQt5 import QtGui
from PyQt5.QtWidgets import *

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import random


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Final")
        self.resize(800, 500)

        #--- Create a top-level layout-
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        
        # PyChart ---------------------
        self.canvas = None
        

        #----------------------- Labels
        # Info Tab---------------------
        self.borrower1 = QLabel()
        self.borrower2 = QLabel()
        self.borrower3 = QLabel()
        self.graph = QLabel()
        self.borrowerLabels = [self.borrower1,self.borrower2,self.borrower3]
        
        
        # Search Tab-------------------
        self.searchTextField = QLineEdit()
        self.ph1 = QLabel()
        self.ph2 = QLabel()
        self.result1 = QLabel()
        self.result2 = QLabel()
        self.result3 = QLabel()
        self.result4 = QLabel()
        self.result5 = QLabel()
        self.result6 = QLabel()
        self.result7 = QLabel()
        self.result8 = QLabel()
        self.result9 = QLabel()
        self.result10 = QLabel()
        self.resultList = [self.result1,self.result2,self.result3,self.result4,
                           self.result5,self.result6,self.result7,self.result8,
                           self.result9,self.result10]
        
        
        # Scan Tab----------------------
        self.scanWait = QLabel('Centre', self)
        self.image = QLabel('Centre', self)
        self.title = QLabel()
        self.author = QLabel()
        self.publisher = QLabel()
        self.publishedDate = QLabel()
        self.pageCount = QLabel()
        self.categorie = QLabel()
        self.isbn13 = QLabel()
        self.isbn10 = QLabel()
        self.scanTextField = QLineEdit(self)
        self.scanTextField.setFocusPolicy(Qt.StrongFocus)


        # Lend Tab---------------------
        self.lendLabel = QLabel('Centre', self)
        self.lendNameTextBox = QLineEdit()
        self.lendScanField = QLineEdit()
        self.lendTitle = QLabel()
        self.lendAuthor = QLabel()
        self.lendPublisher = QLabel()
        self.lendPublishedDate = QLabel()
        self.lendPageCount = QLabel()
        self.lendCategorie = QLabel()
        self.lendisbn13 = QLabel()
        self.lendisbn10 = QLabel()


        # Create the tab widget w/4tabs
        tabs = QTabWidget()
        tabs.addTab(self.infoTabUI(), "Info")
        tabs.addTab(self.searchTabUI(), "Search")
        tabs.addTab(self.scanTabUI(), "Scan")
        tabs.addTab(self.lendTabUI(), "Lend")
        layout.addWidget(tabs)


    def infoTabUI(self):
        """Create the Info page UI."""
        
        infoTab = QWidget()
        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()
        
        self.plotGraph()
        layoutH.addWidget(self.canvas)
        self.graph.setText("graph")
        layoutV.addLayout(layoutH)
        
        layoutV.addWidget(self.borrower1)
        layoutV.addWidget(self.borrower2)
        layoutV.addWidget(self.borrower3)
        
        self.searchBorrow()
       
        # Database Book Count
        conn = sqlite3.connect('books.db')
        sqlQuery = """SELECT * FROM book ORDER BY book_id DESC LIMIT 1"""
        cursor = conn.execute(sqlQuery)
        bookCount = 0
        for i in cursor:
            bookCount = i[0]
        
        self.borrower3.setText(f"Book Count: {bookCount}")
        conn.close()
       
        

        infoTab.setLayout(layoutV)
        
        

        return infoTab


    def searchTabUI(self):
        """Create the Search page UI."""
        
        searchTab = QWidget()
        layoutV = QVBoxLayout()
        
        
        self.ph1.setText("")
        self.ph2.setText("")
        self.result1.setText('')
        self.result2.setText('')
        self.result3.setText('')
        self.result4.setText('')
        self.result5.setText('')
        self.result6.setText('')
        self.result7.setText('')
        self.result8.setText('')
        self.result9.setText('')
        self.result10.setText('')
        
        layoutV.addWidget(self.result1)
        layoutV.addWidget(self.result2)
        layoutV.addWidget(self.result3)
        layoutV.addWidget(self.result4)
        layoutV.addWidget(self.result5)
        layoutV.addWidget(self.result6)
        layoutV.addWidget(self.result7)
        layoutV.addWidget(self.result8)
        layoutV.addWidget(self.result9)
        layoutV.addWidget(self.result10)
        
        
        layoutV.addWidget(self.ph1)
        layoutV.addWidget(self.searchTextField)
        
        
        self.searchTextField.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum);
        self.searchTextField.setMinimumWidth(350)
        self.searchTextField.returnPressed.connect(self.searchDatabase)
        
        
        searchTab.setLayout(layoutV)

        return searchTab

    def scanTabUI(self):
        """Create the Scan page UI."""
        
        scanTab = QWidget()
        layout = QVBoxLayout()
        layoutH = QHBoxLayout()
        layout2 = QVBoxLayout()

        self.scanWait.setText("")
        self.scanWait.setAlignment(QtCore.Qt.AlignCenter)

        self.image.setText("")
        self.image.setAlignment(QtCore.Qt.AlignCenter)

        self.title.setText(" ")
        self.author.setText(" ")
        self.publisher.setText(" ")
        self.publishedDate.setText(" ")
        self.pageCount.setText(" ")
        self.categorie.setText(" ")
        self.isbn13.setText(" ")
        self.isbn10.setText(" ")

        layout.addWidget(self.title)
        layout.addWidget(self.author)
        layout.addWidget(self.publisher)
        layout.addWidget(self.publishedDate)
        layout.addWidget(self.pageCount)
        layout.addWidget(self.categorie)
        layout.addWidget(self.isbn13)
        layout.addWidget(self.isbn10) 
        layout.addWidget(self.scanWait)

        #scanButton = QPushButton("Send Scan")
        #scanButton.clicked.connect(self.sendScan)
        self.scanTextField.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum);
        self.scanTextField.setMinimumWidth(350)
        self.scanTextField.returnPressed.connect(self.sendScan)

        layout2.addWidget(self.image)
        layout2.addWidget(self.scanTextField)
        #layout2.addWidget(scanButton)

        layoutH.addLayout(layout2)
        layoutH.addLayout(layout)

        scanTab.setLayout(layoutH)

        self.scanTextField.setFocus()
        
        return scanTab

    def lendTabUI(self):
        """Create the Lend page UI."""
        
        lendTab = QWidget()
        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()
        layoutV2 = QVBoxLayout()
        

        self.lendLabel.setText("Awaiting Scan..")
        self.lendLabel.setAlignment(QtCore.Qt.AlignCenter)

        layoutV.addWidget(self.lendLabel)
        layoutV.addWidget(self.lendNameTextBox)
        layoutV.addWidget(self.lendScanField)
        
        
        self.lendNameTextBox.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum);
        self.lendNameTextBox.setMinimumWidth(350)
        #self.lendNameTextBox.returnPressed.connect(self.lendScan)
        
        self.lendScanField.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum);
        self.lendScanField.setMinimumWidth(350)
        self.lendScanField.returnPressed.connect(self.lendScan)
        
        
        self.lendTitle.setText("")
        self.lendAuthor.setText("")
        self.lendPublisher.setText("")
        self.lendPublishedDate.setText("")
        self.lendPageCount.setText("")
        self.lendCategorie.setText("")
        self.lendisbn13.setText("")
        self.lendisbn10.setText("")
        
        layoutV2.addWidget(self.lendTitle)
        layoutV2.addWidget(self.lendAuthor)
        layoutV2.addWidget(self.lendPublisher)
        layoutV2.addWidget(self.lendPublishedDate)
        layoutV2.addWidget(self.lendPageCount)
        layoutV2.addWidget(self.lendCategorie)
        layoutV2.addWidget(self.lendisbn13)
        layoutV2.addWidget(self.lendisbn10)
        
        layoutH.addLayout(layoutV)
        layoutH.addLayout(layoutV2)
        

        lendTab.setLayout(layoutH)


        return lendTab


    def sendScan(self):
        """Draws data from API, inputs into database"""

        ISBN = 'isbn:'
        ISBN += self.scanTextField.text()
        
        api_success = False
        try:
        
            bookInfo = list_books(ISBN)

            parsed = []
            parsed.append(bookInfo['items'][0]['volumeInfo']['title'])
            parsed.append(bookInfo['items'][0]['volumeInfo']['authors'])
            parsed.append(bookInfo['items'][0]['volumeInfo']['publisher'])
            parsed.append(bookInfo['items'][0]['volumeInfo']['publishedDate'])
            parsed.append(bookInfo['items'][0]['volumeInfo']['pageCount'])
            parsed.append(bookInfo['items'][0]['volumeInfo']['categories'])
            parsed.append(bookInfo['items'][0]['volumeInfo']['industryIdentifiers'][0]['identifier'])  # isbn13
            parsed.append(bookInfo['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier']) # isbn10
            thumbUrl = bookInfo['items'][0]['volumeInfo']['imageLinks']['thumbnail']

            title = parsed[0]
            author = parsed[1][0]
            publisher = parsed[2]
            publishDate = parsed[3]
            pageCount = parsed[4]
            category = parsed[5][0]
            isbn10 = parsed[6]
            isbn13 = parsed[7]

            r = wget.download(thumbUrl)
            #r = requests.get(thumbUrl)
            image = QtGui.QImage(r)
            pixmapImage = QtGui.QPixmap.fromImage(image)

            self.title.setText(f"Title: {title}")
            self.author.setText(f"Author: {author}")
            self.publisher.setText(f"Publisher: {publisher}")
            self.publishedDate.setText(f"Date: {publishDate}")
            self.pageCount.setText(f"Pages: {pageCount}")
            self.categorie.setText(f"Category: {category}")
            self.isbn10.setText(f"ISBN13: {isbn13}")
            self.isbn13.setText(f"ISBN10: {isbn10}")
            self.image.setPixmap(pixmapImage)
            api_success = True
            
        except:
            self.image.setText("API Error")
            self.scanTextField.clear()
            
        
        if api_success:
            try:
                ## Database Entry
                conn = sqlite3.connect('books.db')
        
                sqlQuery = """INSERT INTO AUTHOR (NAME) VALUES (?)"""
                conn.execute(sqlQuery, [author]);
                sqlQuery = """SELECT author_id FROM AUTHOR WHERE name = ? """
                cursor = conn.execute(sqlQuery, [author])
        
                author_id = 0;
                for i in cursor:
                    author_id = i[0]
            
                with open('content', 'rb') as file:
                    blobData = file.read()
            
                sqlQuery = """INSERT INTO BOOK (TITLE, AUTHOR_ID, PUBLISHER, PUBLISH_DATE, PAGECOUNT, CATEGORY, ISBN13, ISBN10, PHOTO) VALUES (?,?,?,?,?,?,?,?,?)"""
                dataTup = (title, author_id, publisher, publishDate, pageCount, category, isbn13, isbn10, blobData)
                conn.execute(sqlQuery,dataTup)
        
                #conn.commit()
                conn.close()
        
                self.scanTextField.clear()
                
            except:
                conn.close()
                self.image.setText("Database Error.")
                self.scanTextField.clear()
        
            if os.path.exists("content"):
                os.remove("content")

    def searchDatabase(self):
        """Searches database outputs results"""
        
        text = self.searchTextField.text()
        text = '%'+text+'%'
        search = [text]
        
        # Database ---
        #try:
        conn = sqlite3.connect('books.db')
        
        sqlQuery = """SELECT title FROM BOOK WHERE title LIKE ?"""
        cursor = conn.execute(sqlQuery, search)
        
        for i in self.resultList:
            i.clear()
            
        self.searchResults = []
        for i in cursor:
            self.searchResults.append(i[0])
            
        c = 0
        for i in self.searchResults:
            self.resultList[c].setText(i)
            c += 1
            
        self.searchTextField.clear()
                
        #except:
        conn.close()
        #self.ph1.setText("Database Error.")
            
        conn.close()
        
        
    def lendScan(self):
        """Searches database for scan, inputs borrowers name"""
        
        
        text = self.lendScanField.text()
        ISBN = [text,text]
        self.lendScanField.clear()
        
        borrower = self.lendNameTextBox.text()
        borrower = [borrower]
        self.lendNameTextBox.clear()
        
        
        #--- Database ---
        #try:
        conn = sqlite3.connect('books.db')
        
        #--- Grabs book info ---
        sqlQuery = """SELECT * FROM BOOK WHERE isbn13 = ? OR isbn10 = ?"""
        cursor = conn.execute(sqlQuery, ISBN)
        
        for i in cursor:
            result = i
            
        #--- Grabs author name ---
        authorID = str(result[2])
        sqlQuery = """SELECT name FROM AUTHOR WHERE author_id = ?"""
        cursor = conn.execute(sqlQuery, [authorID])
        
        for i in cursor:
            authorName = i[0]
            
        #--- Convert photo blob ---
        with open('convert.tmp', 'wb') as file:
            file.write(result[9])
            
        image = QtGui.QImage('convert.tmp')
        pixmapImage = QtGui.QPixmap.fromImage(image)

        #--- Show book information ---       
        self.lendLabel.setPixmap(pixmapImage)
        self.lendTitle.setText(f"Title: {result[1]}")
        self.lendAuthor.setText(f"Author: {authorName}")
        self.lendPublisher.setText(f"Publisher:{result[3]} ")
        self.lendPublishedDate.setText(f"Date: {result[4]}")
        self.lendPageCount.setText(f"Pages: {result[5]}")
        self.lendCategorie.setText(f"Category: {result[6]} ")
        self.lendisbn13.setText("")
        self.lendisbn10.setText("")
        
        #--- Borrower Database Stuff ---
        sqlQuery = """SELECT * FROM lend WHERE personname = ?"""
        cursor = conn.execute(sqlQuery, borrower)
        
        borrowerExist = ()
        for i in cursor:
            borrowerExist = i
        
        #--- INSERT if borrower doesn't exist ---
        if len(borrowerExist) == 0:    
            sqlQuery = """INSERT INTO lend (PERSONNAME, BORROWING, BOOK_ID) VALUES (?,?,?)"""
            dataTup = (borrower[0], 'yes', result[0])
            conn.execute(sqlQuery,dataTup)
            
        #--- Checkin book     
        elif borrowerExist[2] == 'yes' and borrowerExist[3] == result[0]:
            sqlQuery = """UPDATE lend SET borrowing = ?, book_id = ? WHERE personname = ?"""
            dataTup = ('no', 0, borrower[0])
            conn.execute(sqlQuery,dataTup)
            
        else:
            sqlQuery = """UPDATE lend SET borrowing = ?, book_id = ? WHERE personname = ?"""
            dataTup = ('yes', result[0], borrower[0])
            conn.execute(sqlQuery,dataTup)
        
        conn.commit()
        conn.close()
        self.searchBorrow()
        
    def searchBorrow(self):
        """Displays book borrowers on Info page"""
        
        borrowers = []
        
        conn = sqlite3.connect('books.db')
        
        #--- Grabs borrowers info ---
        sqlQuery = """SELECT personname, book_id, date FROM lend WHERE borrowing = ?"""
        cursor = conn.execute(sqlQuery, ['yes'])
        
        borrowData = []
        for i in cursor:
            borrowData.append(i)
            
        if len(borrowData) == 0:
            for i in range(3):
                borrowers.append([""])
                
        else:
            for i in range(3):
                if i < len(borrowData):
                    bookID = borrowData[i][1]
                    
                    sqlQuery = """SELECT title FROM book WHERE book_id = ?"""
                    cursor = conn.execute(sqlQuery, [bookID])
                    
                    for p in cursor:
                        bookTitle = p[0]
                        
                    rtnData = [borrowData[i][0], bookTitle, borrowData[i][2]]
                    borrowers.append(rtnData)
                               
                else:
                    borrowers.append([""])
                    
        
        idx = 0
        for x in borrowers:
            
            if x[0] == '':
                self.borrowerLabels[idx].setText('')
            else:
                datesplit = x[2].split()
                self.borrowerLabels[idx].setText(f"{x[0]} | {x[1]} | {datesplit[0]}")
            idx += 1
                               
    def plotGraph(self):
        """Creates matplotlib pie graph for Info page"""
        
        #--- Database ---
        conn = sqlite3.connect('books.db')
        sqlQuery = """SELECT category FROM book"""
        cursor = conn.execute(sqlQuery)
        
        #--- Dictionary for category frequencies 
        catDict = {}
        for i in cursor:
    
            if "Biography" in i[0] and "Biography" not in catDict:
                catDict["Biography"] = 1
            elif "Biography" in i[0] and "Biography" in catDict:
                catDict["Biography"] += 1
            elif "Fiction" in i[0] and "Fiction" not in catDict:
                catDict["Fiction"] = 1
            elif "Fiction" in i[0] and "Fiction" in catDict:
                catDict["Fiction"] += 1
            elif "Drama" in i[0] and "Drama" not in catDict:
                catDict["Drama"] = 1
            elif "Drama" in i[0] and "Drama" in catDict:
                catDict["Drama"] += 1
            else:
                if i[0] not in catDict:
                    catDict[i[0]] = 1
                else:
                    catDict[i[0]] += 1
        
        # Dictionary filter
        popList = []
        for i in catDict.items():
            if i[1] < 2:
                popList.append(i[0])
        for i in popList:
            catDict.pop(i)
        
        
        # Apply Category Frequencies to Pie Chart inputs
        labels = []
        sizes = []
        for i in catDict.items():
            labels.append(i[0])
            sizes.append(i[1])
        
        explode = []
        explode.append(0.1) #explodes first slice
        for i in range(len(catDict)-1):
            explode.append(0)
        
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'tomato']
        #explode = (0.1, 0, 0, 0, 0)  # explode 1st slice

        fig = plt.Figure()
        ax1 = fig.add_subplot(111)
        ax1.pie(sizes, labels=labels,colors=colors,explode = explode, autopct='%1.1f%%', shadow=True, startangle=90)
        self.canvas = FigureCanvas(fig)
        
       
            
        
        conn.close()
        
        

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())





