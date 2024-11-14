import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header style={{display: 'flex', justifyContent: 'space-between', padding: '1rem', backgroundColor: '#eee'}}>
      <nav>
        <ul style={{ listStyleType: 'none', display: 'flex', gap: '1rem' }}>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/about">About</Link></li>
          <li><Link to="/contact">Contact</Link></li>
        </ul>
      </nav>
      <div>
        API URL: {process.env.REACT_APP_API_URL}
      </div>
    </header>
  );
};

export default Header;