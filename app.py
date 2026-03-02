from loguru import logger

from transactions import Transaction, Category, calculate_financial_summary
from database import get_session
from sqlalchemy import select
# import decimal 
from decimal import Decimal

def main():
    logger.add("logs/app.log", rotation="1 MB")
    # Initialize database and create tables
    # Get a session
    session = get_session()

    try:
        # Ensure transaction table exists by querying it
        session.query(Transaction).first()

        # Query all transactions from the database
        all_transactions = session.query(Transaction).all()

        # Calculate and display summary
        summary = calculate_financial_summary(all_transactions)
        print("Financial Summary:")
        for key, value in summary.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    except Exception as e:
        logger.error(
            f"You may need to seed the database first, run 'python seed.py' and try again.\n\n"
        )
        raise e

    finally:
        session.close()
        # TODO: Once you have added the Entertainment category and sample  expenses, uncomment the lines below to display them!
        # display_transactions_by_category("Job")
        # display_transactions_by_category("Entertainment")


# TODO: Add the entertainment category, if it does not already exist
# NOTE: This means checking if a category with that name exists first
def add_entertainment_category():
    session = get_session()
    try:
        # check if Entertainment category already exists
        entertainment_category = session.query(Category).filter_by(name="Entertainment").first()
        if entertainment_category:
            logger.info("Entertainment category already exists.")
            return  # If it already exists, do nothing

        # If not, create it
        new_category = Category(name="Entertainment")
        session.add(new_category)
        session.commit()
        logger.info("Entertainment category added successfully.")

        
    finally:
        session.close()


# TODO: Add sample entertainment expenses
# NOTE: Fetch the Entertainment category first, then add two sample expenses linked to that category
def add_entertainment_expenses():
    session = get_session()
    try:
        # check if Entertainment category already exists
        entertainment_category = session.query(Category).filter_by(name="Entertainment").first()
        if not entertainment_category:
            logger.warning("Entertainment category does not exist.")
            return  # If no Entertainment category, do nothing

        # Add sample expenses for the Entertainment category
        sample_expenses = [
            Transaction(
                date="2024-01-15",
                description="Movie tickets",
                amount=Decimal("-45.00"),
                category_ref=entertainment_category,
            ),
            Transaction(
                date="2024-01-20",
                description="Concert tickets",
                amount=Decimal("-85.50"),
                category_ref=entertainment_category,
            ),
        ]
        session.add_all(sample_expenses)
        session.commit()
    finally:
        session.close()


# TODO: Display all transactions for a given category name
def display_transactions_by_category(category_name: str):
    session = get_session()
    try:
        # fetch the category 
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            logger.warning(f"Category '{category_name}' does not exist.")
            return  # If category doesn't exist, do nothing
        transactions = session.query(Transaction).filter_by(category_id=category.id).all() 
        #print the results
        print(f"Transactions in category '{category_name}':")
        for every_transaction in transactions:
            print(every_transaction)

    except Exception as e:
        logger.error(
            f"Error displaying transactions for category '{category_name}': {e}"
        )
    finally:
        session.close()


if __name__ == "__main__":
    main()
