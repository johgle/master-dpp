# Digital Product Passport Prototype

💡 A prototype system for machine-readable Digital Product Passports using CAD and semantic web tech.

A functional proof-of-concept implementation of a Digital Product Passport (DPP) system developed as part of a Master’s thesis at the Norwegian University of Science and Technology (NTNU), June 2025. The prototype implements a modular architecture combining CAD data, a custom-built DPP ontology, a semantic Knowledge Base, and a web-based interface to support circular economy objectives such as product traceability and life cycle transparency.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Ontology](#ontology)
- [Sequence Diagrams](#sequence-diagrams)
- [User Interface](#user-interface)
- [Installation](#installation)
- [Credits](#credits)

## Overview

The DPP prototype includes:
- **CAD Software Integration** using Onshape and OnPy for automatic extraction and generation of product data.
- **Semantic Knowledge Base** with OWL/RDF storage via Apache Jena Fuseki.
- **DPP Agent** as backend to handle data transformation and API logic.
- **Web Portal** for CRUD (Create, Read, Update, Delete) operations on Digital Product Passports.
- **QR Code Integration** for accessing individual passports via physical data carrier.

## Features

- Automatic generation of Digital Product Passports with data from CAD models
- SPARQL-powered semantic queries on structured product data
- CRUD (Create, Read, Update, Delete) operations on DPPs via a web interface
- QR code generation and access to DPP data
- End-to-end performance testing for CRUD operations

## Quick Start

1. **Clone the repository:**
   ```sh
   git clone https://github.com/johgle/master-dpp.git
   ```
   
2. **Create and activate a virtual environment:**
   ```sh
   python -m venv dpp_venv
   dpp_venv\Scripts\activate
   ```
   
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   
4. **Set up Django secret key:**

   Create a `.env` file in the root of the DPP_project directory (same level as manage.py), and add:

   ```
   DJANGO_SECRET_KEY=your-secret-key
   ```

   To generate a new, secure Django secret key, run this command in your terminal:
   
   ```sh
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   
   Copy the generated key and use it as `your-secret-key` in the .env file.

5. **Set up Onshape API keys:**

   Create `ACCESS_KEY` and `SECRET_KEY` for OnShape API integration. See how to generate API keys here: https://onshape-public.github.io/docs/auth/apikeys/.
   
   When creating keys, choose:
   1. Read profile information
   2. Read your documents
   3. Write to your documents

   Set the keys as environment variables:
    ```sh
    set ONSHAPE_API_ACCESS_KEY=your-access-key
    set ONSHAPE_API_SECRET_KEY=your-secret-key
    ```

6. **Download Apache Jena Fuseki Server:**

   Go to [https://jena.apache.org/download/index.cgi](https://jena.apache.org/download/index.cgi) and download the newest version of `apache-jena-fuseki-<version>.zip` under Apache Jena Binary Distributions (prototype uses: 5.3.0)

7. **Start the Fuseki server:**

   Open a new terminal, navigate into the folder where you extracted Apache Jena Fuseki to, and start the server:
    ```sh
    cd path\to\apache-jena-fuseki-x.x.x
    fuseki-server
    ```
    Leave this terminal window open while using the DPP system.
    
8. **Start the development server:**

   
   Open a new terminal, navigate to the folder where the `manage.py` file is located, and start the server:
  
    ```sh
    cd path\to\manage.py
    python manage.py runserver
    ```
    Leave this terminal window open while using the DPP system.

   **To access the server from another device (e.g., your phone) on the same WiFi:**

   Update the `ALLOWED_HOSTS` list in the `settings.py` file to include your local IP address.

   Start the server with:

   ```sh
   python manage.py runserver 0.0.0.0:8000
   ```
   
10. **Access the application:**

   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

   Available pages:

   - [Create DPP](http://127.0.0.1:8000/new_dpp/)
   - [View DPP](http://127.0.0.1:8000/product/?id=DPP_ID)   (replace `DPP_ID` in the url with the ID of your DPP)
   - [Update DPP](http://127.0.0.1:8000/update_dpp/)
   - [Delete DPP](http://127.0.0.1:8000/delete_dpp/)




## Architecture
The figure illustrates the architecture of the prototype system, with specific components, technologies, and communications. 

![dpp_architecture_specific](https://github.com/user-attachments/assets/7dd99166-1627-45d8-aca9-0dcd02136bd3)

| **Component**          | **Description**                                                                                  |
|------------------------|--------------------------------------------------------------------------------------------------|
| **OnShape**            | A cloud-based CAD software platform used for designing and modeling digital products.            |
| **Apache Jena Fuseki** | A SPARQL-based triplestore that serves as the system’s Knowledge Base.                           |
| **DPP Agent**          | The backend system implemented in Python using the Django framework.                             |
| **Web Portal**         | The user interface developed using HTML and styled with Tailwind CSS.                            |
| **QR Code**            | Physical QR code generated by the DPP Agent, pointing to the corresponding DPP.                  |


## Tech Stack

- **Python 3.12** – Backend scripting & DPP Agent logic
- **Django 5.1** – Web framework for backend and web interface
- **OnShape** – CAD software ([OnShape](https://www.onshape.com/en/))
- **OnPy** – Python API for Onshape CAD integration ([OnPy GitHub](https://github.com/kyle-tennison/onpy))
- **Apache Jena Fuseki** – Semantic database ([Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/))
- **RDF / OWL** – Ontology and data modeling
- **HTML + Tailwind CSS** – Frontend templates and styling
- **JSON** – Data storage for generated chair metadata
- **qrcode** (Python lib) – QR code generation
- **Selenium** – End-to-end and performance testing
- **pytest** – Automated testing framework
- **psutil** – RAM and resource usage tracking

## Ontology
The custom-built DPP ontology for the prototype. Each ontology class is marked with a yellow circle, each data property of the ontology marked with a green square.

![DPP_ontology_list_form](https://github.com/user-attachments/assets/ff5b4826-b8e9-44a6-a3b3-02537a31c9bb)        ![DPP_ontology_data_properties](https://github.com/user-attachments/assets/5f456c23-7aac-498b-a896-f3929528900e)


### Ontology Graph
The ontology represented as a graph, with relations (object properties).
![DPP_master_thesis_figures-DPP_ontology_full](https://github.com/user-attachments/assets/dc77bced-65a8-4352-9a76-f7666b5eae1f)

## Sequence Diagrams
Four sequence diagrams, one for each of the CRUD operations.

### Create DPP
Sequence diagram for creating a new DPP. A stakeholder submits a Document ID (DID), Workspace ID (WID) and Element ID (EID) (from the OnShape document) via the user interface of the Web Portal. The Web Portal forwards this input to the DPP Agent, which sends a request to the OnShape API. If the DID, WID or EID are invalid or missing, the system returns an error to the stakeholder. If the input is valid, the OnShape API returns the requested data, which the DPP Agent uses to instantiate product, part, actor and DPP objects. The objects are then inserted into the Knowledge Base with a confirmation of success before proceeding to the next query to ensure consistency. After the successful insertion of all components, the system generates a QR code linking to the newly created DPP. The QR code, along with a summary of the DPP information, is displayed to the stakeholder via the user interface.

![UML_Create_full](https://github.com/user-attachments/assets/20bbcdd1-6595-4013-af38-40e2760fa211)

### Read DPP
Sequence diagram for reading a DPP. A customer scans a QR code, which encodes a URL pointing to the specific DPP. The Web Portal receives the requests and forwards it to the DPP Agent, which queries the Knowledge Base for the DPP data. The data is retrieved and structured into specific formats, and rendered at the endpoint where it is displayed to the customer via the user interface.

![UML_Read](https://github.com/user-attachments/assets/27d3e231-a65c-4db5-952d-3162689f3966)

### Update DPP
Sequence diagram for updating an existing DPP. A stakeholder submits the DPP ID of the DPP it wants to update, along with one or both of the values currently supported to update: timestamp and responsible actor ID (Note: this is a prototype implementation and currently only allows two fields to be updated). The system first checks if the DPP exists in the Knowledge Base. If not, an error message is displayed to the stakeholder and the sequence ends. If the DPP is found, the system checks the format of the provided timestamp (if any). If the format is invalid, an error message is displayed to the stakeholder and the sequence ends. If the timestamp is formatted correctly or not provided, the system continues to check whether the actor exists in the KB. If no, an error is displayed. If yes, or an actor ID is not provided, the sequence continues to first update the timestamp (if provided) and then the actor (if provided). At the end, the updated DPP data is requested from the KB to be displayed to the stakeholder via the user interface.

![UML_Update](https://github.com/user-attachments/assets/be11ba55-ef94-4ae5-a6ef-1fda6a72305d)

### Delete DPP
Sequence diagram for deleting an existing DPP from the KB. The stakeholder submits the ID of the DPP it wishes to remove. The system checks whether the DPP exists in the KB. If no, an error is displayed to the stakeholder and the sequence ends. If yes, the system deletes the DPP from the KB along with all associated data. Upon a successful deletion operation, a success message is displayed to the stakeholder via the user interface.  

![UML_Delete_full](https://github.com/user-attachments/assets/35c91498-2774-436b-bd9a-b78dfba71746)


## User Interface
The DPP prototype includes a Web Portal built with Django, HTML and Tailwind CSS. It provides stakeholders with a front end for interacting with Digital Product Passports, and users to read the DPPs.

The interface supports the following features:

### Create DPP 
Submit a new product using its Onshape Document ID, Workspace ID, and Element ID. After processing, a QR code and summary view of the generated DPP are displayed.

#### Create DPP Form
<img src="https://github.com/user-attachments/assets/8513d941-7e91-49a0-b08a-0258662e1f1e" width="600"/>

#### Successfully created DPP
<img src="https://github.com/user-attachments/assets/d2516db8-6797-4ae1-ba12-9754fbb5c43d" width="600"/>

### Read DPP
View any existing DPP by scanning its QR code.

<img src="https://github.com/user-attachments/assets/b0290f1a-36f6-4dd6-9631-8ae888f6095e" width="600"/>

### Update DPP
Update a DPP’s data (currently limited to `timestamp` and `actorID`). The system checks input validity and reflects updates in real-time.

#### Update DPP Form
<img src="https://github.com/user-attachments/assets/a0daa245-2f91-41bf-a4d6-8dd5b2ec4e2e" width="600"/>

#### Successfully updated DPP
<img src="https://github.com/user-attachments/assets/4b15d640-9f7e-43aa-a1b6-75da107f9a0f" width="600"/>

### Delete DPP
Remove a DPP and its associated data from the Knowledge Base. A confirmation message is displayed upon success.

#### Delete DPP Form
<img src="https://github.com/user-attachments/assets/b1881f45-c189-400e-8b5f-9964d70eac5e" width="600"/>

#### Successfully deleted DPP
<img src="https://github.com/user-attachments/assets/e012bc37-9eaa-4567-a6ed-27e1ffd10706" width="600"/>

### Live Demo
This video demonstrates the full CRUD sequence for a digital passport:
- A passport is created via the UI using IDs from OnShape
- It is then displayed at the /product/?id={DPP_ID} endpoint
- The passport's timestamp for invalidation is updated
- Finally, the passport is deleted

https://github.com/user-attachments/assets/e95bf5be-4f28-4cf8-8e9a-bd5e1f7ee2b0

#### Scan a Physical QR Code on a Chair
The video demonstrates scanning a physical QR code placed on a chair, which redirects the user to the DPP site on their mobile phone. (Note: The chair is used solely for illustrative purposes, I did not design or make it.)

https://github.com/user-attachments/assets/3a042ae9-76f2-472d-81bb-8309fa51839b

#### Scan a QR Code on a Computer Screen
The video demonstrates scanning a QR code displayed on a computer screen, which redirects the user to the DPP site on their mobile phone.

https://github.com/user-attachments/assets/2b60ee31-74d9-4615-8783-e7e03161e7d0

## Installation
...

## Credits
This prototype is part of a Master’s Thesis by Johanne Glende, NTNU, June 2025. Thesis title: Digital Product Passport as Enabler of the Circular Economy: Design, Implementation and Evaluation of a Functional DPP Prototype. Supervisor: Andrei Lobov, NTNU.
