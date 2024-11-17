import React, { useMemo } from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  const navLinks = useMemo(() => [
    { path: "/", text: "Home" },
    { path: "/about", text: "About" },
    { path: "/contact", text: "Contact" },
  ], []);

  return (
    <header style={{display: 'flex', justifyContent: 'space-between', padding: '1rem', backgroundColor: '#eee'}}>
      <nav>
        <ul style={{ listStyleType: 'none', display: 'flex', gap: '1rem' }}>
          {navLinks.map(link => (
            <li key={link.path}><Link to={link.path}>{link.text}</Link></li>
          ))}
        </ul>
      </nav>
      <div>
        API URL: {process.env.REACT_APP_API_URL}
      </div>
    </header>
  );
};

export default Header;