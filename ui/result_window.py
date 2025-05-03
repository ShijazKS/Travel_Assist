import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
    QGridLayout, QScrollArea, QSizePolicy, QHBoxLayout, QStackedWidget, QSpacerItem,QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from qtawesome import icon 
from PyQt6.QtGui import QMovie 
import pandas as pd

from utils.load_places import load_places
from utils.score_manager import save_scores

class FetchPlacesThread(QThread):
    fetched = pyqtSignal(pd.DataFrame)

    def __init__(self, state):
        super().__init__()
        self.state = state

    def run(self):
        df = load_places(self.state) 
        self.fetched.emit(df)  


class ContentBox(QWidget):
    def __init__(self, name,state_district,city,address,category, link_text, stacked_widget, detail_page):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.detail_page = detail_page 
         
        self.title = name
        self.state_district = state_district
        self.city = city
        self.address = address 
        self.category = category
        
        self.liked = False
        self.disliked = False
        self.read_more_clicked = False  

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #292e42;
                padding: 12px;
                border-radius: 10px;
                border: 2px solid #b4f9f8;
            }
            QFrame:hover {
        border: 2px solid #ff007c;
    }
        """)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # Title
        title_label = QLabel(name)
        title_label.setWordWrap(True)
        title_label.setMaximumWidth(250)
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        title_label.setStyleSheet("""
    color: #ffc777 ;
    font-size: 14px;
    font-weight: bold;
    padding: 0px;
    background: transparent;
    border:none;
""")

        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(title_label)
        frame_layout.addSpacing(6)

        # read more Link
        link_button = QPushButton(link_text)
        link_button.setStyleSheet("""
            color: #7dcfff ; background: transparent; border: none; font-size: 12px;
            text-decoration: underline; 
        """)
        link_button.clicked.connect(self.handle_read_more)  
        frame_layout.addWidget(link_button)
        frame_layout.addSpacing(6)

        # Like and Dislike Buttons 
        self.like_button = QPushButton()
        self.dislike_button = QPushButton()    
        self.like_button.setIcon(icon("fa6.thumbs-up", color="white"))
        self.dislike_button.setIcon(icon("fa6.thumbs-down", color="white"))
        self.like_button.setStyleSheet("background: transparent; border: none; font-size: 20px;width:50px;")
        self.dislike_button.setStyleSheet("background: transparent; border: none; font-size: 20px;width:50px;")
        
        # buttons layout
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.like_button)
        button_layout.addWidget(self.dislike_button)
        frame_layout.addLayout(button_layout)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)        

        self.setLayout(main_layout)
        self.setMinimumWidth(250)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # buttons functions
        self.like_button.clicked.connect(self.toggle_like)
        self.dislike_button.clicked.connect(self.toggle_dislike)


    def toggle_like(self):
        if self.liked:
            self.like_button.setStyleSheet("background: transparent; border: none; font-size: 20px;width:50px;")
            self.liked = False
        else:
            self.like_button.setStyleSheet("background: #41a6b5 ; border-radius: 10px; font-size: 20px; padding: 5px;width:50px;")
            self.liked = True
            self.disliked = False
            self.dislike_button.setStyleSheet("background: transparent; border: none; font-size: 20px;width:50px;")

    def toggle_dislike(self):
        if self.disliked:
            self.dislike_button.setStyleSheet("background: transparent; border: none; font-size: 20px;width:50px;")
            self.disliked = False
        else:
            self.dislike_button.setStyleSheet("background: #c53b53 ; border-radius: 10px;font-size: 20px; padding: 5px;width:50px;")
            self.disliked = True
            self.liked = False
            self.like_button.setStyleSheet("background: transparent; border: none; font-size: 20px;width:50px;")

    def handle_read_more(self):
        self.read_more_clicked = True
        self.detail_page.update_details(self.title,self.state_district,self.city,self.address,self.category)
        self.stacked_widget.setCurrentIndex(1)  
    
    def calculate_score(self):
        if self.read_more_clicked and self.liked:
            return 10
        elif self.read_more_clicked and self.disliked:
            return -5
        elif self.liked:
            return 8
        elif self.disliked:
            return -8
        elif self.read_more_clicked:
            return 3
        else:
            return -1  
        
    def open_detail_page(self, title):
        self.detail_page.update_details(title)
        self.stacked_widget.setCurrentIndex(1) 


class DetailPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.setStyleSheet(" color: #c0caf5 ;")
        layout = QVBoxLayout(self)

        # Title Label (Will be updated dynamically)
        self.detail_label = QLabel("")
        self.detail_label.setStyleSheet("font-size: 25px; font-weight: bold; color: #ff007c ; margin-bottom: 10px;")
        self.detail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.detail_label)

        # State/District Label
        self.state_label = QLabel("")
        self.state_label.setStyleSheet("font-size: 18px;font-weight: bold;")
        self.state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.state_label)

        # City Label
        self.city_label = QLabel("")
        self.city_label.setStyleSheet("font-size: 18px;font-weight: bold;")
        self.city_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.city_label)
        
        # Category Label
        self.category_label = QLabel("")
        self.category_label.setStyleSheet("font-size: 18px;font-weight: bold; ")
        self.category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.category_label)

        # Address Label (Multi-line)
        self.address_label = QLabel("")
        self.address_label.setWordWrap(True)  
        self.address_label.setMinimumHeight(50)
        self.address_label.setStyleSheet("font-size: 13px; color: #7dcfff  ; padding: 5px; border: 1px solid #4fd6be ; border-radius: 5px; background-color: #292e42 ;")
        self.address_label.setAlignment(Qt.AlignmentFlag.AlignTop)  
        layout.addWidget(self.address_label)

        # Back Button
        back_button = QPushButton("Back to Main Page")
        back_button.setStyleSheet("""
    QPushButton {
        background-color: #3d59a1;
        color: #c0caf5;
        padding: 8px;
        border-radius: 5px;
        margin-top: 15px;
    }
    QPushButton:hover {
        background-color: #292e42;
        color: #c0caf5;
    }
