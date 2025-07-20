# backend/test_db_init.py
from db.session import init_db, db_session
from app.models import Customer

def run_test():
    print("🔧 Initializing DB...")
    init_db()  # Ensures tables exist

    print("➕ Creating test customer...")
    test_customer = Customer(name="Test User", email="test@example.com")
    db_session.add(test_customer)
    db_session.commit()

    print("🔍 Querying back test customer...")
    result = db_session.query(Customer).filter_by(email="test@example.com").first()

    if result:
        print(f"✅ Retrieved: id={result.id}, name={result.name}, email={result.email}")
        print("🧹 Cleaning up test data...")
        db_session.delete(result)
        db_session.commit()
    else:
        print("❌ Customer not found — something went wrong.")

    print("✅ DB test completed.")

if __name__ == "__main__":
    run_test()
