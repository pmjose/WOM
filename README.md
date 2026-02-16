# Snowflake Intelligence Demo – WOM Chile (Mobile + Fiber Telecom)

This repo configures a Snowflake Intelligence demo themed for **WOM Chile**, using synthetic structured data plus reports in `unstructured_docs` to ground answers in mobile operations, fiber internet, subscriber growth, 5G rollout, and customer service.

## About WOM Chile (real-world facts)
- **Chile's second-largest mobile operator**
- **#1 in Telecommunications** - Total Brands Chile 2025
- Lowered the price per gigabyte by **95%** in Chile
- **5G network** available in major cities
- **Fiber optic national network** with 7,000+ km
- Company: **WOM SpA** (RUT: 78.921.690-8)

### Product Lines
**Planes Moviles (Postpago):**
- 100GB - $9,990/mes
- 200GB - $11,990/mes  
- 300GB - $13,990/mes
- 400GB - $15,990/mes (promo $8,990 x 6 meses)

**Planes Multilinea:**
- 2x 400GB - $6,990 c/u por mes
- 3x 400GB - $6,990 c/u por mes

**Prepago - Plan Zero:**
- eSIM 100GB - $9,990 renovable cada 30 dias

**Internet Fibra Hogar:**
- 400 Mbps - $19,990/mes
- 600 Mbps - $21,990/mes (promo $13,990)
- 800 Mbps - $24,990/mes (promo $15,990)

**TV Online:**
- Zapping - 130+ canales HD

**Equipment:** Smartphones (Samsung, Xiaomi, iPhone), Tablets, Smart Watch, Accesorios

**Services:** 5G, VoLTE, VoWiFi, Roaming WhatsApp libre en 100+ paises

### Contact
- **Movil**: 103 | WhatsApp: 935 223 070
- **Fibra**: 600 600 1106 | WhatsApp: 937 400 691
- Website: [wom.cl](https://wom.cl/)

## What's included
- **SQL setup script**: `sql_scripts/01_demo_setup.sql` builds `WOM_AI_DEMO` and loads sample data + documents into stages.
- **Structured sample data** (`demo_data/`): synthetic fact/dim tables to model revenue, subscriber metrics, service performance, campaigns, and workforce. Segments reflect WOM's business (Movil, Hogar, Empresas).
- **Unstructured reports** (`unstructured_docs/`): narrative files used by Cortex Search. Notable references:
  - Finance: Financial reports, revenue mix, subscriber growth, ARPU analysis.
  - Strategy: Board presentations, market position, competitive analysis.
  - Network: Mobile coverage, 5G rollout, fiber expansion plans.
  - Demo: Demo scripts for CEO, CFO, CMO personas.

## Quick start
1. Open `sql_scripts/01_demo_setup.sql` in a Snowflake worksheet (use `ACCOUNTADMIN` to create integrations, then the `WOM_Demo` role created by the script).
2. Run the script end-to-end to create the database, schema, stage, load CSVs, and register Cortex Search services and the `WOM_Executive_Agent`.
3. Verify objects:
   - `SHOW TABLES IN WOM_AI_DEMO.WOM_SCHEMA;`
   - `SHOW SEMANTIC VIEWS;`
   - `SHOW CORTEX SEARCH SERVICES;`

## Suggested prompts (Telecom context)
- **Subscriber metrics**: "What is our total mobile subscriber count by region and plan type?"
- **Revenue & ARPU**: "Show monthly recurring revenue (MRR) and ARPU trends by segment."
- **Product performance**: "Which mobile plans (100GB to 400GB) have the highest adoption?"
- **Churn analysis**: "What is our churn rate by plan type and region?"
- **5G rollout**: "What is the status of our 5G network deployment?"
- **Marketing ROI**: "Which marketing campaigns generated the most portabilities?"
- **Competitive position**: "How do we compare to Claro and Entel in market share?"

## Personas
- **CEO**: Strategy, subscriber growth, market share, competitive position, 5G strategy.
- **CFO**: Revenue, ARPU, churn, MRR/ARR, cost per acquisition, portability economics.
- **COO/CTO**: Network coverage, 5G deployment, fiber expansion, uptime SLAs, capacity planning.
- **CMO**: Campaign performance, lead generation, brand awareness, portability win rates.

## Notes
- Structured data is synthetic but aligned to telecom business metrics; unstructured reports supply realistic narrative context.
- Update or replace CSVs/documents as needed—`sql_scripts/01_demo_setup.sql` will stage whatever is present in `demo_data/` and `unstructured_docs/`.
- Guardrails in the agent are tuned to only answer questions about WOM's business (mobile plans, fiber internet, TV services, network coverage, customer service).
- Currency is **Chilean Pesos (CLP)** throughout.
