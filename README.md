# datacube-wcps-integration
Transparent WCPS query generation from Python for efficient datacube operations.

# Datacube WCPS Integration

This project implements a **transparent WCPS (Web Coverage Processing Service) query generator** directly from Python code, enabling seamless datacube operations between Python and WCPS servers.  

The work was developed as part of a Software Engineering course project, split into **three sprints**, each handled by different team compositions.

---

## 🚀 Project Overview
- **Goal:** Allow Python operations on datacubes to be translated into WCPS queries, executed server-side for efficient data processing.
- **Why:** WCPS (standardized by OGC & ISO) is powerful for datacube queries, but integrating it directly into Python workflows reduces complexity and improves performance.
- **Key Features:**
  - Python reflection & operator overloading for transparent query generation
  - Lazy evaluation of datacube operations
  - Object-oriented design (`DatabaseConnection`, `DatacubeObject`, etc.)
  - UML class and swimlane diagrams for design
  - Jupyter notebook user guide
  - Regression test suite

---

## 📂 Repository Structure
- `sprint1/` – Initial setup, basic Python-to-WCPS translation
- `sprint2/` – Extended operators, lazy evaluation, UML diagrams
- `sprint3/` – Testing framework, Jupyter notebook, final polishing 

---

## 🛠️ Technologies
- Python 3
- WCPS (OGC standard)
- UML Diagrams
- Jupyter Notebook



## 📖 References
- https://earthserver.eu/wcs/
- https://standards.rasdaman.com/

