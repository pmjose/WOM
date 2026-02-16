-- ========================================================================
-- WOM Demo Validation Script
-- Validates all tables created, data loaded, and unstructured docs parsed
-- ========================================================================

USE ROLE WOM_Demo;
USE DATABASE WOM_AI_DEMO;
USE SCHEMA WOM_SCHEMA;
USE WAREHOUSE WOM_DEMO_WH;

-- ========================================================================
-- SECTION 1: INFRASTRUCTURE VALIDATION
-- ========================================================================

SELECT '=== INFRASTRUCTURE VALIDATION ===' AS section;

-- Check database exists
SELECT 'Database' AS object_type, 
       DATABASE_NAME AS object_name,
       CASE WHEN DATABASE_NAME IS NOT NULL THEN '✓ EXISTS' ELSE '✗ MISSING' END AS status
FROM INFORMATION_SCHEMA.DATABASES 
WHERE DATABASE_NAME = 'WOM_AI_DEMO';

-- Check schema exists
SELECT 'Schema' AS object_type,
       SCHEMA_NAME AS object_name,
       CASE WHEN SCHEMA_NAME IS NOT NULL THEN '✓ EXISTS' ELSE '✗ MISSING' END AS status
FROM INFORMATION_SCHEMA.SCHEMATA 
WHERE SCHEMA_NAME = 'WOM_SCHEMA';

-- Check warehouse exists
SHOW WAREHOUSES LIKE 'WOM_DEMO_WH';

-- Check Git repository
SHOW GIT REPOSITORIES LIKE 'WOM_AI_DEMO_REPO';

-- Check internal stage
SHOW STAGES LIKE 'WOM_INTERNAL_STAGE';

-- ========================================================================
-- SECTION 2: DIMENSION TABLES VALIDATION
-- ========================================================================

SELECT '=== DIMENSION TABLES VALIDATION ===' AS section;

SELECT 'WOM_PRODUCT_CATEGORY_DIM' AS table_name, COUNT(*) AS row_count, 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END AS status 
FROM WOM_PRODUCT_CATEGORY_DIM
UNION ALL
SELECT 'WOM_PRODUCT_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_PRODUCT_DIM
UNION ALL
SELECT 'WOM_VENDOR_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_VENDOR_DIM
UNION ALL
SELECT 'WOM_CUSTOMER_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_CUSTOMER_DIM
UNION ALL
SELECT 'WOM_ACCOUNT_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_ACCOUNT_DIM
UNION ALL
SELECT 'WOM_DEPARTMENT_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_DEPARTMENT_DIM
UNION ALL
SELECT 'WOM_REGION_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_REGION_DIM
UNION ALL
SELECT 'WOM_SALES_REP_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_SALES_REP_DIM
UNION ALL
SELECT 'WOM_CAMPAIGN_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_CAMPAIGN_DIM
UNION ALL
SELECT 'WOM_CHANNEL_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_CHANNEL_DIM
UNION ALL
SELECT 'WOM_EMPLOYEE_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_EMPLOYEE_DIM
UNION ALL
SELECT 'WOM_JOB_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_JOB_DIM
UNION ALL
SELECT 'WOM_LOCATION_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_LOCATION_DIM
UNION ALL
SELECT 'WOM_NETWORK_STATUS_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_NETWORK_STATUS_DIM
ORDER BY table_name;

-- ========================================================================
-- SECTION 3: FACT TABLES VALIDATION
-- ========================================================================

SELECT '=== FACT TABLES VALIDATION ===' AS section;

SELECT 'WOM_SALES_FACT' AS table_name, COUNT(*) AS row_count, 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END AS status 
FROM WOM_SALES_FACT
UNION ALL
SELECT 'WOM_FINANCE_TRANSACTIONS', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_FINANCE_TRANSACTIONS
UNION ALL
SELECT 'WOM_MARKETING_CAMPAIGN_FACT', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_MARKETING_CAMPAIGN_FACT
UNION ALL
SELECT 'WOM_HR_EMPLOYEE_FACT', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_HR_EMPLOYEE_FACT
UNION ALL
SELECT 'WOM_NETWORK_INCIDENTS_FACT', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_NETWORK_INCIDENTS_FACT
UNION ALL
SELECT 'WOM_NETWORK_MAINTENANCE_SCHEDULE', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_NETWORK_MAINTENANCE_SCHEDULE
ORDER BY table_name;

-- ========================================================================
-- SECTION 4: SALESFORCE TABLES VALIDATION
-- ========================================================================

SELECT '=== SALESFORCE TABLES VALIDATION ===' AS section;

SELECT 'WOM_SF_ACCOUNTS' AS table_name, COUNT(*) AS row_count, 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END AS status 
FROM WOM_SF_ACCOUNTS
UNION ALL
SELECT 'WOM_SF_OPPORTUNITIES', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_SF_OPPORTUNITIES
UNION ALL
SELECT 'WOM_SF_CONTACTS', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM WOM_SF_CONTACTS
ORDER BY table_name;

