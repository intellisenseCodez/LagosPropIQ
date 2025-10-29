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

## 📊 Summary of Scraped Data Variables

Each intern is expected to extract the following **core variables** from their assigned web sources. These fields ensure consistency and compatibility across all collected datasets.

| Variable Name | Description |
|----------------|--------------|
| **property_title** | The headline or main title of the listing. |
| **listing_type** | Type of listing: `Rent` or `Sale`. |
| **property_type** | Category of property (House, Flat, Duplex, Land, etc.). |
| **price (₦)** | Total listing price in Naira. |
| **price_per_sqm (derived)** | Computed metric = `price / size_sqm`. |
| **size_sqm** | Property size in square meters. |
| **bedrooms** | Number of bedrooms (if applicable). |
| **bathrooms** | Number of bathrooms (if applicable). |
| **furnishing_status** | Furnished, Semi-Furnished, or Unfurnished. |
| **location** | Area name, LGA, and (if possible) GPS coordinates. |
| **agent_name** | Name of the agent responsible for the listing. |
| **agent_company** | Name of the agent’s agency or firm. |
| **contact** | Contact phone or email of the agent. |
| **listing_date** | Original date the property was posted. |
| **last_updated** | Most recent date the listing was updated. |
| **image_links** | URLs of property photos (if available). |
| **property_description** | Text description of the property features. |
| **listing_url** | The direct URL link to the property page. |

## 🪪 License

This project is for educational and internal research purposes only.
Ensure all data collected respects each website’s robots.txt policy and terms of service.


## 📍Project Maintainer:
- **Lead**: Oyekanmi Lekan
- **Email**: [oyekanmilekan@gmail.com](oyekanmilekan@gmail.com)
- **GitHub**: [github.com/intellisenseCodez](https://github.com/intellisenseCodez/)
