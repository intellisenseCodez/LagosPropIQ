# 🏙️ LagosPropIQ

**LagosPropIQ** is a **data-driven real estate intelligence platform** designed to analyze, visualize, and understand property trends across Lagos, Nigeria.  
This repository powers the **data aggregation and analytics layer** of the project — collecting, cleaning, and organizing real estate data from multiple trusted online and government sources.

## 📘 Project Overview

The **LagosPropIQ** initiative is part of a larger **Real Estate Transaction Platform** project aimed at solving trust, transparency, and pricing inconsistencies in the Nigerian real estate market.

This phase focuses on **data acquisition and market intelligence**, forming the foundation for insights like:
- Average property price per square meter (₦/sqm)
- Rental yield and market trends
- Vacancy rates and “time-on-market” metrics
- Geographic segmentation (Island, Mainland, and Suburban zones)
- Price forecasting and housing deficit analysis

## 🎯 Objectives

- Aggregate property data from top real estate portals.
- Build structured datasets ready for analytics and modeling.
- Validate pricing trends using verified market reports and government statistics.
- Enable future development of predictive and geospatial insights.

---

## 🧱 Data Sources

Below are the primary data sources currently integrated or under consideration:

| Source | Type | Focus Area | Format | Notes |
|--------|------|-------------|---------|--------|
| [PropertyPro.ng](https://www.propertypro.ng) | Primary | Sale & rental listings | HTML | Excellent for structured scraping with consistent pagination. |
| [PrivateProperty.ng](https://www.privateproperty.ng) | Primary | Rentals & sales | HTML | Useful for comparing listings across multiple LGAs. |
| [NigeriaPropertyCentre.com](https://www.nigeriapropertycentre.com) | Primary | Detailed metadata (type, price, furnishing, etc.) | HTML | Best source for “time-on-market” KPIs. |
| [Property24.com.ng](https://www.property24.com.ng) | Primary | Market insights and listings | HTML | Includes analytical summaries. |
| [Jiji.ng - Real Estate](https://www.jiji.ng/real-estate) | Secondary | User-generated listings | HTML/JSON | Requires data cleaning (duplicates and noise). |
| [Lands.ng](https://www.lands.ng) | Secondary | Land sales and pricing | HTML | Great for tracking land value trends (Epe, Ibeju-Lekki). |
