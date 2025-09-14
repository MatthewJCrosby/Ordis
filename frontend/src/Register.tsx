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
      <h2 className='h2-register'>Register</h2>
      <form className="register-form" onSubmit={handleSubmit}>
    <div className="register-form-row">
        <label htmlFor="first_name">First Name:</label>
        <input id="first_name" name="first_name" value={form.first_name} onChange={handleChange} required />
    </div>
    <div className="register-form-row">
        <label htmlFor="last_name">Last Name:</label>
        <input id="last_name" name="last_name" value={form.last_name} onChange={handleChange} required />
    </div>
    <div className="register-form-row">
        <label htmlFor="email">Email:</label>
        <input id="email" name="email" value={form.email} onChange={handleChange} required />
    </div>
    <div className="register-form-row">
        <label htmlFor="password">Password:</label>
        <input id="password" name="password" type="password" value={form.password} onChange={handleChange} required />
    </div>
    <button type="submit" style={{ marginTop: 16 }}>Register</button>
    </form>
        {message && <p style={{ textAlign: 'center', color: 'crimson' }}>{message}</p>}
    </div>
  );
}