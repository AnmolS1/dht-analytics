from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QIntValidator
from datetime import datetime, timedelta
import sys

app = QApplication(sys.argv)

class Window(QWidget):
	def __init__(self):
		super().__init__()
		
		self.setWindowTitle("Update Social Media Data")
		
		today = datetime.today()
		yesterday = today - timedelta(days=1)
		two_days_ago = today - timedelta(days=2)
		yday_date_string = f"{two_days_ago.strftime("%b %d")} - {yesterday.strftime("%b %d")}"
		all_time_date_string = f"Oct 21 - {yesterday.strftime("%b %d")}"
		
		input_validator = QIntValidator()
		input_validator.setBottom(1)
		
		yday_reach_label = QLabel(f'Enter the reach for {yday_date_string}:')
		self.yday_reach_input = QLineEdit()
		self.yday_reach_input.setValidator(input_validator)
		
		all_time_reach_label = QLabel(f'Enter the reach for {all_time_date_string}:')
		self.all_time_reach_input = QLineEdit()
		self.all_time_reach_input.setValidator(input_validator)
		
		yday_views_label = QLabel(f'Enter the views for {yday_date_string}:')
		self.yday_views_input = QLineEdit()
		self.yday_views_input.setValidator(input_validator)
		
		all_time_views_label = QLabel(f'Enter the views for {all_time_date_string}:')
		self.all_time_views_input = QLineEdit()
		self.all_time_views_input.setValidator(input_validator)
		
		submit_btn = QPushButton('Update Data')
		submit_btn.clicked.connect(app.quit)
		
		layout = QVBoxLayout()
		
		layout.addWidget(yday_reach_label)
		layout.addWidget(self.yday_reach_input)
		layout.addWidget(yday_views_label)
		layout.addWidget(self.yday_views_input)
		
		layout.addWidget(all_time_reach_label)
		layout.addWidget(self.all_time_reach_input)
		layout.addWidget(all_time_views_label)
		layout.addWidget(self.all_time_views_input)
		
		layout.addWidget(submit_btn)
		
		self.setLayout(layout)

def run_gui():
	window = Window()
	window.show()
	app.exec()
	return {
		"yday_reach": int(window.yday_reach_input.text()),
		"yday_views": int(window.yday_views_input.text()),
		"all_time_reach": int(window.all_time_reach_input.text()),
		"all_time_views": int(window.all_time_views_input.text())
	}
