import './styles.css'


function NavBar({ generateSearchFields, toggleAuthForm }) {
  const handleClick = (e) => {
    e.preventDefault();
    toggleAuthForm();
  };

  return (
    <nav className="navbar">
      <ul>
        <li><a href="#" onClick={() => generateSearchFields('employees')}>Employees</a></li>
        <li><a href="#" onClick={() => generateSearchFields('customers')}>Customers</a></li>
        <li><a href="#" onClick={() => generateSearchFields('stores')}>Stores</a></li>
        <li><a href="#" onClick={() => generateSearchFields('items')}>Items</a></li>
        <li><a href="#" onClick={() => generateSearchFields('assets')}>Assets</a></li>
        <li><a href="#" onClick={() => generateSearchFields('stock')}>Stock</a></li>
        <li><a href="#" onClick={() => generateSearchFields('tickets')}>Tickets</a></li>
        <li><a href="#" onClick={() => generateSearchFields('invoices')}>Invoices</a></li>
        <li className="right-align">
          <a className="ml-auto" href="#" onClick={handleClick}>
            Sign Up / Sign In
          </a>
        </li>
      </ul>
    </nav>
  );
}

export default NavBar;