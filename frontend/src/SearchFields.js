import {useState} from 'react'
import { createResultsTable } from './utils'
import {apiEndpoint} from './custom-exports'

const searchItems = {
    customers: [
      { name: 'first_name', label: 'First Name' },
      { name: 'last_name', label: 'Last Name' },
      { name: 'business', label: 'Business' },
      { name: 'email', label: 'Email' },
      { name: 'phone', label: 'Phone' },
      { name: 'address_line_1', label: 'Address Line 1' },
      { name: 'address_line_2', label: 'Address Line 2' },
      { name: 'city', label: 'City' },
      { name: 'state_territory', label: 'State/Territory' },
      { name: 'zip_code', label: 'Zip Code' },
      { name: 'country', label: 'Country' },
      { name: 'referred_by', label: 'Referred By' },
      { name: 'tax_rate', label: 'Tax Rate' },
      { name: 'is_sms', label: 'Is SMS' },
      { name: 'is_billing_emails', label: 'Is Billing Emails' },
      { name: 'is_marketing_emails', label: 'Is Marketing Emails' },
      { name: 'is_report_emails', label: 'Is Report Emails' },
      { name: 'is_portal_user', label: 'Is Portal User' },
      { name: 'additional_notification_email', label: 'Additional Notification Email' },
      { name: 'invoice_cc_email', label: 'Invoice CC Email' },
    ],
    stores: [
      { name: 'address_line_1', label: 'Address Line 1' },
      { name: 'city', label: 'City' },
      { name: 'zip_code', label: 'Zip Code' },
      { name: 'phone', label: 'Phone' },
    ],
    items: [
      { name: 'item_display_name', label: 'Item Display Name' },
      { name: 'item_make', label: 'Item Make' },
      { name: 'item_model', label: 'Item Model' },
      { name: 'item_description', label: 'Item Description' },
      { name: 'operating_system', label: 'Operating System' },
      { name: 'website', label: 'Website' },
      { name: 'custom_fields', label: 'Custom Fields' },
    ],
    assets: [
      { name: 'asset_name', label: 'Asset Name' },
      { name: 'asset_serial', label: 'Asset Serial' },
      { name: 'asset_password', label: 'Asset Password' },
      { name: 'warranty_expiration', label: 'Warranty Expiration' },
      { name: 'date_of_manufacture', label: 'Date of Manufacture' },
      { name: 'notes', label: 'Notes' },
    ],
    stock: [
      { name: 'barcode', label: 'Barcode' },
      { name: 'net_paid', label: 'Net Paid' },
      { name: 'tax_paid', label: 'Tax Paid' },
      { name: 'net_sale_price', label: 'Net Sale Price' },
      { name: 'tax_charged', label: 'Tax Charged' },
      { name: 'item', label: 'Item' },
    ],
    employees: [
      { name: 'first_name', label: 'First Name' },
      { name: 'last_name', label: 'Last Name' },
      { name: 'email', label: 'Email' },
      { name: 'store', label: 'Store' },
    ],
    tickets: [
      { name: 'customer_id', label: 'Customer ID' },
      { name: 'ticket_title', label: 'Ticket Title' },
      { name: 'ticket_priority_level', label: 'Ticket Priority Level' },
      { name: 'ticket_description', label: 'Ticket Description' },
      { name: 'creation_date', label: 'Creation Date' },
      { name: 'due_date', label: 'Due Date' },
      { name: 'tech', label: 'Tech' },
      { name: 'net_price', label: 'Net Price' },
      { name: 'gross_price', label: 'Gross Price' },
    ],
    invoices: [
      { name: 'invoice_status', label: 'Invoice Status' },
      { name: 'date_created', label: 'Date Created' },
      { name: 'is_taxable', label: 'Is Taxable' },
      { name: 'date_paid', label: 'Date Paid' },
      { name: 'tech_notes', label: 'Tech Notes' },
      { name: 'ticket', label: 'Ticket' },
      { name: 'payment_method', label: 'Payment Method' },
      { name: 'purchase_order_number', label: 'Purchase Order Number' },
    ]
  };

  const SearchFields = ({ assetType }) => {
    const searchFields = searchItems[assetType];
    const [searchResults, setSearchResults] = useState([]);
    const [searchParams, setSearchParams] = useState({});
  
    if (!searchFields) {
      return null;
    }
  
    const handleInputChange = (event) => {
      const { name, value } = event.target;
      setSearchParams((prevParams) => ({
        ...prevParams,
        [name]: value,
      }));
    };
  
    const handleSubmit = (event) => {
      event.preventDefault();
  
      const API_URL = `${apiEndpoint}/${assetType}`;
  
      fetch(API_URL, {
        method: 'POST',
        body: JSON.stringify(searchParams),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then((data) => {
          setSearchResults(data);
        })
        .catch((error) => {
          console.error(error);
          setSearchResults([]);
        });
    };
  
    const searchFieldsHTML = searchFields.map((item) => (
      <div className="form-group" key={item.name}>
        <label htmlFor={item.name}>{item.label}:</label>
        <input
          type="text"
          id={item.name}
          name={item.name}
          value={searchParams[item.name] || ''}
          onChange={handleInputChange}
        />
      </div>
    ));
  
    const resultsTable = createResultsTable(searchResults); // Use the createResultsTable function
  
    return (
        <div className="search-fields-container">
          <form className="search-form" onSubmit={handleSubmit}>
            {searchFieldsHTML}
            <button type="submit">Search</button>
          </form>
          <div className="results-container">
            <div className="results">{resultsTable}</div>
          </div>
        </div>
      );
    }
  export default SearchFields;