# STEP 0
# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

# View database tables
pd.read_sql("""SELECT * FROM sqlite_master""", conn)


# STEP 1
# Employees working in the Boston office
df_boston = pd.read_sql("""
    SELECT
        e.firstName,
        e.lastName,
        e.jobTitle
    FROM employees e
    JOIN offices o
        ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
""", conn)


# STEP 2
# Offices with zero employees
df_zero_emp = pd.read_sql("""
    SELECT
        o.officeCode,
        o.city,
        o.state
    FROM offices o
    LEFT JOIN employees e
        ON o.officeCode = e.officeCode
    GROUP BY
        o.officeCode,
        o.city,
        o.state
    HAVING COUNT(e.employeeNumber) = 0
""", conn)


# STEP 3
# All employees with their office city and state
df_employee = pd.read_sql("""
    SELECT
        e.firstName,
        e.lastName,
        o.city,
        o.state
    FROM employees e
    LEFT JOIN offices o
        ON e.officeCode = o.officeCode
    ORDER BY
        e.firstName,
        e.lastName
""", conn)


# STEP 4
# Customers who have not placed an order
df_contacts = pd.read_sql("""
    SELECT
        c.contactFirstName,
        c.contactLastName,
        c.phone,
        c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o
        ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY
        c.contactLastName
""", conn)


# STEP 5
# Customer payment details
df_payment = pd.read_sql("""
    SELECT
        c.contactFirstName,
        c.contactLastName,
        p.amount,
        p.paymentDate
    FROM customers c
    JOIN payments p
        ON c.customerNumber = p.customerNumber
    ORDER BY
        CAST(p.amount AS REAL) DESC
""", conn)


# STEP 6
# Employees whose customers have an average credit limit over 90,000
df_credit = pd.read_sql("""
    SELECT
        e.employeeNumber,
        e.firstName,
        e.lastName,
        COUNT(c.customerNumber) AS numCustomers
    FROM employees e
    JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY
        e.employeeNumber,
        e.firstName,
        e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY
        numCustomers DESC
""", conn)


# STEP 7
# Products with number of orders and total units sold
df_product_sold = pd.read_sql("""
    SELECT
        p.productName,
        COUNT(od.orderNumber) AS numorders,
        SUM(od.quantityOrdered) AS totalunits
    FROM products p
    JOIN orderdetails od
        ON p.productCode = od.productCode
    GROUP BY
        p.productCode,
        p.productName
    ORDER BY
        totalunits DESC
""", conn)


# STEP 8
# Number of different customers who purchased each product
df_total_customers = pd.read_sql("""
    SELECT
        p.productName,
        p.productCode,
        COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    JOIN orderdetails od
        ON p.productCode = od.productCode
    JOIN orders o
        ON od.orderNumber = o.orderNumber
    GROUP BY
        p.productCode,
        p.productName
    ORDER BY
        numpurchasers DESC
""", conn)


# STEP 9
# Number of customers per office
df_customers = pd.read_sql("""
    SELECT
        COUNT(c.customerNumber) AS n_customers,
        o.officeCode,
        o.city
    FROM offices o
    LEFT JOIN employees e
        ON o.officeCode = e.officeCode
    LEFT JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY
        o.officeCode,
        o.city
    ORDER BY
        o.city
""", conn)


# STEP 10
# Employees who sold products ordered by fewer than 20 customers
df_under_20 = pd.read_sql("""
    SELECT DISTINCT
        e.employeeNumber,
        e.firstName,
        e.lastName,
        o.city,
        o.officeCode
    FROM employees e
    JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders ord
        ON c.customerNumber = ord.customerNumber
    JOIN orderdetails od
        ON ord.orderNumber = od.orderNumber
    JOIN offices o
        ON e.officeCode = o.officeCode
    WHERE od.productCode IN (
        SELECT
            od2.productCode
        FROM orderdetails od2
        JOIN orders ord2
            ON od2.orderNumber = ord2.orderNumber
        GROUP BY
            od2.productCode
        HAVING COUNT(DISTINCT ord2.customerNumber) < 20
    )
    ORDER BY
        e.lastName
""", conn)


# Close the database connection
conn.close()