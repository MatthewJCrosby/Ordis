def test_workflow(client):

    customer_id = create_and_update_customer(client)
    employee_id = create_update_employee(client)
    product_id = create_update_product(client)
    order_id = create_update_order(client, customer_id, employee_id)
    line_item_id = create_update_line_item(client, order_id, product_id)
    cleanup_entities(client, line_item_id, order_id, product_id, employee_id, customer_id)


def create_and_update_customer(client):
    """Test creating and updating a customer"""
    
    # Step 1: Create Customer
    create_customer_query = """
    mutation {
        createCustomer(input: {
            first_name: "Matt",
            last_name: "C",
            email: "matt@test.com",

        }) {
            id
            first_name
            last_name
            email

        }
    }
    """
    
    create_response = client.post('/graphql', json={'query': create_customer_query})

    assert create_response.status_code == 200
    create_data = create_response.get_json()['data']['createCustomer'] 
    assert create_data['first_name'] == "Matt"
    assert create_data['last_name'] == "C"
    assert create_data['email'] == "matt@test.com"

    
    customer_id = create_data['id']
    print(f"Created customer with ID: {customer_id}")
    
    # Update a customer
    update_customer_query = """
    mutation UpdateCustomer($id: ID!, $input: CustomerUpdateInput!) {
        updateCustomer(id: $id, input: $input) {
            id
            first_name
            email
        }
    }
    """
    
    variables = {
        "id": customer_id,
        "input": {
            "first_name": "Matthew",
            "email": "matthew@test.com"
        }
    }
    
    update_response = client.post('/graphql', json={
        'query': update_customer_query,
        'variables': variables
    })

    assert update_response.status_code == 200
    update_data = update_response.get_json()['data']['updateCustomer']
    assert update_data['first_name'] == "Matthew"
    assert update_data['email'] == "matthew@test.com"

    print(f"Updated customer with ID: {customer_id}")
    return customer_id

def create_update_employee(client):

    create_employee_query = """
    mutation {
        createEmployee(input: {
            name: "John Doe",
            department: "Customer Service"
        }) {
            id
            name
            department
        }
    }
    """

    create_response = client.post('/graphql', json={'query': create_employee_query})

    assert create_response.status_code == 200
    create_data = create_response.get_json()['data']['createEmployee']
    assert create_data['name'] == "John Doe"
    assert create_data['department'] == "Customer Service"

    employee_id = create_data['id']
    print(f"Created employee with ID: {employee_id}")

    #update an employee
    update_employee_query = """
    mutation UpdateEmployee($id: ID!, $input: EmployeeUpdateInput!) {
        updateEmployee(id: $id, input: $input) {
            id
            name
            department
        }
    }
    """

    variables = {
        "id": employee_id,
        "input": {
            "name": "John Smith",
            "department": "Service Technician"
        }
    }

    update_response = client.post('/graphql', json={
        'query': update_employee_query,
        'variables': variables
    })

    assert update_response.status_code == 200
    update_data = update_response.get_json()['data']['updateEmployee']
    assert update_data['name'] == "John Smith"
    assert update_data['department'] == "Service Technician"

    print(f"Updated employee with ID: {employee_id}")
    return employee_id

def create_update_product(client):

    create_product_query = """
    mutation{
        createProduct(input: {
            name: "Sample Product",
            description: "This is a sample product.",
            price: 19.99
        }) {
            id
            name
            description
            price
        }
    }
    """
    create_response = client.post('/graphql', json={'query': create_product_query})
    assert create_response.status_code == 200
    create_data = create_response.get_json()['data']['createProduct']
    assert create_data['name'] == "Sample Product"
    assert create_data['description'] == "This is a sample product."
    assert create_data['price'] == 19.99

    product_id = create_data['id']
    print(f"Created product with ID: {product_id}")

    #update a product
    update_product_query = """
    mutation UpdateProduct($id: ID!, $input: ProductUpdateInput!) {
        updateProduct(id: $id, input: $input) {
            id
            name
            description
            price
        }
    }
    """

    variables = {
        "id": product_id,
        "input": {
            "name": "Updated Product",
            "description": "This is an updated product.",
            "price": 29.99
        }
    }

    update_response = client.post('/graphql', json={
        'query': update_product_query,
        'variables': variables
    })

    assert update_response.status_code == 200
    update_data = update_response.get_json()['data']['updateProduct']
    assert update_data['name'] == "Updated Product"
    assert update_data['description'] == "This is an updated product."
    assert update_data['price'] == 29.99

    print(f"Updated product with ID: {product_id}")
    return product_id

