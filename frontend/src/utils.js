export function createResultsTable(data) {
    if (!data || data.length === 0) {
      return '<p>No results found.</p>';
    }
  
    const tableHeaders = Object.keys(data[0]);
    const tableRows = data.map((row) => {
      return `<tr>${tableHeaders
        .map((header) => `<td>${row[header]}</td>`)
        .join('')}</tr>`;
    });
  
    const tableHTML = `
      <table>
        <thead>
          <tr>${tableHeaders.map((header) => `<th>${header}</th>`).join('')}</tr>
        </thead>
        <tbody>${tableRows.join('')}</tbody>
      </table>
    `;
  
    return tableHTML;
  }