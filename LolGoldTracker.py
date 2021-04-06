import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtWidgets import QLabel, QTableView
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QTimer
import DataConnector as dt
import PandasModel as pm

class LoLGoldTracker(QWidget):
    FETCH_RESOLUTION = 1000 # 1 sec

    def __init__(self, data_connector, parent=None):
        super(LoLGoldTracker, self).__init__(parent)
        
        self.data_connector = data_connector
        self.build_interface()
        self.update_data()
        self.updateTimer = QTimer(self)
        self.updateTimer.setInterval(self.FETCH_RESOLUTION)
        self.updateTimer.timeout.connect(self.update_data)
        self.updateTimer.start()
        self.show()

    def build_interface(self):
        self.order_team_view = QTableView()
        self.chaos_team_view = QTableView()

        main_grid = QHBoxLayout()
        main_grid.addWidget(self.order_team_view)
        main_grid.addWidget(self.chaos_team_view)

        self.setLayout(main_grid)
        
        self.setGeometry(0, 0, 900, 600)
        self.setWindowTitle("Lol Gold Tracker")
        self.center_main_window()

    def update_data(self):
        df = self.data_connector.fetchData()
        order_model = self.build_team_model(df, 'ORDER')
        chaos_model = self.build_team_model(df, 'CHAOS')
        self.order_team_view.setModel(order_model)
        self.chaos_team_view.setModel(chaos_model)

    def build_team_model(self, data, team):
        data = data[data['team'] == team]
        model = pm.PandasModel(data)
        return model

    def center_main_window(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

if __name__ == '__main__':
    data_connector = dt.DataConnector()
    app = QApplication(sys.argv)
    win = LoLGoldTracker(data_connector)
    sys.exit(app.exec_())
