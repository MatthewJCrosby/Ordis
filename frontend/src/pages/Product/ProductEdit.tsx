import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import ProductForm from "./ProductForm";
import { GET_PRODUCT } from "./queries";
import { graphqlRequest } from "../../api";

export default function ProductEdit() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);



  useEffect(() => {
    if (!id) {
      setLoading(false);
      setProduct(null);
      return;
    }
    graphqlRequest(GET_PRODUCT(id)).then(result => {
      setProduct(result.data.product);
      setLoading(false);
    });
  }, [id]);

  if (loading) return <p>Loading...</p>;
  if (!product) return <p>Product not found.</p>;

  if (loading) return <p>Loading...</p>;
  if (!product) return <p>Product not found.</p>;


  return (
    <ProductForm
      initialValues={product}
      editMode={true}
      onSuccess={updated => {alert("Product updated!"); navigate(`/products`)}}
      onCancel={() => window.history.back()}
    />
  );
}