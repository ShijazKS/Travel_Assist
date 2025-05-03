import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from ui.state_selection import StateSelection
from ui.result_window import ResultWindow

class TravelAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # self.setWindowTitle("PyQt6 Dark Mode Grid")
        self.setGeometry(100, 100, 900, 720)

        self.setWindowTitle("Travel Assistant AI")
        # self.resize(900, 720)
        self.setStyleSheet("background-color: #1f2335; color: c0caf5;")

        # Stacked widget to hold multiple screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize screens
        self.state_selection = StateSelection(self)
        self.result_window = ResultWindow(self)

        # Add screens to stack
        self.stacked_widget.addWidget(self.state_selection)
        self.stacked_widget.addWidget(self.result_window)

        # Show state selection as the first screen
        self.stacked_widget.setCurrentWidget(self.state_selection)


    def show_result_screen(self, state):
        """Switch to result screen with selected state."""
        self.result_window.display_recommendations(state)
        self.stacked_widget.setCurrentWidget(self.result_window)

    def show_state_selection(self):
        """Switch back to the state selection screen."""
        self.stacked_widget.setCurrentWidget(self.state_selection)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyleSheet(""" 
                      
    QScrollBar:vertical {
        background: #1e1e2e;
        width: 10px;
        margin: 2px 0 2px 0;
        border-radius: 5px;
    }
    
    QScrollBar::handle:vertical {
        background: #7aa2f7;
        min-height: 20px;
        border-radius: 5px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #bb9af7;
    }

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        background: none;
        height: 0px;
    }

    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {
        background: none;
    }

      """)
    
    window = TravelAssistant()
    window.show()
    sys.exit(app.exec())
