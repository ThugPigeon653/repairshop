-- REQUIRED JSON:
--  - list of OS
--  - ticket priority levels
--  - customisable technicians file for tickets
--  - custom fields in assets
-- CLOUDFORMAION MUST DO:
--  - create parameter store for db creds

CREATE TABLE public.customers (
    customer_id serial PRIMARY KEY,
    first_name text CHECK (first_name ~ '^[A-Za-z]{0,25}$') NOT NULL,
    last_name text CHECK (last_name ~ '^[A-Za-z]{0,25}$') NOT NULL,
    business text,
    email text CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    phone text CHECK (phone ~* '^(\+61|0)4\d{8}$|^\d{8}$') NOT NULL,
    address_line_1 text,
    address_line_2 text,
    city text,
    state_territory text,
    zip_code integer CHECK (zip_code ~ '^\d{4}$'),
    country text CHECK (country ~ '^[^0-9]*$'),
    referred_by integer REFERENCES customers (customer_id),
    tax_rate CHECK (tax_rate ~ '^\d{1,2}(\.\d+)?$'),
    is_sms boolean,
    is_billing_emails boolean,
    is_marketing_emails boolean,
    is_report_emails boolean,
    is_portal_user boolean,
    additional_notification_email text CHECK (additional_notification_email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    invoice_cc_email text CHECK (invoice_cc_email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE TABLE public.stores (
    store_id serial PRIMARY KEY,
    address_line_1 text,
    city text,
    zip_code integer CHECK (zip_code ~ '^\d{4}$'),
    phone text CHECK (phone ~* '^(\+61|0)4\d{8}$|^\d{8}$')
);

CREATE TABLE public.items (
    item_id serial PRIMARY KEY,
    item_display_name text,
    item_make text,
    item_model text,
    item_description text,
    operating_system text,
    website text CHECK (website ~ '^(https?|ftp)://[^\s/$.?#]+\.[^\s]*$'),
    custom_fields jsonb
);

CREATE TABLE public.assets (
    asset_id serial PRIMARY KEY,
    asset_name text NOT NULL,
    asset_serial text,
    asset_password text,
    warranty_expiration date,
    date_of_manufacture date,
    notes text
);

CREATE TABLE public.stock (
    barcode text CHECK (barcode ~ '^.{2,43}$'),
    net_paid decimal NOT NULL,
    tax_paid decimal NOT NULL,
    net_sale_price decimal NOT NULL,
    tax_charged decimal NOT NULL,
    item integer REFERENCES public.items (item_id)
);

CREATE TABLE public.employees (
    employee_id serial PRIMARY KEY,
    first_name text NOT NULL CHECK (first_name ~ '^[A-Za-z]{0,25}$'),
    last_name text NOT NULL CHECK (last_name ~ '^[A-Za-z]{0,25}$'),
    email text CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    store integer REFERENCES stores (store_id)
);

CREATE TABLE public.tickets (
    ticket_id serial PRIMARY KEY,
    customer_id integer REFERENCES customers (customer_id) NOT NULL,
    ticket_title text NOT NULL,
    ticket_priority_level integer NOT NULL,
    ticket_description text NOT NULL,
    creation_date date NOT NULL,
    due_date date NOT NULL,
    tech integer REFERENCES employees (employee_id),
    net_price decimal NOT NULL,
    gross_price decimal
);

CREATE TABLE public.invoices (
    invoice_id serial PRIMARY KEY,
    invoice_status boolean NOT NULL,
    date_created date NOT NULL,
    is_taxable boolean NOT NULL,
    date_paid date,
    tech_notes text,
    ticket integer REFERENCES tickets (ticket_id),
    payment_method text,
    purchase_order_number integer
);