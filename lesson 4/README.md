# BI Source-to-Target Mapping Manager

A comprehensive web application for managing Business Intelligence (BI) source-to-target mappings. This tool helps you track and visualize data lineage across your data warehouse, making it easy to document transformations, source fields, and target tables.

## Features

✨ **Interactive Tree Visualization**
- One-click expandable tree view of all target tables
- Visual hierarchy showing target tables and their source mappings
- Expand/collapse all functionality for easy navigation

📊 **Complete Mapping Management**
- Add, edit, and delete mappings
- Track source tables, source fields, and transformations
- Document SQL transformations and business logic
- Add notes and comments for each mapping

💾 **Excel Integration**
- Export all mappings to Excel with one click
- Import existing mappings from Excel files
- Choose to replace or append when importing
- Automatic backup and data persistence

🔍 **Search & Filter**
- Real-time search across all fields
- Filter by target table, source table, or transformation
- Instant results with highlighting

📈 **Statistics Dashboard**
- Total number of target tables
- Total mappings count
- Unique source tables tracked

## Project Structure

```
lesson 4/
├── bi-mapping-manager.html    # Main HTML interface
├── styles.css                  # Styling and layout
├── app.js                      # JavaScript application logic
├── bi_mapping_manager.py       # Python backend (optional)
├── .github/
│   └── copilot-instructions.md # Coding standards
└── README.md                   # This file
```

## Getting Started

### Web Application (No Installation Required)

1. **Open the application**
   ```bash
   # Simply open the HTML file in your browser
   open bi-mapping-manager.html
   # or double-click the file
   ```

2. **Start adding mappings**
   - Fill in the form on the left panel
   - Click "Add Mapping" to save
   - Your data is stored in browser's localStorage

3. **View your mappings**
   - Click on any target table name to expand/collapse
   - Use the + icon to see all source mappings
   - Edit or delete mappings using the action buttons

### Python Backend (Optional)

For advanced Excel operations and batch processing:

1. **Install dependencies**
   ```bash
   pip install pandas openpyxl
   ```

2. **Use the Python API**
   ```python
   from bi_mapping_manager import BiMappingManager
   
   # Initialize manager
   manager = BiMappingManager('bi_mappings.xlsx')
   
   # Add a mapping
   manager.add_mapping(
       target_table='DIM_CUSTOMER',
       target_field='CUSTOMER_NAME',
       source_table='STG_CUSTOMERS',
       source_field='CUST_NAME',
       transformation='UPPER(TRIM(CUST_NAME))',
       notes='Standardize customer name'
   )
   
   # Get statistics
   stats = manager.get_statistics()
   print(stats)
   
   # Generate lineage report
   manager.generate_lineage_report('lineage_report.xlsx')
   ```

## Usage Guide

### Adding a New Mapping

1. Fill in the required fields:
   - **Target Table**: The destination table in your data warehouse (e.g., `DIM_CUSTOMER`)
   - **Target Field**: The field in the target table (e.g., `CUSTOMER_NAME`)
   - **Source Table**: The source table (e.g., `STG_CUSTOMERS`)
   - **Source Field**: The field in the source table (e.g., `CUST_NAME`)

2. Optional fields:
   - **Transformation**: Document any SQL transformations (e.g., `UPPER(TRIM(CUST_NAME))`)
   - **Notes**: Add business context or comments

3. Click **Add Mapping**

### Viewing Mappings

- **Tree View**: Click on target table names to expand/collapse
- **Expand All**: Show all mappings at once
- **Collapse All**: Hide all mapping details
- **Search**: Type in the search box to filter mappings

### Editing Mappings

1. Click the ✏️ (edit) icon on any mapping
2. Modify the fields in the popup modal
3. Click **Save Changes**

### Deleting Mappings

1. Click the 🗑️ (delete) icon on any mapping
2. Confirm the deletion

### Export to Excel

1. Click **Export to Excel** button
2. File will be downloaded with timestamp (e.g., `BI_Mappings_2025-12-07.xlsx`)
3. Excel file includes all mapping details

