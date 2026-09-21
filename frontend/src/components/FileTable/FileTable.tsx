import "./FileTable.css";

const files = [
  {
    name: "report.pdf",
    size: "2.4 MB",
    type: "PDF",
    date: "21.09.2026",
  },
  {
    name: "photo.jpg",
    size: "1.8 MB",
    type: "Image",
    date: "20.09.2026",
  },
  {
    name: "project.zip",
    size: "14.2 MB",
    type: "Archive",
    date: "19.09.2026",
  },
];

function FileTable() {
  return (
    <section className="file-section">
      <div className="file-header">
        <div>
          <h1>My Files</h1>
          <p>Manage your uploaded files</p>
        </div>

        <button className="upload-button">
          + Upload file
        </button>
      </div>

      <div className="table-container">
        <table className="file-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Size</th>
              <th>Type</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {files.map((file) => (
              <tr key={file.name}>
                <td>{file.name}</td>
                <td>{file.size}</td>
                <td>{file.type}</td>
                <td>{file.date}</td>
                <td>
                  <button className="action-button">↓</button>
                  <button className="action-button delete">🗑</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default FileTable;