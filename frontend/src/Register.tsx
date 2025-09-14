import React, { useState } from 'react';

export default function Register() {
  const [form, setForm] = useState({first_name: '', last_name: '', email: '', password: '' });
  const [message, setMessage] = useState('');
  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setMessage('');
    try {
      const response = await fetch('http://localhost:5000/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      if (response.ok) {
        setMessage('Registration successful!');
        setForm({ first_name: '', last_name: '', email: '', password: '' });
      } else {
        const data = await response.json();
        setMessage(data.error || 'Registration failed. A user with that email already exists.');
      }
    } catch (err) {
      setMessage('Network error.');
    }
  }

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', maxWidth: 300 }}>
        <label>
          First Name:
          <input name="first_name" value={form.first_name} onChange={handleChange} required />
        </label>
        <label>
          Last Name:
          <input name="last_name" value={form.last_name} onChange={handleChange} required />
        </label>
        <label>
          Email:
          <input name="email" value={form.email} onChange={handleChange} required />
        </label>
        <label>
          Password:
          <input name="password" type="password" value={form.password} onChange={handleChange} required />
        </label>
        <button type="submit" style={{ marginTop: 16 }}>Register</button>
      </form>
        {message && <p>{message}</p>}
    </div>
  );
}