import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { GET_PRODUCTS } from "./queries";
import { graphqlRequest } from "../../api";

type Product = {
  id: number;
  name: string;
  description: string;
  price: string;
};

export default function ProductList() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    graphqlRequest(GET_PRODUCTS).then(result => {
        setProducts(result.data.products);
        setLoading(false);
    });
    }, []);

  if (loading) return <p>Loading...</p>;

  return (
  <div>
    <h2>Products</h2>
    <Link to="/product/create">Create New Product</Link>
    <div className="card-form-grid">
      {products.map(prod => (
        <div className="card-form" key={prod.id}>
          <div className="card-form-header">{prod.name}</div>
          <div className="card-form-body">
            <div className="product-card-description">{prod.description}</div>
            <div className="product-card-price">${prod.price}</div>
            <div style={{ marginTop: "1rem" }}>
              <Link to={`/product/edit/${prod.id}`}>Edit</Link>
            </div>
          </div>
        </div>
      ))}
    </div>
  </div>
);
}