# Purchase/Sales Management App

## 📖 About

The **Purchase/Sales Management App** is a robust and user-friendly web application designed to streamline inventory and financial management for small businesses. Built using Flask, this application offers an intuitive platform for tracking stock levels, managing purchases, processing sales, and maintaining an up-to-date cash balance—all in real-time.

## 🛠️ Technology Stack

- **Backend**: Flask (Python)  
  - Utilized Flask to create RESTful APIs and handle backend operations.  

- **Frontend**: HTML, CSS, JavaScript  
  - Designed an interactive and responsive user interface for seamless user experience.  

- **Database**: SQLite (via SQLAlchemy)  
  - Used SQLAlchemy as the Object Relational Mapper (ORM) for efficient database operations.  

## 🖼️Application Screenshots

### 01.HomePage:
![Screenshot 2024-11-17 141435](https://github.com/user-attachments/assets/0bada802-b8d4-4748-94b7-564c2fb8a267)

**Overview**:  
The home page serves as the central hub for navigating the application. It offers quick access to all major features via neatly organized action cards.

**Key Features**:
- **Displays current cash balance** in real-time for better financial tracking.
- Four main options for managing the inventory:
  1. **Add Items**: Redirects users to a page for adding new items to the inventory.
  2. **Purchase Items**: Allows users to record and manage stock purchases.
  3. **Sale Items**: For selling items and updating inventory.
  4. **Overall Reports**: Access detailed reports on purchases and sales.

 ### 02.Add/View Products Page:
 ![Screenshot 2024-11-17 142931](https://github.com/user-attachments/assets/2838b424-214f-4327-ae45-d7abdf9a2bdb)

This page allows users to add new products to the inventory by entering the item name. It displays a list of existing products with their current stock levels and options to edit or delete them. The current cash balance is prominently shown on the top right for easy tracking. The left sidebar provides navigation to key sections: Home, Add Items, Purchase, Sales, and Reports.

 ### 03.Purchase Page:
 ![Screenshot 2024-11-17 145206](https://github.com/user-attachments/assets/62aa8103-4459-4ecd-a817-cce20600c768)
 ![Screenshot 2024-11-17 153432](https://github.com/user-attachments/assets/5e36e56b-0870-4b84-820a-d57bbe319be1)

The **Purchase** page enables users to:
- **Items Search:** Quickly find specific items to purchase using the search box.
- **Filter Options:** Display the product table based on:
  - All items
  - Selected items
  - Unselected items
- **Purchase Multiple Items:** Set quantities and rates for multiple items simultaneously.
- **Cash balance** Updates are shown at the top right for quick tracking.
- **Scroll for Purchase History:** At the bottom of the page, view a detailed table of past purchases to track previous transactions.

### 04.Sales Page:
![Screenshot (361)](https://github.com/user-attachments/assets/498e99b1-f9a1-409d-9ef9-13c13107d9e4)
![Screenshot 2024-11-17 153602](https://github.com/user-attachments/assets/bac9598f-0cf5-4591-bbd3-1dc9d819b200)

  This page allows users to manage item sales efficiently. Key features include:
- **Search and Filter**: Users can search for items to sell using the provided search bar or filter dropdown.
- **Real-Time Updates**: The cash balance is prominently displayed on the top-right corner and updates dynamically after every transaction.
- **Item Management**: 
  - View available stock levels for each item.
  - Enter the quantity of items to be sold in the corresponding input field.
  - Automatically calculate the total amount based on the quantity and item rate.
- **Scroll for Purchase History:** At the bottom of the page, view a detailed table of past purchases to track previous transactions.
The left sidebar provides easy navigation to other sections like Home, Add Items, Purchase, Sales, and Reports.

### 05.Overall Reports
![Screenshot 2024-11-17 152400](https://github.com/user-attachments/assets/70def4b8-bef1-42ad-b636-ad08f258670a)

This page provides a comprehensive summary of all transactions, including purchases and sales, highlighting the profit or loss for each item.
- **Item Details**: Displays item names along with their stock availability.
- **Financial Metrics**:
  - Purchased Amount: Total cost of items purchased.
  - Sold Amount: Revenue generated from sales.
  - Profit/Loss: Indicates the net profit (in green) or loss (in red) for each item.
- **Cash Balance**: Current cash balance is prominently displayed at the top right for easy reference.

  
## ⚙️ Setup and Installation

Follow these steps to set up the project locally:

### Prerequisites
- **Python 3.x**  
- **Flask**: Install Flask by running:  
  ```bash
  pip install flask
  ```  
- **SQLite**: Required for database management.

### Installation

1. **Clone the Repository**:  
    Clone the project repository to your local machine.
    ```bash
    git clone https://github.com/yourusername/Flask-Inventory-Management-App.git
    cd Flask-Inventory-Management-App
    ```

2. **Install Required Packages**:  
    Install all necessary dependencies listed in the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

3. **Initialize Database**:  
    Set up the SQLite database by running the following command:  
    ```bash
    python initialize_db.py
    ```  
    This will create the necessary tables for storing item data, purchase and sales history, and cash balance.

4. **Run the Application**:  
    Start the Flask application.
    ```bash
    flask run
    ```

5. **Access the Application**:  
    Open the application in your browser at:  
    [http://127.0.0.1:5000](http://127.0.0.1:5000)


## 🚀 Key Features

- **Inventory Management:** Add, edit, and track items with live updates to stock levels.
- **Transaction Recording:** Record purchases and sales with dynamic adjustments to inventory and cash balance.
- **Real-Time Reporting:** Generate real-time reports for stock levels and financial metrics.
- **User-Friendly Interface:** Intuitive forms and dashboards for easy navigation and operation.

## 🎁 Bonus Features

- **Automatically track item quantities:**
  - Increase stock levels with purchases.
  - Decrease stock levels with sales.
- **Generate consolidated reports** for both cash balance and item quantities.
