/**
 * BI Source-to-Target Mapping Manager
 * Application logic and Excel integration
 */

class MappingManager {
    constructor() {
        this.mappings = [];
        this.init();
    }

    /**
     * Initialize the application
     */
    init() {
        this.loadFromLocalStorage();
        this.attachEventListeners();
        this.renderTree();
        this.updateStatistics();
    }

    /**
     * Load mappings from localStorage
     */
    loadFromLocalStorage() {
        const stored = localStorage.getItem('biMappings');
        if (stored) {
            try {
                this.mappings = JSON.parse(stored);
            } catch (e) {
                console.error('Error loading mappings:', e);
                this.mappings = [];
            }
        }
    }

    /**
     * Save mappings to localStorage
     */
    saveToLocalStorage() {
        localStorage.setItem('biMappings', JSON.stringify(this.mappings));
    }

    /**
     * Attach event listeners to UI elements
     */
    attachEventListeners() {
        // Form submission
        document.getElementById('mappingForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addMapping();
        });

        // Clear form
        document.getElementById('clearForm').addEventListener('click', () => {
            this.clearForm();
        });

        // Export to Excel
        document.getElementById('exportExcel').addEventListener('click', () => {
            this.exportToExcel();
        });

        // Import from Excel
        document.getElementById('importExcel').addEventListener('click', () => {
            document.getElementById('fileInput').click();
        });

        document.getElementById('fileInput').addEventListener('change', (e) => {
            this.importFromExcel(e.target.files[0]);
        });

        // Expand/Collapse All
        document.getElementById('expandAll').addEventListener('click', () => {
            this.expandAll();
        });

        document.getElementById('collapseAll').addEventListener('click', () => {
            this.collapseAll();
        });

        // Search
        document.getElementById('searchBox').addEventListener('input', (e) => {
            this.filterMappings(e.target.value);
        });

