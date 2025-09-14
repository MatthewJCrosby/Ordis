import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

export default function Login() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const { setUser } = useAuth();

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setMessage('');
    try {
      const response = await fetch('http://localhost:5000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
        credentials: 'include', 
      });
      const data = await response.json();
      if (response.ok) {
        setUser(data)
        setMessage('Login successful!');
        localStorage.setItem('user', JSON.stringify({ name: data.name, email: data.email }));
        setForm({ email: '', password: '' });
        navigate('/');
      } else {
        setMessage(data.error || 'Login failed.');
      }
    } catch (err) {
      setMessage('Network error.');
    }
  }

  return (
    <div>
      <h2 style={{ textAlign: 'center' }}>Login</h2>
      <h3 className='h2-register'>Dont have an account? <Link to="/register">Register</Link></h3>
      <form className="register-form" onSubmit={handleSubmit}>
        <div className="register-form-row">
          <label htmlFor="email">Email:</label>
          <input id="email" name="email" type="email" value={form.email} onChange={handleChange} required />
        </div>
        <div className="register-form-row">
          <label htmlFor="password">Password:</label>
          <input id="password" name="password" type="password" value={form.password} onChange={handleChange} required />
        </div>
        <button type="submit">Login</button>
      </form>
      {message && <p style={{ textAlign: 'center', color: 'crimson' }}>{message}</p>}
    </div>
  );
}