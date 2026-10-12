import { apiRequest, apiDownload } from "./api";

export interface StoredFile {
  id: number;
  filename: string;
  size: number;
  content_type: string;
  checksum: string;
  created_at: string;
}

export async function listFiles(
  token: string,
): Promise<StoredFile[]> {
  return apiRequest<StoredFile[]>("/files", { token });
}

export async function uploadFile(
  token: string,
  file: File,
): Promise<StoredFile> {
  const formData = new FormData();
  formData.append("file", file);

  return apiRequest<StoredFile>("/files", {
    method: "POST",
    token,
    body: formData,
  });
}

export async function downloadFile(
  token: string,
  file: StoredFile,
): Promise<void> {
  const blob = await apiDownload(`/files/${file.id}`, token);
  const url = URL.createObjectURL(blob);

  try {
    const link = document.createElement("a");
    link.href = url;
    link.download = file.filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
  } finally {
    URL.revokeObjectURL(url);
  }
}

export async function deleteFile(
  token: string,
  fileId: number,
): Promise<void> {
  await apiRequest<unknown>(`/files/${fileId}`, {
    method: "DELETE",
    token,
  });
}