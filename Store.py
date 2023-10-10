from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['stock_database']
collection = db['stocks']

# Function to prompt user for stock data
def prompt_stock_data():
    category = input("Enter the category: ")
    sub_category = input("Enter the sub-category: ")
    item = input("Enter the item: ")
    volume = int(input("Enter the volume: "))
    condition = input("Is the stock new or used? (new/used): ")

    if condition == "new":
        warranty = input("Enter the warranty information: ")

        stock_data = {
            'category': category,
            'sub_category': sub_category,
            'item': item,
            'volume': volume,
            'condition': condition,
            'warranty': warranty
        }

    elif condition == "used":
        previous_owner = input("Enter the previous owner: ")
        reason_for_change = input("Enter the reason for changing: ")

        stock_data = {
            'category': category,
            'sub_category': sub_category,
            'item': item,
            'volume': volume,
            'condition': condition,
            'previous_owner': previous_owner,
            'reason_for_change': reason_for_change
        }

    else:
        print("Invalid condition. Stock data not stored.")
        return None

    return stock_data

# Function to store stock data
def store_stock_data(stock_data):
    if stock_data['condition'] == "new":
        collection_new = db['stocks_new']
        existing_item = collection_new.find_one({'item': stock_data['item']})
        if existing_item:
            new_volume = existing_item['volume'] + stock_data['volume']
            collection_new.update_one({'item': stock_data['item']}, {'$set': {'volume': new_volume}})
            print("Item already exists. Volume updated successfully!")
        else:
            collection_new.insert_one(stock_data)
            print("New item added to the database!")
    elif stock_data['condition'] == "used":
        collection_used = db['stocks_used']
        existing_item = collection_used.find_one({'item': stock_data['item']})
        if existing_item:
            new_volume = existing_item['volume'] + stock_data['volume']
            collection_used.update_one({'item': stock_data['item']}, {'$set': {'volume': new_volume}})
            print("Item already exists. Volume updated successfully!")
        else:
            collection_used.insert_one(stock_data)
            print("Used item added to the database!")
    else:
        print("Invalid condition. Stock data not stored.")

# Function to find and display stock data
def find_stock_data():
    condition = input("Are you searching for new or used items? (new/used): ")

    if condition == "new":
        collection = db['stocks_new']
    elif condition == "used":
        collection = db['stocks_used']
    else:
        print("Invalid condition. Stock data not found.")
        return

    category = input("Enter the category: ")
    sub_category = input("Enter the sub-category: ")
    item = input("Enter the item: ")

    stock_data = {
        'category': category,
        'sub_category': sub_category,
        'item': item
    }
    
    result = collection.find(stock_data)
    count = collection.count_documents(stock_data   )


    if count > 0:
        print("Stock data found:")
        for item in result:
            print(item)
    else:
        print("No stock data found.")
        
def run_interface():
    print("Welcome to the Stock Management System!")
    while True:
        print("\nWhat would you like to do?")
        print("1. Store stock data")
        print("2. Find stock data")
        print("3. Exit")

        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == "1":
            stock_data = prompt_stock_data()
            if stock_data:
                store_stock_data(stock_data)
        elif choice == "2":
            find_stock_data()  # Remove the arguments from this line
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the CLI interface
run_interface()