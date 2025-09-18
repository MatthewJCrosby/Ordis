import React, { useState } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import { Routes, Route } from 'react-router-dom';
import './App.css';
import Register from './Register';
import Login from './Login';
import Logout from './Logout';
import MyAccount from './pages/MyAccount';
import ProductCreate from './pages/Product/ProductCreate';
import ProductEdit from './pages/Product/ProductEdit';
// Temporary placeholder components
function Home() { return <h2>Home Page</h2>; }
function Customers() { return <h2>Customers Page</h2>; }
function Users() { return <h2>Users Page</h2>; }


function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="app-container">
      <Header />
      <div className="app-content">
        <Sidebar />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/customers" element={<Customers />} />
            <Route path="/users" element={<Users />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/logout" element={<Logout />} />
            <Route path="/me" element={<MyAccount />} />
            <Route path="/product/create" element={<ProductCreate />} />
            <Route path="/product/edit/:id" element={<ProductEdit />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default App;