def create_update_order(client, customer_id, employee_id):
    """Test creating and updating an order"""
    
    # Create Order
    create_order_query = """
    mutation CreateOrder($input: OrderCreateInput!) {
        createOrder(input: $input) {
            id
            customer {
                first_name
                last_name
            }
            total
        }
    }
    """
    
    variables = {
        "input": {
            "customer_id": customer_id  # Use the passed customer_id
        }
    }
    
    create_response = client.post('/graphql', json={
        'query': create_order_query,
        'variables': variables
    })

    assert create_response.status_code == 200
    create_data = create_response.get_json()['data']['createOrder']
    assert create_data['customer']['first_name'] == "Matthew"  # From your updated customer
    assert create_data['customer']['last_name'] == "C"
    # total should be null/0 since no line items yet

    order_id = create_data['id']
    print(f"Created order with ID: {order_id}")

    #Update order
    update_order_query = """
    mutation UpdateOrder($id: ID!, $input: OrderUpdateInput!) {
        updateOrder(id: $id, input: $input) {
            id
            service_tech {
                id
                name
                department
            }
        }
    }
    """

    update_variables = {
        "id": order_id,
        "input": {
            "service_tech_id": employee_id
        }
    }

    update_response = client.post('/graphql', json={
        'query': update_order_query,
        'variables': update_variables
    })

    assert update_response.status_code == 200
    update_data = update_response.get_json()['data']['updateOrder']
    assert update_data['service_tech'] is not None, "Service tech should not be None"
    assert update_data['service_tech']['name'] == "John Smith"
    assert update_data['service_tech']['department'] == "Service Technician"

    print(f"Updated order - assigned service tech: {update_data['service_tech']['name']}")
    return order_id

def create_update_line_item(client, order_id, product_id):
    """Test creating and updating a line item (tests order total calculation)"""
    
    #Create LineItem
    create_line_item_query = """
    mutation CreateLineItem($input: LineItemCreateInput!) {
        createLineItem(input: $input) {
            id
            name
            description
            qty
            price
            order {
                id
                total
            }
        }
    }
    """
    
    variables = {
        "input": {
            "order_id": order_id,
            "product_id": product_id,
            "qty": 2
        }
    }
    
    create_response = client.post('/graphql', json={
        'query': create_line_item_query,
        'variables': variables
    })

    assert create_response.status_code == 200
    create_data = create_response.get_json()['data']['createLineItem']
    assert create_data['qty'] == 2
    assert create_data['name'] == "Updated Product"  # Copied from product
    assert create_data['description'] == "This is an updated product."  # Copied from product
    assert float(create_data['price']) == 29.99  # Copied from product
    
    # Test order total calculation: 2 * 29.99 = 59.98
    expected_total = 2 * 29.99
    assert float(create_data['order']['total']) == expected_total

    line_item_id = create_data['id']
    print(f"Created line item with ID: {line_item_id}")
    print(f"Line item copied product data: {create_data['name']}")
    print(f"Order total calculated: ${create_data['order']['total']}")

    #Update LineItem
    update_line_item_query = """
    mutation UpdateLineItem($id: ID!, $input: LineItemUpdateInput!) {
        updateLineItem(id: $id, input: $input) {
            id
            qty
            price
            order {
                total
            }
        }
    }
    """

    update_variables = {
        "id": line_item_id,
        "input": {
            "qty": 3
        }
    }

    update_response = client.post('/graphql', json={
        'query': update_line_item_query,
        'variables': update_variables
    })

    assert update_response.status_code == 200
    update_data = update_response.get_json()['data']['updateLineItem']
    assert update_data['qty'] == 3
    
    # Test order total recalculation
    expected_total = 3 * 29.99
    assert float(update_data['order']['total']) == expected_total

    print(f"Updated line item quantity to 3")
    print(f"Order total recalculated: ${update_data['order']['total']}")
    
    return line_item_id

def cleanup_entities(client, line_item_id, order_id, product_id, employee_id, customer_id):
    """Delete all entities in logical order"""
    
    #Delete Line Item
    delete_line_item_query = """
    mutation DeleteLineItem($id: ID!) {
        deleteLineItem(id: $id)
    }
    """
    
    variables = {"id": line_item_id}
    response = client.post('/graphql', json={'query': delete_line_item_query, 'variables': variables})
    assert response.status_code == 200
    print(f"Deleted line item {line_item_id}")
    
    # Delete Order
    delete_order_query = """
    mutation DeleteOrder($id: ID!) {
        deleteOrder(id: $id)
    }
    """
    
    variables = {"id": order_id}
    response = client.post('/graphql', json={'query': delete_order_query, 'variables': variables})
    assert response.status_code == 200
    print(f"Deleted order {order_id}")
    
    #Delete Product
    delete_product_query = """
    mutation DeleteProduct($id: ID!) {
        deleteProduct(id: $id)
    }
    """
    
    variables = {"id": product_id}
    response = client.post('/graphql', json={'query': delete_product_query, 'variables': variables})
    assert response.status_code == 200
    print(f"Deleted product {product_id}")
    
    #Delete Employee
    delete_employee_query = """
    mutation DeleteEmployee($id: ID!) {
        deleteEmployee(id: $id)
    }
    """
    
    variables = {"id": employee_id}
    response = client.post('/graphql', json={'query': delete_employee_query, 'variables': variables})
    assert response.status_code == 200
    print(f"Deleted employee {employee_id}")
    
    # Step 5: Delete Customer
    delete_customer_query = """
    mutation DeleteCustomer($id: ID!) {
        deleteCustomer(id: $id)
    }
    """
    
    variables = {"id": customer_id}
    response = client.post('/graphql', json={'query': delete_customer_query, 'variables': variables})
    assert response.status_code == 200
    print(f"Deleted customer {customer_id}")
    
    print("All entities cleaned up successfully!")