### Import from Excel

1. Click **Import from Excel** button
2. Select your Excel file
3. Choose to **Replace** (OK) or **Append** (Cancel) existing mappings
4. Excel must have these columns:
   - Target Table
   - Target Field
   - Source Table
   - Source Field
   - Transformation (optional)
   - Notes (optional)

## Data Storage

### Web Application
- Uses browser's **localStorage**
- Data persists across browser sessions
- Stored locally on your computer
- No server required

### Python Backend
- Stores data in **Excel files** (`.xlsx`)
- Default file: `bi_mappings.xlsx`
- Can be version controlled with Git
- Compatible with Excel, Google Sheets, and other tools

## Excel File Format

When exporting or importing, the Excel file should have these columns:

| Column Name | Type | Required | Description |
|------------|------|----------|-------------|
| Target Table | Text | Yes | Target table name (uppercase) |
| Target Field | Text | Yes | Target field name (uppercase) |
| Source Table | Text | Yes | Source table name (uppercase) |
| Source Field | Text | Yes | Source field name (uppercase) |
| Transformation | Text | No | SQL transformation logic |
| Notes | Text | No | Additional comments |
| Created At | DateTime | Auto | When mapping was created |
| Updated At | DateTime | Auto | When mapping was last updated |

## Python API Reference

### BiMappingManager Class

```python
# Initialize
manager = BiMappingManager(excel_file='bi_mappings.xlsx')

# Add mapping
manager.add_mapping(target_table, target_field, source_table, source_field, 
                   transformation='', notes='')

# Update mapping
manager.update_mapping(target_table, target_field, **kwargs)

# Delete mapping
manager.delete_mapping(target_table, target_field)

# Get mappings
manager.get_mappings_by_target_table(target_table)
manager.get_mappings_by_source_table(source_table)
manager.search_mappings(search_term)
manager.get_all_mappings()

# Get lists
manager.get_target_tables()
manager.get_source_tables()
manager.get_statistics()

# Import/Export
manager.export_to_excel(filename)
manager.import_from_excel(filename, replace=False)
manager.generate_lineage_report(output_file)
```

## Best Practices

1. **Naming Conventions**
   - Use uppercase for table and field names
   - Be consistent with naming patterns
   - Use descriptive names

2. **Transformations**
   - Document all SQL transformations
   - Include business logic in notes
   - Keep transformations readable

3. **Regular Backups**
   - Export to Excel regularly
   - Store Excel files in version control
   - Keep historical versions

4. **Documentation**
   - Add notes for complex mappings
   - Document business rules
   - Explain transformation logic

## Troubleshooting

### Mappings not saving
- Check browser's localStorage is enabled
- Try a different browser
- Export to Excel as backup

### Excel import not working
- Verify column names match exactly
- Check for required fields (Target Table, Target Field, etc.)
- Ensure data is in the first sheet

### Python errors
- Install required packages: `pip install pandas openpyxl`
- Check Excel file path is correct
- Verify Python version (3.7+)

## Technologies Used

- **HTML5**: Structure and layout
- **CSS3**: Styling with modern gradients and animations
- **JavaScript (ES6+)**: Application logic and interactivity
- **SheetJS (xlsx.js)**: Excel file operations
- **Python**: Backend data management (optional)
- **Pandas**: Data manipulation and Excel I/O (optional)

## Browser Compatibility

- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ⚠️ Internet Explorer (not supported)

## Future Enhancements

- [ ] Database backend integration
- [ ] Multi-user support with authentication
- [ ] Visual data lineage diagrams
- [ ] Impact analysis tools
- [ ] Change history tracking
- [ ] REST API for integration
- [ ] Docker containerization

## License

This project is provided as-is for educational purposes.

## Support

For questions or issues, please refer to the coding standards in `.github/copilot-instructions.md`.

---

**Created for the AI Course - Lesson 4**  
*BI Data Lineage and Source-to-Target Mapping Management*
