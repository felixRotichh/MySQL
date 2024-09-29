from crud import *

# Creating database interactions
def make_customer():
    name = input("Enter customer name: ")
    email = input("Enter customer email: ")
    create_customer(name, email)
    print(f"Customer '{name}' created.")

def make_product():
    name = input("Enter product name: ")
    price = float(input("Enter product price: "))
    stock = int(input("Enter stock quantity: "))
    create_product(name, price, stock)
    print(f"Product '{name}' added.")

def make_order():
    customer_id = int(input("Enter customer ID to create order for: "))
    product_quantities = {}

    while True:
        product_name = input("Enter product name (or 'done' to finish): ")
        if product_name.lower() == 'done':
            break
        quantity = int(input(f"Enter quantity for {product_name}: "))
        product_quantities[product_name] = quantity
    
    try:
        create_order(customer_id, product_quantities)
        print(f"Order created for customer ID {customer_id}.")
    except Exception as e:
        print(f"Failed to create order: {e}")

# Add function to update product stock
def update_product_stock_menu():
    product_id = int(input("Enter the product ID to update stock: "))
    new_stock = int(input("Enter the new stock quantity: "))
    update_product_stock(product_id, new_stock)

# Main function
def main():
    while True:
        print("\n=== Store Management System ===")        
        print("1. Create Customer")
        print("2. Create Product")
        print("3. Create Order")
        print("4. View Customers")
        print("5. View Products")
        print("6. View Orders")
        print("7. Update Product Price")
        print("8. Update Product Stock")
        print("9. Delete Customer")
        print("10. Exit")

        option = input("Select an option (1-10): ")
        
        if option == "1":
            make_customer()
        elif option == "2":
            make_product()
        elif option == "3":
            make_order()
        elif option == "4":
            customers = get_customers()
            print("Customers: ", customers if customers else "No customers found.")
        elif option == "5":
            products = get_products()
            print("Products: ", products if products else "No products found.")
        elif option == "6":
            orders = get_orders()
            print("Orders: ", orders if orders else "No orders found.")
        elif option == "7":
            product_id = int(input("Enter product ID to update price: "))
            new_price = float(input("Enter new price: "))
            update_product_price(product_id, new_price)
            print("Product price updated.")
        elif option == "8":
            update_product_stock_menu()
        elif option == "9":
            customer_id = int(input("Enter Customer ID to delete: "))
            delete_customer(customer_id)
            print("Customer deleted.")
        elif option == "10":
            print("Exiting the application.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
