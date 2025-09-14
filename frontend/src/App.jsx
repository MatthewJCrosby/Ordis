import React, { useState } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import { Routes, Route } from 'react-router-dom';
import './App.css';
import Register from './Register';

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
          </Routes>
          <div className="card">
            <button onClick={() => setCount((count) => count + 1)}>
              count is {count}
            </button>
            <h1>Welcome to Oridis!</h1>
            <p>The Order Information System</p>
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;