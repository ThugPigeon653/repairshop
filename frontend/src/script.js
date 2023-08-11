import { Amplify } from '../node_modules/aws-amplify';
import { awsExports } from './aws-exports';
import { Authenticator } from './@aws-amplify/ui-react';


Amplify.configure({
  Auth: {
    region:awsExports.REGION,
    userPoolId: awsExports.USER_POOL_ID,
    userPoolClientId: awsExports.USER_POOL_CLIENT_ID
  }
})



document.addEventListener('DOMContentLoaded', () => {
  // Load the Amazon Cognito Identity script dynamically
  const script = document.createElement('script');
  script.onload = () => {
    console.log("Vagina");
    initCognitoUserPool();

    const signUpForm = document.getElementById('sign-up-form');
    signUpForm.addEventListener('submit', handleSignUp);

    const verificationForm = document.getElementById('verification-form');
    verificationForm.addEventListener('submit', handleVerification);

    const searchButton = document.getElementById('search-button');
    searchButton.addEventListener('click', submitForm);
  };

  // Append the script to the document's head
  document.head.appendChild(script);
});

function submitForm(event) {
  console.log("submitForm called");
  event.preventDefault();

  const forms = document.querySelectorAll('.form-group');
  forms.forEach((form) => {
    const assetType = form.getAttribute('id').replace('search-form-', '');

    // Retrieve the form inputs dynamically
    const inputs = Array.from(form.getElementsByTagName('input'));
    const searchParams = {};

    inputs.forEach((input) => {
      if (input.value) {
        searchParams[input.name] = input.value;
      }
    });
    
    // Construct the API endpoint dynamically based on the asset type
    const API_URL = `https://uqjk9p8ob6.execute-api.ap-southeast-2.amazonaws.com/prod/dev/${assetType}`;

    // Send the payload to the API Gateway
    fetch(API_URL, {
      method: 'POST',
      body: JSON.stringify(searchParams)
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        // Handle the search results here
        const searchResults = document.getElementById('search-results');
        searchResults.innerHTML = createResultsTable(data);
      })
      .catch((error) => {
        // Handle fetch error here and display "No results found"
        console.error(error);
        const searchResults = document.getElementById('search-results');
        searchResults.innerHTML = '<p>No results found.</p>';
      });
  });
}

function createResultsTable(data) {
  // Create a table based on the search results data
  let tableHTML = '<table>';

  if (data.length === 0) {
    tableHTML += '<tr><td colspan="100%">No results found.</td></tr>';
  } else {
    // Add the table headers
    tableHTML += '<thead><tr>';
    for (const key in data[0]) {
      tableHTML += `<th>${key}</th>`;
    }
    tableHTML += '</tr></thead>';

    // Add the table rows
    tableHTML += '<tbody>';
    data.forEach((row) => {
      tableHTML += '<tr>';
      for (const key in row) {
        tableHTML += `<td>${row[key]}</td>`;
      }
      tableHTML += '</tr>';
    });
    tableHTML += '</tbody>';
  }

  tableHTML += '</table>';

  return tableHTML;
}

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
  ],
};

function generateSearchFields(assetType) {
  console.log(assetType)
  const searchFields = searchItems[assetType];
  const searchFieldsHTML = searchFields
    .map((item) => `<div class="form-group" id="search-form-${item.name}">
                      <label for="${item.name}">${item.label}:</label>
                      <input type="text" id="${item.name}" name="${item.name}" required>
                    </div>`)
    .join('');

  console.log(searchFieldsHTML)
  const searchFieldsContainer = document.getElementById('search-fields');
  searchFieldsContainer.innerHTML = searchFieldsHTML;

  const searchResults = document.getElementById('search-results');
  searchResults.innerHTML = '';

}



