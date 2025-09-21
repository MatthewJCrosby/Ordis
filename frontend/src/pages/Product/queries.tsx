// Query: Get all products
export const GET_PRODUCTS = `
  query {
    products {
      id
      name
      description
      price
    }
  }
`;

// Query: Get a single product by ID
export const GET_PRODUCT = (id: string | number) => `
  query {
    product(id: ${id}) {
      id
      name
      description
      price
    }
  }
`;

// Mutation: Create a product
export const CREATE_PRODUCT = (name: string, description: string, price: number) => `
  mutation {
    createProduct(input: {
      name: "${name}",
      description: "${description}",
      price: ${price}
    }) {
      id
      name
      description
      price
    }
  }
`;

// Mutation: Update a product
export const UPDATE_PRODUCT = (id: string | number, name: string, description: string, price: number) => `
  mutation {
    updateProduct(id: ${id}, input: {
      name: "${name}",
      description: "${description}",
      price: ${price}
    }) {
      id
      name
      description
      price
    }
  }
`;

// Mutation: Delete a product
export const DELETE_PRODUCT = (id: string | number) => `
  mutation {
    deleteProduct(id: ${id}) 
  }
`;