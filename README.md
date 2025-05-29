# Digital Product Passport Prototype

A proof-of-concept implementation of a Digital Product Passport (DPP) system developed as part of a Master’s thesis at the Norwegian University of Science and Technology (NTNU). The prototype implements a modular architecture combining CAD data, a custom-built DPP ontology, and a web-based interface to support circular economy objectives such as product traceability and lifecycle transparency.

## Overview

The DPP prototype includes:
- **CAD Integration** using Onshape and OnPy for automatic extraction and generation of product data.
- **Semantic Knowledge Base** with OWL/RDF storage via Apache Jena Fuseki.
- **DPP Agent** to handle data transformation and API logic.
- **Web Portal** for CRUD operations (Create, Read, Update, Delete) on Digital Product Passports.
- **QR Code Integration** for accessing individual passports via physical tags.

## Technologies Used

- **Python** – Backend scripting & agent logic
- **Django** – Web server & API endpoints
- **Onshape & OnPy** – CAD system & Python interface
- **Apache Jena Fuseki** – Semantic triple store (SPARQL endpoint)
- **RDF / OWL** – Ontology and data modeling
- **HTML + Tailwind** – Frontend web interface
- **qrcode** (Python lib) – QR code generation

## Features

- Automatic generation of Digital Product Passports from CAD models
- SPARQL-powered semantic queries over structured product data
- CRUD operations on DPPs via a web interface
- QR code access to DPP details for individual items

## Installation