-- ========================================================================
-- SECTION 5: UNSTRUCTURED DATA VALIDATION
-- ========================================================================

SELECT '=== UNSTRUCTURED DATA VALIDATION ===' AS section;

-- Check files in internal stage
SELECT 'Files in WOM_INTERNAL_STAGE' AS check_type;
SELECT COUNT(*) AS file_count, 
       CASE WHEN COUNT(*) > 0 THEN '✓ FILES PRESENT' ELSE '✗ NO FILES' END AS status
FROM DIRECTORY(@WOM_INTERNAL_STAGE);

-- List unstructured doc files
SELECT 'Unstructured Documents' AS check_type;
SELECT relative_path, size, last_modified
FROM DIRECTORY(@WOM_INTERNAL_STAGE)
WHERE relative_path ILIKE 'unstructured_docs/%'
ORDER BY relative_path;

-- Check parsed content tables
SELECT 'WOM_PARSED_CONTENT_DOCS' AS table_name, COUNT(*) AS row_count, 
       CASE WHEN COUNT(*) > 0 THEN '✓ PARSED' ELSE '✗ EMPTY' END AS status 
FROM WOM_PARSED_CONTENT_DOCS
UNION ALL
SELECT 'WOM_PARSED_CONTENT_MD', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ PARSED' ELSE '✗ EMPTY' END 
FROM WOM_PARSED_CONTENT_MD
UNION ALL
SELECT 'WOM_PARSED_CONTENT', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ PARSED' ELSE '✗ EMPTY' END 
FROM WOM_PARSED_CONTENT
ORDER BY table_name;

-- Show parsed document details
SELECT 'Parsed Documents Detail' AS check_type;
SELECT relative_path, LENGTH(content) AS content_length
FROM WOM_PARSED_CONTENT
ORDER BY relative_path;

-- ========================================================================
-- SECTION 6: SEMANTIC VIEWS VALIDATION
-- ========================================================================

SELECT '=== SEMANTIC VIEWS VALIDATION ===' AS section;

SHOW SEMANTIC VIEWS IN SCHEMA WOM_AI_DEMO.WOM_SCHEMA;

-- Validate each semantic view exists
SELECT 'Semantic View Check' AS check_type;
SELECT 'WOM_FINANCE_SEMANTIC_VIEW' AS view_name, 
       CASE WHEN COUNT(*) > 0 THEN '✓ EXISTS' ELSE '✗ MISSING' END AS status
FROM INFORMATION_SCHEMA.VIEWS 
WHERE TABLE_SCHEMA = 'WOM_SCHEMA' AND TABLE_NAME = 'WOM_FINANCE_SEMANTIC_VIEW'
UNION ALL
SELECT 'WOM_SALES_SEMANTIC_VIEW', 
       CASE WHEN COUNT(*) > 0 THEN '✓ EXISTS' ELSE '✗ MISSING' END
FROM INFORMATION_SCHEMA.VIEWS 
WHERE TABLE_SCHEMA = 'WOM_SCHEMA' AND TABLE_NAME = 'WOM_SALES_SEMANTIC_VIEW'
UNION ALL
SELECT 'WOM_MARKETING_SEMANTIC_VIEW', 
       CASE WHEN COUNT(*) > 0 THEN '✓ EXISTS' ELSE '✗ MISSING' END
FROM INFORMATION_SCHEMA.VIEWS 
WHERE TABLE_SCHEMA = 'WOM_SCHEMA' AND TABLE_NAME = 'WOM_MARKETING_SEMANTIC_VIEW'
UNION ALL
SELECT 'WOM_HR_SEMANTIC_VIEW', 
       CASE WHEN COUNT(*) > 0 THEN '✓ EXISTS' ELSE '✗ MISSING' END
FROM INFORMATION_SCHEMA.VIEWS 
WHERE TABLE_SCHEMA = 'WOM_SCHEMA' AND TABLE_NAME = 'WOM_HR_SEMANTIC_VIEW'
UNION ALL
SELECT 'WOM_INFRASTRUCTURE_SEMANTIC_VIEW', 
       CASE WHEN COUNT(*) > 0 THEN '✓ EXISTS' ELSE '✗ MISSING' END
FROM INFORMATION_SCHEMA.VIEWS 
WHERE TABLE_SCHEMA = 'WOM_SCHEMA' AND TABLE_NAME = 'WOM_INFRASTRUCTURE_SEMANTIC_VIEW';

-- ========================================================================
-- SECTION 7: CORTEX SEARCH SERVICES VALIDATION
-- ========================================================================

SELECT '=== CORTEX SEARCH SERVICES VALIDATION ===' AS section;

SHOW CORTEX SEARCH SERVICES IN SCHEMA WOM_AI_DEMO.WOM_SCHEMA;

-- ========================================================================
-- SECTION 8: GEOSPATIAL DATA VALIDATION
-- ========================================================================

SELECT '=== GEOSPATIAL DATA VALIDATION ===' AS section;

