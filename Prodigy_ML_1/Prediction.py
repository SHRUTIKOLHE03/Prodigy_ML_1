import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtGui import QLinearGradient, QColor
from PyQt5.QtCore import Qt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Prodigy_ML_Task1')

        # Apply gradient background
        self.set_gradient_background()

        # Read the dataset
        dataset_path = r"C:\Users\HP\Desktop\Prodigy Infotech\Prodigy_ML_1\Housing.csv"
        try:
            self.df = pd.read_csv(dataset_path)
        except FileNotFoundError:
            print(f"Dataset not found at {dataset_path}. Make sure the file path is correct.")
            sys.exit(1)

        # Create input widgets
        self.areaLabel = QLabel('Enter Area in Sq. Ft:')
        self.areaInput = QLineEdit(self)

        self.bedroomsLabel = QLabel('Enter Number of Bedrooms:')
        self.bedroomsInput = QLineEdit(self)

        self.bathroomsLabel = QLabel('Enter Number of Bathrooms:')
        self.bathroomsInput = QLineEdit(self)

        self.predictButton = QPushButton('Predict Estimated Price', self)
        self.predictButton.clicked.connect(self.predict_price)

        # Create a table widget
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(['Estimated Price: '])

        # Create a label for context
        self.resultLabel = QLabel(self)
        self.resultLabel.setAlignment(Qt.AlignCenter)

        # Create a layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.areaLabel)
        input_layout.addWidget(self.areaInput)
        input_layout.addWidget(self.bedroomsLabel)
        input_layout.addWidget(self.bedroomsInput)
        input_layout.addWidget(self.bathroomsLabel)
        input_layout.addWidget(self.bathroomsInput)
        input_layout.addWidget(self.predictButton)

        result_layout = QVBoxLayout()
        result_layout.addWidget(self.resultLabel)

        table_layout = QVBoxLayout()
        table_layout.addWidget(self.tableWidget)

        main_layout = QHBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(result_layout)
        main_layout.addLayout(table_layout)

        self.setLayout(main_layout)
        self.show()

    def set_gradient_background(self):
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(255, 255, 255))   # White
        gradient.setColorAt(1.0, QColor(0, 0, 0))  # Black

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(self.backgroundRole(), gradient)
        self.setPalette(palette)

    def predict_price(self):
        # Prepare the features (X) and target variable (y)
        features = self.df[['area', 'bedrooms', 'bathrooms']]
        target = self.df['price']

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        # Create a linear regression model
        model = LinearRegression()

        # Train the model
        model.fit(X_train, y_train)

        # Make predictions
        area = float(self.areaInput.text())
        bedrooms = float(self.bedroomsInput.text())
        bathrooms = float(self.bathroomsInput.text())

        # Predict the price
        predicted_price = model.predict([[area, bedrooms, bathrooms]])

        # Clear the table and display the predicted price
        self.tableWidget.clearContents()
        item = QTableWidgetItem(f'${predicted_price[0]:,.2f}')
        self.tableWidget.setItem(0, 0, item)

        # Update the label with context
        self.resultLabel.setText(f'<font color="white">Estimated Price: ${predicted_price[0]:,.2f}</font>')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MyApp()
    sys.exit(app.exec_())