""")
        back_button.clicked.connect(self.go_back)

        layout.addWidget(back_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    def update_details(self, title,state_district,city,address,category):
        self.detail_label.setText(f"Details of {title}")
        self.state_label.setText(f"District: {state_district}")
        self.city_label.setText(f"City: {city}")
        self.category_label.setText(f"Category: {category}")
        self.address_label.setText(f"{address}")

    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)


class ResultWindow(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent

        # Stacked Widget 
        self.stacked_widget = QStackedWidget()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stacked_widget)

        # Create pages
        self.grid_page = QWidget()
        self.detail_page = DetailPage(self.stacked_widget)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.grid_page)
        self.stacked_widget.addWidget(self.detail_page)
        
        # Store content boxes
        self.content_boxes = []

        # Loading Widget
        self.loading_widget = QWidget()
        loading_layout = QVBoxLayout(self.loading_widget)

        # State Label (Displays "Loading for: <State>")
        self.loading_label = QLabel("")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #ff007c ;
        """)
        loading_layout.addWidget(self.loading_label)

        # Loading GIF Animation
        self.loading_spinner = QLabel()
        self.movie = QMovie("assets/loading0.gif")  
        self.loading_spinner.setMovie(self.movie)
        self.loading_spinner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_layout.addWidget(self.loading_spinner)

        self.stacked_widget.addWidget(self.loading_widget)  

        # Setup Grid Page
        self.setup_grid_page()
        


    def setup_grid_page(self):
        main_layout = QVBoxLayout(self.grid_page)

        # Heading
        self.heading_label = QLabel("")
        self.heading_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #4fd6be ; margin-bottom: 10px;")
        self.heading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.heading_label)

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # Grid Container
        grid_container = QWidget()
        self.grid_layout = QGridLayout(grid_container)
        self.scroll_area.setWidget(grid_container)
        main_layout.addWidget(self.scroll_area)

        # Footer
        footer_layout = QHBoxLayout()

        home_button = QPushButton("Back")
        home_button.setStyleSheet("background-color: #9d7cd8; color: #24283b;font-weight: bold; padding: 8px; border-radius: 5px;")
        home_button.clicked.connect(self.parent.show_state_selection)
        footer_layout.addWidget(home_button)

        next_button = QPushButton("Save")
        next_button.setStyleSheet("background-color: #c3e88d; color: #24283b;font-weight: bold; padding: 8px; border-radius: 5px;")
        next_button.clicked.connect(self.print_scores)  
        footer_layout.addWidget(next_button)

        main_layout.addLayout(footer_layout)
        
    def display_recommendations(self, state):
        
        self.state = state
        self.heading_label.setText(f"State : {self.state}")

        # Update loading text
        self.loading_label.setText(f"Fetching places for: {state}")

        # Show loading screen with animation
        self.movie.start() 
        self.stacked_widget.setCurrentWidget(self.loading_widget)  

        # Start fetching places in a separate thread
        self.thread = FetchPlacesThread(state)
        self.thread.fetched.connect(self.update_ui)
        self.thread.start()

        
    def update_ui(self, df):
        if df.empty:
            df = pd.DataFrame([{"name": "No places found", "state_district": "", "city": "", "address": ""}])
       
        df = df[~df['name'].fillna('NaN').isin(['NaN', 'N/A'])].drop_duplicates()
        
        place_names = df["name"].tolist() if not df.empty else ["No places found"]
        
        # Hide loading screen
        self.movie.stop() 
        self.stacked_widget.setCurrentWidget(self.grid_page)  
        
         # Clear previous widgets from the grid
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Compute grid size
        cols = 3
        rows = (len(place_names) + cols - 1) // cols  
        index=0;
        # print(place_names[index])
        for row in range(rows):
            for col in range(cols):
                if index >= len(place_names):  # Avoid out-of-bounds error
                    break
                
                # Extract details from df for this place
                place = df.iloc[index]
                name = place["name"]
                state_district = place["district"]
                city = place["city"]
                address = place["address"]
                category = place["category"]
                
                # Add ContentBox
                box = ContentBox(name,state_district,city,address,category, "Read more:", self.stacked_widget, self.detail_page)
                self.content_boxes.append(box)  
                self.grid_layout.addWidget(box, row, col)  
                index +=1


        # Ensure layout is applied
        self.scroll_area.widget().setLayout(self.grid_layout)
        self.scroll_area.widget().update()
    
    def print_scores(self, state):
        """Calculate scores for each category and store them using score_manager.py."""

        # Categories being used in this project
        categories = ["tourism", "entertainment", "leisure", "natural", "camping", "beach"]

        # Initialize dictionary to store category scores
        category_scores = {category: {"reward": 0, "count": 0} for category in categories}

        # Compute scores per category
        for box in self.content_boxes:
            category = box.category.lower()  # Ensure consistent casing
            if category in category_scores:  # Only count known categories
                category_scores[category]["reward"] += box.calculate_score()
                category_scores[category]["count"] += 1

        # Call save_scores() to store results in a file
        save_scores(self.state, category_scores)
         

