import React from 'react';
import {Link} from 'react-router-dom';
function Sidebar() {
  return (
    <aside>
      <nav>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/customers">Customers</Link></li>
          <li><Link to="/users">Users</Link></li>
            <li><Link to="/register">Register</Link></li>
        </ul>
      </nav>
    </aside>
  );
}

export default Sidebar;