In MongoDB (especially MongoDB Atlas), the structure is **hierarchical** — from top-level **organization** down to individual **collections** inside databases. Here’s the breakdown:

1. **Organization**
   * The top-most level (usually represents your company or team).
   * It contains multiple  **projects** .
   * Used mainly for billing, access control, and management across projects.
2. **Project**
   * A logical grouping inside an organization.
   * Each project can contain one or more  **clusters** .
   * Think of it like an environment — e.g., `dev`, `staging`, or `prod`.
3. **Cluster**
   * A cluster is a **group of servers** that host your MongoDB deployment.
   * It can be:
     * **Shared** (M0–M5): for smaller workloads.
     * **Dedicated** : for production workloads (M10 and above).
   * Each cluster can contain multiple  **databases** .
4. **Database**
   * A logical container for related collections.
   * Each database contains **collections** (like tables in SQL).
   * Example: `users_db`, `inventory_db`.
5. **Collection**
   * Similar to a table in relational databases.
   * Contains multiple **documents** (JSON-like records).
6. **Document**
   * The smallest data unit, stored in BSON (binary JSON).
   * Example:
     ```json
     {
       "name": "Raj",
       "age": 27,
       "skills": ["ML", "Backend"]
     }
     ```

**Hierarchy example:**

```
Organization: MyCompany
└── Project: Production
    └── Cluster: Cluster0
        └── Database: users_db
            └── Collection: profiles
                └── Document: { "name": "Raj", "age": 27 }
```

So:

* **Organization** → groups projects
* **Project** → groups clusters
* **Cluster** → runs MongoDB databases
* **Database** → groups collections
* **Collection** → holds documents
