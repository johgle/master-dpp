# Digital Product Passport Prototype

A functional proof-of-concept implementation of a Digital Product Passport (DPP) system developed as part of a Master’s thesis at the Norwegian University of Science and Technology (NTNU), June 2025. The prototype implements a modular architecture combining CAD data, a custom-built DPP ontology, a semantic knowledge base, and a web-based interface to support circular economy objectives such as product traceability and lifecycle transparency.

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
...

## Ontology Graph
The custom-built DPP ontology for the prototype.
![DPP_master_thesis_figures-DPP_ontology_full](https://github.com/user-attachments/assets/dc77bced-65a8-4352-9a76-f7666b5eae1f)

## Architecture
Architecture of the prototype system, with specific components and technologies.
![dpp_architecture_specific](https://github.com/user-attachments/assets/7dd99166-1627-45d8-aca9-0dcd02136bd3)

## Sequence Diagrams
Four sequence diagrams, one for each of the CRUD operations. Sequence diagrams for each alternative within the CRUD operations is presented in the master thesis.
### Create DPP
![UML_Create_OLD](https://github.com/user-attachments/assets/d46e465c-93cb-43c0-804f-f1afe380e825)

### Read DPP
![UML_Read](https://github.com/user-attachments/assets/27d3e231-a65c-4db5-952d-3162689f3966)

### Update DPP
![UML_Update](https://github.com/user-attachments/assets/be11ba55-ef94-4ae5-a6ef-1fda6a72305d)

### Delete DPP
![UML_Delete](https://github.com/user-attachments/assets/16acff57-5d25-4cba-9bc9-4ab17b5796e0)

## Web Pages

### Web Pages interaction

## Credits
This prototype is part of a Master’s Thesis by Johanne Glende, NTNU, June 2025. Thesis title: Digital Product Passport as Enabler for Circular Economy − Design, Implementation and Evaluation of a Functional DPP Prototype. Supervisor: Andrei Lobov, NTNU.
