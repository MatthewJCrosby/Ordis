import React from 'react';
import { Link } from 'react-router-dom';
import ordisLogo from './assets/OrdisLogo.png';
import { useAuth } from './AuthContext'; 

function Header() {
  const { user } = useAuth();

  return (
    <header style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '1rem', background: '#222', color: '#fff' }}>
      <img src={ordisLogo} className="logo" alt="Ordis logo" style={{ height: '2.5em' }} />
      <nav>
        {user ? (
          <>
            <Link to="/me" style={{ color: '#fff', marginRight: '1rem', textDecoration: 'underline' }}>My Account</Link>
            <Link to="/logout" style={{ color: '#fff', textDecoration: 'underline' }}>Logout</Link>
          </>
        ) : (
          <Link to="/login" style={{ color: '#fff', textDecoration: 'underline' }}>Login</Link>
        )}
      </nav>
    </header>
  );
}

export default Header;