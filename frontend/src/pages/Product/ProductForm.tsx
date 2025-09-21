import React, {useState, useEffect} from "react";
import { CREATE_PRODUCT, DELETE_PRODUCT, UPDATE_PRODUCT } from "./queries";
import { graphqlRequest } from "../../api";

type Product ={
    id?: number;
    name: string;
    description: string;
    price: string;
}


type ProductFormProps = {
    initialValues?: Product;
    editMode?: boolean;
    onSuccess?: (product: Product) => void;
    onCancel?: () => void;
};

export default function ProductForm({ initialValues, editMode = false, onSuccess, onCancel}: ProductFormProps) {
    const [form, setForm] = useState<Product>({
    name: "",
    description: "",
    price: "",
    ...initialValues,
  });
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (initialValues) setForm({...initialValues, price: String(initialValues.price)});
  }, [initialValues]);

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
  e.preventDefault();
  setMessage("");
  try {
    const mutation = editMode
      ? UPDATE_PRODUCT(
        form.id!,
        form.name,
        form.description,
        parseFloat(form.price)
      )
      : CREATE_PRODUCT(
        form.name,
        form.description,
        parseFloat(form.price)
      )

    const result = await graphqlRequest(mutation);
    
    const data = editMode ? result.data.updateProduct : result.data.createProduct;

    if (data) {
      setMessage(editMode ? "Product updated!" : "Product created!");
      if (onSuccess) onSuccess(data);
      if (!editMode) setForm({ name: "", description: "", price: "" });
    } else {
      setMessage(result.errors?.[0]?.message || "Operation failed.");
    }
  } catch (err) {
    setMessage("Network error.");
  }
}

async function handleDelete() {
    if (!form.id) return;
    if (!window.confirm("Are you sure you want to delete this product?")) return;
    try {
      const result = await graphqlRequest(DELETE_PRODUCT(form.id));
      if (result.data?.deleteProduct) {
        setMessage("Product deleted!");
        if (onSuccess) onSuccess(result.data.deleteProduct);
      } else {
        setMessage(result.errors?.[0]?.message || "Delete failed.");
      }
    } catch {
      setMessage("Network error.");
    }
  }
  
  return (
    <div className="card-form">
  <div className="card-form-header">
    {editMode ? "Edit Product" : "Create Product"}
  </div>
  <form className="card-form-body" onSubmit={handleSubmit}>
    <div className="card-form-row">
      <label>Name:</label>
      <input name="name" value={form.name} onChange={handleChange} required />
    </div>
    <div className="card-form-row">
      <label>Description:</label>
      <textarea name="description" value={form.description} onChange={handleChange} />
    </div>
    <div className="card-form-row">
      <label>Price:</label>
      <input name="price" type="number" step="0.01" value={form.price} onChange={handleChange} required />
    </div>
    <div>
      {editMode && onCancel && (
        <button type="button" onClick={onCancel} style={{ marginRight: 8 }}>
          Cancel
        </button>
      )}
      <button type="submit">{editMode ? "Save" : "Create"}</button>
          {editMode && (
            <button
              type="button"
              onClick={handleDelete}
              style={{ marginLeft: 8, background: "crimson", color: "#fff" }}
            >
              Delete
            </button>
          )}
    </div>
    {message && <p style={{ color: "crimson" }}>{message}</p>}
  </form>
</div>
  );
}