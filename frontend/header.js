import React, { useMemo } from 'react';
import { Link } from 'react-router-dom';

const headerStyle = {
  display: 'flex', 
  justifyContent: 'space-between', 
  padding: '1rem',
  backgroundColor: '#eee'
};

const listStyle = {
  listStyleType: 'none', 
  display: 'flex', 
  gap: '1rem'
};

const useNavigationLinks = () => {
  return useMemo(() => [
    { path: "/", text: "Home" },
    { path: "/about", text: "About" },
    { path: "/contact", text: "Contact" },
  ], []);
};

const Header = () => {
  const navLinks = useNavigationLinks();

  return (
    <header style={headerStyle}>
      <nav>
        <ul style={listStyle}>
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