        // Edit form submission
        document.getElementById('editForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveEdit();
        });

        // Modal close
        document.querySelector('.close').addEventListener('click', () => {
            this.closeModal();
        });

        document.querySelector('.modal-cancel').addEventListener('click', () => {
            this.closeModal();
        });

        window.addEventListener('click', (e) => {
            const modal = document.getElementById('editModal');
            if (e.target === modal) {
                this.closeModal();
            }
        });
    }

    /**
     * Add a new mapping
     */
    addMapping() {
        const mapping = {
            id: Date.now(),
            targetTable: document.getElementById('targetTable').value.trim().toUpperCase(),
            targetField: document.getElementById('targetField').value.trim().toUpperCase(),
            sourceTable: document.getElementById('sourceTable').value.trim().toUpperCase(),
            sourceField: document.getElementById('sourceField').value.trim().toUpperCase(),
            transformation: document.getElementById('transformation').value.trim(),
            notes: document.getElementById('notes').value.trim(),
            createdAt: new Date().toISOString()
        };

        this.mappings.push(mapping);
        this.saveToLocalStorage();
        this.renderTree();
        this.updateStatistics();
        this.clearForm();
        this.showNotification('Mapping added successfully!', 'success');
    }

    /**
     * Clear the form
     */
    clearForm() {
        document.getElementById('mappingForm').reset();
    }

    /**
     * Delete a mapping
     */
    deleteMapping(id) {
        if (confirm('Are you sure you want to delete this mapping?')) {
            this.mappings = this.mappings.filter(m => m.id !== id);
            this.saveToLocalStorage();
            this.renderTree();
            this.updateStatistics();
            this.showNotification('Mapping deleted successfully!', 'success');
        }
    }

    /**
     * Open edit modal for a mapping
     */
    editMapping(id) {
        const mapping = this.mappings.find(m => m.id === id);
        if (!mapping) return;

        document.getElementById('editIndex').value = id;
        document.getElementById('editTargetTable').value = mapping.targetTable;
        document.getElementById('editTargetField').value = mapping.targetField;
        document.getElementById('editSourceTable').value = mapping.sourceTable;
        document.getElementById('editSourceField').value = mapping.sourceField;
        document.getElementById('editTransformation').value = mapping.transformation;
        document.getElementById('editNotes').value = mapping.notes;

        document.getElementById('editModal').style.display = 'block';
    }

    /**
     * Save edited mapping
     */
    saveEdit() {
        const id = parseInt(document.getElementById('editIndex').value);
        const mapping = this.mappings.find(m => m.id === id);
        
        if (mapping) {
            mapping.targetTable = document.getElementById('editTargetTable').value.trim().toUpperCase();
            mapping.targetField = document.getElementById('editTargetField').value.trim().toUpperCase();
            mapping.sourceTable = document.getElementById('editSourceTable').value.trim().toUpperCase();
            mapping.sourceField = document.getElementById('editSourceField').value.trim().toUpperCase();
            mapping.transformation = document.getElementById('editTransformation').value.trim();
            mapping.notes = document.getElementById('editNotes').value.trim();
            mapping.updatedAt = new Date().toISOString();

            this.saveToLocalStorage();
            this.renderTree();
            this.closeModal();
            this.showNotification('Mapping updated successfully!', 'success');
        }
    }

    /**
     * Close the edit modal
     */
    closeModal() {
        document.getElementById('editModal').style.display = 'none';
    }

    /**
     * Render the tree view
     */
    renderTree() {
        const treeView = document.getElementById('treeView');
        
        if (this.mappings.length === 0) {
            treeView.innerHTML = `
                <div class="empty-state">
                    <p>No mappings yet. Add your first mapping to get started!</p>
                </div>
            `;
            return;
        }

        // Group mappings by target table
        const grouped = this.mappings.reduce((acc, mapping) => {
            if (!acc[mapping.targetTable]) {
                acc[mapping.targetTable] = [];
            }
            acc[mapping.targetTable].push(mapping);
            return acc;
        }, {});

        // Sort target tables alphabetically
        const sortedTables = Object.keys(grouped).sort();

        let html = '';
        sortedTables.forEach(targetTable => {
            const tableMappings = grouped[targetTable];
            html += `
                <div class="tree-node">
                    <div class="tree-target" onclick="app.toggleNode('${targetTable}')">
                        <div class="tree-target-name">
                            <span class="expand-icon" id="icon-${this.sanitizeId(targetTable)}">+</span>
                            ${targetTable}
                        </div>
                        <span class="mapping-count">${tableMappings.length}</span>
                    </div>
                    <div class="tree-mappings" id="mappings-${this.sanitizeId(targetTable)}">
                        ${tableMappings.map(mapping => this.renderMappingItem(mapping)).join('')}
                    </div>
                </div>
            `;
        });

        treeView.innerHTML = html;
    }

    /**
     * Render a single mapping item
     */
    renderMappingItem(mapping) {
        return `
            <div class="mapping-item">
                <div class="mapping-header">
                    <div class="mapping-field">${mapping.targetField}</div>
                    <div class="mapping-actions">
                        <button class="btn-icon btn-edit" onclick="app.editMapping(${mapping.id})" title="Edit">✏️</button>
                        <button class="btn-icon btn-delete" onclick="app.deleteMapping(${mapping.id})" title="Delete">🗑️</button>
                    </div>
                </div>
                <div class="mapping-details">
                    <div class="mapping-detail-row">
                        <span class="detail-label">Source Table:</span>
                        <span class="detail-value">${mapping.sourceTable}</span>
                    </div>
                    <div class="mapping-detail-row">
                        <span class="detail-label">Source Field:</span>
                        <span class="detail-value">${mapping.sourceField}</span>
                    </div>
                    ${mapping.transformation ? `
                        <div class="mapping-detail-row">
                            <span class="detail-label">Transformation:</span>
                            <span class="detail-value">
                                <div class="transformation-text">${this.escapeHtml(mapping.transformation)}</div>
                            </span>
                        </div>
                    ` : ''}
                    ${mapping.notes ? `
                        <div class="mapping-detail-row">
                            <span class="detail-label">Notes:</span>
                            <span class="detail-value">${this.escapeHtml(mapping.notes)}</span>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    /**
     * Toggle tree node expansion
     */
    toggleNode(targetTable) {
        const sanitized = this.sanitizeId(targetTable);
        const mappingsDiv = document.getElementById(`mappings-${sanitized}`);
        const icon = document.getElementById(`icon-${sanitized}`);

        if (mappingsDiv && icon) {
            mappingsDiv.classList.toggle('expanded');
            icon.classList.toggle('expanded');
            icon.textContent = icon.classList.contains('expanded') ? '−' : '+';
        }
    }

    /**
     * Expand all nodes
     */
    expandAll() {
        document.querySelectorAll('.tree-mappings').forEach(el => {
            el.classList.add('expanded');
        });
        document.querySelectorAll('.expand-icon').forEach(el => {
            el.classList.add('expanded');
            el.textContent = '−';
        });
    }

    /**
     * Collapse all nodes
     */
    collapseAll() {
        document.querySelectorAll('.tree-mappings').forEach(el => {
            el.classList.remove('expanded');
        });
        document.querySelectorAll('.expand-icon').forEach(el => {
            el.classList.remove('expanded');
            el.textContent = '+';
        });
    }

    /**
     * Filter mappings based on search query
     */
    filterMappings(query) {
        const searchTerm = query.toLowerCase();
        
        if (!searchTerm) {
            this.renderTree();
            return;
        }

        const filtered = this.mappings.filter(mapping => 
            mapping.targetTable.toLowerCase().includes(searchTerm) ||
            mapping.targetField.toLowerCase().includes(searchTerm) ||
            mapping.sourceTable.toLowerCase().includes(searchTerm) ||
            mapping.sourceField.toLowerCase().includes(searchTerm) ||
            mapping.transformation.toLowerCase().includes(searchTerm) ||
            mapping.notes.toLowerCase().includes(searchTerm)
        );

        // Temporarily replace mappings for rendering
        const original = this.mappings;
        this.mappings = filtered;
        this.renderTree();
        this.mappings = original;
        
        // Auto-expand all when searching
        if (filtered.length > 0) {
            setTimeout(() => this.expandAll(), 100);
        }
    }

    /**
     * Update statistics
     */
    updateStatistics() {
        const uniqueTargets = new Set(this.mappings.map(m => m.targetTable));
        const uniqueSources = new Set(this.mappings.map(m => m.sourceTable));

        document.getElementById('totalTargets').textContent = uniqueTargets.size;
        document.getElementById('totalMappings').textContent = this.mappings.length;
        document.getElementById('totalSources').textContent = uniqueSources.size;
    }

    /**
     * Export mappings to Excel
     */
    exportToExcel() {
        if (this.mappings.length === 0) {
            this.showNotification('No mappings to export!', 'error');
            return;
        }

        // Prepare data for Excel
        const excelData = this.mappings.map(m => ({
            'Target Table': m.targetTable,
            'Target Field': m.targetField,
            'Source Table': m.sourceTable,
            'Source Field': m.sourceField,
            'Transformation': m.transformation,
            'Notes': m.notes,
            'Created At': new Date(m.createdAt).toLocaleString(),
            'Updated At': m.updatedAt ? new Date(m.updatedAt).toLocaleString() : ''
        }));

        // Create workbook and worksheet
        const wb = XLSX.utils.book_new();
        const ws = XLSX.utils.json_to_sheet(excelData);

        // Set column widths
        const colWidths = [
            { wch: 25 }, // Target Table
            { wch: 25 }, // Target Field
            { wch: 25 }, // Source Table
            { wch: 25 }, // Source Field
            { wch: 40 }, // Transformation
            { wch: 30 }, // Notes
            { wch: 20 }, // Created At
            { wch: 20 }  // Updated At
        ];
        ws['!cols'] = colWidths;

        XLSX.utils.book_append_sheet(wb, ws, 'Mappings');

        // Generate filename with timestamp
        const timestamp = new Date().toISOString().split('T')[0];
        const filename = `BI_Mappings_${timestamp}.xlsx`;

        // Save file
        XLSX.writeFile(wb, filename);
        this.showNotification(`Exported ${this.mappings.length} mappings to ${filename}`, 'success');
    }

    /**
     * Import mappings from Excel
     */
    importFromExcel(file) {
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const data = new Uint8Array(e.target.result);
                const workbook = XLSX.read(data, { type: 'array' });
                const sheetName = workbook.SheetNames[0];
                const worksheet = workbook.Sheets[sheetName];
                const jsonData = XLSX.utils.sheet_to_json(worksheet);

                // Convert imported data to mapping format
                const importedMappings = jsonData.map(row => ({
                    id: Date.now() + Math.random(),
                    targetTable: (row['Target Table'] || '').toString().trim().toUpperCase(),
                    targetField: (row['Target Field'] || '').toString().trim().toUpperCase(),
                    sourceTable: (row['Source Table'] || '').toString().trim().toUpperCase(),
                    sourceField: (row['Source Field'] || '').toString().trim().toUpperCase(),
                    transformation: (row['Transformation'] || '').toString().trim(),
                    notes: (row['Notes'] || '').toString().trim(),
                    createdAt: new Date().toISOString()
                })).filter(m => m.targetTable && m.targetField && m.sourceTable && m.sourceField);

                if (importedMappings.length === 0) {
                    this.showNotification('No valid mappings found in the file!', 'error');
                    return;
                }

                // Ask user if they want to replace or append
                const replace = confirm(
                    `Found ${importedMappings.length} mappings in the file.\n\n` +
                    `Click OK to REPLACE existing mappings\n` +
                    `Click Cancel to APPEND to existing mappings`
                );

                if (replace) {
                    this.mappings = importedMappings;
                } else {
                    this.mappings.push(...importedMappings);
                }

                this.saveToLocalStorage();
                this.renderTree();
                this.updateStatistics();
                this.showNotification(`Imported ${importedMappings.length} mappings successfully!`, 'success');
            } catch (error) {
                console.error('Import error:', error);
                this.showNotification('Error importing file. Please check the format.', 'error');
            }

            // Reset file input
            document.getElementById('fileInput').value = '';
        };

        reader.readAsArrayBuffer(file);
    }

    /**
     * Show notification message
     */
    showNotification(message, type = 'success') {
        // Simple alert for now - can be enhanced with a better notification system
        alert(message);
    }

    /**
     * Sanitize ID for DOM
     */
    sanitizeId(str) {
        return str.replace(/[^a-zA-Z0-9]/g, '_');
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application
const app = new MappingManager();
