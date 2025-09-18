import ProductForm from "./ProductForm";

export default function ProductCreate() {
  return (
    <div>
      <ProductForm onSuccess={product => {
        
        alert("Product created!");
      }} />
    </div>
  );
}