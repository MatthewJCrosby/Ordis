import { useEffect, useState } from "react";

type User = {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  created_on: string;
  last_login: string | null;
  is_active: boolean;
  is_admin: boolean;
  user_type: string;
};

export default function Me() {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState("");
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState<User | null>(null)

    useEffect(() => {
    fetch("http://localhost:5000/auth/me", { credentials: "include" })
      .then(res => res.ok ? res.json() : Promise.reject("Not authenticated"))
      .then(data => { setUser(data); setForm(data); })
      .catch(setError);
  }, []);

  if (error) return <p>{error}</p>;
  if (!user) return <p>Loading...</p>;

  return (
    <div>
      <h2>My Account</h2>
        <p><strong>User Type:</strong> {user.user_type}</p>
        <p><strong>Status:</strong> {user.is_active ? 'Active' : 'Inactive'}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>First Name:</strong> {user.first_name}</p>
        <p><strong>Last Name:</strong> {user.last_name}</p>
        <p><strong>Account Created:</strong> {new Date(user.created_on).toLocaleString()}</p>
        <p><strong>Last Login:</strong> {user.last_login ? new Date(user.last_login).toLocaleString() : 'Never'}</p>
        <p><strong>Is Admin:</strong> {user.is_admin ? 'Yes' : 'No'}</p>
        
        

        </div>
    );
}