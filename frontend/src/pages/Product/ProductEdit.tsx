import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import ProductForm from "./ProductForm";

export default function ProductEdit() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:5000/products/${id}`)
      .then(res => res.json())
      .then(setProduct);
  }, [id]);

  if (!product) return <p>Loading...</p>;

  return (
    <ProductForm
      initialValues={product}
      editMode={true}
      onSuccess={updated => alert("Product updated!")}
      onCancel={() => window.history.back()}
    />
  );
}