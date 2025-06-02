# Digital Product Passport Prototype

A functional proof-of-concept implementation of a Digital Product Passport (DPP) system developed as part of a Master’s thesis at the Norwegian University of Science and Technology (NTNU), June 2025. The prototype implements a modular architecture combining CAD data, a custom-built DPP ontology, a semantic knowledge base, and a web-based interface to support circular economy objectives such as product traceability and life cycle transparency.

## Overview

The DPP prototype includes:
- **CAD Software Integration** using Onshape and OnPy for automatic extraction and generation of product data.
- **Semantic Knowledge Base** with OWL/RDF storage via Apache Jena Fuseki.
- **DPP Agent** as backend to handle data transformation and API logic.
- **Web Portal** for CRUD (Create, Read, Update, Delete) operations on Digital Product Passports.
- **QR Code Integration** for accessing individual passports via physical data carrier.

## Technologies Used

- **Python 3.12** – Backend scripting & DPP Agent logic
- **Django 5.1** – Web framework for backend and web interface
- **OnShape** – CAD software ([OnShape](https://www.onshape.com/en/))
- **OnPy** – Python API for Onshape CAD integration ([OnPy GitHub](https://github.com/kyle-tennison/onpy))
- **Apache Jena Fuseki** – Semantic database ([Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/))
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

## Ontology
The custom-built DPP ontology for the prototype. Each ontology class is marked with a yellow circle, each data property of the ontology marked with green square.

![DPP_ontology_list_form](https://github.com/user-attachments/assets/ff5b4826-b8e9-44a6-a3b3-02537a31c9bb)        ![DPP_ontology_data_properties](https://github.com/user-attachments/assets/5f456c23-7aac-498b-a896-f3929528900e)

### Ontology Graph
![DPP_master_thesis_figures-DPP_ontology_full](https://github.com/user-attachments/assets/dc77bced-65a8-4352-9a76-f7666b5eae1f)

## Architecture
Architecture of the prototype system, with specific components and technologies.
![dpp_architecture_specific](https://github.com/user-attachments/assets/7dd99166-1627-45d8-aca9-0dcd02136bd3)

## Sequence Diagrams
Four sequence diagrams, one for each of the CRUD operations. Sequence diagrams for each alternative within the CRUD operations is presented in the master thesis.

### Create DPP
Sequence diagram for creating a new DPP. The stakeholder submits Document ID, Workspace ID and Element ID from the OnShape document into the User Interface of the Web Portal. The DPP Agent requests data from the OnShape API based on the provided identifiers. If the DID, WID or EID is not found, the system returns an error. If the input is valid, the system returns the response body from the API and uses it to create product, part, actor and DPP instances. This is then inserted into the KB with a confirmation of success before proceeding to the next query to ensure consistency. After the sucsessfull intsertion of all components, the system generates a QR code linking to the specific DPP. The QR code, together with a summary of the DPP data, is displayed to the stakeholder in the UI.

![UML_Create_OLD](https://github.com/user-attachments/assets/d46e465c-93cb-43c0-804f-f1afe380e825)

### Read DPP
Sequence diagram for reading a DPP. A customer scans a QR code and is directed to the endpoint for the specific product. The system requests data for the DPP ID found in the URL encoded in the QR code, and returns it in full. The data is then structured into specific formats, and rendered to the endpoint and displayed for the customer.

![UML_Read](https://github.com/user-attachments/assets/27d3e231-a65c-4db5-952d-3162689f3966)

### Update DPP
Sequence diagram for updating an existing DPP. A stakeholder submits the DPP ID of the DPP it wants to update, along with the values to update (Note: it is a prototype, so currently only two values are available to update). The system first checks if the DPP exists, if not, an error message is displayed for the stakeholder and the sequence ends. If the DPP exists, the system checks the timestamp format. If it is invalid, an error message is displayed to the stakeholder and the sequence ends. If the timstamp is formateted correctly or not provided, the system continoues to check whether the actor exists in the KB. If no, an error is displayed to the stakeholder, if yes or an actorID is not provided, the sequence continous to firstly update the timestamp (if provided) and then te actor (if provided). At the end, the updated DPP data is requested from the KB to display the updated data in the UI for the stakeholder.

![UML_Update](https://github.com/user-attachments/assets/be11ba55-ef94-4ae5-a6ef-1fda6a72305d)

### Delete DPP
Sequence diagram for deleting an existing DPP from the KB. The stakehodler submits the ID of the DPP it wishes to remove. The system then checks wether the DPP exists in the KB. If no, an error is displayed to the stakehodler and the sequence ends. If yes, the system deletes the DPP from the KB together with all data connected to the prouct and parts represented by the DPP. Upon sucessfull operation, a success message is displayed to the stakehodler on the UI.  

![UML_Delete](https://github.com/user-attachments/assets/16acff57-5d25-4cba-9bc9-4ab17b5796e0)

## User Interface

### UI interaction

## Credits
This prototype is part of a Master’s Thesis by Johanne Glende, NTNU, June 2025. Thesis title: Digital Product Passport as Enabler for Circular Economy − Design, Implementation and Evaluation of a Functional DPP Prototype. Supervisor: Andrei Lobov, NTNU.