-- Check customers have lat/long
SELECT 'Customers with Geospatial' AS check_type,
       COUNT(*) AS total_customers,
       SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) AS with_coordinates,
       ROUND(100.0 * SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_complete
FROM WOM_CUSTOMER_DIM;

-- Check regions have lat/long
SELECT 'Regions with Geospatial' AS check_type,
       COUNT(*) AS total_regions,
       SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) AS with_coordinates,
       ROUND(100.0 * SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_complete
FROM WOM_REGION_DIM;

-- Check locations have lat/long
SELECT 'Locations with Geospatial' AS check_type,
       COUNT(*) AS total_locations,
       SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) AS with_coordinates,
       ROUND(100.0 * SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_complete
FROM WOM_LOCATION_DIM;

-- Check network nodes have lat/long
SELECT 'Network Nodes with Geospatial' AS check_type,
       COUNT(*) AS total_nodes,
       SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) AS with_coordinates,
       ROUND(100.0 * SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_complete
FROM WOM_NETWORK_STATUS_DIM;

-- ========================================================================
-- SECTION 9: DATA QUALITY CHECKS
-- ========================================================================

SELECT '=== DATA QUALITY CHECKS ===' AS section;

-- Check for Chile-specific data
SELECT 'Chile Data Validation' AS check_type,
       'Customers in Chile regions' AS metric,
       COUNT(*) AS count
FROM WOM_CUSTOMER_DIM
WHERE city IN ('Santiago', 'Valparaiso', 'Concepcion', 'Temuco', 'Antofagasta', 'Rancagua', 'Puerto Montt', 'Talca', 'Iquique', 'La Serena');

-- Check SF Accounts are Chile-based
SELECT 'SF Accounts Chile Check' AS check_type,
       SUM(CASE WHEN billing_state IN ('Metropolitana', 'Valparaiso', 'Biobio', 'Araucania', 'Maule', 'OHiggins', 'Los Lagos', 'Antofagasta', 'Coquimbo', 'Los Rios', 'Tarapaca', 'Atacama') THEN 1 ELSE 0 END) AS chile_accounts,
       COUNT(*) AS total_accounts,
       ROUND(100.0 * SUM(CASE WHEN billing_state IN ('Metropolitana', 'Valparaiso', 'Biobio', 'Araucania', 'Maule', 'OHiggins', 'Los Lagos', 'Antofagasta', 'Coquimbo', 'Los Rios', 'Tarapaca', 'Atacama') THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_chile
FROM WOM_SF_ACCOUNTS;

-- Check SF Contacts have Chile phone numbers (+56)
SELECT 'SF Contacts Chile Phone Check' AS check_type,
       SUM(CASE WHEN phone LIKE '+56%' THEN 1 ELSE 0 END) AS chile_phones,
       COUNT(*) AS total_contacts,
       ROUND(100.0 * SUM(CASE WHEN phone LIKE '+56%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_chile
FROM WOM_SF_CONTACTS;

-- ========================================================================
-- SECTION 10: SUMMARY REPORT
-- ========================================================================

SELECT '=== VALIDATION SUMMARY ===' AS section;

WITH table_counts AS (
    SELECT 'Dimension Tables' AS category, 14 AS expected,
           (SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'WOM_SCHEMA' 
            AND TABLE_NAME LIKE 'WOM_%_DIM') AS actual
    UNION ALL
    SELECT 'Fact Tables', 4,
           (SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'WOM_SCHEMA' 
            AND TABLE_NAME LIKE 'WOM_%_FACT')
    UNION ALL
    SELECT 'Salesforce Tables', 3,
           (SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'WOM_SCHEMA' 
            AND TABLE_NAME LIKE 'WOM_SF_%')
    UNION ALL
    SELECT 'Parsed Content Tables', 3,
           (SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'WOM_SCHEMA' 
            AND TABLE_NAME LIKE 'WOM_PARSED_%')
    UNION ALL
    SELECT 'Semantic Views', 5,
           (SELECT COUNT(*) FROM INFORMATION_SCHEMA.VIEWS 
            WHERE TABLE_SCHEMA = 'WOM_SCHEMA' 
            AND TABLE_NAME LIKE 'WOM_%_SEMANTIC_VIEW')
)
SELECT category,
       expected,
       actual,
       CASE WHEN actual >= expected THEN '✓ PASS' ELSE '✗ FAIL' END AS status
FROM table_counts;

-- Total row counts
SELECT 'Total Data Rows' AS metric,
       (SELECT COUNT(*) FROM WOM_CUSTOMER_DIM) +
       (SELECT COUNT(*) FROM WOM_SALES_FACT) +
       (SELECT COUNT(*) FROM WOM_SF_ACCOUNTS) +
       (SELECT COUNT(*) FROM WOM_SF_OPPORTUNITIES) +
       (SELECT COUNT(*) FROM WOM_SF_CONTACTS) AS total_rows;

SELECT '=== VALIDATION COMPLETE ===' AS section;
