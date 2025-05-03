from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QListWidget
from PyQt6.QtGui import QFont

from ui.search_line_edit import SearchLineEdit

class StateSelection(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent  

        self.states = [
            "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
            "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
            "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
            "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
            "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
            "Andaman and Nicobar Islands", "Chandigarh", "Daman and Diu",
            "Lakshadweep", "Delhi", "Puducherry", "Ladakh", "Jammu and Kashmir"
        ]

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)

        # List Widget for States
        self.state_list = QListWidget()
        self.state_list.setFont(QFont("Arial", 15))
        self.state_list.setStyleSheet("""
            QListWidget {
                background-color: #24283b ;
                border: 1px solid #4fd6be  ;
                border-radius: 6px;
                color: #41a6b5 ;
                padding: 5px;
            }

            QListWidget::item:selected {
                background-color: #565f89;
                color: #ffc777  ;
            }
        """)
        self.state_list.addItems(self.states)
        self.state_list.itemClicked.connect(self.select_state)
        
        # Search Bar 
        self.search_input = SearchLineEdit(list_widget=self.state_list, on_enter_callback=self.select_state)
        self.search_input.setPlaceholderText("Search or select a state...")
        self.search_input.setFont(QFont("Arial", 16))
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 6px;
                border: 1px solid #4fd6be  ;
                color: #bb9af7 ;
                background-color: #24283b ;
            }
        """)
        self.search_input.textChanged.connect(self.update_list)
        
        
        self.layout.addWidget(self.search_input)
        self.layout.addWidget(self.state_list)


    def update_list(self):
        search_term = self.search_input.text().lower()
        self.state_list.clear()
        for state in self.states:
            if search_term in state.lower():
                self.state_list.addItem(state)
        if self.state_list.count() > 0:
            self.state_list.setCurrentRow(0)


    def select_state(self, item):
        selected_state = item.text()
        self.parent.show_result_screen(selected_state) 
