import React, {useState, useEffect} from "react";

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
      ? `
        mutation {
          updateProduct(id: ${form.id}, input: {
            name: "${form.name}",
            description: "${form.description}",
            price: ${parseFloat(form.price)}
          }) {
            id
            name
            description
            price
          }
        }
      `
      : `
        mutation {
          createProduct(input: {
            name: "${form.name}",
            description: "${form.description}",
            price: ${parseFloat(form.price)}
          }) {
            id
            name
            description
            price
          }
        }
      `;

    const response = await fetch('http://localhost:5000/graphql', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: mutation }),
      credentials: "include",
    });

    const result = await response.json();
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
  return (
    <div>
      <h2>{editMode ? "Edit Product" : "Create Product"}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input name="name" value={form.name} onChange={handleChange} required />
        </div>
        <div>
          <label>Description:</label>
          <textarea name="description" value={form.description} onChange={handleChange} />
        </div>
        <div>
          <label>Price:</label>
          <input name="price" type="number" step="0.01" value={form.price} onChange={handleChange} required />
        </div>
        {onCancel && (
          <button type="button" onClick={onCancel} style={{ marginRight: 8 }}>
            Cancel
          </button>
        )}
        <button type="submit">{editMode ? "Save" : "Create"}</button>
      </form>
      {message && <p style={{ color: "crimson" }}>{message}</p>}
    </div>
  );
}