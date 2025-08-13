## 🧭 User-Desktop App – Functional Guideline (2025 Edition)

---

### 🔹 **1. Owner Management (Dashboard Item #1)**

#### ✅ Features:

- View, search, and list all owners (`Owners` table)
- Add New Owner: Opens a **modal form**:
  - `Ownercode` (auto-generated)
  - `Ownername`
  - `Ownerphone`
  - `Note`
- Edit/Delete owner (only if not linked to properties)

#### 🔄 Behavior:

- Accessed from dashboard or **inline from property form** if no owner found
- Owner selection is required for property creation

---

### 🔹 **2. Property Management (Dashboard Item #2)**

#### ✅ Add New Property:

##### Form Fields:

- `realstatecode`: Auto-generated → `Companyco + Random(4)`
- `Property Type`: Dropdown from `Maincode` (`recty = 03`)
- `Build Type`: Dropdown from `Maincode` (`recty = 04`)
- `Unit of Measure`: Dropdown from `Maincode` (`recty = 05`)
- `Yearmake`: Year input
- `Area`, `Facade`, `Depth`: Decimal
- `Bedrooms`, `Bathrooms`: Integer
- `Is Corner`: Yes/No
- `Offer Type`: Dropdown (`Maincode`, `recty = 06`)
- `Province` & `Region`: Dropdowns from `Maincode`
- `Address`, `Descriptions`: Text
- `Photo Upload`: 5–10 files (saved to `data/realstateimages`)
- `Owner`: Select from `Owners` table (add new owner inline if needed)

##### On Save:

- Insert into `Realstatspecification`
- Insert photos into `realstatephotos`

---

### 🟦 **3. Update Property GUI (Dashboard Item #3)**

#### ✅ Workflow:

1. View all properties in a summary list
2. Search by:
   - `realstatecode`
   - Owner name
   - Region
   - Property type, etc.

#### 📋 On Result:

- Click property row → open action dropdown:
  - **Edit**: Opens pre-filled form, updates `Realstatspecification` and photo/owner links
  - **Delete**: Confirm delete (cascade removes photos from both DB and filesystem)

---

### 📊 **4. Search & Report (Dashboard Item #4)**

#### ✅ Features:

- Filter properties by type, year, region, corner, size, etc.
- View property details (read-only)
- Export to CSV (saved in `data/csv/`) for:
  - Filtered list
  - Single property full report
- Optionally include photos in report

#### 🧩 Technologies:

- Filtering logic uses SQLite queries with LIKE, BETWEEN, etc.
- Joins with `Maincode`, `Owners` for dropdowns and lookups

---

### ⚙️ **5. Settings (Dashboard Item #5)**

#### Options:

- Set local company code (`Companyco`)
- Default photo save path
- Auto-backup/export directory
- Theme/UI preferences

---

### 🕓 **6. Recent Activity (Dashboard Item #6)**

#### Functionality:

- View last actions (insert, update, delete)
- Show:
  - Timestamp
  - Action type
  - Property code
  - Performed by (optional)
- Activity can be stored in a local log file or activity DB table

---

## 💾 Database Usage Overview

| Table                   | Used In                                               |
| ----------------------- | ----------------------------------------------------- |
| `Realstatspecification` | Add, Update, Search, Reports                          |
| `Owners`                | Owner Management, Add/Edit Property                   |
| `realstatephotos`       | Photo uploads (files in `data/realstateimages`)       |
| `Maincode`              | Dropdowns & lookups (type, units, offer, build, etc.) |

---
