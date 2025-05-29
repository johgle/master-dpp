# Digital Product Passport Prototype

A functional proof-of-concept implementation of a Digital Product Passport (DPP) system developed as part of a Master’s thesis at the Norwegian University of Science and Technology (NTNU), June 2025. The prototype implements a modular architecture combining CAD data, a custom-built DPP ontology, and a web-based interface to support circular economy objectives such as product traceability and lifecycle transparency.

## Overview

The DPP prototype includes:
- **CAD Software Integration** using Onshape and OnPy for automatic extraction and generation of product data.
- **Semantic Knowledge Base** with OWL/RDF storage via Apache Jena Fuseki.
- **DPP Agent** as backend to handle data transformation and API logic.
- **Web Portal** for CRUD (Create, Read, Update, Delete) operations on Digital Product Passports.
- **QR Code Integration** for accessing individual passports via physical data carrier.

## Technologies Used

- **Python 3.12** – Backend scripting & agent logic
- **Django 5.1** – Web framework for backend and web interface
- **Onshape** – CAD software
- **OnPy** – Python API for Onshape CAD integration ([OnPy GitHub]((https://github.com/kyle-tennison/onpy)))
- **Apache Jena Fuseki** – Semantic database
- **RDF / OWL** – Ontology and data modeling
- **HTML + Tailwind CSS** – Frontend templates and styling
- **qrcode** (Python lib) – QR code generation
- **JSON** – Data storage for generated chair metadata
- **Selenium** – End-to-end and performance testing
- **pytest** – Automated testing framework
- **psutil** – RAM and resource usage tracking

## Features

- Automatic generation of Digital Product Passports with data from CAD models
- SPARQL-powered semantic queries on structured product data
- CRUD (Create, Read, Update, Delete) operations on DPPs via a web interface
- QR code generation and access to DPP data
- End-to-end and performance testing for CRUD operations

## Installation


## Credits
This prototype is part of:
Master’s Thesis, NTNU, June 2025. By Johanne Glende, Digital Product Passport as Enabler for Circular Economy − Design, Implementation and Evaluation of a DPP System Architecture.
Supervisor: Andrei Lobov, NTNU.
