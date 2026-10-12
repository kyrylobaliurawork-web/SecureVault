import { useCallback, useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import {listFiles, uploadFile, downloadFile, deleteFile, type StoredFile,} from "../../services/file";
import "./FileTable.css";

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;

  const units = ["KB", "MB", "GB"];
  let size = bytes / 1024;
  let unitIndex = 0;

  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }

  return `${size.toFixed(1)} ${units[unitIndex]}`;
}

function formatDate(date: string): string {
  return new Date(date).toLocaleDateString("uk-UA");
}

function FileTable() {
  const { user, loading: authLoading } = useAuth();

  const [files, setFiles] = useState<StoredFile[]>([]);
  const [loadingFiles, setLoadingFiles] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const loadFiles = useCallback(async () => {
    const token = sessionStorage.getItem("access_token");

    if (!token || !user) {
      setFiles([]);
      setLoadingFiles(false);
      return;
    }

    setLoadingFiles(true);
    setError("");

    try {
      const result = await listFiles(token);
      setFiles(result);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to load files",
      );
    } finally {
      setLoadingFiles(false);
    }
  }, [user]);

  useEffect(() => {
    if (!authLoading) {
      void loadFiles();
    }
  }, [authLoading, loadFiles]);

  async function handleUpload(
    event: React.ChangeEvent<HTMLInputElement>,
  ) {
    const file = event.target.files?.[0];

    // Дозволяємо повторно вибрати той самий файл.
    event.target.value = "";

    if (!file) return;

    const token = sessionStorage.getItem("access_token");
    if (!token) {
      setError("Please log in to upload files.");
      return;
    }

    setBusy(true);
    setError("");

    try {
      await uploadFile(token, file);
      await loadFiles();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to upload file",
      );
    } finally {
      setBusy(false);
    }
  }

  async function handleDownload(file: StoredFile) {
    const token = sessionStorage.getItem("access_token");
    if (!token) {
      setError("Please log in to download files.");
      return;
    }

    setBusy(true);
    setError("");

    try {
      await downloadFile(token, file);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to download file",
      );
    } finally {
      setBusy(false);
    }
  }

  async function handleDelete(file: StoredFile) {
    if (!window.confirm(`Delete "${file.filename}"?`)) return;

    const token = sessionStorage.getItem("access_token");
    if (!token) {
      setError("Please log in to delete files.");
      return;
    }

    setBusy(true);
    setError("");

    try {
      await deleteFile(token, file.id);
      setFiles((currentFiles) =>
        currentFiles.filter((item) => item.id !== file.id),
      );
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to delete file",
      );
    } finally {
      setBusy(false);
    }
  }

  if (authLoading) {
    return <section className="file-section">Loading account...</section>;
  }

  if (!user) {
    return (
      <section className="file-section">
        <h1>My Files</h1>
        <p>Please log in to manage your files.</p>
        <Link to="/login">Go to Login</Link>
      </section>
    );
  }

  return (
    <section className="file-section">
      <div className="file-header">
        <div>
          <h1>My Files</h1>
          <p>Manage your uploaded files</p>
        </div>

        <button
          className="upload-button"
          type="button"
          disabled={busy}
          onClick={() => fileInputRef.current?.click()}
        >
          {busy ? "Please wait..." : "+ Upload file"}
        </button>

        <input
          ref={fileInputRef}
          type="file"
          hidden
          onChange={handleUpload}
        />
      </div>

      {error && (
        <p className="file-error" role="alert">
          {error}
        </p>
      )}

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
            {loadingFiles ? (
              <tr>
                <td colSpan={5}>Loading files...</td>
              </tr>
            ) : files.length === 0 ? (
              <tr>
                <td colSpan={5}>No files yet. Upload your first file!</td>
              </tr>
            ) : (
              files.map((file) => (
                <tr key={file.id}>
                  <td>{file.filename}</td>
                  <td>{formatSize(file.size)}</td>
                  <td>{file.content_type || "Unknown"}</td>
                  <td>{formatDate(file.created_at)}</td>
                  <td>
                    <button
                      className="action-button"
                      type="button"
                      title="Download file"
                      aria-label={`Download ${file.filename}`}
                      disabled={busy}
                      onClick={() => void handleDownload(file)}
                    >
                      ↓
                    </button>

                    <button
                      className="action-button delete"
                      type="button"
                      title="Delete file"
                      aria-label={`Delete ${file.filename}`}
                      disabled={busy}
                      onClick={() => void handleDelete(file)}
                    >
                      🗑
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default FileTable;