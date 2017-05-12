import sys
from ApplicationView import *

def main():    
    app = QApplication(sys.argv)
    view = ApplicationView()
    sys.exit(app.exec_())
    
if __name__ == '__main__' :
    main()