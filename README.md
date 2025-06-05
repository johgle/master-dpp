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
The ontology represented as a graph, with relations (object properties).
![DPP_master_thesis_figures-DPP_ontology_full](https://github.com/user-attachments/assets/dc77bced-65a8-4352-9a76-f7666b5eae1f)

## Architecture
Architecture of the prototype system, with specific components and technologies.
![dpp_architecture_specific](https://github.com/user-attachments/assets/7dd99166-1627-45d8-aca9-0dcd02136bd3)

## Sequence Diagrams
Four sequence diagrams, one for each of the CRUD operations. Sequence diagrams for each alternative within the CRUD operations is presented in the master thesis.

### Create DPP
Sequence diagram for creating a new DPP. A stakeholder submits a Document ID (DID), Workspace ID (WID) and Element ID (EID) (from the OnShape document) via the user interface of the Web Portal. The Web Portal forwards this input to the DPP Agent, which sends a request to the OnShape API. If the DID, WID or EID are invalid or missing, the system returns an error to the stakeholder. If the input is valid, the OnShape API returns the requested data, which the DPP Agent uses to instansiate product, part, actor and DPP objects. The objectcs are then inserted into the Knowledge Base with a confirmation of success before proceeding to the next query to ensure consistency. After the sucsessfull insertion of all components, the system generates a QR code linking to the newly created DPP. The QR code, along with a summary of the DPP information, is displayed to the stakeholder via the user interface.

![UML_Create_full](https://github.com/user-attachments/assets/20bbcdd1-6595-4013-af38-40e2760fa211)


### Read DPP
Sequence diagram for reading a DPP. A customer scans a QR code, which encodes a URL pointing to the specific DPP. The Web Portal receives the requests and forwards it to the DPP Agent, which queries the Knowledge Base for the DPP data. The data is retrieved and structured into specific formats, and rendered to the endpoint where it is displayed to the customer via the user interface.

![UML_Read](https://github.com/user-attachments/assets/27d3e231-a65c-4db5-952d-3162689f3966)

### Update DPP
Sequence diagram for updating an existing DPP. A stakeholder submits the DPP ID of the DPP it wants to update, along with one or both or the values currently supported to update: timestamp and responosible avctor ID (Note: this is a prototype implementation and currently only allows two fields to be updated). The system first checks if the DPP exists in the Knowledge Base. If not, an error message is displayed to the stakeholder and the sequence ends. If the DPP is found, the system checks the format of the provided timestamp (if any). If the format is invalid, an error message is displayed to the stakeholder and the sequence ends. If the timstamp is formateted correctly or not provided, the system continoues to check whether the actor exists in the KB. If no, an error is displayed. If yes, or an actorID is not provided, the sequence continous to firstly update the timestamp (if provided) and then the actor (if provided). At the end, the updated DPP data is requested from the KB to be displayed to the stakeholder via the user interface.

![UML_Update](https://github.com/user-attachments/assets/be11ba55-ef94-4ae5-a6ef-1fda6a72305d)

### Delete DPP
Sequence diagram for deleting an existing DPP from the KB. The stakehodler submits the ID of the DPP it wishes to remove. The system checks whether the DPP exists in the KB. If no, an error is displayed to the stakehodler and the sequence ends. If yes, the system deletes the DPP from the KB along with all assosiated data. Upon sucessful deletion operation, a success message is displayed to the stakeholder via the user interface.  

![UML_Delete_full](https://github.com/user-attachments/assets/35c91498-2774-436b-bd9a-b78dfba71746)


## User Interface

### UI interaction

## Credits
This prototype is part of a Master’s Thesis by Johanne Glende, NTNU, June 2025. Thesis title: Digital Product Passport as Enabler of the Circular Economy − Design, Implementation and Evaluation of a Functional DPP Prototype. Supervisor: Andrei Lobov, NTNU.
