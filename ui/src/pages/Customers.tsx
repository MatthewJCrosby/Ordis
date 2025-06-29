import { useEffect, useState } from "react";

export default function Customers() {
  const [customers, setCustomers] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/customers")
      .then((res) => res.json())
      .then((data) => setCustomers(data));
  }, []);

  return (
    <div>
      <h1>Customer List</h1>
      <ul>
        {customers.map((c: any) => (
          <li key={c.id}>{c.first_name} {c.last_name} - {c.email}</li>
        ))}
      </ul>
    </div>
  );
}
