import ProductForm from "./ProductForm";
import { useNavigate } from "react-router-dom";

export default function ProductCreate() {
  const navigate = useNavigate();

  return (
    <div>
      <ProductForm
        onSuccess={product => {
          alert("Product created!");
          navigate("/products");
        }}
      />
    </div>
  );
}